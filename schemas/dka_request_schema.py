# standard imports
from datetime import date, datetime
from email import message
from typing import Optional, Literal, Union, List

# third party imports
from pydantic import BaseModel, Field, validator

class ChildStatusRequestParameters(BaseModel):
    """
    This class defines the schema for a python model which will be converted to by FastAPI to openAPI3 schema.
    All validation etc is defined here.
    All fields are essential, except the weight field - if not provided, 
    an estimated weight can be derived based on the sex and age rounded to the nearest year
    """
    birth_date: date = Field(
        ..., description="Date of birth of the patient, in the format YYYY-MM-DD")
    resuscitation_start_date_time: date = Field(
        ..., description="Date and time of start of resuscitation YYYY-MM-DD HH:MM:SS")
    sex: Literal['male', 'female'] = Field(
        ...,
        description="The sex of the patient, as a string value which can either be `male` or `female`. Abbreviations or alternatives are not accepted."
    )
    pH: float = Field(
        default=None,
        ge=6.0, 
        lt=8.0,
        description="The pH of the initial blood gas."
    )
    shocked: bool = Field(
        default=False,
        description="A boolean value to represent whether the child or young person is shocked at presentation."
    )
    insulin_infusion_rate: float = Field(
        default=0.05,
        message="The user requested insulin infusion rate. Usually Either 0.05 or 0.1 U/kg/hr but this is not constrained. A bespoke alternative value can be selected.",
    )
    weight: Optional[float] = Field(
        default=None,
        ge=0.5, 
        lt=220,
        description="The weight of the child in kg. Cannot be >220 kg."
    )