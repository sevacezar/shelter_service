class UserAlreadyExists(Exception):
    """Exception, when user with same email has already existed"""
    pass

class UserNotFound(Exception):
    """Exception, when user can`t be found"""
    pass

class AnimalNotFound(Exception):
    """Exception, when animal can`t be found"""
    pass

class ImageNotFound(Exception):
    """Exception, when image can`t be found"""
    pass
