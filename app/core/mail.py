from fastapi_mail import FastMail, ConnectionConfig
from app.core.config import settings

mail_config = ConnectionConfig(
    MAIL_USERNAME=settings.mail_username,
    MAIL_PASSWORD=settings.mail_password,
    MAIL_FROM=settings.mail_from,
    MAIL_SERVER=settings.mail_server,
    MAIL_PORT=settings.mail_port,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    SUPPRESS_SEND=settings.mail_suppress_send,
)

mail = FastMail(mail_config)