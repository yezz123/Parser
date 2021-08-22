# standard imports
import unittest

# local imports
from base import JSON_PRC
from interface import (
    json_request,
    jsonrpc_response,
    json_result,
    json_is_response_to,
)


class TestRequest(unittest.TestCase):
    def test_request(self):
        req = json_request("foo_barBaz")
        self.assertEqual(req["jsonrpc"], JSON_PRC.version_string)
        self.assertEqual(type(req["id"]).__name__, "str")
        self.assertEqual(req["method"], "foo_barBaz")
        self.assertEqual(len(req["params"]), 0)

    def test_response(self):
        res = jsonrpc_response("foo", 42)
        self.assertEqual(res["id"], "foo")
        self.assertEqual(res["result"], 42)
        r = json_result(res, None)
        self.assertEqual(r, 42)

    def test_response_compare(self):
        req = json_request("foo_barBaz")
        res = jsonrpc_response(req["id"], 42)
        self.assertTrue(json_is_response_to(req, res))


if __name__ == "__main__":
    unittest.main()
