import unittest
import json

from src.error import (
    JSONException,
    JSONCustomException,
    JSONErrors,
    JSONParseError,
)
from src.interface import (
    json_error,
    DefaultErrorParser,
)


class WrongError(Exception):
    pass


class RightError(JSONCustomException):
    message = "Right"
    code = -32001


class TestError(unittest.TestCase):
    def test_base(self):
        e = JSONException("foo")
        self.assertEqual(str(e), "Unknown error: foo")

    def test_error_by_code(self):
        e = JSONErrors.get(-32700)
        self.assertTrue(isinstance(e, JSONParseError))

    def test_custom_error(self):
        with self.assertRaises(KeyError):
            e = JSONErrors.get(-1000)

        with self.assertRaises(ValueError):
            JSONErrors.add(-32000, WrongError)

        with self.assertRaises(ValueError):
            JSONErrors.add(JSONErrors.local_min - 1, RightError)

        with self.assertRaises(ValueError):
            JSONErrors.add(JSONErrors.local_max + 1, RightError)

        JSONErrors.add(-32000, RightError)
        e_retrieved = JSONErrors.get(-32000, "foo")
        self.assertEqual(type(RightError(None)), type(e_retrieved))
        self.assertEqual(str(e_retrieved), "Right error: foo")

    def test_error_interface(self):
        uu = "foo"
        e = json_error(uu, -32700)
        self.assertEqual(e["error"]["code"], -32700)
        self.assertEqual(e["error"]["message"], "Parse error")

    def test_default_error_translate(self):
        uu = "foo"
        p = DefaultErrorParser()
        e = json_error(uu, -32700)
        o = p.translate(e)
        print("e {}".format(o))

    def test_error_serialize(self):
        e = JSONParseError("foo", request_id="bar")
        o = dict(e)
        self.assertEqual(o["json"], "2.0")
        self.assertEqual(o["id"], "bar")
        self.assertEqual(o["error"]["code"], -32700)
        self.assertEqual(o["error"]["message"], "Parse error: foo")


if __name__ == "__main__":
    unittest.main()
