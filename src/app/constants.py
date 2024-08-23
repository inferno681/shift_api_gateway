"""Ссылки для auth_service."""

REGISTRATION_LINK = '/registration'
AUTH_LINK = '/auth'
CHECK_TOKEN_LINK = '/check_token'
PHOTO_UPLOAD_LINK = '/verify'

"""Ссылки для transaction_service."""
CREATE_TRANSACTION_LINK = '/create_transaction'
CREATE_REPORT_LINK = '/create_report'


"""Сообщения об ошибках"""
INVALID_TOKEN_MESSAGE = 'Недействительный токен'
TOKEN_EXPIRED_MESSAGE = 'Срок действия токена истек'
SERVICE_UNAVAILABLE = 'Следующие сервисы не доступны: {services}'
FILENAME_ERROR = 'Имя файла слищком короткое или файл не имеет расширения'


"""Общие ссылки."""
HEALTH_LINK = '/healthz/ready'

"""Текст для ответов."""
KAFKA_RESPONSE = 'Сообщение принято в обработку'
