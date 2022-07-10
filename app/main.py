from fastapi import Depends, FastAPI
from fastapi import status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ValidationError, validator

from app.messages import generate_summary

app = FastAPI()


class SummaryInput(BaseModel):
    lat: float = None
    lon: float = None

    @validator('lat')
    def validate_lat(cls, lat):
        if lat is None or (not -90 <= lat < 90):
            raise ValueError('lat is required')
        return lat

    @validator('lon')
    def validate_lon(cls, lon):
        if lon is None or (not -180 <= lon < 180):
            raise ValueError('lon is required')
        return lon


@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc: ValidationError):
    return JSONResponse(status_code=400, content={"error": str(exc)})


@app.get('/summary/', status_code=status.HTTP_200_OK)
def summary(value: SummaryInput = Depends()):
    return generate_summary(value.lat, value.lon)
