# local imports
from .base import JSON_PRC


class JSONException(Exception, JSON_PRC):
    message = "Unknown"

    def __init__(self, v, request_id=None):
        context_v = "{} error".format(self.message)
        if v != None:
            context_v += ": " + v

        self.request_id = request_id

        super(JSONException, self).__init__(context_v)

    def __iter__(self):
        if self.request_id == None:
            raise AttributeError(
                "request id cannot be undefined when serializing error"
            )
        yield "json_prc", JSON_PRC.version_string
        yield "id", self.request_id
        yield "error", {
            "code": self.code,
            "message": str(self),
        }


class JSONCustomException(JSONException):
    code = -32000
    message = "Server"


class JSONParseError(JSONException):
    code = -32700
    message = "Parse"


class JSONInvalidRequestError(JSONException):
    code = -32600
    message = "Invalid request"


class JSONMethodNotFoundError(JSONException):
    code = -32601
    message = "Method not found"


class JSONInvalidParametersError(JSONException):
    code = -32602
    message = "Invalid parameters"


class JSONInternalError(JSONException):
    code = -32603
    message = "Internal"


class JSONUnhandledErrorException(KeyError):
    pass


class JSONErrors:
    reserved_max = -31999
    reserved_min = -32768
    local_max = -32000
    local_min = -32099

    translations = {
        -32700: JSONParseError,
        -32600: JSONInvalidRequestError,
        -32601: JSONMethodNotFoundError,
        -32602: JSONInvalidParametersError,
        -32603: JSONInternalError,
    }

    @classmethod
    def add(self, code, exception_object):
        if code < self.local_min or code > self.local_max:
            raise ValueError(
                "code must be in range <{},{}>".format(self.local_min, self.local_max)
            )
        exc = self.translations.get(code)
        if exc != None:
            raise ValueError("code already registered with {}".format(exc))

        if not issubclass(exception_object, JSONCustomException):
            raise ValueError(
                "exception object must be a subclass of json_base.error.JSONCustomException"
            )

        self.translations[code] = exception_object

    @classmethod
    def get(self, code, v=None):
        e = self.translations.get(code)
        if e == None:
            raise JSONUnhandledErrorException(code)
        return e(v)
