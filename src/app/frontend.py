import sys
sys.path.append("..")

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field, AnyUrl, IPvAnyAddress, ValidationError
# Necesarios para el frontend
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from typing import Optional

from app.users import current_active_user_frontend, fastapi_front_user
from app.db import User

import requests

# Necesarios para el frontend agrego los templates de Jinja2
templates = Jinja2Templates(directory="templates")

router = APIRouter(
    prefix="/info",
    tags=["Frontend"],
    responses={404: {"description": "Not Found"}}
)

class LoginForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.username: Optional[str] = None
        self.password: Optional[str] = None

    async def create_form(self):
        form = await self.request.form()
        self.username = form.get("username")
        self.password = form.get("password")

@router.get("/", response_class=HTMLResponse)
async def user_page(request: Request, user: User = Depends(current_active_user_frontend)):
    return {"message": f"Hola {user.email}!"}

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("users/login.html",{"request":request} )

@router.post("/login", response_class=HTMLResponse)
async def login(request: Request):
    
    form = LoginForm(request)
    await form.create_form()

    response = await requests.post(url="http://127.0.0.1:8000/auth/cookie/login", data={"username":form.username,"password":form.password})

    print(response)
    #return RedirectResponse(url="/user", status_code=status.HTTP_302_FOUND)

    
    # form = await request.form()
    # data = {"username":form.get("username"),"password":form.get("password")}
    # response = await requests.post(url="/auth/cookie", data=data)
    # if response is "null":
    #     return RedirectResponse(url="/authenticated-route", status_code=status.HTTP_302_FOUND)

    # try:
    #     form = LoginForm(request)
    #     await form.create_form()
    #     response = RedirectResponse(url="/inventario/home/", status_code=status.HTTP_302_FOUND)

    #     validate_user_cookie = await login_for_token(response=response, form_data=form, db=db)

    #     if not validate_user_cookie:
    #         msg = "Usuario o contraseña Incorrecto"
    #         return templates.TemplateResponse("users/login.html", {"request":request, "msg": msg })
        
    #     return response
    
    # except HTTPException:
    #     msg = "Error Desconocido"
    #     return templates.TemplateResponse("users/login.html", {"request":request, "msg": msg })