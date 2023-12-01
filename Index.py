from reactpy.backend.fastapi import configure
from reactpy import component, html
from fastapi.staticfiles import StaticFiles
from reactpy.core.hooks import create_context
from reactpy_router import route, simple

from fastapi import FastAPI

# Content

from components.consultas import Consultas
from components.gestion import ShippingManagement
from components.login import LoginPage

from components.principal import Dashboard
from components.userInterface import UserInterface
from components.usersCRUD import UserCreationForm

app = FastAPI()


@component
def Index():
    

    return simple.router(
        route("/", LoginPage()),
        route("/principal", Dashboard()),
        route("/consultas", Consultas()),
        route("/gestion", ShippingManagement()),
        route("/users", UserCreationForm()),
        route("/clientes", UserInterface())
        
        
    )
    
    
configure(app, Index)