from fastapi.routing import APIRouter
from fastapi import Form, Depends, Body, BackgroundTasks
from pydantic import EmailStr

from core.dependencies import get_database
from core.exceptions import NotFoundException, BadRequest
from services.auth import AuthService
from services.subscriber import SubscriberService
from services.utils.mailing import Mailing, TemplateBodyVars
from application.schema.subscriber import SubscriberResponseSchema, LoginResponseSchema
from services.utils.codec import TokenCodec


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=LoginResponseSchema)
async def login(
    email: EmailStr = Form(...),
    password: str = Form(...),
    database: str = Depends(get_database),
):
    """Subscriber Login Endpoint"""
    auth_service = AuthService(database)
    subscriber = await auth_service.login(email, password)
    subscriber.id = str(subscriber.id)
    subscriber_dict = subscriber.dict(
        exclude={"password", "subscribed_blogs", "created_at"}
    )
    account_token = TokenCodec().encode(subscriber_dict)
    login_response = LoginResponseSchema(
        **subscriber.dict(), token_type="Bearer", access_token=account_token
    )
    return login_response


@router.get("/account/verify", response_model=SubscriberResponseSchema)
async def verify_account(token: str, db=Depends(get_database)):
    """
    Confirm account activation
    """
    auth_service = AuthService(db)
    subscriber = await auth_service.verify_account(token)
    subscriber_response = SubscriberResponseSchema(**subscriber.dict())
    return subscriber_response


@router.get("/account/reactivate", response_model=SubscriberResponseSchema)
async def reactivate_account(
    email: EmailStr, background_tasks: BackgroundTasks, db=Depends(get_database)
):
    """
    Reactivate account
    """
    subscriber_service = SubscriberService(db)
    auth_service = AuthService(db)
    mailing = Mailing()

    subscriber = await subscriber_service.get_by_email(email)
    if not subscriber:
        raise NotFoundException("Subscriber not found")

    template_vars = TemplateBodyVars(
        header="Activate your account",
        body=f"To complete your registration, please click on the link below:",
        action=token_url,
        action_message="Activate Account",
    )

    token_url = await auth_service.create_token_url(
        "api/v1/auth/account/activate", subscriber
    )

    background_tasks.add_task(
        mailing.send_email,
        "Complete Account Activation",
        template_vars,
        subscriber.email,
    )
    return SubscriberResponseSchema(**subscriber.dict())


@router.get("/account/forgot_password")
async def forgot_password(
    email: EmailStr, background_task: BackgroundTasks, db=Depends(get_database)
):
    """Send email with link to reset password"""
    auth_service = AuthService(db)
    subscriber_service = SubscriberService(db)
    subscriber = await subscriber_service.get_by_email(email)
    if subscriber is None:
        raise NotFoundException("Subscriber with email not found")

    token_url = await auth_service.create_token_url(
        "api/v1/auth/reset_password", subscriber
    )
    mailing = Mailing()
    template_vars = TemplateBodyVars(
        header="Password Reset",
        body=f"To reset your password, please click on the link below:",
        action=token_url,
        action_message="Reset Password",
    )
    background_task.add_task(
        mailing.send_email, "Reset Password", template_vars, subscriber.email
    )
    return {"message": "Email with link to reset password has been sent"}


@router.post("/account/reset_password", response_model=SubscriberResponseSchema)
async def reset_password(
    token: str = Body(...),
    password: str = Body(...),
    confirm_password: str = Body(...),
    db=Depends(get_database),
):
    """Reset password"""
    auth_service = AuthService(db)
    if password == confirm_password:
        subscriber = await auth_service.reset_password(token, password)
        return SubscriberResponseSchema(**subscriber.dict())
    raise BadRequest("Passwords do not match")
