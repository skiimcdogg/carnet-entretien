from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def lire_racine():
    return {"message": "FastAPI intégré avec succès !"}
