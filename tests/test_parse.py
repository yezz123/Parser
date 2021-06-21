# standard imports
import unittest
import io

# local imports
from src.parse import *
from src.error import (
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
        o = self.valid_o
        del o["jsonrpc"]
        with self.assertRaises(JSONParseError):
            json_from_dict(o)

    def test_id(self):
        o = self.valid_o
        del o["id"]
        with self.assertRaises(JSONParseError):
            json_from_dict(o)

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
        o = self.valid_o
        del o["method"]

        with self.assertRaises(JSONParseError):
            json_from_dict(o)

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
        o = self.valid_o
        del o["params"]

        with self.assertRaises(JSONParseError):
            json_from_dict(o)

        o["params"] = None
        with self.assertRaises(JSONParseError):
            json_from_dict(o)

        o["params"] = {}
        with self.assertRaises(JSONParseError):
            json_from_dict(o)


if __name__ == "__main__":
    unittest.main()
