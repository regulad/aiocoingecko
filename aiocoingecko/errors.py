from aiohttp import ClientResponse


class LibraryException(Exception):
    """Base Error that other errors inherit from."""

    pass


class NoInitialisedSession(LibraryException):
    """Raised when a ClientSession is not available. Created on __aenter__, or when passed."""

    pass


class HTTPException(LibraryException):
    """Raised when an HTTP Error occurs."""

    def __init__(self, *args, status_code: int):
        """:argument status_code The HTTP status code of the error in question."""

        self.status_code = status_code

        super().__init__(*args)


class RatelimitException(HTTPException):
    """Raised when getting a 429 response from the API"""

    def __init__(self, *args):
        super().__init__(*args, status_code=429)


class UnknownResponse(HTTPException):
    """Raised when getting an unknown JSON response from the API"""

    def __init__(self, *args, resp: ClientResponse):
        """:argument resp The response that could not be decoded."""

        self.resp = resp

        super().__init__(*args, status_code=200)


__all__ = ["LibraryException", "NoInitialisedSession", "HTTPException", "RatelimitException", "UnknownResponse"]
