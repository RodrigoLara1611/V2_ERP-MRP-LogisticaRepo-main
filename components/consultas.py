#consultas.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from reactpy.backend.fastapi import configure
from reactpy import component, html
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db, SessionLocal
from models import Usuario, Vehiculo, Ruta, SolicitudEmbarque, Notificacion, Reporte
from components.panels import UsuariosComponent, VehiculosComponent, RutasComponent, SolicitudesComponent, NotificacionesComponent, ReportesComponent
from sqlalchemy.orm import joinedload

app = FastAPI()

# por buenas prácticas según se montan así los recursos en fastapi, yo digo que le hacen a la mamada nomás
app.mount("/img", StaticFiles(directory="img"), name="images")
app.mount("/css", StaticFiles(directory="css"), name="css")

# estilos y otras cosillas
bootstrap_css = html.link({
    "rel": "stylesheet",
    "href": "https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css"
})

font_awesome = html.link({
    "rel": "stylesheet",
    "href": "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.1/css/all.min.css"
})

google_fonts = html.link({
    "href": "https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap",
    "rel": "stylesheet"
})

custom_css = html.link({
    "rel": "stylesheet",
    "href": "/css/styles.css"
})

def obtener_usuarios():
    db = SessionLocal()  
    try:
        usuarios = db.query(Usuario).all()  
        return usuarios  
    finally:
        db.close()  

def obtener_vehiculos():
    db = SessionLocal()  
    try:
        vehiculos = db.query(Vehiculo).options(joinedload(Vehiculo.usuario)).all()
        return vehiculos  
    finally:
        db.close()  

def obtener_rutas():
    db = SessionLocal()  
    try:
        rutas = db.query(Ruta).options(joinedload(Ruta.vehiculo)).all()
        return rutas  
    finally:
        db.close()  

def obtener_solicitudes():
    db = SessionLocal()  
    try:
        solicitudes = db.query(SolicitudEmbarque).options(joinedload(SolicitudEmbarque.usuario)).all()
        return solicitudes 
    finally:
        db.close() 

def obtener_notificaciones():
    db = SessionLocal()
    try:
        notificaciones = db.query(Notificacion).options(joinedload(Notificacion.usuario)).all()
        return notificaciones
    finally:
        db.close()

def obtener_reportes():
    db = SessionLocal()
    try:
        reportes = db.query(Reporte).all()
        return reportes
    finally:
        db.close()

@component
def Consultas():
    usuarios = obtener_usuarios() 
    vehiculos=obtener_vehiculos()
    rutas=obtener_rutas()
    solicitudes = obtener_solicitudes()
    notificaciones=obtener_notificaciones()
    reportes=obtener_reportes()
    return html.div(
        {
            "className": "container mt-5"
        },
        bootstrap_css,
        font_awesome,
        google_fonts,
        custom_css,
        [
            html.ul(
                {
                    "className": "nav nav-tabs"
                },
                [
                    html.li(
                        {
                            "className": "nav-item"
                        },
                        html.a(
                            {
                                "className": "nav-link",
                                "href": "/principal" 
                            },
                            "Principal"
                        )
                    ),
                    html.li(
                        {
                            "className": "nav-item"
                        },
                        html.a(
                            {
                                "className": "nav-link",
                                "href": "/consultas" 
                            },
                            "Consultas"
                        )
                    ),
                    html.li(
                        {
                            "className": "nav-item"
                        },
                        html.a(
                            {
                                "className": "nav-link",
                                "href": "gestion"
                            },
                            "Gestionar Rutas"
                        )
                    ),
                    html.li(
                        {
                            "className": "nav-item"
                        },
                        html.a(
                            {
                                "className": "nav-link",
                                "href": "users"
                            },
                            "Administrar usuarios"
                        )
                    ),
                    html.li(
                        {
                            "className": "nav-item"
                        },
                        html.a(
                            {
                                "className": "nav-link",
                                "href": "clientes"
                            },
                            "Solicitud Manual"
                        )
                    ),
                    html.li(
                        {
                            "className": "nav-item"
                        },
                        html.a(
                            {
                                "className": "nav-link",
                                "href": "/"
                            },
                            "Cerrar Sesión"
                        )
                    ),
                ]
            ),
            html.br(),
            html.br(),
            
            html.ul(
                {
                    "className": "nav nav-tabs"
                },
                [
                    html.li(
                        {
                            "className": "nav-item"
                        },
                        html.a(
                            {
                                "className": "nav-link",
                                "href": "#usuarios",
                                "data-toggle": "tab",
                            },
                            "Usuarios"
                        )
                    ),
                    html.li(
                        {
                            "className": "nav-item"
                        },
                        html.a(
                            {
                                "className": "nav-link",
                                "href": "#vehiculos",
                                "data-toggle": "tab",
                            },
                            "Vehículos"
                        )
                    ),
                    html.li(
                        {
                            "className": "nav-item"
                        },
                        html.a(
                            {
                                "className": "nav-link",
                                "href": "#rutas",
                                "data-toggle": "tab",
                            },
                            "Rutas"
                        )
                    ),
                    html.li(
                        {
                            "className": "nav-item"
                        },
                        html.a(
                            {
                                "className": "nav-link",
                                "href": "#SolicitudesDeEmbarque",
                                "data-toggle": "tab",
                            },
                            "Solicitudes De Embarque"
                        )
                    ),
                    html.li(
                        {
                            "className": "nav-item"
                        },
                        html.a(
                            {
                                "className": "nav-link",
                                "href": "#Notificaciones",
                                "data-toggle": "tab",
                            },
                            "Notificaciones"
                        )
                    ),
                    html.li(
                        {
                            "className": "nav-item"
                        },
                        html.a(
                            {
                                "className": "nav-link",
                                "href": "#Reportes",
                                "data-toggle": "tab",
                            },
                            "Reportes"
                        )
                    ),
                ]
            ),
            html.div(
                {
                    "className": "tab-content mt-3"
                },
                [
                    html.div(
                        {
                            "className": "tab-pane",
                            "id": "usuarios"
                        },
                        [
                            html.h4("Tablero de Usuarios"),
                            UsuariosComponent(usuarios)
                        ]
                    ),
                    html.div(
                        {
                            "className": "tab-pane",
                            "id": "vehiculos"
                        },
                        [
                            html.h4("Tablero de Vehículos"),
                            VehiculosComponent(vehiculos)
                        ]
                            ),
                    html.div(
                        {
                            "className": "tab-pane",
                            "id": "rutas"
                        },
                        [
                            html.h4("Tablero de Rutas"),
                            RutasComponent(rutas)
                        ]
                    ),
                    html.div(
                        {
                            "className": "tab-pane",
                            "id": "SolicitudesDeEmbarque"
                        },
                        [
                            html.h4("Tablero de Solicitudes De Embarque"),
                            SolicitudesComponent(solicitudes)
                        ]
                    ),
                    html.div(
                        {
                            "className": "tab-pane",
                            "id": "Notificaciones"
                        },
                        [
                            html.h4("Tablero de Notificaciones"),
                            NotificacionesComponent(notificaciones)
                        ]
                    ),
                    html.div(
                        {
                            "className": "tab-pane",
                            "id": "Reportes"
                        },
                        [
                            html.h4("Tablero de Reportes"),
                            ReportesComponent(reportes)
                        ]
                    )      
                ]
            )
            ,
            html.script(
                {
                    "src": "https://code.jquery.com/jquery-3.5.1.slim.min.js"
                }
            ),
            html.script(
                {
                    "src": "https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"
                }
            ),
            #html.script("window.onload = function() { if(!window.location.hash) { window.location = window.location + '#loaded'; window.location.reload(); }}"),
        ]
    )

configure(app, Consultas)

# # app.mount("/static", StaticFiles(directory="static"), name="static")
# app.mount("/img", StaticFiles(directory="img"), name="3")
# app.mount("/css", StaticFiles(directory="css"), name="css")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)