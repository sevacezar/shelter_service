from pydantic import BaseModel, EmailStr, constr, field_validator
from fastapi import Form

class RegistrationForm(BaseModel):
    first_name: constr(strip_whitespace=True, min_length=2, max_length=50)
    second_name: constr(strip_whitespace=True, min_length=2, max_length=50)
    email: EmailStr
    phone: constr(regex=r'^\+?\d{10,15}$')
    password: constr(min_length=8, max_length=128)
    password_confirm: constr(min_length=8, max_length=128)

    @field_validator('password_confirm')
    @classmethod
    def password_match(cls, password_confirm, values):
        if 'password' in values and password_confirm != values['password']:
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
