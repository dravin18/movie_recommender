from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
import module.modules   
import module.schemas
import bson.objectid
from bson import ObjectId
import pandas as pd
import oauth2

app = FastAPI()

@app.put("/update_rating",response_model = module.schemas.ReturnUpdatedRating)
def update_movie_rating_api(pydantic_model: module.schemas.UpdateRating,
                            get_current_user :int = Depends(oauth2.get_current_user)):
    info = pydantic_model.model_dump()
    info["user_id"] = ObjectId(info["user_id"])
    info["movie_id"] = ObjectId(info["movie_id"])
    if module.modules.Movie.update_rating(user_id=info["user_id"],
                                                 movie_id=info["movie_id"],rating=info["rating"]):
        return {"rating":"movie_rating_database_updated_successfully"} 
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail = f"There is an error in the code")

@app.put("/watch_movie",response_model = module.schemas.ReturnWatchMovie)
def watch_movie_api(pydantic_model: module.schemas.UpdateWatchMovie,
                    get_current_user :int = Depends(oauth2.get_current_user)):
    pydantic_info = pydantic_model.model_dump()
    pydantic_info["movie_id"] = ObjectId(pydantic_info["movie_id"])
    pydantic_info["user_id"] = ObjectId(pydantic_info["user_id"])
    output = module.modules.User.watch_movie(pydantic_info["movie_id"],pydantic_info["user_id"])
    if output:
        return {"watched": 1}
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail = f"There is an error in the code")
    
@app.post("/get_recommendations",response_model= module.schemas.ReturnGetRecommendations)
def get_recommendations_api(pydantic_model: module.schemas.PostGetRecommendations,
                            get_current_user :dict = Depends(oauth2.get_current_user)):
    pydantic_dict = pydantic_model.model_dump()
    frame = module.modules.User.get_recommendations(pydantic_dict["username"])
    print(frame)
    recommended_movies = module.modules.pandas_bson_object_to_dict_str(frame)
    if recommended_movies:
        return {"recommendations":recommended_movies}
    elif len(recommended_movies) == 0:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail = f"There is an error in the code")
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail = f"There is an error in the code")
        
@app.get("/get_top_rated_movies", response_model=module.schemas.ReturnGetTopRatedMovies)
def get_top_rated_movies_api(get_current_user :int = Depends(oauth2.get_current_user)):
    pandas_top_movies = module.modules.MovieManager.get_top_rated_movies()
    top_movies  = module.modules.pandas_bson_object_to_dict_str(pandas_top_movies)

    if top_movies:
        return {"top_rated_movies": top_movies}
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail = f"There is an error in the code")

@app.post("/search_movies",response_model=module.schemas.ReturnSearchMovie)
def search_movie_api(pydantic_model: module.schemas.PostSearchMovie,
                     get_current_user :int = Depends(oauth2.get_current_user)):
    pydantic_dict = pydantic_model.model_dump()
    print(pydantic_dict)
    results = module.modules.MovieManager.search_movie(pydantic_model.short_title)
    if isinstance(results,pd.DataFrame):
        search_results = module.modules.pandas_bson_object_to_dict_str(results)
        return {"searched_movies":search_results}
    elif isinstance(results, str):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail = f"No search results were obtained")
    else:
        return {"searched_movies":results}
    
@app.put("/add_movie",response_model=module.schemas.ReturnAddMovie)
def add_movie_api(pydantic_model: module.schemas.UpdateAddMovie,
                  get_current_user :int = Depends(oauth2.get_current_user)):
    pydantic_dict = pydantic_model.model_dump()
    if module.modules.MovieManager.add_movie(pydantic_dict) == True:
        return {"movie_addition_status":"success"}
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail = f"movie_was_not_added_successfully")

@app.put("/add_user",response_model=module.schemas.ReturnAddUser)
def add_user_api(pydantic_model: module.schemas.UpdateAddUser):
    pydantic_dict = pydantic_model.model_dump()
    pydantic_dict["password"] = module.modules.get_password_hash(pydantic_dict["password"])
    output = module.modules.User.add_user(pydantic_dict)
    if isinstance(output,bson.objectid.ObjectId):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail = f"username already exists")
    if output == True:
        return {"username":f"{pydantic_dict["username"]} has been added successfully"}
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail = f"username has not been added successfully")
    
@app.get("/get_user_info/{username}",response_model=module.schemas.ReturnGetUser)
def get_user_api(username: str,get_current_user :int = Depends(oauth2.get_current_user)):
    checked_user_name = module.modules.check_username(username)
    if checked_user_name is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"username {username} is not found")
    else:
        return checked_user_name

@app.post("/user_login")
def user_login_api(user_credentials_inbuild_model: OAuth2PasswordRequestForm = Depends()):
    hashed_password = module.modules.find_password(user_credentials_inbuild_model.username)
    if not hashed_password:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid credentials")
    if not module.modules.verify_password(user_credentials_inbuild_model.password,hashed_password["password"]):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid credentials")
    access_token = oauth2.create_access_token({"username":user_credentials_inbuild_model.username})
    return {"access_token":access_token,"token_type":"bearer"}