# usersCRUD.py
from requests_toolbelt.multipart.encoder import MultipartEncoder
from fastapi import FastAPI, Depends, Form, HTTPException, status, File, UploadFile
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Boolean, Text, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from models import Usuario
from reactpy.backend.fastapi import configure
from reactpy import component, html
from fastapi.staticfiles import StaticFiles
import shutil
from pathlib import Path
from reactpy import use_state
import requests

DATABASE_URL = "mysql+mysqlconnector://root@localhost/logistic"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def obtener_usuarios():
    db = SessionLocal()  
    try:
        usuarios = db.query(Usuario).all()  
        return usuarios  
    finally:
        db.close()  

@app.post("/crear-usuario/")
async def crear_usuario(
    correo: str = Form(...),
    password: str = Form(...),
    nombre: str = Form(...),
    perfil_img: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    db_usuario = db.query(Usuario).filter(Usuario.correo == correo).first()
    if db_usuario:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El correo ya está en uso")

    fecha_registro = datetime.utcnow()  
    nuevo_usuario = Usuario(
        correo=correo,
        password=password,
        nombre=nombre,
        fecha_registro=fecha_registro,
        perfil_img=perfil_img
    )

    img_path = Path(f"img/usuarios/{nombre}.png")
    with open(f"img/usuarios/{nombre}.png", "wb") as buffer:
        shutil.copyfileobj(perfil_img.file, buffer)

    nuevo_usuario.perfil_img = str(img_path)
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    # db.close()
    return {"message": "Usuario creado exitosamente", "usuario_id": nuevo_usuario.id}

def modificar_usuario_db(usuario_id: int, correo: str, password: str, nombre: str, perfil_img: UploadFile, db: Session):
    """
    Esta función encapsula la lógica de modificación de un usuario.
    """
    try:
        db_usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
        if db_usuario is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
        
        db_usuario.correo = correo
        db_usuario.password = password
        db_usuario.nombre = nombre

        img_path = None
        if perfil_img is not None:
            img_path = Path(f"img/usuarios/{nombre}.png")
            with open(f"img/usuarios/{nombre}.png", "wb") as buffer:
                shutil.copyfileobj(perfil_img.file, buffer)
            db_usuario.perfil_img = img_path.as_posix()
            print(db_usuario.perfil_img)  

        db.commit()
        db.refresh(db_usuario)
        return {"message": "Usuario modificado exitosamente", "usuario": db_usuario}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    finally:
        db.close()

@app.put("/modificar-usuario/{usuario_id}")
async def modificar_usuario_api(
    usuario_id: int,
    correo: str = Form(...),
    password: str = Form(...),
    nombre: str = Form(...),
    perfil_img: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    return await modificar_usuario_db(usuario_id, correo, password, nombre, perfil_img, db)

def eliminar_usuario_db(usuario_id: int, db: Session):
    """
    Esta función encapsula la lógica de eliminación de usuario.
    """
    try:
        db_usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
        if db_usuario is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
        db.delete(db_usuario)
        db.commit()
        return {"message": "Usuario eliminado exitosamente"}
    except Exception as e:
        db.rollback() 
        raise
    finally:
        db.close()  

@app.delete("/eliminar-usuario/{usuario_id}")
async def eliminar_usuario_api(usuario_id: int, db: Session = Depends(get_db)):
    return eliminar_usuario_db(usuario_id, db)

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

custom_css = html.link({
    "rel": "stylesheet",
    "href": "/css/styles.css"
})

session = requests.Session()

@component
def FormularioModificacion(usuario, cancelar_modificacion, setUsuarios, setUsuarioSeleccionado):
    correo, setCorreo = use_state(usuario.correo)
    # password, setPassword = use_state('')
    password, setPassword = use_state(usuario.password)
    nombre, setNombre = use_state(usuario.nombre)
    perfil_img, setPerfilImg = use_state(usuario.perfil_img)

    def modificar_usuario():
        datos_modificados = {
            'correo': correo,
            'password': password,
            'nombre': nombre,
            'perfil_img': perfil_img
        }
        datos_para_enviar = {k: v for k, v in datos_modificados.items() if v}
        try:
            m = MultipartEncoder(fields=datos_para_enviar)
            result = modificar_usuario_db(usuario.id, correo, password, nombre, datos_modificados['perfil_img'], db=SessionLocal())
            print(result.get('message', 'Usuario modificado exitosamente'))
            setUsuarios(obtener_usuarios())
            setUsuarioSeleccionado(None)
        except HTTPException as e:
            print(f'Error: {e.detail}')
        except Exception as e:
            print(f'Error: {e}')

    def handle_correo_change(value):
        setCorreo(value)

    def handle_password_change(value):
        setPassword(value)

    def handle_nombre_change(value):
        setNombre(value)

    def handle_perfil_img_change(event):
        setPerfilImg(event['target']['files'][0] if 'files' in event['target'] else None)

    return html.div(
        {
            "className": "container mt-5",
            "style": {
                "display": "flex",
                "justifyContent": "center",
                "alignItems": "center",
                "height": "100vh",  
                "flexDirection": "column",
                "marginBottom": "1em",  
            }
        },
        bootstrap_css,
        font_awesome,
        google_fonts,
        custom_css,
        html.div(  
            {
                "style": {
                    "background": "rgba(169, 169, 169, 0.6)",  
                    "borderRadius": "15px", 
                    "padding": "20px", 
                    "width": "50%", 
                    "textAlign": "center" 
                }
            },
        html.form(
            {
                "enctype": "multipart/form-data"
            },
            # html.br(),
            html.h2("Modificar Usuario"),
            html.div(
                {"className": "form-group"},
                html.label({"htmlFor": "correo"}, "Correo:"),
                html.input({
                    "type": "email",
                    "value": correo,
                    "onChange": lambda event: handle_correo_change(event['target']['value']),
                    "required": True,
                    "className": "form-control",
                    "style": 
                    {
                    "borderRadius": "10px",
                    "border": "2px solid #ced4da",
                    "padding": "10px",
                    "fontSize": "1rem",
                    "width":"70%",
                    "display":"flex",
                    "flex-direction":"column",
                    "align-items":"center"
                    }   
                })
            ),
            html.div(
                {"className": "form-group"},
                html.label({"htmlFor": "password"}, "Contraseña:"),
                html.input({
                    "type": "password",
                    "value": password,
                    "onChange": lambda event: handle_password_change(event['target']['value']),
                    "className": "form-control",
                    "style": 
                    {
                    "borderRadius": "10px",
                    "border": "2px solid #ced4da",
                    "padding": "10px",
                    "fontSize": "1rem",
                    "width":"70%"
                    }
                })
            ),
            html.div(
                {"className": "form-group"},
                html.label({"htmlFor": "nombre"}, "Nombre:"),
                html.input({
                    "type": "text",
                    "value": nombre,
                    "onChange": lambda event: handle_nombre_change(event['target']['value']),
                    "required": True,
                    "className": "form-control",
                    "style": 
                    {
                    "borderRadius": "10px",
                    "border": "2px solid #ced4da",
                    "padding": "10px",
                    "fontSize": "1rem",
                    "width":"70%"
                    }
                })
            ),
            html.div(
                {"className": "form-group"},
                html.label({"htmlFor": "perfil_img"}, "Imagen de Perfil:"),
                html.input({
                    "type": "file",
                    "value": perfil_img,
                    "onChange": lambda event: handle_perfil_img_change(event),
                    "className": "form-control",
                    "name": "perfil_img",
                    "style": 
                    {
                    "borderRadius": "10px",
                    "border": "2px solid #ced4da",
                    "padding": "10px",
                    "fontSize": "1rem",
                    "width":"70%"
                    }                    
                })
            ),
            html.button(
                {
                    "type": "button",
                    "onClick": lambda event: modificar_usuario(),  
                    "className": "btn btn-primary"
                },
                "Guardar Cambios"
            ),
            html.button(
                {
                    "type": "button",
                    "onClick": cancelar_modificacion,  
                     "className": "btn btn-secondary ml-2"  
                },
                "Cancelar"
            )
        )
    ))

@component
def UsuariosDeleteComponent():

    usuarios, setUsuarios = use_state(obtener_usuarios())
    usuarioSeleccionado, setUsuarioSeleccionado = use_state(None)

    def modificar_usuario(usuario):
        setUsuarioSeleccionado(usuario)

    def eliminar_usuario(usuario_id):
        try:
            url = f'http://localhost:8000/eliminar-usuario/{usuario_id}'
            print(url)
            result = eliminar_usuario_db(usuario_id, SessionLocal())
            print(result.get('message', 'Usuario eliminado exitosamente'))
            setUsuarios(obtener_usuarios())
        except HTTPException as e:
            print(f'Error: {e.detail}')
        except Exception as e:
            print(f'Error: {e}')
    
    def cancelar_modificacion(event): 
        setUsuarioSeleccionado(None)

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
                        "width": "50px", 
                        "height": "50px"  
                    }
                })
            ),
            html.td(
                html.button(
                    {
                        "type": "button",
                        "onClick": (lambda event, usuario_id=usuario.id: eliminar_usuario(usuario_id)),
                        "className": "btn btn-danger"
                    },
                    "Eliminar"
                ),
                html.button(
                    {
                        "type": "button",
                        "onClick": lambda event, usuario=usuario: modificar_usuario(usuario),
                        "className": "btn btn-warning"
                    },
                    "Modificar"
                )
            )
        ]) for usuario in usuarios
    ]

    if usuarioSeleccionado:
        return html.div(
        {
            "className": "container mt-5"
        },
        bootstrap_css,
        font_awesome,
        google_fonts,
        custom_css,
        FormularioModificacion
        (
            usuarioSeleccionado,
            cancelar_modificacion,
            setUsuarios,
            setUsuarioSeleccionado
        ),            
        html.table(
                {
                    "className": "custom-table"
                },
                [
                    html.thead(
                        html.tr([
                            html.th("ID"),
                            html.th("Nombre"),
                            html.th("Correo"),
                            html.th("Contraseña"),
                            html.th("Fecha de Registro"),
                            html.th("Imagen de Perfil"),
                            html.th("Acciones")
                        ])
                    ),
                    html.tbody(rows)
                ]
            )
        )

    return html.div(
        {
            "className": "container mt-5",
            "style": {
                "marginBottom": "1em",
            }
        },
        bootstrap_css,
        font_awesome,
        google_fonts,
        custom_css,            
        html.table(
                {
                    "className": "custom-table"
                },
                [
                    html.thead(
                        html.tr([
                            html.th("ID"),
                            html.th("Nombre"),
                            html.th("Correo"),
                            html.th("Contraseña"),
                            html.th("Fecha de Registro"),
                            html.th("Imagen de Perfil"),
                            html.th("Acciones")
                        ])
                    ),
                    html.tbody(rows)
                ]
            )
    )

@component
def UserCreationForm():
    usuarios = obtener_usuarios() 

    def handle_submit(event):
        event.preventDefault()
        form_elements = event['currentTarget']['elements']
        correo = next(element['value'] for element in form_elements if element['tagName'] == 'INPUT' and element['name'] == 'correo')
        password = next(element['value'] for element in form_elements if element['tagName'] == 'INPUT' and element['name'] == 'password')
        nombre = next(element['value'] for element in form_elements if element['tagName'] == 'INPUT' and element['name'] == 'nombre')
        perfil_img = next(element for element in form_elements if element['tagName'] == 'INPUT' and element['name'] == 'perfil_img')

        m = MultipartEncoder(
            fields={
                'correo': correo,
                'password': password,
                'nombre': nombre,
                'perfil_img': (perfil_img, open(perfil_img, 'rb'), 'image/png')
            }
        )

        response = requests.post(
            'http://localhost:8000/crear-usuario/',
            data=m,
            headers={'Content-Type': m.content_type}
        )

    return html.div(
        {
            "style": {
                "fontFamily": "'Roboto', sans-serif",
                "backgroundImage": "url('/img/1.png')",  
                "backgroundSize": "cover", 
                "backgroundRepeat": "no-repeat"  
            }
        },
        bootstrap_css,
        font_awesome,
        google_fonts,
        custom_css,
        html.header(
            {
                "className": "bg-primary text-white text-center p-3"
            },
            html.img({
                "src": "/img/logo_logistica.png",
                "alt": "Logo",
                "style": {
                    "width": "50px",
                    "height": "50px"
                }
            }),
            html.h1("Creación de Usuario"),
        ),
        html.main(
            {
                "className": "container mt-5"
            },
            html.div({"className":"card mb-4"},
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
            )),
            html.div(
                {
                    "className": "mb-5",
                    "style": {
                        "background": "rgba(169, 169, 169, 0.6)",
                        "borderRadius": "15px", 
                        "padding": "20px",  
                        "textAlign": "center"  
                    }
                },
                html.h2("Formulario de Registro"),
                html.form(
                    {
                        "action": "/crear-usuario/",
                        "method": "post",
                        "enctype": "multipart/form-data"  # Añade esta línea
                    },
                    html.div(
                        {
                            "className": "form-group"
                        },
                        html.label({"htmlFor": "correo"}, "Correo:"),
                        html.input(
                            {
                                "type": "email",
                                "className": "form-control",
                                "name": "correo",
                                "required": True
                            }
                        )
                    ),
                    html.div(
                        {
                            "className": "form-group"
                        },
                        html.label({"htmlFor": "password"}, "Contraseña:"),
                        html.input(
                            {
                                "type": "password",
                                "className": "form-control",
                                "name": "password",
                                "required": True
                            }
                        )
                    ),
                    html.div(
                        {
                            "className": "form-group"
                        },
                        html.label({"htmlFor": "nombre"}, "Nombre:"),
                        html.input(
                            {
                                "type": "text",
                                "className": "form-control",
                                "name": "nombre",
                                "required": True
                            }
                        )
                    ),
                    html.div(
                        {
                            "className": "form-group"
                        },
                        html.label({"htmlFor": "perfil_img"}, "Imagen de Perfil:"),
                        html.input(
                            {
                                "type": "file",
                                "className": "form-control",
                                "name": "perfil_img",
                                "accept": "image/png"
                            }
                        )
                    ),
                    html.button(
                        {
                            "type": "submit",
                            "className": "btn btn-primary"
                        },
                        "Crear Usuario"
                    ),
                    UsuariosDeleteComponent()
                )
            ),
        ),
    )

configure(app, UserCreationForm)
# configure(app, UsuariosDeleteComponent)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)



# @app.post("/crear-usuario/")
# async def crear_usuario(
#     correo: str = Form(...),
#     password: str = Form(...),
#     nombre: str = Form(...),
#     perfil_img: str = Form(None),  
#     db: Session = Depends(get_db)
# ):
#     db_usuario = db.query(Usuario).filter(Usuario.correo == correo).first()
#     if db_usuario:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El correo ya está en uso")

#     fecha_registro = datetime.utcnow()  
#     nuevo_usuario = Usuario(
#         correo=correo,
#         password=password,
#         nombre=nombre,
#         fecha_registro=fecha_registro,
#         perfil_img=perfil_img
#     )

#     db.add(nuevo_usuario)
#     db.commit()
#     db.refresh(nuevo_usuario)
#     db.close()
#     return {"message": "Usuario creado exitosamente", "usuario_id": nuevo_usuario.id}
# --------------- NOTAS PARA MI YO DEL FUTURO by jdfr ---------------

# Tenía problemas al intentar eliminar un usuario usando HTTP.
# En lugar de llamar a mi propia API (lo cual era overkill), decidí
# simplificar el proceso y llamar directamente a la función que maneja 
# la eliminación del usuario.

# Si alguna vez piensas en llamar a tu propia API usando HTTP:
# NO LO HAGA COMPA, A menos que realmente sepas lo que estás haciendo y 
# estés dispuesto a lidiar con los bloqueos y otros problemas 
# inesperados.

# Intentaba eliminar un usuario usando una petición HTTP a mi propia API. Básicamente:
#   @app.delete("/eliminar-usuario/{usuario_id}")
#   async def eliminar_usuario():
#       # ...
#       response = client.delete(...)  # llamada HTTP a la misma API
# El problema con esto es que puede bloquear el event loop, especialmente con `async`.

# POR QUÉ ES INCORRECTO:
# Es overkill y puede causar problemas de rendimiento. Imagina hacer una solicitud 
# HTTP para algo que puedes manejar directamente con una función. 

# SOLUCIÓN:
# Llamar directamente a la función que maneja la eliminación del usuario.
#   def eliminar_usuario_db(usuario_id: int, db: Session):
#       # ... lógica de eliminación ...
#   Esta función es ahora utilizada tanto por la ruta como por el manejo del evento.

# POR QUÉ ES CORRECTO:
# Es más eficiente, no tienes el overhead de la solicitud HTTP, y evitas problemas 
# potenciales con el event loop.

# Refactoricé el código para tener una función `eliminar_usuario_db` que encapsula 
# la lógica de eliminar un usuario. Menos código duplicado, más funcionalidad.

# IMPORTANTE:
# Hacer solicitudes HTTP a tu propio servidor, especialmente de forma síncrona, 
# puede bloquear el event loop. Especialmente con `async`. Mejor evitarlo cuando 
# no es necesario.

# Mejor hubiera vendido avón.
# Refresher y ayuda en general de endpoints en FastAPI: https://fastapi.tiangolo.com/tutorial/first-steps/

# ------------------- FIN DE LAS NOTAS -----------------------
