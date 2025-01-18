from fastapi import FastAPI, Request, Query
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from domain.animals import AnimalType, AnimalGender, CoatType, Size, Age
from web.fastapi.animals.filters import FiltersManager

app = FastAPI()

templates = Jinja2Templates(directory='web/fastapi/templates')
app.mount('/static', StaticFiles(directory='static'), name='static')

animals_db = [
    {
        "id": '1',
        "name": "Луна",
        'animal_type': AnimalType.CAT.value,
        "age": "3",
        'age_type': Age.JUNIOUR.value,
        'gender': AnimalGender.FEMALE.value,
        'size': Size.MEDIUM.value,
        'coat': CoatType.SHORT.value,
        'main_photo': {'path': '/static/images/1/photo.jpg', 'description': 'Супер милое фото!'},
        'additional_photos': [
            {'path': '/static/images/1/photo_1.jpg', 'description': 'Еще милое фото1'},
            {'path': '/static/images/1/photo_2.jpg', 'description': 'Еще милое фото2'},
            {'path': '/static/images/1/photo_3.jpg', 'description': 'Еще милое фото3'},
        ],
        'description': 'энергичный и дружелюбный пес, который ищет любящую семью. Он отлично ладит с детьми и другими собаками, обожает длительные прогулки и активные игры. Барон прошел базовый курс дрессировки и знает основные команды.',
        'health': 'Вакцинирован, кастрирован. Имеет ветеринарный паспорт.',
        'ok_with': 'Подходит для семей с: детьми, собаками и другими животными.',
     },
     {
        "id": '2',
        "name": "Бруня",
        'animal_type': AnimalType.DOG.value,
        "age": "8",
        'age_type': Age.ADULT.value,
        'gender': AnimalGender.MALE.value,
        'size': Size.EXTRA_LARGE.value,
        'coat': CoatType.LONG.value,
        'main_photo': {'path': '/static/images/2/photo.jpg', 'description': 'Супер милое фото!'},
        'additional_photos': [
            {'path': '/static/images/1/photo_1.jpg', 'description': 'Еще милое фото1'},
            {'path': '/static/images/1/photo_2.jpg', 'description': 'Еще милое фото2'},
            {'path': '/static/images/1/photo_3.jpg', 'description': 'Еще милое фото3'},
        ],
        'description': 'энергичный и дружелюбный пес, который ищет любящую семью. Он отлично ладит с детьми и другими собаками, обожает длительные прогулки и активные игры. Барон прошел базовый курс дрессировки и знает основные команды.',
        'health': 'Вакцинирован, кастрирован. Имеет ветеринарный паспорт.',
        'ok_with': 'Подходит для семей с: детьми, собаками и другими животными.',
     },
     {
        "id": '3',
        "name": "Леопольд",
        'animal_type': AnimalType.CAT.value,
        "age": "1",
        'age_type': Age.BABY.value,
        'gender': AnimalGender.MALE.value,
        'size': Size.SMALL.value,
        'coat': CoatType.MEDIUM.value,
        'main_photo': {'path': '/static/images/3/photo.jpg', 'description': 'Супер милое фото!'},
        'additional_photos': [
            {'path': '/static/images/1/photo_1.jpg', 'description': 'Еще милое фото1'},
            {'path': '/static/images/1/photo_2.jpg', 'description': 'Еще милое фото2'},
            {'path': '/static/images/1/photo_3.jpg', 'description': 'Еще милое фото3'},
        ],
        'description': 'энергичный и дружелюбный пес, который ищет любящую семью. Он отлично ладит с детьми и другими собаками, обожает длительные прогулки и активные игры. Барон прошел базовый курс дрессировки и знает основные команды.',
        'health': 'Вакцинирован, кастрирован. Имеет ветеринарный паспорт.',
        'ok_with': 'Подходит для семей с: детьми, собаками и другими животными.',
     },
     {
        "id": '4',
        "name": "Дейзи",
        'animal_type': AnimalType.DOG.value,
        "age": "12",
        'age_type': Age.SENIOR.value,
        'gender': AnimalGender.FEMALE.value,
        'size': Size.MEDIUM.value,
        'coat': CoatType.SHORT.value,
        'main_photo': {'path': '/static/images/4/photo.jpg', 'description': 'Супер милое фото!'},
        'additional_photos': [
            {'path': '/static/images/1/photo_1.jpg', 'description': 'Еще милое фото1'},
            {'path': '/static/images/1/photo_2.jpg', 'description': 'Еще милое фото2'},
            {'path': '/static/images/1/photo_3.jpg', 'description': 'Еще милое фото3'},
        ],
        'description': 'энергичный и дружелюбный пес, который ищет любящую семью. Он отлично ладит с детьми и другими собаками, обожает длительные прогулки и активные игры. Барон прошел базовый курс дрессировки и знает основные команды.',
        'health': 'Вакцинирован, кастрирован. Имеет ветеринарный паспорт.',
        'ok_with': 'Подходит для семей с: детьми, собаками и другими животными.',
     },

    # Добавьте больше данных...
]

def filter_animals(
    animals: list[dict],
    animal_type: list[str] | None = None,
    age_type: list[str] | None = None,
    gender: list[str] | None = None,
    coat: list[str] | None = None,
    size: list[str] | None = None
) -> list[dict]:
    filtered = animals
    if animal_type:
        filtered = [a for a in filtered if a["animal_type"] in animal_type]
    if age_type:
        filtered = [a for a in filtered if a["age_type"] in age_type]
    if gender:
        filtered = [a for a in filtered if a["gender"] in gender]
    if coat:
        filtered = [a for a in filtered if a["coat"] in coat]
    if size:
        filtered = [a for a in filtered if a["size"] in size]
    return filtered

@app.get('/', response_class=HTMLResponse)
async def home(
    request: Request,
    animal_type: list[str] | None = Query(None),
    age_type: list[str] | None = Query(None),
    gender: list[str] | None = Query(None),
    coat: list[str] | None = Query(None),
    size: list[str] | None = Query(None),
):
    filtered_animals = filter_animals(
        animals_db,
        animal_type,
        age_type,
        gender,
        coat,
        size,
    )
    return templates.TemplateResponse(
        'animals.html',
        {
            'request': request,
            'animals': filtered_animals,
            'query_params': request.query_params,
            'filters': FiltersManager.get_filters_data_with_options(),
        }
    )

@app.get('/animals/{animal_id}', response_class=HTMLResponse)
async def animal_detail(request: Request, animal_id: str):
    animal = next((a for a in animals_db if a['id'] == animal_id))
    if not animal:
        return HTMLResponse(content='Animal not found', status_code=404)
    return templates.TemplateResponse('animal_detail.html', {'request': request, 'animal': animal})


@app.get('/admin/{entity_name}', response_class=HTMLResponse)
async def admin_list(request: Request, entity_name: str):
    if entity_name == 'animals':
        items_ = animals_db
        for _ in range(10):
            items_.extend(animals_db)

        entity = {
            'label': "Питомцы",
            'name': 'animals',
            'columns': [
                {'label': 'ID', 'name': 'id'},
                {'label': 'Имя', 'name': 'name'},
                {'label': 'Возраст', 'name': 'age'},
                {'label': 'Пол', 'name': 'gender'},
                {'label': 'Размер', 'name': 'size'},
            ],
            'items_': items_,
        }
        meta = [
            {'name': 'users', 'label': 'Пользователи', 'icon': 'fas fa-users', 'url': '/admin/users'},
            {'name': 'animals', 'label': 'Питомцы', 'icon': 'fas fa-paw', 'url': '/admin/animals'},
            {'name': 'views', 'label': 'Просмотры', 'icon': 'fas fa-eye', 'url': '/admin/views'},
            {'name': 'requests', 'label': 'Заявки на усыновление', 'icon': 'fas fa-heart', 'url': '/admin/requests'},

        ]
    else:
        return HTMLResponse(content='Сущность не найдена', status_code=404)
    return templates.TemplateResponse('admin_list.html', {'request': request, 'entity': entity, 'meta': meta})