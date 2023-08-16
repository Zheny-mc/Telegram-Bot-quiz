import pymongo
from pymongo import MongoClient


cluster = MongoClient('mongodb://localhost:27017/')
db = cluster['Quiz']

collections = db['Question']


# вставка одного документа
# post = {
#     'name': 'Tim',
#     'age': 25
# }
#
# collections.insert_one(post)

# вставка массива документа
# posts = [{'name': 'Tim', 'age': 25}, {'name': 'Evg', 'age': 28}]
# collections.insert_many(posts)

# Прочитаем все данные
# result = collections.find({'name': 'Tim'})
# for i in result:
#     print(i)

# прочитаем одну запись
# result = collections.find_one({'name': 'Tim'})
# print(result)

# обновить одну запись
# collections.update_one({'name': 'Tim', 'age': 23}, {'$set': {'name': 'Jordon'}})

# обновить все записи
# collections.update_many({'name': 'Tim'}, {'$set': {'name': 'Alex'}})

# Удалить запись из документа
# collections.delete_one({'name': 'Jordon'})

# Удалить все записи из документа
# collections.delete_many({'name': 'Alex'})

