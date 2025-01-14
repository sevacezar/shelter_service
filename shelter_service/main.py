from fastapi import FastAPI, Request, Query
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

templates = Jinja2Templates(directory='web/fastapi/templates')
app.mount('/static', StaticFiles(directory='static'), name='static')

animals_db = [
    {
        "id": '1',
        "name": "Луна",
        "type": "cat",
        "age": "3",
        "gender": "девочка",
        "size": "средний",
        "fur": "long",
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
    {"id": '2', "name": "Max", "type": "dog", "age": "adult", "gender": "male", "size": "large", "fur": "short"},
    {"id": '3', "name": "Charlie", "type": "dog", "age": "baby", "gender": "male", "size": "small", "fur": "medium"},
    {"id": '4', "name": "Lula", "type": "dog", "age": "baby", "gender": "male", "size": "small", "fur": "medium"},

    # Добавьте больше данных...
]

def filter_animals(
    animals: list[dict],
    animal_type: list[str] | None = None,
    age: list[str] | None = None,
    gender: list[str] | None = None,
    fur: list[str] | None = None,
    size: list[str] | None = None
) -> list[dict]:
    filtered = animals
    if animal_type:
        filtered = [a for a in filtered if a["type"] in animal_type]
    if age:
        filtered = [a for a in filtered if a["age"] in age]
    if gender:
        filtered = [a for a in filtered if a["gender"] in gender]
    if fur:
        filtered = [a for a in filtered if a["fur"] in fur]
    if size:
        filtered = [a for a in filtered if a["size"] in size]
    return filtered

@app.get('/', response_class=HTMLResponse)
async def home(
    request: Request,
    animal_type: list[str] | None = Query(None),
    age: list[str] | None = Query(None),
    gender: list[str] | None = Query(None),
    fur: list[str] | None = Query(None),
    size: list[str] | None = Query(None),
):
    filtered_animals = filter_animals(
        animals_db,
        animal_type,
        age,
        gender,
        fur,
        size,
    )
    return templates.TemplateResponse(
        'animals.html',
        {
            'request': request,
            'animals': filtered_animals,
            'query_params': request.query_params,
        }
    )

@app.get('/animals/{animal_id}', response_class=HTMLResponse)
async def animal_detail(request: Request, animal_id: str):
    animal = next((a for a in animals_db if a['id'] == animal_id))
    if not animal:
        return HTMLResponse(content='Animal not found', status_code=404)
    return templates.TemplateResponse('animal_detail.html', {'request': request, 'animal': animal})
