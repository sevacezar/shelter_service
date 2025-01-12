from fastapi import FastAPI, Request, Query
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

templates = Jinja2Templates(directory='web/fastapi/templates')
app.mount('/static', StaticFiles(directory='static'), name='static')

animals_db = [
    {"id": '1', "name": "Luna", "type": "cat", "age": "young", "gender": "female", "size": "medium", "fur": "long"},
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
