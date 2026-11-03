import csv
import json
import tempfile
import unittest
from pathlib import Path

import requests

from ad_library.cli import main
from ad_library.client import AdLibraryClient, AdLibraryError
from ad_library.export import flatten_ad, write_ads

AD1 = {
    "id": "111",
    "page_id": "9",
    "page_name": "Acme",
    "ad_creative_bodies": ["Buy now", "Sale"],
    "publisher_platforms": ["facebook", "instagram"],
    "ad_snapshot_url": "https://www.facebook.com/ads/archive/render_ad/?id=111",
}
AD2 = {
    "id": "222",
    "page_id": "9",
    "page_name": "Acme",
    "spend": {"lower_bound": "100", "upper_bound": "199"},
    "demographic_distribution": [{"age": "18-24", "gender": "male", "percentage": "0.5"}],
}


class FakeResponse:
    def __init__(self, status, payload):
        self.status_code = status
        self._payload = payload
        self.text = json.dumps(payload)

    def json(self):
        return self._payload


class FakeSession:
    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = []

    def get(self, url, params=None, timeout=None):
        self.calls.append((url, params))
        item = self.responses.pop(0)
        if isinstance(item, Exception):
            raise item
        return item


def make_client(responses, **kw):
    session = FakeSession(responses)
    client = AdLibraryClient("TOKEN", session=session, sleep=lambda s: None, **kw)
    return client, session


class ClientTests(unittest.TestCase):
    def test_requires_token(self):
        with self.assertRaises(ValueError):
            AdLibraryClient("")

    def test_build_params(self):
        client, _ = make_client([])
        params = client.build_params(
            countries=["us", "gb"], search_terms="shoes", platforms=["instagram"], page_size=5000
        )
        self.assertEqual(params["ad_reached_countries"], '["US", "GB"]')
        self.assertEqual(params["search_terms"], "shoes")
        self.assertEqual(params["search_type"], "KEYWORD_UNORDERED")
        self.assertEqual(params["publisher_platforms"], '["INSTAGRAM"]')
        self.assertEqual(params["limit"], 1000)
        self.assertIn("ad_snapshot_url", params["fields"])
        self.assertNotIn("spend", params["fields"])

    def test_political_fields_added(self):
        client, _ = make_client([])
        params = client.build_params(countries=["US"], search_terms="x", ad_type="POLITICAL_AND_ISSUE_ADS")
        self.assertIn("spend", params["fields"])

    def test_requires_query(self):
        client, _ = make_client([])
        with self.assertRaises(ValueError):
            client.build_params(countries=["US"])

    def test_pagination_follows_next(self):
        client, session = make_client([
            FakeResponse(200, {"data": [AD1], "paging": {"next": "https://graph.facebook.com/next?after=abc"}}),
            FakeResponse(200, {"data": [AD2]}),
        ])
        ads = list(client.iter_ads(countries=["US"], search_terms="x"))
        self.assertEqual([a["id"] for a in ads], ["111", "222"])
        self.assertEqual(session.calls[0][1]["access_token"], "TOKEN")
        self.assertEqual(session.calls[1], ("https://graph.facebook.com/next?after=abc", None))

    def test_max_items_stops_early(self):
        client, session = make_client([
            FakeResponse(200, {"data": [AD1, AD2], "paging": {"next": "https://x/next"}}),
        ])
        ads = list(client.iter_ads(max_items=1, countries=["US"], search_terms="x"))
        self.assertEqual(len(ads), 1)
        self.assertEqual(len(session.calls), 1)

    def test_retries_rate_limit_then_succeeds(self):
        client, session = make_client([
            FakeResponse(400, {"error": {"code": 613, "message": "Calls limited"}}),
            requests.ConnectionError("boom"),
            FakeResponse(200, {"data": [AD1]}),
        ])
        ads = list(client.iter_ads(countries=["US"], search_terms="x"))
        self.assertEqual(len(ads), 1)
        self.assertEqual(len(session.calls), 3)

    def test_permanent_error_raises(self):
        client, _ = make_client([
            FakeResponse(400, {"error": {"code": 190, "message": "Invalid OAuth access token"}}),
        ])
        with self.assertRaises(AdLibraryError) as ctx:
            list(client.iter_ads(countries=["US"], search_terms="x"))
        self.assertEqual(ctx.exception.code, 190)
        self.assertIn("Invalid OAuth", str(ctx.exception))

    def test_gives_up_after_max_retries(self):
        client, session = make_client(
            [FakeResponse(500, {"error": {"code": 2, "message": "Service unavailable"}})] * 3,
            max_retries=2,
        )
        with self.assertRaises(AdLibraryError):
            list(client.iter_ads(countries=["US"], search_terms="x"))
        self.assertEqual(len(session.calls), 3)


class ExportTests(unittest.TestCase):
    def test_flatten(self):
        row = flatten_ad(AD2)
        self.assertEqual(row["spend_lower"], "100")
        self.assertEqual(row["spend_upper"], "199")
        self.assertEqual(json.loads(row["demographic_distribution"])[0]["age"], "18-24")
        self.assertEqual(flatten_ad(AD1)["ad_creative_bodies"], "Buy now | Sale")

    def test_write_all_formats(self):
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            write_ads([AD1, AD2], d / "a.json", "json")
            self.assertEqual(len(json.loads((d / "a.json").read_text())), 2)
            write_ads([AD1, AD2], d / "a.jsonl", "jsonl")
            self.assertEqual(len((d / "a.jsonl").read_text().splitlines()), 2)
            write_ads([AD1, AD2], d / "sub" / "a.csv", "csv")
            with (d / "sub" / "a.csv").open() as fh:
                rows = list(csv.DictReader(fh))
            self.assertEqual(rows[0]["id"], "111")
            self.assertEqual(rows[1]["spend_upper"], "199")
            self.assertEqual(list(rows[0])[0], "id")


class CliTests(unittest.TestCase):
    def test_missing_token_fails_cleanly(self):
        import os
        old = os.environ.pop("META_ACCESS_TOKEN", None)
        try:
            self.assertEqual(main(["-q", "shoes", "-o", "/dev/null"]), 1)
        finally:
            if old is not None:
                os.environ["META_ACCESS_TOKEN"] = old

    def test_requires_search_or_pages(self):
        with self.assertRaises(SystemExit):
            main([])


if __name__ == "__main__":
    unittest.main()
