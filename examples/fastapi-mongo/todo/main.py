import os
from bson import ObjectId
from typing import List

import motor.motor_asyncio
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

load_dotenv()

mongodb_url = os.getenv("MONGODB_URL")
if mongodb_url is None:
    raise ValueError("'MONGODB_URL' env variable is required.")
client = motor.motor_asyncio.AsyncIOMotorClient(mongodb_url)
todo_collection = client.test.todos

app = FastAPI()


class TodoItem(BaseModel):
    name: str
    done: bool


class TodoItemInDB(TodoItem):
    id: str


@app.post("/todos", response_model=TodoItemInDB)
async def create_todo(item: TodoItem):
    todo = item.model_dump()
    result = await todo_collection.insert_one(todo)
    return {**todo, "id": str(result.inserted_id)}


@app.get("/todos", response_model=List[TodoItemInDB])
async def list_todos():
    todos = await todo_collection.find().to_list(length=100)
    return [{"id": str(todo["_id"]), **todo} for todo in todos]


@app.get("/todos/{todo_id}", response_model=TodoItemInDB)
async def read_todo(todo_id: str):
    todo = await todo_collection.find_one({"_id": ObjectId(todo_id)})
    if todo is None:
        raise HTTPException(status_code=404, detail=f"Todo {todo_id} not found")
    return {"id": str(todo["_id"]), **todo}


@app.put("/todos/{todo_id}", response_model=TodoItemInDB)
async def update_todo(todo_id: str, item: TodoItem):
    todo = await todo_collection.find_one({"_id": ObjectId(todo_id)})
    if todo is None:
        raise HTTPException(status_code=404, detail=f"Todo {todo_id} not found")
    updated_todo = await todo_collection.find_one_and_update(
        {"_id": ObjectId(todo_id)}, {"$set": item.model_dump()}, return_document=True
    )
    return {"id": str(updated_todo["_id"]), **updated_todo}


@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: str):
    delete_result = await todo_collection.delete_one({"_id": ObjectId(todo_id)})
    if delete_result.deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"Todo {todo_id} not found")
    return {"message": f"Deleted todo {todo_id}"}
