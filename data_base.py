# -*- coding: utf-8 -*-

import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# функция создания базы
def create_db(name_db):
	connection = psycopg2.connect(user="postgres",
									password="postgres",
									host="127.0.0.1",
									port="5432")
	connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
	# Курсор для выполнения операций с базой данных
	cursor = connection.cursor()
	# запрос на создание базы данных
	sql_create_database = f'create database {name_db}'
	cursor.execute(sql_create_database)
	print(f'successfully created db "{name_db}')
	cursor.close()
	connection.close()

# функция подключения к СУЩЕСТВУЮЩЕЙ базе данных
def connection_db(database):
	connection = psycopg2.connect(user="postgres",
									password="postgres",
									host="127.0.0.1",
									port="5432",
									database=database)
	return connection


# отправка запроса 
def request_db(database, text_SQL):
	try:
		connection = connection_db(database)
		cursor = connection.cursor()
		cursor.execute(text_SQL)
		connection.commit()
		cursor.close()
		connection.close()
		return 'successful request'
	except Exception as e:
		return e

if __name__ == "__main__":
	# создаем базу данных
	create_db('recipe_app')
	# создаем таблицы
	connection = connection_db('recipe_app')
	cursor = connection.cursor()
	# запрос на создание таблицы
	sql_create_table = '''CREATE TABLE users
						(id int PRIMARY KEY NOT NULL,
						nickname text NOT NULL,
						status bool NOT NULL,
						favorites int[],
						date_of_creation date NOT NULL,
						date_of_change date); '''
	cursor.execute(sql_create_table)
	connection.commit()
	print('successfully created table')
	sql_create_table = '''CREATE TABLE recipes
							(id int PRIMARY KEY NOT NULL,
							author int NOT NULL,
							date_of_creation date NOT NULL,
							date_of_change date,
							name text NOT NULL,
							type_of_dish text,
							description text,
							preparation_steps text,
							photo text,
							likes int,
							hashtags text,
							status bool NOT NULL); '''
	cursor.execute(sql_create_table)
	connection.commit()
	print('successfully created table')

	cursor.close()
	connection.close()