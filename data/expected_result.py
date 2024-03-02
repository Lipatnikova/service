"""
This section contains the main code statuses and other result from API methods
"""


class StatusCode:
    OK = 200
    NO_CONTENT = 204
    INTERNAL_ERROR = 500


class Expected:
    content_type = 'application/json'
    count_headers = 3
