from pymongo import MongoClient
from bson import ObjectId

#A function to get all the unique genre from the database
def get_unique_genre():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['moviedatabase']
    movie_collection = db['movies_database']
    unique_genre= []
    for document in movie_collection.find({}):
        genre_string = document["Genre"]
        genre_list = genre_string.split(",")
        for genre in genre_list:
            if genre not in unique_genre:
                unique_genre.append(genre)
    return unique_genre

#A method to convert strings from pandas dataframe to ObjectId
def str_to_bson_object_id(input_dict: dict):
    list_updated = []
    for strings in input_dict["_id"]:
        list_updated.append(ObjectId(strings))
    input_dict["_id"] = list_updated
    return input_dict

#A method to unique genre
def get_unique_genre_using_set():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['moviedatabase']
    movie_collection = db['movies_database']
    unique_genre= []
    for document in movie_collection.find({}):
        genre_string = document["Genre"]
        genre_list = genre_string.split(",")
        for genre in genre_list:
            unique_genre.append(genre)
    unique_genre = set(unique_genre)
    return unique_genre