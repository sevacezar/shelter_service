import sys, os

from contextlib import asynccontextmanager
from datetime import datetime
from fastapi import FastAPI, Request, Query, APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorCollection

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from config import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USERNAME
from config import ADMIN_EMAIL, ADMIN_FIRST_NAME, ADMIN_PASSWORD, ADMIN_PHONE, ADMIN_SECOND_NAME
from database import MongoDBManager
from domain.animals import AnimalType, AnimalGender, CoatType, Size, Age
from domain.users import User
from repositories.mongodb.users_repo import UserMongoRepository
from use_cases.users.create_admin import CreateAdminUseCase
from web.fastapi.animals.filters import FiltersManager
from web.fastapi.users.routers import get_user_router

# Инициализация БД
mongo_manager: MongoDBManager = MongoDBManager(
    host=DB_HOST,
    port=DB_PORT,
    username=DB_USERNAME,
    password=DB_PASSWORD,
    db_name=DB_NAME,
)
db: AsyncIOMotorDatabase = mongo_manager.get_db()
user_repo: UserMongoRepository = UserMongoRepository(db=db)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Creating admin if not exist
    use_case: CreateAdminUseCase = CreateAdminUseCase(user_repo=user_repo)
    admin: User | None = await use_case.execute(
        first_name=ADMIN_FIRST_NAME,
        second_name=ADMIN_SECOND_NAME,
        email=ADMIN_EMAIL,
        phone=ADMIN_PHONE,
        password=ADMIN_PASSWORD,
    )
    if admin:
        print('Добавил в БД админа!')
    yield


app = FastAPI(lifespan=lifespan)
templates = Jinja2Templates(directory='web/fastapi/templates')
app.mount('/static', StaticFiles(directory='static'), name='static')

user_router: APIRouter = get_user_router(user_repo=user_repo, templates=templates)

app.include_router(user_router)

# animals_db = [
#     {
#         "id": '1',
#         "name": "Луна",
#         'animal_type': AnimalType.CAT.value,
#         "age": "3",
#         'age_type': Age.JUNIOUR.value,
#         'gender': AnimalGender.FEMALE.value,
#         'size': Size.MEDIUM.value,
#         'coat': CoatType.SHORT.value,
#         'main_photo': {'path': '/static/images/1/photo.jpg', 'description': 'Супер милое фото!'},
#         'additional_photos': [
#             {'path': '/static/images/1/photo_1.jpg', 'description': 'Еще милое фото1'},
#             {'path': '/static/images/1/photo_2.jpg', 'description': 'Еще милое фото2'},
#             {'path': '/static/images/1/photo_3.jpg', 'description': 'Еще милое фото3'},
#         ],
#         'description': 'энергичный и дружелюбный пес, который ищет любящую семью. Он отлично ладит с детьми и другими собаками, обожает длительные прогулки и активные игры. Барон прошел базовый курс дрессировки и знает основные команды.',
#         'health': 'Вакцинирован, кастрирован. Имеет ветеринарный паспорт.',
#         'ok_with': 'Подходит для семей с: детьми, собаками и другими животными.',
#      },
#      {
#         "id": '2',
#         "name": "Бруня",
#         'animal_type': AnimalType.DOG.value,
#         "age": "8",
#         'age_type': Age.ADULT.value,
#         'gender': AnimalGender.MALE.value,
#         'size': Size.EXTRA_LARGE.value,
#         'coat': CoatType.LONG.value,
#         'main_photo': {'path': '/static/images/2/photo.jpg', 'description': 'Супер милое фото!'},
#         'additional_photos': [
#             {'path': '/static/images/1/photo_1.jpg', 'description': 'Еще милое фото1'},
#             {'path': '/static/images/1/photo_2.jpg', 'description': 'Еще милое фото2'},
#             {'path': '/static/images/1/photo_3.jpg', 'description': 'Еще милое фото3'},
#         ],
#         'description': 'энергичный и дружелюбный пес, который ищет любящую семью. Он отлично ладит с детьми и другими собаками, обожает длительные прогулки и активные игры. Барон прошел базовый курс дрессировки и знает основные команды.',
#         'health': 'Вакцинирован, кастрирован. Имеет ветеринарный паспорт.',
#         'ok_with': 'Подходит для семей с: детьми, собаками и другими животными.',
#      },
#      {
#         "id": '3',
#         "name": "Леопольд",
#         'animal_type': AnimalType.CAT.value,
#         "age": "1",
#         'age_type': Age.BABY.value,
#         'gender': AnimalGender.MALE.value,
#         'size': Size.SMALL.value,
#         'coat': CoatType.MEDIUM.value,
#         'main_photo': {'path': '/static/images/3/photo.jpg', 'description': 'Супер милое фото!'},
#         'additional_photos': [
#             {'path': '/static/images/1/photo_1.jpg', 'description': 'Еще милое фото1'},
#             {'path': '/static/images/1/photo_2.jpg', 'description': 'Еще милое фото2'},
#             {'path': '/static/images/1/photo_3.jpg', 'description': 'Еще милое фото3'},
#         ],
#         'description': 'энергичный и дружелюбный пес, который ищет любящую семью. Он отлично ладит с детьми и другими собаками, обожает длительные прогулки и активные игры. Барон прошел базовый курс дрессировки и знает основные команды.',
#         'health': 'Вакцинирован, кастрирован. Имеет ветеринарный паспорт.',
#         'ok_with': 'Подходит для семей с: детьми, собаками и другими животными.',
#      },
#      {
#         "id": '4',
#         "name": "Дейзи",
#         'animal_type': AnimalType.DOG.value,
#         "age": "12",
#         'age_type': Age.SENIOR.value,
#         'gender': AnimalGender.FEMALE.value,
#         'size': Size.MEDIUM.value,
#         'coat': CoatType.SHORT.value,
#         'main_photo': {'path': '/static/images/4/photo.jpg', 'description': 'Супер милое фото!'},
#         'additional_photos': [
#             {'path': '/static/images/1/photo_1.jpg', 'description': 'Еще милое фото1'},
#             {'path': '/static/images/1/photo_2.jpg', 'description': 'Еще милое фото2'},
#             {'path': '/static/images/1/photo_3.jpg', 'description': 'Еще милое фото3'},
#         ],
#         'description': 'энергичный и дружелюбный пес, который ищет любящую семью. Он отлично ладит с детьми и другими собаками, обожает длительные прогулки и активные игры. Барон прошел базовый курс дрессировки и знает основные команды.',
#         'health': 'Вакцинирован, кастрирован. Имеет ветеринарный паспорт.',
#         'ok_with': 'Подходит для семей с: детьми, собаками и другими животными.',
#      },

#     # Добавьте больше данных...
# ]

# def filter_animals(
#     animals: list[dict],
#     animal_type: list[str] | None = None,
#     age_type: list[str] | None = None,
#     gender: list[str] | None = None,
#     coat: list[str] | None = None,
#     size: list[str] | None = None
# ) -> list[dict]:
#     filtered = animals
#     if animal_type:
#         filtered = [a for a in filtered if a["animal_type"] in animal_type]
#     if age_type:
#         filtered = [a for a in filtered if a["age_type"] in age_type]
#     if gender:
#         filtered = [a for a in filtered if a["gender"] in gender]
#     if coat:
#         filtered = [a for a in filtered if a["coat"] in coat]
#     if size:
#         filtered = [a for a in filtered if a["size"] in size]
#     return filtered

# @app.get('/', response_class=HTMLResponse)
# async def home(
#     request: Request,
#     animal_type: list[str] | None = Query(None),
#     age_type: list[str] | None = Query(None),
#     gender: list[str] | None = Query(None),
#     coat: list[str] | None = Query(None),
#     size: list[str] | None = Query(None),
# ):
#     filtered_animals = filter_animals(
#         animals_db,
#         animal_type,
#         age_type,
#         gender,
#         coat,
#         size,
#     )
#     return templates.TemplateResponse(
#         'animals.html',
#         {
#             'request': request,
#             'animals': filtered_animals,
#             'query_params': request.query_params,
#             'filters': FiltersManager.get_filters_data_with_options(),
#         }
#     )

# @app.get('/animals/{animal_id}', response_class=HTMLResponse)
# async def animal_detail(request: Request, animal_id: str):
#     animal = next((a for a in animals_db if a['id'] == animal_id))
#     if not animal:
#         return HTMLResponse(content='Animal not found', status_code=404)
#     return templates.TemplateResponse('animal_detail.html', {'request': request, 'animal': animal})


# @app.get('/admin/{entity_name}', response_class=HTMLResponse)
# async def admin_list(request: Request, entity_name: str):
#     if entity_name == 'animals':
#         items_ = animals_db
#         for _ in range(10):
#             items_.extend(animals_db)

#         entity = {
#             'label': "Питомцы",
#             'name': 'animals',
#             'columns': [
#                 {'label': 'ID', 'name': 'id'},
#                 {'label': 'Имя', 'name': 'name'},
#                 {'label': 'Возраст', 'name': 'age'},
#                 {'label': 'Пол', 'name': 'gender'},
#                 {'label': 'Размер', 'name': 'size'},
#             ],
#             'items_': items_,
#         }
#         meta = [
#             {'name': 'users', 'label': 'Пользователи', 'icon': 'fas fa-users', 'url': '/admin/users'},
#             {'name': 'animals', 'label': 'Питомцы', 'icon': 'fas fa-paw', 'url': '/admin/animals'},
#             {'name': 'views', 'label': 'Просмотры', 'icon': 'fas fa-eye', 'url': '/admin/views'},
#             {'name': 'requests', 'label': 'Заявки на усыновление', 'icon': 'fas fa-heart', 'url': '/admin/requests'},

#         ]
#     else:
#         return HTMLResponse(content='Сущность не найдена', status_code=404)
#     return templates.TemplateResponse('admin_list.html', {'request': request, 'entity': entity, 'meta': meta})

# @app.get('/admin/{entity_name}/add', response_class=HTMLResponse)
# @app.get('/admin/{entity_name}/{id}/update', response_class=HTMLResponse)
# async def admin_add(request: Request, entity_name: str):
#     if entity_name == 'animals':
#         entity = {
#             'label': "Питомца",
#             'name': 'animals',
#             'fields': [
#                 {
#                     'name': 'name',
#                     'label': 'Имя',
#                     'type': 'input',
#                     'input_type': 'text',
#                     'required': True,
#                     'value': 'Дейзи',
#                 },
#                 {
#                     'name': 'gender',
#                     'label': 'Пол',
#                     'type': 'select',
#                     'options': [
#                         {'value': 'male', 'label': 'Мальчик'},
#                         {'value': 'female', 'label': 'Девочка', 'selected': True},
#                     ],
#                     'required': True,
#                 },
#                 {
#                     'name': 'birth_date',
#                     'label': 'День рождения',
#                     'type': 'input',
#                     'input_type': 'date',
#                     'required': True,
#                     # 'value': datetime(2023, 1, 1),
#                     'value': datetime(2023, 1, 1).strftime(format='%Y-%m-%d'),
#                 },
#                 {
#                     'name': 'description',
#                     'label': 'Описание',
#                     'type': 'textarea',
#                     'required': True,
#                     'value': 'Очень хорошая собака',
#                 },
#             ],
#             'extras': [
#                 {'name': 'has_vaccinations', 'label': 'Вакцинирован', 'checked': True},
#                 {'name': 'is_sterilized', 'label': 'Стерилизован',},
#             ],
#             'images': [
#                 {'id': '1', 'path': '/static/images/1/photo.jpg', 'description': 'Супер милое фото!', 'is_avatar': True},
#                 {'id': '2', 'path': '/static/images/1/photo_1.jpg', 'description': 'Супер милое фото 1!', 'is_avatar': False},
#                 {'id': '3', 'path': '/static/images/1/photo_2.jpg', 'description': 'Супер милое фото 2!', 'is_avatar': False},
#             ],
#         }
#         meta = [
#             {'name': 'users', 'label': 'Пользователи', 'icon': 'fas fa-users', 'url': '/admin/users'},
#             {'name': 'animals', 'label': 'Питомцы', 'icon': 'fas fa-paw', 'url': '/admin/animals'},
#             {'name': 'views', 'label': 'Просмотры', 'icon': 'fas fa-eye', 'url': '/admin/views'},
#             {'name': 'requests', 'label': 'Заявки на усыновление', 'icon': 'fas fa-heart', 'url': '/admin/requests'},

#         ]
#     else:
#         return HTMLResponse(content='Сущность не найдена', status_code=404)
#     return templates.TemplateResponse('admin_form.html', {'request': request, 'entity': entity, 'meta': meta, 'action': 'update'})


# @app.get('/admin/{entity_name}/{id}', response_class=HTMLResponse)
# async def admin_detail_view(request: Request, entity_name: str, id: str):
#     if entity_name == 'animals':
#         entity = {
#             'label': "Питомца",
#             'name': 'animals',
#             'fields': [
#                 {
#                     'name': 'name',
#                     'label': 'Имя',
#                     'type': 'input',
#                     'input_type': 'text',
#                     'required': True,
#                     'value': 'Дейзи',
#                 },
#                 {
#                     'name': 'gender',
#                     'label': 'Пол',
#                     'type': 'select',
#                     'options': [
#                         {'value': 'male', 'label': 'Мальчик'},
#                         {'value': 'female', 'label': 'Девочка', 'selected': True},
#                     ],
#                     'required': True,
#                 },
#                 {
#                     'name': 'birth_date',
#                     'label': 'День рождения',
#                     'type': 'input',
#                     'input_type': 'date',
#                     'required': True,
#                     # 'value': datetime(2023, 1, 1),
#                     'value': datetime(2023, 1, 1).strftime(format='%Y-%m-%d'),
#                 },
#                 {
#                     'name': 'description',
#                     'label': 'Описание',
#                     'type': 'textarea',
#                     'required': True,
#                     'value': 'Очень хорошая собака',
#                 },
#             ],
#             'extras': [
#                 {'name': 'has_vaccinations', 'label': 'Вакцинирован', 'checked': True},
#                 {'name': 'is_sterilized', 'label': 'Стерилизован',},
#             ],
#             'images': [
#                 {'id': '1', 'path': '/static/images/1/photo.jpg', 'description': 'Супер милое фото!', 'is_avatar': True},
#                 {'id': '2', 'path': '/static/images/1/photo_1.jpg', 'description': 'Супер милое фото 1!', 'is_avatar': False},
#                 {'id': '3', 'path': '/static/images/1/photo_2.jpg', 'description': 'Супер милое фото 2!', 'is_avatar': False},
#             ],
#         }
#         meta = [
#             {'name': 'users', 'label': 'Пользователи', 'icon': 'fas fa-users', 'url': '/admin/users'},
#             {'name': 'animals', 'label': 'Питомцы', 'icon': 'fas fa-paw', 'url': '/admin/animals'},
#             {'name': 'views', 'label': 'Просмотры', 'icon': 'fas fa-eye', 'url': '/admin/views'},
#             {'name': 'requests', 'label': 'Заявки на усыновление', 'icon': 'fas fa-heart', 'url': '/admin/requests'},

#         ]
#     else:
#         return HTMLResponse(content='Сущность не найдена', status_code=404)
#     return templates.TemplateResponse('admin_detail.html', {'request': request, 'entity': entity, 'meta': meta,})


# @app.get('/users/register', response_class=HTMLResponse)
# async def register(request: Request):
#     return templates.TemplateResponse('users_register_form.html', {'request': request,})

# @app.get('/users/login', response_class=HTMLResponse)
# async def register(request: Request):
#     return templates.TemplateResponse('users_login_form.html', {'request': request,})

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app=app, reload=True)
    