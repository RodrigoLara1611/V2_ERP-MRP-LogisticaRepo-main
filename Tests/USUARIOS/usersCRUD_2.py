from fastapi import FastAPI, Depends, Form, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from models import Usuario
from reactpy.backend.fastapi import configure
from reactpy import component, html
# from panels import UsuariosDeleteComponent
from fastapi.staticfiles import StaticFiles
from functools import partial
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
    perfil_img: str = Form(None), 
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

    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return {"message": "Usuario creado exitosamente", "usuario_id": nuevo_usuario.id}

@app.delete("/eliminar-usuario/{usuario_id}")
async def eliminar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    try:
        db_usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
        if db_usuario is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
        db.delete(db_usuario)
        db.commit()
        return {"message": "Usuario eliminado exitosamente"}
    except Exception as e:
        print(f"Error: {e}")  
        db.rollback() 
        raise
    finally:
        db.close() 

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

# def make_handle_delete(usuario_id):
#     def handle_delete(event):
#         # Define la URL del endpoint, incluyendo el ID del usuario
#         url = f'http://localhost:8000/eliminar-usuario/{usuario_id}'
#         # Realiza una solicitud DELETE al endpoint
#         response = requests.delete(url)
#         # Comprueba si la solicitud fue exitosa (código de estado HTTP 200-299)
#         if response.ok:
#             print('Usuario eliminado exitosamente')
#         else:
#             # Si hubo un error, imprime el mensaje de error
#             print(f'Error: {response.json().get("detail", "Error desconocido")}')

#     return handle_delete

# def make_handle_delete(usuario_id):
#     def handle_delete(event):
#         url = f'http://localhost:8000/eliminar-usuario/{usuario_id}'
#         print(url)  # Debug: Print the URL to the console
#         response = requests.delete(url)
#         if response.ok:
#             print(response.json().get('message', 'Usuario eliminado exitosamente'))
#         else:
#             print(response.json().get('detail', 'Error desconocido'))
#     return handle_delete

session = requests.Session()

def make_handle_delete(usuario_id):
    def handle_delete(event):
        url = f'http://localhost:8000/eliminar-usuario/{usuario_id}'
        print(url) 
        
        try:
            response = session.delete(url, timeout=2)  
            print(f'Status Code: {response.status_code}')
            print(response.text)
            if response.ok:
                print(response.json().get('message', 'Usuario eliminado exitosamente'))
            else:
                print(response.json().get('detail', 'Error desconocido'))
        except requests.exceptions.RequestException as e:
            print(f'Error: {e}')
            
    return handle_delete


@component
def UsuariosDeleteComponent(usuarios):
    # def handle_delete(event, usuario_id):
    #     db = SessionLocal()
    #     try:
    #         db_usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    #         if db_usuario is None:
    #             print(f'Error: Usuario no encontrado')
    #         else:
    #             db.delete(db_usuario)
    #             db.commit()
    #             print('Usuario eliminado exitosamente')
    #     finally:
    #         db.close()

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
                        "onClick": (lambda event: make_handle_delete(usuario.id)(event)),
                        "className": "btn btn-danger"
                    },
                    "Eliminar"
                )
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
        form_elements = event['currentTarget']['elements']
        event.preventDefault()
        correo = next(element['value'] for element in form_elements if element['tagName'] == 'INPUT' and element['name'] == 'correo')
        password = next(element['value'] for element in form_elements if element['tagName'] == 'INPUT' and element['name'] == 'password')
        nombre = next(element['value'] for element in form_elements if element['tagName'] == 'INPUT' and element['name'] == 'nombre')
        perfil_img = next((element['value'] for element in form_elements if element['tagName'] == 'INPUT' and element['name'] == 'perfil_img'), None)

        response = requests.post(
            'http://localhost:8000/crear-usuario/',
            data={
                'correo': correo,
                'password': password,
                'nombre': nombre,
                'perfil_img': perfil_img
            }
        )

    return html.div(
        {
            "style": {
                "fontFamily": "'Roboto', sans-serif"
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
            html.div(
                {
                    "className": "mb-5"
                },
                html.h2("Formulario de Registro"),
                html.form(
                    {
                        "action": "/crear-usuario/",
                        "method": "post"
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
                        html.label({"htmlFor": "perfil_img"}, "Imagen de Perfil (URL):"),
                        html.input(
                            {
                                "type": "text",
                                "className": "form-control",
                                "name": "perfil_img"
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
                    UsuariosDeleteComponent(usuarios)
                )
            ),
        ),
    )

configure(app, UserCreationForm)
configure(app, UsuariosDeleteComponent)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)