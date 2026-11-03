"""Thin client for Meta's official Ad Library API (Graph API `ads_archive`).

Docs: https://www.facebook.com/ads/library/api
"""

from __future__ import annotations

import json
import logging
import time
from typing import Any, Dict, Iterator, List, Optional, Sequence

import requests

LOGGER = logging.getLogger(__name__)

DEFAULT_API_VERSION = "v23.0"
GRAPH_BASE_URL = "https://graph.facebook.com"

# Fields available to every ad in the Ad Library API.
BASE_FIELDS: List[str] = [
    "id",
    "ad_creation_time",
    "ad_creative_bodies",
    "ad_creative_link_captions",
    "ad_creative_link_descriptions",
    "ad_creative_link_titles",
    "ad_delivery_start_time",
    "ad_delivery_stop_time",
    "ad_snapshot_url",
    "languages",
    "page_id",
    "page_name",
    "publisher_platforms",
]

# Extra fields only returned for political/issue ads.
POLITICAL_FIELDS: List[str] = [
    "bylines",
    "currency",
    "spend",
    "impressions",
    "estimated_audience_size",
    "demographic_distribution",
    "delivery_by_region",
]

# Extra fields only returned for ads delivered in the EU / UK.
EU_FIELDS: List[str] = [
    "eu_total_reach",
    "target_ages",
    "target_gender",
    "target_locations",
    "beneficiary_payers",
]

# Graph API error codes that mean "slow down and retry".
RATE_LIMIT_CODES = {4, 17, 32, 613, 80004}
TRANSIENT_CODES = {1, 2}


class AdLibraryError(RuntimeError):
    """Raised when the Graph API returns an error we cannot recover from."""

    def __init__(self, message: str, code: Optional[int] = None, payload: Any = None):
        super().__init__(message)
        self.code = code
        self.payload = payload


def default_fields(ad_type: str) -> List[str]:
    fields = list(BASE_FIELDS)
    if ad_type == "POLITICAL_AND_ISSUE_ADS":
        fields += POLITICAL_FIELDS
    return fields


class AdLibraryClient:
    def __init__(
        self,
        access_token: str,
        api_version: str = DEFAULT_API_VERSION,
        session: Optional[requests.Session] = None,
        timeout: float = 30.0,
        max_retries: int = 5,
        backoff_base: float = 2.0,
        sleep=time.sleep,
    ):
        if not access_token:
            raise ValueError(
                "An access token is required. Set META_ACCESS_TOKEN or pass --token."
            )
        self.access_token = access_token
        self.api_version = api_version
        self.session = session or requests.Session()
        self.timeout = timeout
        self.max_retries = max_retries
        self.backoff_base = backoff_base
        self._sleep = sleep

    @property
    def endpoint(self) -> str:
        return f"{GRAPH_BASE_URL}/{self.api_version}/ads_archive"

    def build_params(
        self,
        countries: Sequence[str],
        search_terms: Optional[str] = None,
        page_ids: Optional[Sequence[str]] = None,
        ad_type: str = "ALL",
        active_status: str = "ACTIVE",
        search_type: str = "KEYWORD_UNORDERED",
        platforms: Optional[Sequence[str]] = None,
        languages: Optional[Sequence[str]] = None,
        media_type: Optional[str] = None,
        date_min: Optional[str] = None,
        date_max: Optional[str] = None,
        fields: Optional[Sequence[str]] = None,
        page_size: int = 100,
    ) -> Dict[str, Any]:
        if not countries:
            raise ValueError("At least one country (ISO code, or ALL) is required.")
        if not search_terms and not page_ids:
            raise ValueError("Provide search terms and/or page IDs.")

        params: Dict[str, Any] = {
            "ad_reached_countries": json.dumps([c.upper() for c in countries]),
            "ad_type": ad_type,
            "ad_active_status": active_status,
            "fields": ",".join(fields or default_fields(ad_type)),
            "limit": max(1, min(int(page_size), 1000)),
        }
        if search_terms:
            params["search_terms"] = search_terms
            params["search_type"] = search_type
        if page_ids:
            params["search_page_ids"] = json.dumps([str(p) for p in page_ids])
        if platforms:
            params["publisher_platforms"] = json.dumps([p.upper() for p in platforms])
        if languages:
            params["languages"] = json.dumps(list(languages))
        if media_type:
            params["media_type"] = media_type.upper()
        if date_min:
            params["ad_delivery_date_min"] = date_min
        if date_max:
            params["ad_delivery_date_max"] = date_max
        return params

    def _request(self, url: str, params: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        attempt = 0
        while True:
            attempt += 1
            try:
                resp = self.session.get(url, params=params, timeout=self.timeout)
            except requests.RequestException as err:
                if attempt > self.max_retries:
                    raise AdLibraryError(f"Network error: {err}") from err
                self._backoff(attempt, f"network error: {err}")
                continue

            try:
                payload = resp.json()
            except ValueError:
                payload = None

            error = payload.get("error") if isinstance(payload, dict) else None
            if resp.status_code == 200 and not error:
                return payload

            code = error.get("code") if error else None
            message = error.get("message") if error else resp.text[:300]
            retryable = (
                code in RATE_LIMIT_CODES
                or code in TRANSIENT_CODES
                or resp.status_code >= 500
                or bool(error and error.get("is_transient"))
            )
            if retryable and attempt <= self.max_retries:
                self._backoff(attempt, f"HTTP {resp.status_code} code={code}: {message}")
                continue
            raise AdLibraryError(
                f"Ad Library API error (HTTP {resp.status_code}, code={code}): {message}",
                code=code,
                payload=payload,
            )

    def _backoff(self, attempt: int, reason: str) -> None:
        delay = self.backoff_base ** attempt
        LOGGER.warning("Retrying in %.0fs (attempt %d) after %s", delay, attempt, reason)
        self._sleep(delay)

    def iter_ads(self, max_items: Optional[int] = None, **query: Any) -> Iterator[Dict[str, Any]]:
        """Yield ads across all result pages until exhausted or max_items reached."""
        params: Optional[Dict[str, Any]] = self.build_params(**query)
        params["access_token"] = self.access_token
        url: Optional[str] = self.endpoint
        count = 0
        page = 0
        while url:
            page += 1
            payload = self._request(url, params)
            data = payload.get("data") or []
            LOGGER.info("Page %d: %d ads", page, len(data))
            for ad in data:
                yield ad
                count += 1
                if max_items is not None and count >= max_items:
                    return
            # `paging.next` is a fully-formed URL that already carries the token
            # and every query parameter, so stop sending our own params.
            url = (payload.get("paging") or {}).get("next")
            params = None
            if not data:
                break
