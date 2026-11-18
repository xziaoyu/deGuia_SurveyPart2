from contextlib import asynccontextmanager
import hashlib
import secrets

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session
from starlette.middleware.sessions import SessionMiddleware

from database import create_db_and_tables, engine
from models import LoginForm, RegisterForm, User


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)
app.add_middleware(SessionMiddleware, secret_key=secrets.token_hex(32))


@app.exception_handler(RequestValidationError)
async def invalid_form(request, error):
    return JSONResponse(
        status_code=422,
        content={"detail": "Check the form fields."},
    )


def hash_username(username):
    username = username.strip()
    if not username:
        raise HTTPException(422, "Enter a username.")
    return hashlib.sha256(username.encode()).hexdigest()


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


@app.get("/")
def show_login():
    return FileResponse("login.html")


@app.get("/register")
def show_register():
    return FileResponse("register.html")


@app.get("/main")
def show_main(request: Request):
    if not request.session.get("logged_in"):
        return RedirectResponse("/", status_code=303)
    return FileResponse("mainpage.html")


@app.get("/styles.css", include_in_schema=False)
def show_styles():
    return FileResponse("styles.css", media_type="text/css")


@app.post("/register", status_code=201)
def register(form: RegisterForm):
    if form.password != form.confirm_password:
        raise HTTPException(422, "Passwords do not match.")

    user = User(
        username_hash=hash_username(form.username),
        password_hash=hash_password(form.password),
    )

    with Session(engine) as session:
        session.add(user)
        try:
            session.commit()
        except IntegrityError:
            session.rollback()
            raise HTTPException(409, "Username is already registered.")

    return {"message": "Account created."}


@app.post("/login")
def login(form: LoginForm, request: Request):
    with Session(engine) as session:
        user = session.get(User, hash_username(form.username))
        if user is None or hash_password(form.password) != user.password_hash:
            raise HTTPException(401, "Invalid username or password.")

    request.session["logged_in"] = True
    return {"message": "Logged in."}