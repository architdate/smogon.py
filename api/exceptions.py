class Error(Exception):
    """Base class for other exceptions"""
    pass

class InvalidSpecies(Error):
    """Species out of bounds of legitimate species"""
    pass

class InvalidForm(Error):
    """Form is invalid"""
    pass

class APIError(Error):
    """Something wrong with the API"""
    pass