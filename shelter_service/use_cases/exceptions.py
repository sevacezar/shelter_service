class UserAlreadyExists(Exception):
    """Exception, when user with same email has already existed"""
    pass

class UserNotFound(Exception):
    """Exception, when user can`t be found"""
    pass