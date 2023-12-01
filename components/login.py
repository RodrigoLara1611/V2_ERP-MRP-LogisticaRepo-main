# login.py
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from reactpy.backend.fastapi import configure
from reactpy import component, html

app = FastAPI()

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

@component
def LoginPage():
    return html.div(
        {
            "style": {
                "backgroundImage": "url('/img/1.png')",
                "backgroundSize": "cover",
                "backgroundAttachment": "fixed"
            }
        },
        bootstrap_css,
        font_awesome,
        google_fonts,
        custom_css,
        html.div({"className": "container mt-5"},
            html.div({"className": "row"},
                html.div({"className": "col-md-6 mx-auto"},
                    html.div({"className": "card"},
                        html.div({"className": "card-header text-center"},
                            html.img({
                                "src": "/img/logo_logistica.png",
                                "alt": "Logo Logística",
                                "style": {
                                    "width": "50px",
                                    "height": "50px"
                                }
                            }),
                            html.h3("Iniciar Sesión")
                        ),
                        html.div({"className": "card-body"},
                            html.form({"action":"principal"},
                                html.div({"className": "form-group"},
                                    html.label({"htmlFor": "email"}, "Correo Electrónico:"),
                                    html.input({
                                        "type": "email",
                                        "className": "form-control",
                                        "id": "email",
                                        "placeholder": "ejemplo@dominio.com",
                                        "required": True
                                    })
                                ),
                                html.div({"className": "form-group"},
                                    html.label({"htmlFor": "password"}, "Contraseña:"),
                                    html.input({
                                        "type": "password",
                                        "className": "form-control",
                                        "id": "password",
                                        "placeholder": "Ingresa tu contraseña",
                                        "required": True
                                    })
                                ),
                                html.div({"className": "form-group text-center"},
                                    html.button({
                                        "type": "submit",
                                        "className": "btn btn-primary",
                                        "style": {
                                            "transition": "0.3s"
                                        }
                                    }, "Acceder")
                                ),
                                html.div({"className": "text-center"},
                                    html.h6({"href": "consultas"}, "¿Olvidaste tu contraseña?"),
                                    html.h6({"href": "principal"}, "Contacta con un administrador")
                                )
                            )
                        ),
                        html.div({"className": "card-footer text-center"},
                            html.small("©2023 Logística. Todos los derechos reservados.")
                        )
                    )
                )
            )
        )
    )

configure(app, LoginPage)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
