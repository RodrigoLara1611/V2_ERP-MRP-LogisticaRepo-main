# panels.py
from fastapi import FastAPI, Depends, Request
from reactpy import component, html
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from database import get_db, SessionLocal
from models import Usuario
from models import Vehiculo, Ruta, SolicitudEmbarque, Notificacion
from fastapi.staticfiles import StaticFiles
from reactpy import component, html
from reactpy.backend.fastapi import configure
from sqlalchemy.orm import joinedload
import requests

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.mount("/img", StaticFiles(directory="img"), name="images")
app.mount("/css", StaticFiles(directory="css"), name="css")

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

# custom_css = html.link({
#     "rel": "stylesheet",
#     "href": "css/styles.css"
# })

custom_css = html.link({
    "rel": "stylesheet",
    "href": "/D:/1 Universidad/9no Semestre/4 TÓPICOS/2 Unidad/3 Otros/Proyecto/Desarrollo/ERP-MRP-Logistica/css/styles.css"
})

# @app.get("/panel/usuarios")
# def panel_usuarios():
#     return PanelUsuariosComponent()

@app.get("/panel/usuarios")
def panel_usuarios(request: Request, db: Session = Depends(get_db)):
    usuarios = db.query(Usuario).all()
    rendered_table = UsuariosComponent(usuarios=usuarios)
    return HTMLResponse(content=rendered_table)

@app.get("/panel/vehiculos")
def panel_vehiculos(request: Request, db: Session = Depends(get_db)):
    vehiculos = db.query(Vehiculo).all()
    rendered_table = VehiculosComponent(vehiculos=vehiculos)
    return HTMLResponse(content=rendered_table)

@app.get("/panel/rutas")
def panel_rutas(request: Request, db: Session = Depends(get_db)):
    rutas = db.query(Ruta).options(joinedload(Ruta.vehiculo)).all()  
    rendered_table = RutasComponent(rutas=rutas)  
    return HTMLResponse(content=rendered_table)  

@app.get("/panel/solicitudes")
def panel_solicitudes(request: Request, db: Session = Depends(get_db)):
    solicitudes = db.query(SolicitudEmbarque).options(joinedload(SolicitudEmbarque.usuario)).all()
    rendered_table = SolicitudesComponent(solicitudes=solicitudes)
    return HTMLResponse(content=rendered_table)

@app.get("/panel/notificaciones")
def panel_notificaciones(request: Request, db: Session = Depends(get_db)):
    notificaciones = db.query(Notificacion).options(joinedload(Notificacion.usuario)).all()
    rendered_table = NotificacionesComponent(notificaciones=notificaciones)
    return HTMLResponse(content=rendered_table)

@component
def PanelVehiculosComponent():
    db = SessionLocal()  
    try:
        # vehiculos = db.query(Vehiculo).all()  
        vehiculos = db.query(Vehiculo).options(joinedload(Vehiculo.usuario)).all()
        return VehiculosComponent(vehiculos=vehiculos)  
    finally:
        db.close()  

@component
def PanelUsuariosComponent():
    db = SessionLocal()  
    try:
        usuarios = db.query(Usuario).all() 
        return UsuariosComponent(usuarios=usuarios)  
    finally:
        db.close()

@component
def PanelRutasComponent():
    db = SessionLocal()  
    try:
        rutas = db.query(Ruta).options(joinedload(Ruta.vehiculo)).all()
        return RutasComponent(rutas=rutas)  
    finally:
        db.close() 

@component
def PanelSolicitudesComponent():
    db = SessionLocal() 
    try:
        # solicitudes = db.query(SolicitudEmbarque).all()  
        solicitudes = db.query(SolicitudEmbarque).options(joinedload(SolicitudEmbarque.usuario)).all()
        return SolicitudesComponent(solicitudes=solicitudes) 
    finally:
        db.close()  

@component
def PanelNotificacionesComponent():
    db = SessionLocal()  
    try:
        notificaciones = db.query(Notificacion).options(joinedload(Notificacion.usuario)).all()
        return NotificacionesComponent(notificaciones=notificaciones)  
    finally:
        db.close()

@component
def UsuariosComponent(usuarios):
    rows = [
        html.tr([
            html.td(usuario.id),
            html.td(usuario.nombre),
            html.td(usuario.correo),
            html.td("********"), 
            html.td(usuario.fecha_registro.strftime('%Y-%m-%d %H:%M:%S')),
            html.td(
                html.img({
                    "src": usuario.perfil_img, 
                    "alt": "Imagen de perfil", 
                    "className": "img-thumbnail", 
                    "style": {
                        "width": "70px", 
                        "height": "70px"  
                    }
                })
            ) 
        ]) for usuario in usuarios
    ]
    return html.div(
        {
            "className": "container mt-5"
        },
        bootstrap_css,
        font_awesome,
        google_fonts,
        custom_css,            
        html.table(
                {
                "className": "table table-striped"
                },
                [
                    html.thead(
                        html.tr([
                            html.th("ID"),
                            html.th("Nombre"),
                            html.th("Correo"),
                            html.th("Contraseña"),
                            html.th("Fecha de Registro"),
                            html.th("Imagen de Perfil")
                        ])
                    ),
                    html.tbody(rows)
                ]
            )
    )

@component
def VehiculosComponent(vehiculos):
    rows = [
        html.tr([
            html.td(vehiculo.id),
            html.td(vehiculo.usuario.nombre),
            html.td(vehiculo.tipo),
            html.td(vehiculo.modelo),
            html.td(vehiculo.capacidad),
            html.td(
                html.img({
                    "src": vehiculo.imagen, 
                    "alt": "Imagen del vehículo", 
                    "className": "img-thumbnail", 
                    "style": {
                        "width": "100px",
                        "height": "100px" 
                    }
                })
            )        ]) for vehiculo in vehiculos
    ]
    return html.div(
        {
            "className": "container mt-5"
        },
        bootstrap_css,
        font_awesome,
        google_fonts,
        custom_css,            
        html.table(
                {
                    "className": "table table-striped"
                },
                [
                    html.thead(
                        html.tr([
                            html.th("ID"),
                            html.th("Usuario"),
                            html.th("Tipo"),
                            html.th("Modelo"),
                            html.th("Capacidad"),
                            html.th("Imagen")
                        ])
                    ),
                    html.tbody(rows)
                ]
            )
    )

@component
def RutasComponent(rutas):
    rows = [
        html.tr([
            html.td(ruta.id),
            html.td(ruta.origen),
            html.td(ruta.destino),
            html.td(ruta.duracion_estimada), 
            html.td(ruta.vehiculo_id),
            html.td(ruta.vehiculo.modelo) if ruta.vehiculo else html.td(None) 
        ]) for ruta in rutas
    ]
    return html.div(
        {
            "className": "container mt-5"
        },
        bootstrap_css,
        font_awesome,
        google_fonts,
        custom_css,
        html.table(
            {
                "className": "table table-striped"
            },
            [
                html.thead(
                    html.tr([
                        html.th("ID"),
                        html.th("Origen"),
                        html.th("Destino"),
                        html.th("Duración Estimada"), 
                        html.th("ID de Vehículo"),
                        html.th("Modelo de Vehículo")
                    ])
                ),
                html.tbody(rows)
            ]
        )
    )

@component
def SolicitudesComponent(solicitudes):
    rows = [
        html.tr([
            html.td(solicitud.id),
            html.td(solicitud.usuario.nombre),
            html.td(solicitud.origen),
            html.td(solicitud.destino),
            html.td(solicitud.fecha_solicitud.strftime('%Y-%m-%d %H:%M:%S')),  
            html.td(solicitud.fecha_recoleccion_estimada.strftime('%Y-%m-%d %H:%M:%S') if solicitud.fecha_recoleccion_estimada else None),
            html.td(solicitud.fecha_entrega_estimada.strftime('%Y-%m-%d %H:%M:%S') if solicitud.fecha_entrega_estimada else None),
            html.td(solicitud.estado),
            html.td(solicitud.peso)
        ]) for solicitud in solicitudes
    ]
    return html.div(
        {
            "className": "container mt-5"
        },
        bootstrap_css,
        font_awesome,
        google_fonts,
        custom_css,
        html.table(
            {
                "className": "table table-striped"
            },
            [
                html.thead(
                    html.tr([
                        html.th("ID"),
                        html.th("Usuario"),
                        html.th("Origen"),
                        html.th("Destino"),
                        html.th("Fecha de Solicitud"),
                        html.th("Fecha de Recolección Estimada"),
                        html.th("Fecha de Entrega Estimada"),
                        html.th("Estado"),
                        html.th("Peso")
                    ])
                ),
                html.tbody(rows)
            ]
        )
    )

@component
def NotificacionesComponent(notificaciones):
    rows = [
        html.tr([
            html.td(notificacion.id),
            html.td(notificacion.usuario.nombre),  
            html.td(notificacion.mensaje),
            html.td(notificacion.fecha_notificacion.strftime('%Y-%m-%d %H:%M:%S')),  
            html.td("Sí" if notificacion.leido else "No"),
        ]) for notificacion in notificaciones
    ]
    return html.div(
        {
            "className": "container mt-5"
        },
        bootstrap_css,
        font_awesome,
        google_fonts,
        custom_css,
        html.table(
            {
                "className": "table table-striped"
            },
            [
                html.thead(
                    html.tr([
                        html.th("ID"),
                        html.th("Usuario"),
                        html.th("Mensaje"),
                        html.th("Fecha de Notificación"),
                        html.th("Leído")
                    ])
                ),
                html.tbody(rows)
            ]
        )
    )

@component    
def ReportesComponent(reportes):
    rows = [
        html.tr([
            html.td(reporte.id),
            html.td(reporte.titulo),  
            html.td(reporte.contenido),
            html.td(reporte.fecha_reporte.strftime('%Y-%m-%d %H:%M:%S')),  
            html.td(reporte.tipo),
        ]) for reporte in reportes
    ]
    return html.div(
        {
            "className": "container mt-5"
        },
        bootstrap_css,
        font_awesome,
        google_fonts,
        custom_css,
        html.table(
            {
                "className": "table table-striped"
            },
            [
                html.thead(
                    html.tr([
                        html.th("ID"),
                        html.th("Titulo"),
                        html.th("Contenido"),
                        html.th("Fecha de Reporte"),
                        html.th("Tipo")
                    ])
                ),
                html.tbody(rows)
            ]
        )
    )

configure(app, PanelSolicitudesComponent)
configure(app, PanelRutasComponent)
configure(app, PanelVehiculosComponent)
configure(app, PanelUsuariosComponent)

# from fastapi import FastAPI, Depends, Request, HTMLResponse
# from sqlalchemy.orm import Session
# from database import get_db
# from models import Usuario

# app = FastAPI()

# @app.get("/", response_class=HTMLResponse)
# async def read_root():
#     html_content = """
#     <!DOCTYPE html>
#     <html>
#     <head>
#         <title>Panel de Usuarios</title>
#         <script src="/static/reactpy.js"></script>  
#     </head>
#     <body>
#         <div id="react-root"></div>
#         <script type="text/javascript">
#             async function fetchUsuarios() {
#                 const response = await fetch('/usuarios');
#                 const usuarios = await response.json();
#                 // Renderizar los datos usando ReactPy
#                 ReactPy.render(UsuarioTable, document.getElementById('react-root'), { usuarios: usuarios });
#             }

#             fetchUsuarios();
#         </script>
#     </body>
#     </html>
#     """
#     return HTMLResponse(content=html_content)

# @app.get("/usuarios")
# def get_usuarios(db: Session = Depends(get_db)):
#     usuarios = db.query(Usuario).all()
#     return usuarios



################################################################################################
################################################################################################
################################################################################################

# from fastapi import FastAPI, Depends
# from fastapi.templating import Jinja2Templates
# from sqlalchemy.orm import Session
# from database import get_db
# from models import Usuario
# from fastapi import FastAPI, Depends, Request
# import requests

# app = FastAPI()

# templates = Jinja2Templates(directory="templates")

# @app.get("/")
# def saludar():
#     return {"mensaje": "hola mundo"}

# @app.get("/usuarios")
# def get_usuarios(db: Session = Depends(get_db)):
#     usuarios = db.query(Usuario).all()
#     return usuarios

# @app.get("/panel/usuarios")
# def panel_usuarios(request: Request, db: Session = Depends(get_db)):
#     usuarios = db.query(Usuario).all()
#     return templates.TemplateResponse("usuarios.html", {"request": request, "usuarios": usuarios})

#

################################################################################################
################################################################################################
################################################################################################
################################################################################################

# from fastapi import FastAPI, Depends, Request
# from fastapi.templating import Jinja2Templates
# from sqlalchemy.orm import Session
# from database import get_db, SessionLocal
# from models import Usuario
# from fastapi.staticfiles import StaticFiles
# from fastapi.responses import HTMLResponse
# from reactpy import component, html
# from reactpy.backend.fastapi import configure
# import requests


# app = FastAPI()

# @app.get("/panel")
# def read_panel(request: Request):
#     return templates.TemplateResponse("panel.html", {"request": request})


# # @app.get("/panel/usuarios")
# # def panel_usuarios(request: Request, db: Session = Depends(get_db)):
# #     usuarios = db.query(Usuario).all()
# #     return templates.TemplateResponse("usuarios.html", {"request": request, "usuarios": usuarios})

# # @app.get("/panel/usuarios")
# # def panel_usuarios(request: Request, db: Session = Depends(get_db)):
# #     usuarios = db.query(Usuario).all()
# #     rendered_table = UsuariosComponent(usuarios=usuarios)
# #     return HTMLResponse(content=rendered_table)

# @app.get("/panel/usuarios")
# def panel_usuarios():
#     return PanelUsuariosComponent()

# templates = Jinja2Templates(directory="templates")


# app.mount("/img", StaticFiles(directory="img"), name="images")
# app.mount("/css", StaticFiles(directory="css"), name="css")

# bootstrap_css = html.link({
#     "rel": "stylesheet",
#     "href": "https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css"
# })

# font_awesome = html.link({
#     "rel": "stylesheet",
#     "href": "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.1/css/all.min.css"
# })

# google_fonts = html.link({
#     "href": "https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap",
#     "rel": "stylesheet"
# })

# custom_css = html.link({
#     "rel": "stylesheet",
#     "href": "/css/styles.css"
# })


# @component
# def PanelUsuariosComponent():
#     db = SessionLocal()  
#     try:
#         usuarios = db.query(Usuario).all()  
#         return UsuariosComponent(usuarios)  
#     finally:
#         db.close()  


# @component
# def UsuariosComponent(usuarios):
#     rows = [
#         html.tr(
#             html.td(usuario.nombre),
#             html.td(usuario.correo)
#         ) for usuario in usuarios
#     ]

#     return html.div(
#         "container mt-5",  
#         [
#             html.table(
#                 "table table-striped", 
#                 [
#                     html.thead(
#                         html.tr(
#                             html.th("Nombre"),
#                             html.th("Correo")
#                         )
#                     ),
#                     html.tbody(rows)
#                 ]
#             )
#         ]
#     )

#
# configure(app, PanelUsuariosComponent)


# @component
# def UsuariosDeleteComponent(usuarios):
#     def handle_delete(event, usuario_id):
#         event.preventDefault()
#         response = requests.delete(f'http://localhost:8000/eliminar-usuario/{usuario_id}')
#         if response.ok:
#             print('Usuario eliminado exitosamente')
#         else:
#             print(f'Error: {response.json().get("detail", "Error desconocido")}')

#     rows = [
#         html.tr([
#             html.td(usuario.id),
#             html.td(usuario.nombre),
#             html.td(usuario.correo),
#             html.td("********"), 
#             html.td(usuario.fecha_registro.strftime('%Y-%m-%d %H:%M:%S')),
#             html.td(
#                 html.img({
#                     "src": usuario.perfil_img, 
#                     "alt": "Imagen de perfil", 
#                     "className": "img-thumbnail", 
#                     "style": {
#                         "width": "50px", 
#                         "height": "50px"  
#                     }
#                 })
#             ),
#             html.td(
#                 html.button(
#                     {
#                         "onClick": lambda event: handle_delete(event, usuario.id),
#                         "className": "btn btn-danger"
#                     },
#                     "Eliminar"
#                 )
#             )
#         ]) for usuario in usuarios
#     ]

#     return html.div(
#         {
#             "className": "container mt-5"
#         },
#         bootstrap_css,
#         font_awesome,
#         google_fonts,
#         custom_css,            
#         html.table(
#                 {
#                     "className": "custom-table"
#                 },
#                 [
#                     html.thead(
#                         html.tr([
#                             html.th("ID"),
#                             html.th("Nombre"),
#                             html.th("Correo"),
#                             html.th("Contraseña"),
#                             html.th("Fecha de Registro"),
#                             html.th("Imagen de Perfil"),
#                             html.th("Acciones")
#                         ])
#                     ),
#                     html.tbody(rows)
#                 ]
#             )
#     )