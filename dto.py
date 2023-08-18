# import pymongo
# from bson import ObjectId
from pymongo import MongoClient

class DataBase:
    def __init__(self):
        cluster = MongoClient('mongodb://localhost:27017/')
        self.db = cluster['QuizBto']

        self.users = self.db['Users']
        self.questions = self.db['Question']
        self.question_counts = len( list(self.questions.find({})) )

    def add_question(self, question):
        return self.questions.insert_one(question)

    def add_all_question(self, questions):
        return self.questions.insert_many(questions)

    def get_question(self, index: str):
        return self.questions.find_one({'id': index})

    def get_user(self, chat_id):
        user = self.users.find_one({'chat_id': chat_id})

        if user is None:
            user = {
                'chat_id': chat_id,
                'question_index': -1,
                'is_passing': False,
                'is_passed': False,
                'answers': []
            }
            self.users.insert_one(user)
        return user

    def set_user(self, chat_id, update):
        return self.users.update_one({"chat_id": chat_id}, {"$set": update})

class TextAndKeyboard:
    def __init__(self, text, keyboard):
        self.text = text
        self.keyboard = keyboard


# db = DataBase()
#
# new_user = {'uid': 154356,
#             'passing': False,
#             'passed': False
#             }
#
# questions = [
#     {
#         "id": 0,
#         "title": '1 + 1 = ?',
#         "answers": ["2", "3"],
#         "is_right": 0
#     },
#     {
#         "id": 1,
#         "title": '2 + 1 = ?',
#         "answers": ["3", "4"],
#         "is_right": 0
#     }
# ]
#
# print( db.add_all_question(questions) )