# standard imports
import unittest
import io

# local imports
from parse import *
from error import (
    JSONParseError,
)


class TestParse(unittest.TestCase):
    def setUp(self):
        self.valid_o = {
            "json": "2.0",
            "id": 42,
            "method": "foo_bazBaz",
            "params": [
                13,
                {
                    "xyzzy": 666,
                    "inky": ["pinky", "blinky", "clyde"],
                },
            ],
        }

    def test_from_dict(self):
        r = json_from_dict(self.valid_o)
        self.assertEqual(r["id"], self.valid_o["id"])
        self.assertEqual(r["params"], self.valid_o["params"])
        self.assertEqual(r["method"], self.valid_o["method"])

        s = json.dumps(self.valid_o)
        r = json_from_str(s)
        self.assertEqual(r["id"], self.valid_o["id"])
        self.assertEqual(r["params"], self.valid_o["params"])
        self.assertEqual(r["method"], self.valid_o["method"])

        r = json_from_file(io.BytesIO(s.encode("utf-8")))
        self.assertEqual(r["id"], self.valid_o["id"])
        self.assertEqual(r["params"], self.valid_o["params"])
        self.assertEqual(r["method"], self.valid_o["method"])

    def test_missing_version(self):
        o = self._extracted_from_test_params_2("jsonrpc")

    def test_id(self):
        o = self._extracted_from_test_params_2("id")
        o["id"] = None
        with self.assertRaises(JSONParseError):
            json_from_dict(o)

        o["id"] = {}
        with self.assertRaises(JSONInvalidRequestError):
            json_from_dict(o)

        o["id"] = JSON_PRC()
        with self.assertRaises(JSONInvalidRequestError):
            json_from_dict(o)

    def test_method(self):
        o = self._extracted_from_test_params_2("method")
        o["method"] = None
        with self.assertRaises(JSONParseError):
            json_from_dict(o)

        o["method"] = 42
        with self.assertRaises(JSONInvalidRequestError):
            json_from_dict(o)

        o["method"] = {}
        with self.assertRaises(JSONInvalidRequestError):
            json_from_dict(o)

        o["method"] = JSON_PRC()
        with self.assertRaises(JSONInvalidRequestError):
            json_from_dict(o)

    def test_params(self):
        o = self._extracted_from_test_params_2("params")
        o["params"] = None
        with self.assertRaises(JSONParseError):
            json_from_dict(o)

        o["params"] = {}
        with self.assertRaises(JSONParseError):
            json_from_dict(o)

    def _extracted_from_test_params_2(self, arg0):
        result = self.valid_o
        del result[arg0]
        with self.assertRaises(JSONParseError):
            json_from_dict(result)
        return result


if __name__ == "__main__":
    unittest.main()
