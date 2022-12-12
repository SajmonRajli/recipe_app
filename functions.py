from data_base import request_db
from pydantic import BaseModel

# Проверка статуса пользователя
def get_status_user(id):
    text_SQL = f"select * from users  where id = '{id}'"
    res = request_db('recipe_app',text_SQL)
    row = res["response"][0]
    user = User(row[0],row[1],row[2],row[3],row[4],row[5])
    return user.status

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

class Recipe:
    def __init__(self, id, author, date_of_creation, date_of_change, name, type_of_dish, description, preparation_steps, photo, likes, hashtags, status):
        self.id = id
        self.author = author
        self.date_of_creation = date_of_creation
        self.date_of_change = date_of_change
        self.name = name
        self.type_of_dish = type_of_dish
        self.description = description
        self.preparation_steps = preparation_steps
        self.photo = photo
        self.likes = likes
        self.hashtags = hashtags
        self.status = status
    def to_json(self):
        return {"id": self.id,
                "author": self.author,
                "date_of_creation": self.date_of_creation,
                "date_of_change": self.date_of_change,
                "name": self.name,
                "type_of_dish": self.type_of_dish,
                "description": self.description,
                "preparation_steps": self.preparation_steps,
                "photo": self.photo,
                "likes": self.likes,
                "hashtags": self.hashtags,
                "status": self.status}

#Класс для post запроса добавления рецепта
class Recipe_post(BaseModel): 
    author: int
    name: str
    type_of_dish: str = None
    description: str = None
    preparation_steps: str = None
    photo: str = None
    hashtags: str = None