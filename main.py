# -*- coding: utf-8 -*-
from typing import Union
from fastapi import FastAPI
from datetime import datetime, date, time
from pydantic import BaseModel
from data_base import request_db

app = FastAPI()

class User:
    def __init__(self, id, nickname, status, favorites, date_of_creation, date_of_change):
        self.id = id
        self.nickname = nickname
        self.status = status
        self.favorites = favorites
        self.date_of_creation = date_of_creation
        self.date_of_change = date_of_change
    def to_json_all(self):
        return {"id": self.id,
                "nickname": self.nickname,
                "status": self.status,
                "favorites": self.favorites,
                "date_of_creation": self.date_of_creation,
                "date_of_change": self.date_of_change}
    def to_json(self, number_of_recipes): #возвращает поля пользователя + кол-во его рецептов
        return {"id": self.id,
                "nickname": self.nickname,
                "status": self.status,
                "number_of_recipes": number_of_recipes}







@app.get("/")
def read_root():
    return {"Hello": "World"} 


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

	
# Регистрация
@app.get("/user/add/{nickname}")
def user_add(nickname: str):
    text_SQL = f"select nickname from users  where nickname = '{nickname}'"
    res = request_db('recipe_app',text_SQL)
    if res["response"] == []:
        date_of_creation = date.today()
        id_user = int(datetime.now().timestamp())
        text_SQL = f'''
            INSERT INTO users (id, nickname, status, date_of_creation)
            VALUES ({id_user}, '{nickname}', {True}, '{date_of_creation}')
            RETURNING *;
        '''
        res = request_db('recipe_app',text_SQL)
        return {"response":res["response"]}
    else: 
        return {"response": f'имя мользователя "{nickname}" уже занято'}

# Получениe профиля пользователя  
@app.get("/user/get/{nickname}")
def user_get(nickname: str):
    text_SQL = f"select * from users  where nickname = '{nickname}'"
    res = request_db('recipe_app',text_SQL)
    if res["response"] != []:
        row = res["response"][0]
        user = User(row[0],row[1],row[2],row[3],row[4],row[5])
        
        # получаем айди рецептов, что бы посчитать их
        text_SQL = f"select id from recipes  where author = '{user.id}'"
        res = request_db('recipe_app',text_SQL)
        if res["response"] != []:
            number_of_recipes = len(res["response"])
        else: number_of_recipes = 0

        return {"response": user.to_json(number_of_recipes)}
    else: 
        return {"response": f'имя мользователя "{nickname}" не найдено'}


#Класс для post запроса
class Recipe(BaseModel): 
    author: int
    name: str
    type_of_dish: str = None
    description: str = None
    preparation_steps: str = None
    photo: str = None
    hashtags: str = None
# Добавление пользователем рецепта
@app.post("/recipe/add/")
def recipe_add(item: Recipe):
    date_of_creation = date.today()
    id_recipe = int(datetime.now().timestamp())
    likes = 0
    status = True
    print(item.author)
    text_SQL = f'''
            INSERT INTO recipes (id, author, date_of_creation, name, type_of_dish, description, preparation_steps, photo, likes, hashtags, status)
            VALUES (
                {id_recipe}, 
                {item.author}, 
                '{date_of_creation}',
                '{item.name}', 
                '{item.type_of_dish}', 
                '{item.description}', 
                '{item.preparation_steps}', 
                '{item.photo}', 
                {likes}, 
                '{item.hashtags}', 
                {status})
            RETURNING *;
        '''
    res = request_db('recipe_app',text_SQL)
    return {"response":res["response"]}