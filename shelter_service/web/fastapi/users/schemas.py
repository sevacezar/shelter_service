import re

from pydantic import BaseModel, EmailStr, constr, field_validator, Field
from fastapi import Form

class RegistrationForm(BaseModel):
    first_name: str
    second_name: str
    email: str
    phone: str
    password: str
    password_confirm: str

    @field_validator('first_name', 'second_name')
    @classmethod
    def validate_name(cls, value):
        if len(value) < 2 or len(value) > 50:
            raise ValueError('Имя и фамилия должны быть от 2 до 50 символов')
        return value.strip()
    
    @field_validator('email')
    @classmethod
    def validate_email(cls, value):
        if not re.match(
            r'^[a-zA-Z0-9\_\.\-\+]+@[a-zA-Z0-9\.\-]+\.[a-zA-Z0-9\-\.]{2,}$',
            value,
        ):
            raise ValueError('Некорректный формат email')
        return value

    @field_validator('phone')
    @classmethod
    def validate_phone(cls, value):
        if not re.match(r'^\+?\d{10,15}$', value):
            raise ValueError('Телефон должен содержать от 10 до 15 цифр и может начинаться с +')
        return value
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, value):
        if len(value) < 8 or len(value) > 128:
            raise ValueError('Пароль должен быть от 8 до 128 символов')
        return value

    @field_validator('password_confirm')
    @classmethod
    def password_match(cls, password_confirm, values):
        if 'password' in values.data and password_confirm != values.data['password']:
            raise ValueError('Пароли не совпадают')
        return password_confirm

    @classmethod
    def as_form(
        cls,
        first_name: str = Form(...),
        second_name: str = Form(...),
        email: str = Form(...),
        phone: str = Form(...),
        password: str = Form(...),
        password_confirm: str = Form(...),
    ):
        return cls(
            first_name=first_name,
            second_name=second_name,
            email=email,
            phone=phone,
            password=password,
            password_confirm=password_confirm,
        )


class LoginForm(BaseModel):
    email: str
    password: str

    @field_validator('email')
    @classmethod
    def validate_email(cls, value):
        if not re.match(
            r'^[a-zA-Z0-9\_\.\-\+]+@[a-zA-Z0-9\.\-]+\.[a-zA-Z0-9\-\.]{2,}$',
            value,
        ):
            raise ValueError('Некорректный формат email')
        return value


    @classmethod
    def as_form(
        cls,
        email: str = Form(...),
        password: str = Form(...),
    ):
        return cls(
            email=email,
            password=password,
        )