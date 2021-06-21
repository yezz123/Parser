import uuid
from .base import JSON_PRC
from .error import JSONErrors, JSONUnhandledErrorException


class DefaultErrorParser:
    def translate(self, error):
        code = error["error"]["code"]
        message = error["error"]["message"]
        if type(code).__name__ != "int":
            raise ValueError(
                "error code is not int by {} in error {}".format(type(code), error)
            )

        exc = None
        try:
            exc = JSONErrors.get(code, message)
        except KeyError:
            return JSONUnhandledErrorException(code, message)


def json_template(request_id=None):
    if request_id == None:
        request_id = str(uuid.uuid4())

    return {
        "json_prc": JSON_PRC.version_string,
        "id": request_id,
        "method": None,
        "params": [],
    }


def json_request(method, request_id=None):
    req = json_template(request_id=request_id)
    req["method"] = method
    return req


def json_result(o, ep):
    if o.get("error") != None:
        raise ep.translate(o)
    return o["result"]


def jsonrpc_response(request_id, result):
    return {
        "json_prc": JSON_PRC.version_string,
        "id": request_id,
        "result": result,
    }


def json_error(request_id, code, message=None):
    e = JSONErrors.get(code, message)
    return {
        "json_prc": JSON_PRC.version_string,
        "id": request_id,
        "error": {
            "code": code,
            "message": str(e),
        },
    }


def json_is_response_to(request, response):
    return request["id"] == response["id"]
