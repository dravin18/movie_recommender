from .database import user_collection,movie_collection,rating_collection
import pandas as pd
from passlib.context import CryptContext
import bson
from bson import ObjectId

pwd_context = CryptContext(schemes=["bcrypt"],deprecated = "auto")

#Defining the hashing function
def get_password_hash(password):
    return pwd_context.hash(password)

#Defining password verification function
def verify_password(user_password,hash_password):
    return pwd_context.verify(user_password,hash_password)

#Defining important functions
def bson_object_to_str(output_dict: dict) -> dict:
    i = 0 
    for list_item in output_dict["_id"]:
        output_dict["_id"][i] = str(list_item)
     #   print(type(output_dict["_id"][i]))
        i += 1
    return output_dict

#A method to convert object_ids from pandas to str
def pandas_bson_object_to_dict_str(output_frame):
    print(output_frame)
    output_frame['_id'] = output_frame['_id'].astype(str)
    schema_compat_json = output_frame.to_dict("list")
    #print(type(schema_compat_json["_id"]))
    return schema_compat_json

#A method to convert strings from pandas dataframe to ObjectId
def str_to_bson_object_id(input_dict: dict):
    list_updated = []
    for strings in input_dict["_id"]:
        list_updated.append(ObjectId(strings))
    input_dict["_id"] = list_updated
    return input_dict

#A function for checking if username exists
def check_username(username):
    return user_collection.find_one({"username":username},{"_id":0,"username":1,"preferred_genres":1})

def find_password(username):
    return user_collection.find_one({"username":username},{"_id":0,"password":1})

#Defining the classes
class Movie:
    def __init__(self):
        print()
    
    @staticmethod
    def get_movie_info(object_id):
        table = movie_collection.find({"_id":{"$in":object_id}})
        print(repr(table))
        df = pd.DataFrame(list(table))
        return df
    
    @staticmethod
    def update_rating(user_id,movie_id,rating):
            rating_collection.update_one({"movie_id":movie_id},
                                         {'$push':{'Rating':{"user_id":user_id,"Rating":rating}}})
            rating_with_object_id = rating_collection.find_one({"movie_id":movie_id},{'Rating':1})
            return {"rating": "movie_rating_record_updated_successfully"}
    
class User:
    @staticmethod
    def add_user(pydantic_dictionary):
        unique_id_check = user_collection.find_one({"username":pydantic_dictionary["username"]},{"_id": 1})

        if unique_id_check is None:
            user_collection.insert_one(pydantic_dictionary)
            return True

        elif isinstance(unique_id_check["_id"],bson.objectid.ObjectId):
            return unique_id_check["_id"]

        else:
            return False

    @staticmethod
    def watch_movie(movie_id,user_id):
        cursor_object = user_collection.find({"_id": user_id},{"watched_movies":1})
        for dict_type in cursor_object:
            user_movie_list = dict_type["watched_movies"]
        user_movie_list.append(movie_id) #Extracting only the list of user_ids since it is a dictionary also containing object_ids
        try:
            user_collection.update_one({"_id": user_id},{"$set":{"watched_movies": user_movie_list}})
            return True
        except:
            return False

    @staticmethod
    def get_recommendations(username):
        preferred_genre = user_collection.find_one({"username":username},{"preferred_genres":1})
        genre = preferred_genre["preferred_genres"].split(",")

        sorted_collection = movie_collection.find().sort({"Rating":-1})

        iter = 5
        df = pd.DataFrame()
        for document in sorted_collection:
            movie_genre = document["Genre"].split(",")
            for individual_genre in genre:
                if movie_genre[0] == individual_genre and iter > 0:
                    df2 = pd.DataFrame([document])
                    df = pd.concat([df,df2],ignore_index = True)
                    iter -= 1
                    break 
                else:
                    continue
        return df

class MovieManager:

    @staticmethod
    def add_movie(input_dictionary):
        if movie_collection.insert_one(input_dictionary):
            return True
        else:
            return False

    @staticmethod
    def search_movie(title: str):
        title = title.lower()
        df = pd.DataFrame()
        iter = 5
        for document in movie_collection.find({}):
            check_title = document["Title"].lower()
            if title in check_title and iter > 0:
                df2 = pd.DataFrame([document])
                df = pd.concat([df,df2],ignore_index=True)
                iter -= 1
            elif iter <= 0:
                return df
        if len(df) == 0:
            return "no match found"
        else:
            return df

    @staticmethod
    def get_top_rated_movies():
        sorted_collection = movie_collection.find().sort({"Rating":-1}).limit(10)
        df = pd.DataFrame(list(sorted_collection))
        return df