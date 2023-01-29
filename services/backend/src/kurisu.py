from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, Request
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
import crud, models, schemas
from database import SessionLocal, engine
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates") 

models.Base.metadata.create_all(bind=engine)

app = FastAPI()




app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.get("/", response_class=HTMLResponse)
async def serve_home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})



@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.get("/users/{user_name}", response_model=schemas.User)
def read_user(user_name: str, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user_name)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user



@app.post("/users/{user_id}/messages/", response_model=schemas.Message)
def create_message_for_user(
    user_id: int, message: schemas.MessageCreate, db: Session = Depends(get_db)
):
    return crud.create_user_message(db=db, message=message, user_id=user_id)


@app.get("/messages/", response_model=list[schemas.Message])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_messages(db, skip=skip, limit=limit)
    return items
