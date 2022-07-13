from pydantic import EmailStr
from core.config import settings
from fastapi_mail import FastMail, MessageSchema,ConnectionConfig
from pydantic import BaseModel, AnyUrl
from typing import Union

class TemplateBodyVars(BaseModel):
    header: str
    body: str
    action: Union[AnyUrl, None]
    action_message: Union[str, None]

class Mailing:
    def __init__(self):
        self.mail_conf = ConnectionConfig(
            MAIL_USERNAME=settings.EMAIL_HOST_USER,
            MAIL_PASSWORD=settings.EMAIL_HOST_PASSWORD,
            MAIL_SERVER=settings.EMAIL_HOST,
            MAIL_PORT=settings.EMAIL_PORT,
            MAIL_USE_TLS=True,
            MAIL_USE_SSL=False,
            MAIL_FROM=settings.MAIL_FROM,
            MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
            TEMPLATE_FOLDER="services/utils/mail_templates"
        )


    def send_email(
        self, 
        subject: str, 
        template_vars: TemplateBodyVars,
        *recipients: EmailStr, 
    ):
        message = MessageSchema(
            recipients=recipients,
            subject=subject,
            template_body = template_vars.dict(),
        )
        mail = FastMail(self.mail_conf)
        mail.send(message, template_name="email_base.html")
        mail.close()
        return True