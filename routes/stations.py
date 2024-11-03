import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from database.db_manager import DatabaseManager
from pydantic import BaseModel
from typing import List

app = FastAPI()


# Modèles Pydantic pour la validation des données
class GeoJSONFeature(BaseModel):
    type: str = "Feature"
    geometry: dict
    properties: dict


class GeoJSONFeatureCollection(BaseModel):
    type: str = "FeatureCollection"
    features: List[GeoJSONFeature]


@app.get("/api/stations", response_model=GeoJSONFeatureCollection)
async def get_stations():
    try:
        with DatabaseManager() as db:
            geojson_data = db.get_stations_geojson()

        if geojson_data is None:
            raise HTTPException(status_code=500, detail="Erreur lors de la récupération des données")

        # Validation des données avec Pydantic
        validated_data = GeoJSONFeatureCollection(**geojson_data)

        return JSONResponse(content=validated_data.dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)