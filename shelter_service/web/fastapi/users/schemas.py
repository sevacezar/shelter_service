from pydantic import BaseModel, EmailStr, constr
from fastapi import Form

class RegistrationForm(BaseModel):
    first_name: constr(strip_whitespace=True, min_length=2, max_length=50)
    second_name: constr(strip_whitespace=True, min_length=2, max_length=50)
    email: EmailStr
    phone: constr(regex=r'^\+?\d{10,15}$')
    password: constr(min_length=8, max_length=128)

    @classmethod
    def as_form(
        cls,
        first_name: str = Form(...),
        second_name: str = Form(...),
        email: str = Form(...),
        phone: str = Form(...),
        password: str = Form(...),
    ):
        return cls(
            first_name=first_name,
            second_name=second_name,
            email=email,
            phone=phone,
            password=password,
        )
