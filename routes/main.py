import psycopg2
import psycopg2.extras
from fastapi import HTTPException
from fastapi.responses import JSONResponse

from .models import UserCreate, UserUpdate
from fastapi import APIRouter
from .database import create_tables, connection

create_tables()
router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}}
)
# OAuth2 scheme
conn = connection()
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

@router.post("/users/")
async def create_user(user: UserCreate):
    cur.execute("INSERT INTO users (email, password) VALUES (%s, %s) RETURNING *", (user.email, user.password))
    conn.commit()
    return JSONResponse(status_code=200, content={"message": "User created successfully"})

@router.post("/login")
async def login_user(user: UserCreate):
    cur.execute("SELECT * FROM users WHERE email = %s AND password = %s", (user.email, user.password))
    user_data = cur.fetchone()
    if user_data:
        return JSONResponse(status_code=200, content={"message": "User Login successfully"})
    else:
        raise HTTPException(status_code=401, detail="Invalid email or password")

@router.get("/users/")
async def read_users():
    cur.execute("SELECT * FROM users")
    users_data = cur.fetchall()
    users = []
    for user_data in users_data:
        users.append({"id": user_data["id"], "email": user_data["email"]})
    return JSONResponse(status_code=200, content={"users": users})

@router.get("/users/{user_id}")
async def read_user(user_id: int):
    cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user_data = cur.fetchone()
    if user_data:
        return JSONResponse(status_code=200, content={"id": user_data["id"], "email": user_data["email"]})
    else:
        raise HTTPException(status_code=404, detail="User not found")

@router.put("/users/{user_id}")
async def update_user(user_id: int, user: UserUpdate):
    cur.execute("UPDATE users SET email = %s, password = %s WHERE id = %s RETURNING *", (user.email, user.password, user_id))
    conn.commit()
    return JSONResponse(status_code=200, content={"message": "User updated successfully"})

@router.delete("/users/{user_id}")
async def delete_user(user_id: int):
    cur.execute("DELETE FROM users WHERE id = %s", (user_id,))
    conn.commit()
    return JSONResponse(status_code=200, content={"message": "User deleted successfully"})
