from rest_framework.response import Response
from rest_framework.status import is_informational, is_success, is_redirect, is_client_error, is_server_error


class AppResponse(Response):

    def __init__(self, data=None, status=None, message=None):

        super(AppResponse, self).__init__(None, status=status)

        status_message = ""
        try:
            if is_informational(status):
                status_message = "informational"
            elif is_success(status):
                status_message = "ok"
            elif is_redirect(status):
                status_message = "redirect"
            elif is_client_error(status):
                status_message = "client_error"
            elif is_server_error(status):
                status_message = "server_error"
        except TypeError:
            status_message = ""

        self.data = {
            'data': data,
            'status_message': status_message,
            'message': message
        }



