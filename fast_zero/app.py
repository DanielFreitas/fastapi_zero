from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get('/')
def read_root():
    return {'message': 'Olá Mundo!'}


@app.get('/ola', response_class=HTMLResponse)
def ola_html():
    html_content = """
    <!doctype html>
    <html>
        <head>
            <meta charset="utf-8">
            <title>Olá</title>
        </head>
        <body>
            <h1>olá mundo</h1>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)
