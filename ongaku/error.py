class OngakuBaseException(Exception):
    """
    The base exception for all Ongaku exceptions.    
    """

class ResponseException(OngakuBaseException):
    """
    Raised when a 4XX or 5XX error gets recieved.
    """

class BuildException(OngakuBaseException):
    """
    Raised when a model fails to build correctly.
    """