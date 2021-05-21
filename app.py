
from config import MongoConfig
from pydantic import BaseModel
import pymongo
from fastapi import FastAPI, Depends, HTTPException
from auth import AuthHandler
from schemas import SignInModel, SignUpModel


app = FastAPI()
auth_handler = AuthHandler()
users = []

@app.get("/")
def main():
    return {"isRunning": "Application is running successfully..."}

@app.get('/protected')
def protected(username=Depends(auth_handler.auth_wrapper)):
    return { 'name': username }

@app.post("/SignIn")
async def SignIn(auth_details: SignInModel):
    user = MongoConfig.Usersdb.find({});
    for data in user:
        if (data["_id"] != auth_details.email):
            return {"status" : 401, "message": "Email id is not register"}
        if not auth_handler.verify_password(auth_details.password, data['password']):
            return {"status" : 401, "message": "Invalid password"}
    token = auth_handler.encode_token(data['_id'])
    return {"status" : 200, "message": "Sign In successfully.","token": token}

@app.post("/SignUp")
def SignUp(auth_details: SignUpModel):
    try:
        hashed_password = auth_handler.get_password_hash(auth_details.password)
        MongoConfig.Usersdb.insert_one({"_id": auth_details.email, "name": auth_details.name , "password": hashed_password});
    except pymongo.errors.DuplicateKeyError:
        return {"status" : 409, "message": "Account already exists"}
    return {"status" : 200, "message": "Sign Up successfully."}