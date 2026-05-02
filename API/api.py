from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import pandas as pd
import joblib

api = FastAPI(docs_url=None, redoc_url=None)
model = joblib.load("model.pkl")

# ROOT

@api.get("/")
def home():
    return {"message": "Getaround API is running 🚗"}

# PREDICT

@api.post("/predict")
def predict(data: dict):

    columns = [
        "model_key",
        "mileage",
        "engine_power",
        "fuel",
        "paint_color",
        "car_type",
        "private_parking_available",
        "has_gps",
        "has_air_conditioning",
        "automatic_car",
        "has_getaround_connect",
        "has_speed_regulator",
        "winter_tires"
    ]

    df = pd.DataFrame(data["input"], columns=columns)

    prediction = model.predict(df)

    return {"prediction": prediction.tolist()}


# REQUIRED DOCS PAGE

@api.get("/docs", response_class=HTMLResponse)
def docs():
    return """
    <html>
    <head>
        <title>Getaround API Documentation</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 40px;
                background-color: #d6d6d6;
            }
            h1 {
                color: #2c3e50;
            }
            .box {
                background: grey;
                padding: 20px;
                border-radius: 10px;
                margin-bottom: 20px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }
            input, button {
                padding: 8px;
                margin: 5px 0;
                width: 250px;
            }
            button {
                cursor: pointer;
            }
            pre {
                background: #eee;
                padding: 10px;
                border-radius: 5px;
            }
        </style>
    </head>

    <body>

        <h1>🚗 Getaround Pricing API</h1>

        <div class="box">
            <h2>POST /predict</h2>

            <p><b>Description:</b> Predict rental price of a car using ML model</p>

            <p><b>Required input format:</b></p>

            <pre>
{
  "input": [[
    "model_key",
    mileage,
    engine_power,
    "fuel",
    "paint_color",
    "car_type",
    private_parking_available,
    has_gps,
    has_air_conditioning,
    automatic_car,
    has_getaround_connect,
    has_speed_regulator,
    winter_tires
  ]]
}
            </pre>

            <p><b>Example request:</b></p>

            <pre>
{
  "input": [[
    "bmw",
    120000,
    90,
    "diesel",
    "black",
    "sedan",
    true,
    true,
    true,
    false,
    true,
    false,
    true
  ]]
}
            </pre>
        </div>

        <div class="box">

            <h2>🧪 Try the API</h2>

            <input id="model_key" placeholder="model_key"><br>
            <input id="mileage" placeholder="mileage" type="number"><br>
            <input id="engine_power" placeholder="engine_power" type="number"><br>
            <input id="fuel" placeholder="fuel (diesel/petrol/...)"><br>
            <input id="paint_color" placeholder="paint_color"><br>
            <input id="car_type" placeholder="car_type"><br><br>

            <button onclick="sendRequest()">Predict</button>

            <h3>Result:</h3>
            <pre id="result"></pre>

        </div>

        <script>
        async function sendRequest() {

            const data = {
                input: [[
                    document.getElementById("model_key").value,
                    parseFloat(document.getElementById("mileage").value),
                    parseFloat(document.getElementById("engine_power").value),
                    document.getElementById("fuel").value,
                    document.getElementById("paint_color").value,
                    document.getElementById("car_type").value,
                    true,
                    true,
                    true,
                    false,
                    true,
                    false,
                    true
                ]]
            };

            const response = await fetch("/predict", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            document.getElementById("result").innerText =
                JSON.stringify(result, null, 2);
        }
        </script>

    </body>
    </html>
    """
