from pydantic import BaseModel, Field
from typing_extensions import Annotated
from pydantic.functional_validators import BeforeValidator
from typing import Optional
from bson.objectid import ObjectId

#PyObjectId = Annotated[str, BeforeValidator(str)]

class UpdateRating(BaseModel):
    movie_id: str
    user_id: str
    rating: float

class UpdateWatchMovie(BaseModel):
    movie_id: str
    user_id: str

class ReturnUpdatedRating(BaseModel):
    rating: str

class ReturnWatchMovie(BaseModel):
    watched: bool

class PostGetRecommendations(BaseModel):
    username: str

class ReturnGetRecommendations(BaseModel):
    recommendations: dict

class ReturnGetTopRatedMovies(BaseModel):
    top_rated_movies: dict

class PostSearchMovie(BaseModel):
    short_title: str

class ReturnSearchMovie(BaseModel):
    searched_movies: dict

class PostAddMovie(BaseModel):
    movie_title: str

class ReturnAddMovie(BaseModel):
    movie_addition_status : str

class UpdateAddMovie(BaseModel):
    Title:str
    Genre:str 
    Actors:str
    Year:int
    Rating:float

class UpdateAddUser(BaseModel):
    username: str
    password: str
    watched_movies: Optional[list] = []
    preferred_genres: str

class ReturnAddUser(BaseModel):
    username: str

class ReturnGetUser(BaseModel):
    username: str
    preferred_genres: str

class PostUserLogin(BaseModel):
    username: str
    password: str

class TokenData(BaseModel):
    username: Optional[str] = None