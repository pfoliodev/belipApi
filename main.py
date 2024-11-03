from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from database.db_manager import DatabaseManager

app = FastAPI()

# Monter les fichiers statiques
# app.mount("/static", StaticFiles(directory="static"), name="static")

# Configurer les templates
templates = Jinja2Templates(directory="templates")


# Route pour servir la page HTML
@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Route pour obtenir les données GeoJSON
@app.get("/api/stations")
async def get_stations():
    with DatabaseManager() as db:
        geojson_data = db.get_stations_geojson()
    return geojson_data

if __name__ == "__main__":
    import uvicorn
    # Lancer le serveur
    uvicorn.run(app, host="0.0.0.0", port=8000)