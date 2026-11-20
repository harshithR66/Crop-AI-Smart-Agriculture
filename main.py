from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException
import joblib
import pandas as pd
from pathlib import Path
from fastapi import FastAPI

app = FastAPI(
    title="Crop Suitability Prediction API",
    description="Random Forest based Crop Recommendation System",
    version="1.0"
)

BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = BASE_DIR / "crop_model.pkl"

model = joblib.load(MODEL_PATH)

print("Model loaded successfully!")
print("Model type:", type(model))
print("Random Forest model loaded successfully!")


# ---------------------------------
# 3. Define input parameters
# ---------------------------------

class CropInput(BaseModel):

    N: float = Field(ge=0)
    P: float = Field(ge=0)
    K: float = Field(ge=0)

    temperature: float

    humidity: float = Field(ge=0, le=100)

    ph: float = Field(ge=0, le=14)

    rainfall: float = Field(ge=0)


# ---------------------------------
# 4. Home endpoint
# ---------------------------------

@app.get("/")
def home():

    return {
        "message": "Crop Suitability Prediction API is running",
        "algorithm": "Random Forest"
    }


@app.get("/health")
def health():

    return {
        "status": "Healthy",
        "model_loaded": model is not None
    }


@app.post("/predict")
def predict_crop(data: CropInput):

    try:

        input_data = pd.DataFrame([{

            "N": data.N,
            "P": data.P,
            "K": data.K,
            "temperature": data.temperature,
            "humidity": data.humidity,
            "ph": data.ph,
            "rainfall": data.rainfall

        }])

        # Generate prediction

        prediction = model.predict(input_data)[0]

        # Calculate prediction probability

        probabilities = model.predict_proba(input_data)[0]

        confidence = round(
            float(max(probabilities)) * 100, 2
        )

        return {

            "recommended_crop": str(prediction),

            "confidence_score": confidence,

            "algorithm": "Random Forest"

        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )