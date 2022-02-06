<p align="center">
    <img width="200px" src="https://github.com/rcpch/digital-growth-charts-documentation/raw/live/docs/_assets/_images/rcpch_logo.png"/>
    <p align="center">Designed and built by the RCPCH, by clinicians for clinicians.</p>
</p>
<p align="center">
    <p align="center">This project is part of the <a href="https://publicmoneypubliccode.org.uk/">Public Money Public Code</a> community</p>
</p>

# BSPED DKA Calculator API

An API (application programming interface) in python 3.10 to produce calculations for the resuscitation of children and young people <18y with diabetic ketoacidos, produced and validated by The Royal College of Paediatrics and Child Health ([RCPCH](https://rcpch.ac.uk/), and British Society of Paediatric Endocrinology and Diabetes).

## Setup

1. Create a virtual environment based on python 3.10 (pyenv is recommended)
2. ```pip install -r requirements.txt```
3. ```uvicorn main:app --reload --port:8000```

## Testing

1. Set up Postman for localhost on port 8000
2. Post a request using raw json in the body
```json
{
    "birth_date": "2015-04-12",
    "resuscitation_start_date_time": "2022-02-06",
    "sex": "female",
    "weight": 23,
    "pH": 6.86,
    "shocked": true,
    "insulin_infusion_rate": 0.05
}
```

## To Do

1. Wire up OpenAPI
2. Fix resuscitation start_date_time to be a time also
3. Validate calculations
4. Implement a database if needed server-side
5. anything else