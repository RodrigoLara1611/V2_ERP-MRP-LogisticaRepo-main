from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
from fastapi.responses import JSONResponse

DATABASE_URL = "mysql+mysqlconnector://root@localhost/logistic"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    correo = Column(String, index=True, unique=True, nullable=False)
    password = Column(String, nullable=False)
    nombre = Column(String, index=True)
    fecha_registro = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/usuarios/")
async def crear_usuario(correo: str, password: str, nombre: str, db: Session = Depends(get_db)):
    db_usuario = Usuario(correo=correo, password=password, nombre=nombre)
    db.add(db_usuario)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    db.refresh(db_usuario)
    return db_usuario

@app.get("/usuarios/")
async def leer_usuarios(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    usuarios = db.query(Usuario).offset(skip).limit(limit).all()
    return usuarios

@app.get("/usuarios/{usuario_id}")
async def leer_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@app.put("/usuarios/{usuario_id}")
async def actualizar_usuario(
        usuario_id: int,
        correo: str = None,
        nombre: str = None,
        password: str = None,
        db: Session = Depends(get_db)
):
    db_usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if correo is not None:
        db_usuario.correo = correo
    if nombre is not None:
        db_usuario.nombre = nombre
    if password is not None:
        db_usuario.password = password
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

@app.delete("/usuarios/{usuario_id}")
async def eliminar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    db_usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.delete(db_usuario)
    db.commit()
    return {"message": "Usuario eliminado"}


import requests
from fastapi.responses import HTMLResponse
from fastapi import Request
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/create_user/")
async def create_user(correo: str, password: str, nombre: str):
    data = {
        "correo": correo,
        "password": password,
        "nombre": nombre,
    }
    try:
        response = requests.post('http://localhost:8000/usuarios/', json=data)
        if response.ok:
            return {"message": "Usuario creado exitosamente."}
        else:
            return {"error": response.json().get('detail', 'Error desconocido')}
    except requests.RequestException as e:
        return {"error": f"Error de red: {e}"}

@app.get("/get_users/")
async def get_users():
    try:
        response = requests.get('http://localhost:8000/usuarios/')
        if response.ok:
            usuarios = response.json()
            return {"usuarios": usuarios}
        else:
            return {"error": response.json().get('detail', 'Error desconocido')}
    except requests.RequestException as e:
        return {"error": f"Error de red: {e}"}

# from fastapi import FastAPI, Depends, HTTPException, status
# from fastapi.staticfiles import StaticFiles
# from sqlalchemy import create_engine, Column, Integer, String, DateTime
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker, Session
# from datetime import datetime
# from reactpy.backend.fastapi import configure
# from reactpy import component, html
# import requests

# DATABASE_URL = "mysql+mysqlconnector://root@localhost/logistic"

# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# Base.metadata.create_all(bind=engine)

# class Usuario(Base):
#     __tablename__ = "usuarios"
#     id = Column(Integer, primary_key=True, index=True, autoincrement=True)
#     correo = Column(String, index=True, unique=True, nullable=False)
#     password = Column(String, nullable=False)
#     nombre = Column(String, index=True)
#     fecha_registro = Column(DateTime, nullable=False)
#     perfil_img = Column(String)

# app = FastAPI()

# @app.post("/usuarios/")
# async def crear_usuario(correo: str, password: str, nombre: str, db: Session = Depends(get_db)):
#     db_usuario = Usuario(correo=correo, password=password, nombre=nombre)  # Asegúrate de usar la clase de modelo correcta
#     db.add(db_usuario)
#     try:
#         db.commit()
#     except Exception as e:
#         db.rollback()
#         raise HTTPException(status_code=400, detail=str(e))
#     db.refresh(db_usuario)
#     return db_usuario

# @app.get("/usuarios/")
# async def leer_usuarios(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
#     usuarios = db.query(Usuario).offset(skip).limit(limit).all()
#     return usuarios

# @app.get("/usuarios/{usuario_id}")
# async def leer_usuario(usuario_id: int, db: Session = Depends(get_db)):
#     usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
#     if usuario is None:
#         raise HTTPException(status_code=404, detail="Usuario no encontrado")
#     return usuario

# @app.put("/usuarios/{usuario_id}")
# async def actualizar_usuario(
#         usuario_id: int,
#         correo: str = None,
#         nombre: str = None,
#         password: str = None,
#         db: Session = Depends(get_db)
# ):
#     db_usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
#     if db_usuario is None:
#         raise HTTPException(status_code=404, detail="Usuario no encontrado")
#     if correo is not None:
#         db_usuario.correo = correo
#     if nombre is not None:
#         db_usuario.nombre = nombre
#     if password is not None:
#         db_usuario.password = password
#     db.commit()
#     db.refresh(db_usuario)
#     return db_usuario

# @app.delete("/usuarios/{usuario_id}")
# async def eliminar_usuario(usuario_id: int, db: Session = Depends(get_db)):
#     db_usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
#     if db_usuario is None:
#         raise HTTPException(status_code=404, detail="Usuario no encontrado")
#     db.delete(db_usuario)
#     db.commit()
#     return {"message": "Usuario eliminado"}

# @component
# def FormularioCreacionUsuario():
#     def handle_submit(event):
#         form_elements = event['currentTarget']['elements']
#         data = {
#             "correo": form_elements[0]['value'],
#             "password": form_elements[1]['value'],
#             "nombre": form_elements[2]['value'],
#         }
#         try:
#             response = requests.post('http://localhost:8000/usuarios/', json=data)
#             if response.ok:
#                 # Manejar respuesta exitosa
#                 print("Usuario creado exitosamente.")
#             else:
#                 # Manejar error
#                 print("Error al crear usuario:", response.json().get('detail', 'Error desconocido'))
#         except requests.RequestException as e:
#             print(f"Error de red: {e}")

#     return html.form(
#         {
#             "onSubmit": handle_submit
#         },
#         html.label({"for": "correo"}, "Correo:"),
#         html.input({"type": "email", "name": "correo", "required": True}),
#         html.label({"for": "password"}, "Contraseña:"),
#         html.input({"type": "password", "name": "password", "required": True}),
#         html.label({"for": "nombre"}, "Nombre:"),
#         html.input({"type": "text", "name": "nombre", "required": True}),
#         html.button({"type": "submit"}, "Crear Usuario")
#     )


# @component
# def TablaUsuarios():
#     response = requests.get('http://localhost:8000/usuarios/')
#     usuarios = []
#     if response.ok:
#         usuarios = response.json()
#     else:
#         # Manejar error
#         print(f"Error: {response.status_code}")
#         return html.div("Error al obtener los usuarios")

#     return html.table(
#         [
#             html.thead(
#                 html.tr(
#                     [
#                         html.th("ID"),
#                         html.th("Correo"),
#                         html.th("Nombre"),
#                         html.th("Acciones"),
#                     ]
#                 )
#             ),
#             html.tbody(
#                 [
#                     html.tr(
#                         [
#                             html.td(usuario['id']),
#                             html.td(usuario['correo']),
#                             html.td(usuario['nombre']),
#                             html.td(
#                                 [
#                                     # Botones o links para editar/eliminar
#                                     html.a("Editar", href=f"/editar-usuario/{usuario['id']}"),
#                                     html.span(" | "),
#                                     html.a("Eliminar", href=f"/eliminar-usuario/{usuario['id']}")
#                                 ]
#                             )
#                         ]
#                     ) for usuario in usuarios
#                 ]
#             )
#         ]
#     )

# @component
# def FormularioEdicionUsuario(usuario_id):
#     def handle_submit(event):
#         event.preventDefault()
#         form_elements = event['currentTarget']['elements']
#         correo = next(element['value'] for element in form_elements if element['name'] == 'correo')
#         nombre = next(element['value'] for element in form_elements if element['name'] == 'nombre')
#         password = next(element['value'] for element in form_elements if element['name'] == 'password')
        
#         response = requests.put(
#             f'http://localhost:8000/usuarios/{usuario_id}',
#             json={
#                 'correo': correo,
#                 'nombre': nombre,
#                 'password': password
#             }
#         )
        
#         if response.ok:
#             print('Usuario actualizado exitosamente')
#         else:
#             print(f'Error: {response.status_code}')

#     return html.form(
#         {"onSubmit": handle_submit},
#         html.div(
#             {"className": "form-group"},
#             html.label({"htmlFor": "correo"}, "Correo:"),
#             html.input(
#                 {
#                     "type": "email",
#                     "className": "form-control",
#                     "name": "correo",
#                     "required": True
#                 }
#             )
#         ),
#         html.div(
#             {"className": "form-group"},
#             html.label({"htmlFor": "nombre"}, "Nombre:"),
#             html.input(
#                 {
#                     "type": "text",
#                     "className": "form-control",
#                     "name": "nombre",
#                     "required": True
#                 }
#             )
#         ),
#         html.div(
#             {"className": "form-group"},
#             html.label({"htmlFor": "password"}, "Contraseña:"),
#             html.input(
#                 {
#                     "type": "password",
#                     "className": "form-control",
#                     "name": "password",
#                     "required": True
#                 }
#             )
#         ),
#         html.button(
#             {"type": "submit", "className": "btn btn-primary"},
#             "Actualizar Usuario"
#         )
#     )

# @component
# def BotonEliminarUsuario(usuario_id):
#     def handle_click(event):
#         response = requests.delete(f'http://localhost:8000/usuarios/{usuario_id}')
#         if response.ok:
#             print('Usuario eliminado exitosamente')
#         else:
#             print(f'Error: {response.status_code}')

#     return html.button({"onClick": handle_click}, "Eliminar Usuario")

# configure(app, FormularioCreacionUsuario)
# configure(app, FormularioEdicionUsuario)
# configure(app, BotonEliminarUsuario)
# configure(app, TablaUsuarios)