from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from calculator import Calculator
from datetime import datetime

label = {
    "calculator_version": "0.1",
    "calculator_url": "https://api.dka-calculator.co.uk",
    "author": "Daniel Leach",
    "author_url": "https://danleach.uk",
    "author_email": "web@danleach.uk",
    "request_timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
}

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
        <head>
            <title>DKA Calculator API</title>
        </head>
        <body>
            <h1>DKA Calculator API - Root</h1>
            Welcome to the DKA Calculator API. This API is under development and is not suitable for clinical use. You should use <a href="https://dka-calculator.co.uk">dka-calculator.co.uk</a> instead.<br>
            <hr>
            Version: """ + label["calculator_version"] + """<br>
            URL: """ + label["calculator_url"] + """<br>
            Author: """ + label["author"] + """<br>
            Author URL: """ + label["author_url"] + """<br>
            Author Email: """ + label["author_email"] + """<br>
            Timestamp: """ + label["request_timestamp"] + """<br>
            <hr>
            <a href="/docs">View the documentation</a>

        </body>
    </html>
    """

@app.post("/calculator/")
async def calculator(calc: Calculator):
    return {
        "Label": label,
        "Input": {
            "age": {
                "value": calc.age,
                "data type": "float",
                "optional": False,
                "units": "decimal years",
                "accepted range": ">=0, <19",
                "comment": "Age of patient in decimal years at time of starting DKA protocol. Used to determine if submitted weight is within expected safe range.",
            },
            "pH": {
                "value": calc.pH,
                "data type": "float",
                "optional": False,
                "units": "n/a",
                "accepted range": ">=6.2, <7.5",
                "comment": "Blood pH of patient at time of starting DKA protocol. Used to determine DKA severity which deterimines fluid deficit percentage, fluid deficit volume, fluid deficit rate and fluid total rate calculations.",
            },
            "bicarbonate": {
                "value": calc.bicarbonate,
                "data type": "float",
                "optional": True,
                "units": "millimoles per litre",
                "accepted range": ">=0, <35",
                "comment": "Blood bicarbonate of patient at time of starting DKA protocol. Optional: if provided the DKA severity grading based on the bicarbonate will be used if this is worse than the severity grading based on pH",
            },
            "weight": {
                "value": calc.weight,
                "data type": "float",
                "optional": False,
                "units": "kilograms",
                "accepted range": ">=0.5, <150",
                "comment": "Weight of patient. Used to calculate fluid maintenance volume, fluid maintenance rate, fluid deficit volume, fluid deficit rate, fluid total rate. Value is checked against expected safe range based on patient age, and upper limit of 80Kg is used for calculations.",
            },
            "shock": {
                "value": calc.shock,
                "data type": "boolean",
                "optional": False,
                "units": "n/a",
                "accepted range": "True or False",
                "comment": "If the patient is clinically shocked at the time of starting DKA protocol (and would therefore be given rapid resuscitation boluses). Used to determine if slow 10mL/Kg bolus is subtracted from fluid deficit volume.",
            },
            "insulinDose": {
                "value": calc.insulinDose,
                "data type": "float",
                "optional": True,
                "units": "units per kilogram per hour",
                "accepted range": ">=0.05, <=0.1",
                "comment": "The desired starting rate of insulin. If not provided default value is 0.05",
            },
        },
        "Fluid": {
            "Maintenance Volume": {
                "value": round(calc.fluidMaintenanceVolume(), 1),
                "data type": "float",
                "units": "millilitres",
                "comment": "Volume of fluid maintenance required for this patient each 24 hours. Rounded to 1 decimal place.",
            },
            "Maintenance Rate": {
                "value": round(calc.fluidMaintenanceRate(), 1),
                "data type": "float",
                "units": "millilitres per hour",
                "comment": "Rate of fluid maintenance required for this patient each hour. Rounded to 1 decimal place.",
            },
            "Deficit Percentage": {
                "value": calc.fluidDeficitPercentage(),
                "data type": "integer",
                "units": "percent",
                "comment": "Percetage fluid deficit estimate based on pH (or bicarbonate if provided and more severe).",
            },
            "Deficit Volume": {
                "value": round(calc.fluidDeficitVolume(), 1),
                "data type": "float",
                "units": "millilitres",
                "comment": "Volume of fluid deficit estimate, less slow 10mL/kg bolus volume unless patient shocked. Rounded to 1 decimal place.",
            },
            "Deficit Rate": {
                "value": round(calc.fluidDeficitRate(), 1),
                "data type": "float",
                "units": "millilitres per hour",
                "comment": "Rate of fluid deficit correction required for this patient each hour to replace deficit volume over 48 hours. Rounded to 1 decimal place.",
            },
            "Total Rate": {
                "value": round(calc.fluidTotalRate(), 1),
                "data type": "float",
                "units": "millilitres per hour",
                "comment": "Rate of fluid required for this patient each hour, combining maintenance rate and deficit rate. Rounded to 1 decimal place.",
            },
        },
        "Insulin": {
            "Rate": {
                "value": round(calc.insulinRate(), 2),
                "data type": "float",
                "units": "units per hour",
                "comment": "Rate of insulin infusion required for this patient each hour. Providing standard infusion concentration of 1 unit in 1 millilitre is used, then infusion rate in millilitres per hour is the same value. Rounded to 2 decimal place. ",
            },
        },
    }