import os
import tempfile
import unittest
from pathlib import Path

from adsonar.envfile import load_env_file


class EnvFileTests(unittest.TestCase):
    def test_loads_and_respects_existing(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / ".env"
            p.write_text('# comment\nexport ADSONAR_T1="abc"\nADSONAR_T2=keep\nnot a line\n')
            os.environ["ADSONAR_T2"] = "existing"
            try:
                self.assertTrue(load_env_file(p))
                self.assertEqual(os.environ["ADSONAR_T1"], "abc")
                self.assertEqual(os.environ["ADSONAR_T2"], "existing")
            finally:
                os.environ.pop("ADSONAR_T1", None)
                os.environ.pop("ADSONAR_T2", None)

    def test_missing_file(self):
        self.assertFalse(load_env_file("/nonexistent/.env"))


if __name__ == "__main__":
    unittest.main()
