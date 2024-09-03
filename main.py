from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional, List

app = FastAPI()

# Simulamos una base de datos en memoria.
db = []

class User(BaseModel):
    user_name: str
    user_id: int
    user_email: EmailStr
    age: Optional[int] = None
    recommendations: List[str]
    ZIP: Optional[str] = None

@app.post("/create_user/")
def create_user(user: User):
    # Chequear si el email ya existe en la base de datos
    for u in db:
        if u['user_email'] == user.user_email:
            raise HTTPException(status_code=400, detail="Email ya registrado.")
    db.append(user.dict())
    return {"message": "Usuario creado exitosamente."}

@app.put("/update_user/{user_id}")
def update_user(user_id: int, user: User):
    for index, u in enumerate(db):
        if u['user_id'] == user_id:
            db[index] = user.dict()
            return {"message": "Usuario actualizado exitosamente."}
    raise HTTPException(status_code=404, detail="Usuario no encontrado.")

@app.get("/get_user/{user_id}")
def get_user(user_id: int):
    for u in db:
        if u['user_id'] == user_id:
            return u
    raise HTTPException(status_code=404, detail="Usuario no encontrado.")

@app.delete("/delete_user/{user_id}")
def delete_user(user_id: int):
    for index, u in enumerate(db):
        if u['user_id'] == user_id:
            del db[index]
            return {"message": "Usuario eliminado exitosamente."}
    raise HTTPException(status_code=404, detail="Usuario no encontrado.")