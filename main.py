from fastapi import FastAPI
import users
app = FastAPI(title="Coffee Orders API")
app.include_router(users.router)
@app.get("/")
def home():
    return {"message": "Coffee Orders Api"}