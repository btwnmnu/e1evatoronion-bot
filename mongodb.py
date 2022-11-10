from pymongo import MongoClient
from settings import MONGODB, MONGODB_LINK

mdb = MongoClient(MONGODB_LINK)[MONGODB]

def search_or_save_user(mdb, userID, fileID):
    # Search in 'users' collection by user.id
    user = mdb.users.find_one({'user_id': userID})
    # Create user if DB does not have him
    if not user:
        user = {
            'user_id': userID,
            'file_id': fileID,
            'date': None,
            'city': None
        }
        mdb.users.insert_one(user)
    else:
        mdb.users.update_one({'user_id': userID}, {'$set': {'file_id': fileID}})
    
    return user

def search_user(mdb, userID):
    user = mdb.users.find_one({'user_id': userID})
    return user

def add_date(mdb, userID, date):
    mdb.users.update_one({'user_id': userID}, {'$set': {'date': date}})

def add_city(mdb, userID, city):
    mdb.users.update_one({'user_id': userID}, {'$set': {'city': city}})

def add_feedback(mdb, feedback):
    mdb.feedback.insert_one({'feedback': feedback})