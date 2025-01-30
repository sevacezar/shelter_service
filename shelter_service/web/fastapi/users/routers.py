from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError

from domain.users import User
from repositories.base.user_base_repo import UserBaseRepository
from use_cases.exceptions import UserAlreadyExists, UserNotFound, WrongPassword
from use_cases.users.login_user import LoginUserUseCase
from use_cases.users.register_user import RegisterUserUseCase
from web.fastapi.users.auth import create_access_token
from web.fastapi.users.schemas import RegistrationForm, LoginForm


def get_user_router(
        user_repo: UserBaseRepository,
        templates: Jinja2Templates,
    ) -> APIRouter:
    router = APIRouter(prefix='/auth', tags=['Auth'])
    register_user_use_case: RegisterUserUseCase = RegisterUserUseCase(user_repo=user_repo)
    login_user_use_case: LoginUserUseCase = LoginUserUseCase(user_repo=user_repo)

    @router.get('/register')
    async def get_register_page(request: Request):
        return templates.TemplateResponse('users_register_form.html', {'request': request})

    @router.post('/register')
    async def register(
        request: Request,
        form_data: RegistrationForm = Depends(RegistrationForm.as_form),
    ):
        try:
            user: User = await register_user_use_case.execute(
                first_name=form_data.first_name,
                second_name=form_data.second_name,
                email=form_data.email,
                phone=form_data.phone,
                password=form_data.password,
                password_confirm=form_data.password_confirm,

            )
            return RedirectResponse('/', status_code=302)
        except UserAlreadyExists as exc:
            return templates.TemplateResponse(
                'users_register_form.html',
                {'request': request, 'error': str(exc), 'form_data': form_data.model_dump()},
            )
        except ValidationError as exc:
            return templates.TemplateResponse(
                'users_register_form.html',
                {'requset': request, 'errors': exc.errors(), 'form_data': form_data.model_dump()}
            )
        
    @router.get('/login')
    async def get_login_page(request: Request):
        return templates.TemplateResponse('users_login_form.html', {'request': request})
    
    @router.post('/login')
    async def login(
        request: Request,
        response: Response,
        form_data: LoginForm = Depends(LoginForm.as_form)
    ):
        try:
            user: User = await login_user_use_case.execute(
                email=form_data.email,
                password=form_data.password,
            )
            access_token: str = create_access_token(
                data={'sub': str(user.id)}
            )
            print(access_token)
            response = RedirectResponse('/animals', status_code=302)
            response.set_cookie(key='token', value=access_token, httponly=True)
            return response
        except (UserNotFound, WrongPassword) as exc:
            return templates.TemplateResponse(
                'users_login_form.html',
                {'request': request, 'error': str(exc), 'form_data': form_data.model_dump()}
            )
        except ValidationError as exc:
            return templates.TemplateResponse(
                'users_login_form.html',
                {'requset': request, 'errors': exc.errors(), 'form_data': form_data.model_dump()}
            )

    return router