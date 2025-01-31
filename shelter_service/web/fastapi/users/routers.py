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
    ):
        form_data = await request.form()
        try:
            form = RegistrationForm.as_form(
                first_name=form_data.get('first_name'),
                second_name=form_data.get('second_name'),
                email=form_data.get('email'),
                phone=form_data.get('phone'),
                password=form_data.get('password'),
                password_confirm=form_data.get('password_confirm'),
            )
            user: User = await register_user_use_case.execute(
                first_name=form.first_name,
                second_name=form.second_name,
                email=form.email,
                phone=form.phone,
                password=form.password,
            )
            return RedirectResponse('/', status_code=302)
        except ValidationError as exc:
            validation_errors = {}
            for err in exc.errors():
                field = err['loc'][0]
                message = err['msg'].replace('Value error, ', '')
                validation_errors[field] = message
            return templates.TemplateResponse(
                'users_register_form.html',
                {'request': request, 'validation_errors': validation_errors, 'form_data': form_data}
            )
        except UserAlreadyExists as exc:
            return templates.TemplateResponse(
                'users_register_form.html',
                {'request': request, 'error_message': 'Пользователь с данным email уже зарегистрирован', 'form_data': form_data.model_dump()},
            )
        except ValueError as exc:
            return templates.TemplateResponse(
                'users_register_form.html',
                {'request': request, 'error_message': str(exc), 'form_data': form_data.model_dump()},
            )

    @router.get('/login')
    async def get_login_page(request: Request):
        return templates.TemplateResponse('users_login_form.html', {'request': request})
    
    @router.post('/login')
    async def login(
        request: Request,
    ):
        form_data = await request.form()
        try:
            form = LoginForm(
                email=form_data.get('email'),
                password=form_data.get('password'),
            )
            user: User = await login_user_use_case.execute(
                email=form.email,
                password=form.password,
            )
            access_token: str = create_access_token(
                data={'sub': str(user.id)}
            )
            response = RedirectResponse('/animals', status_code=302)
            response.set_cookie(key='token', value=access_token, httponly=True)
            return response
        except ValidationError as exc:
            validation_errors = {}
            for err in exc.errors():
                field = err['loc'][0]
                message = err['msg'].replace('Value error, ', '')
                validation_errors[field] = message
            return templates.TemplateResponse(
                'users_login_form.html',
                {'request': request, 'validation_errors': validation_errors, 'form_data': form_data}
            )
        except (UserNotFound, WrongPassword) as exc:
            return templates.TemplateResponse(
                'users_login_form.html',
                {'request': request, 'error_message': 'Неправильный email или пароль', 'form_data': form_data}
            )

    return router