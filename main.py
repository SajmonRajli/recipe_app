# -*- coding: utf-8 -*-
from typing import Union
from fastapi import FastAPI
from datetime import datetime, date, time
from data_base import request_db
from functions import User, Recipe, Recipe_post, get_status_user, check_admin, get_status_recipe
app = FastAPI()


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

# Авторизация 
@app.get("/user/login/{nickname}")
def user_login(nickname: str):
    text_SQL = f"select * from users  where nickname = '{nickname}'"
    res = request_db('recipe_app',text_SQL)
    if res["response"] != []:
        row = res["response"][0]
        user = User(row[0],row[1],row[2],row[3],row[4],row[5])
        return {"response": user.to_json_all()}
    else: 
        return {"response": f'имя мользователя "{nickname}" не найдено'}

# Получениe профиля пользователя  
@app.get("/user/get/nickname={nickname}&login={login}")
def user_get(nickname: str, login: int):
    text_SQL = f"select * from users  where nickname = '{nickname}'"
    res = request_db('recipe_app',text_SQL)
    if res["response"] != []:
        row = res["response"][0]
        user = User(row[0],row[1],row[2],row[3],row[4],row[5])
        status = get_status_user(login)
        if (status == True) or (status == False and login == user.id):
            # получаем айди рецептов, что бы посчитать их
            text_SQL = f"select id from recipes  where author = '{user.id}'"
            res = request_db('recipe_app',text_SQL)
            if res["response"] != []:
                number_of_recipes = len(res["response"])
            else: number_of_recipes = 0
            return {"response": user.to_json(number_of_recipes)}
        else:
            return {"response": 'Вы заблокированы и не можете смотреть других пользователей'}
    else: 
        return {"response": f'Имя мользователя "{nickname}" не найдено'}


# Добавление пользователем рецепта
@app.post("/recipe/add/")
def recipe_add(item: Recipe_post):
    date_of_creation = date.today()
    id_recipe = int(datetime.now().timestamp())
    likes = 0
    status = True
    if get_status_user(item.author) == True:
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
    else:
        return {"response": 'Пользователь заблокирован'}


# Получениe рецепта
@app.get("/recipe/get/{id}&login={login}")
def recipe_get(id: int, login: int):
    if get_status_user(login) == True:
        text_SQL = f"select * from recipes  where id = '{id}'"
        res = request_db('recipe_app',text_SQL)
        if res["response"] != []:
            row = res["response"][0]
            print(row[0])
            print(row[11])
            recipe = Recipe(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11])

            return {"response": recipe.to_json()}
        else: 
            return {"response": 'Рецепт не найден'}
    else: 
        return {"response": 'Вы заблокированы и не можете просматривать рецепты'}


# Админский API
# Авторизация
@app.get("/admin/login/{token}")
def admin_login(token: str):
    if check_admin(token):
        return {"response": 'Успешная авторизация'}
    else:
        return {"response": 'Неверный токен'}

# Блокировка/разблокировка пользователя
@app.get("/admin/user_ban/{token}&id_user={id_user}")
def user_ban(token: str, id_user: int):
    if check_admin(token):

        if get_status_user(id_user) == True:
            text_SQL = f"UPDATE users SET status = false WHERE id={id_user}"
            res = request_db('recipe_app',text_SQL)
            return {"response": 'Пользователь заблокирован'}
        elif get_status_user(id_user) == False:
            text_SQL = f"UPDATE users SET status = true WHERE id={id_user}"
            res = request_db('recipe_app',text_SQL)
            return {"response": 'Пользователь разблокирован'}

    else:
        return {"response": 'Неверный токен'}

# Блокировка/разблокировка рецепта
@app.get("/admin/recipe_ban/{token}&id_recipe={id_recipe}")
def recipe_ban(token: str, id_recipe: int):
    if check_admin(token):

        if get_status_recipe(id_recipe) == True:
            text_SQL = f"UPDATE recipes SET status = false WHERE id={id_recipe}"
            res = request_db('recipe_app',text_SQL)
            return {"response": 'Рецепт заблокирован'}
        elif get_status_recipe(id_recipe) == False:
            text_SQL = f"UPDATE recipes SET status = true WHERE id={id_recipe}"
            res = request_db('recipe_app',text_SQL)
            return {"response": 'Рецепт разблокирован'}

    else:
        return {"response": 'Неверный токен'}