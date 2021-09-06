import json

from Parser.base import JSON_PRC
from Parser.error import JSONInvalidRequestError, JSONParseError
from Parser.interface import json_request


def json_validate_dict(o):
    version = o.get("json")
    if version is None:
        raise JSONParseError("missing json version field")
    elif version != JSON_PRC.version_string:
        raise JSONInvalidRequestError("Invalid version {}".format(version))

    method = o.get("method")
    if method is None:
        raise JSONParseError("missing method field")
    elif type(method).__name__ != "str":
        raise JSONInvalidRequestError("method must be str")

    params = o.get("params")
    if params is None:
        raise JSONParseError("missing params field")
    elif type(params).__name__ != "list":
        raise JSONParseError("params field must be array")

    request_id = o.get("id")
    if request_id is None:
        raise JSONParseError("missing id field")
    if type(request_id).__name__ not in ["str", "int"]:
        raise JSONInvalidRequestError("invalid id value, must be string or integer")

    return o


def json_from_str(s):
    o = json.loads(s)
    return json_from_dict(o)


def json_from_dict(o):
    o_parsed = json_validate_dict(o)
    req = json_request(o_parsed["method"], request_id=o_parsed["id"])
    req["params"] = o_parsed["params"]
    return req


def json_from_file(f):
    o = json.load(f)
    return json_from_dict(o)
