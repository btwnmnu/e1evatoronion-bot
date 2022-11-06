from pymongo import MongoClient
from settings import MONGODB, MONGODB_LINK

mdb = MongoClient(MONGODB_LINK)[MONGODB]

def search_or_save_user(mdb, userID, fileID):
    # поиск в коллекции users по user.id
    user = mdb.users.find_one({'user_id': userID})
    # если его нет, то создаем словарь
    if not user:
        user = {
            'user_id': userID,
            'file_id': fileID,
            'date': None,
            'city': None
        }
        mdb.users.insert_one(user)
    else:
        user = {
            'file_id': fileID,
            'date': None
        }
    return user

def search_user(mdb, userID):
    user = mdb.users.find_one({'user_id': userID})
    return user

def add_date(mdb, userID, date):
    mdb.users.update_one({'user_id': userID}, {'$set': {'date': date}})

def add_city(mdb, userID, city):
    mdb.users.update_one({'user_id': userID}, {'$set': {'city': city}})