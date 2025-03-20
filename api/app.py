from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return [{"message": "Welcome PatentPatenteLabBR!",
            "version": "v0.25.03.20",
            "author": "Rene Faustino Gabriel Junior <rene.gabriel@ufrgs.br>"}]


@app.get("/hello/{name}")
def hello(name: str):
    return {"message": f"Olá, {name}!"}
