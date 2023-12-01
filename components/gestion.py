# gestion.py
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
def ShippingManagement():
    return html.div(
        bootstrap_css,
        font_awesome,
        google_fonts,
        custom_css,
        html.div({"className": "container mt-5"},
            html.div({"className": "mb-5"},
                #html.h2("Ingreso de Nuevos Envíos y Cargas"),
                html.h2("Aqui no me quedo claro si realmente nos refierimos a la gestion de rutas?"),
                html.form({"action":"principal"},
                    # reserved para: los campos del formulario creo que son-> dirección, contenido del envío, fecha de entrega, blah blah blah
                    html.button({"type": "submit", "className": "btn btn-primary"}, "Regresar")
                )
            ),
            
            html.div(
                html.h2("Historial de Entregas"),
                html.table({"className": "table"},
                    html.tr(
                        html.td("Envío #1234"),
                        html.td("Fecha de Envío"),
                        html.td(
                            html.button({
                                "className": "btn btn-info",
                                "data-toggle": "collapse",
                                "data-target": "#detalles1234"
                            }, "Ver Detalles"),
                            
                            html.div({"id": "detalles1234", "className": "collapse"},
                                "Detalles del envío #1234"
                            )
                        )
                    )
                )
            )
        )
    )

configure(app, ShippingManagement)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
