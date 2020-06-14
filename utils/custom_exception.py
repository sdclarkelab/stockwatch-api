from .custom_json_resp import CustomJsonResponse


# define Python user-defined exceptions
class UnAuthorizedException(Exception):
    """Raised when unauthorized"""

    def __init__(self, username):
        self.message = CustomJsonResponse.return_user_unauth()


class InvalidSerializedObject(Exception):
    """Raised if serialized object is invalid"""

    def __init__(self, message):
        self.message = message
