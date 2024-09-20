"""Auth_service links."""

REGISTRATION_LINK = '/registration'
AUTH_LINK = '/auth'
CHECK_TOKEN_LINK = '/check_token'
PHOTO_UPLOAD_LINK = '/verify'

"""Transaction_service links."""
CREATE_TRANSACTION_LINK = '/create_transaction'
CREATE_REPORT_LINK = '/create_report'


"""Errors messages"""
INVALID_TOKEN_MESSAGE = 'Invalid token'
TOKEN_EXPIRED_MESSAGE = 'Token is expired'
SERVICE_UNAVAILABLE = 'Next services are unavailable: {services}'
FILENAME_ERROR = 'File name is too shot or file has no extension.'


"""General links."""
HEALTH_LINK = '/healthz/ready'

"""Response texts."""
KAFKA_RESPONSE = 'Photo was uploaded'
