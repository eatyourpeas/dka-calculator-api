"""
Fluids
"""
# Standard imports
import json
from pathlib import Path
from typing import List
from dka_calculator import dka_calculator

from dka_calculator.dka_calculator.fluid import holliday_segar_volume

# Third party imports
from schemas.dka_request_schema import ChildStatusRequestParameters
from schemas.dka_response_schema import DKACalculationResponse
from fastapi import APIRouter, Body, HTTPException

# local imports to do the calculations - in future this could be put into its own module and imported



# set up the API router
dka = APIRouter(
    prefix="/dka",
)

@dka.post("/calculation", tags=["dka"], response_model=DKACalculationResponse)
def dka_calculation_response(child_request_parameters: ChildStatusRequestParameters = Body(
            ...,
            example={
                "birth_date": "2015-04-12",
                "resuscitation_start_date_time": "2022-02-06",
                "sex": "female",
                "weight": 23,
                "pH": 6.86,
                "shocked": True,
                "insulin_infusion_rate": 0.05
            }
        )
):
    """
    This is the main calculation endpoint which receives all the fields from the web form
    and returns the calculated values and working.
    """
    print("hello")
    print(child_request_parameters)
    # calculate the age
    try:
        age = dka_calculator.age_to_nearest_year(
            birth_date=child_request_parameters.birth_date,
            observation_date=child_request_parameters.resuscitation_start_date_time
        )
    except:
        raise Exception('Unable to calculate age from dates provided')

    # if the weight is not provided, calculate one from the age and the sex
    if child_request_parameters.weight is None:
        if child_request_parameters.sex is not None:
            # derive weight from age and sex
            try:
                weight = dka_calculator.derive_weight(
                    age=age,
                    sex=child_request_parameters.sex
                )
            except Exception as error:
                raise error
        else:
            raise Exception("Weight cannot be derived without knowing the sex of the child or young person.")
    else:
        weight = child_request_parameters.weight

    # derive the deficit based on the pH
    
    try:
        child_deficit_percentage = dka_calculator.deficit_percentage(
            pH=child_request_parameters.pH
        )
    except Exception as error:
        raise error
    
    # derive the deficit volume from the percentage deficit
    try:
        child_deficit_volume = dka_calculator.deficit_volume(
            percentage_deficit=child_deficit_percentage,
            weight=weight
        )
    except Exception as error:
        raise error
    
    # calculate the bolus sizes based on weight
    try: 
        child_bolus_volume = dka_calculator.crystalloid_bolus(
            weight=weight,
            volume_per_kilogram=10
        )
    except Exception as error:
        raise error
    

    # subtract the bolus from the total deficit if shocked
    deficit_volume_less_bolus_volume = None
    if child_request_parameters.shocked:
        child_deficit_volume_less_bolus_volume = child_deficit_volume - child_bolus_volume
        deficit_volume_stem = {
            "deficit_volume_less_bolus_volume_output": child_deficit_volume_less_bolus_volume,
            "deficit_volume_less_bolus_volume_working": f"[{child_deficit_volume}ml]-[{child_bolus_volume}ml] = {child_deficit_volume_less_bolus_volume}ml",
            "deficit_volume_less_bolus_volume_formula": "[Deficit volume] - [10mL/kg bolus (only for non-shocked patients)]"
        }
    else:
        deficit_volume_stem = {
            "deficit_volume_less_bolus_volume_output": 0,
            "deficit_volume_less_bolus_volume_working": "No subtraction has been made for fluid boluses as the child or young person has not been reported as shocked.",
            "deficit_volume_less_bolus_volume_formula": "[Deficit volume] - [10mL/kg bolus (only for non-shocked patients)]"
        }
    
    # calculate the maintenance fluid volume
    daily_maintenance_volume = holliday_segar_volume(
        weight=weight
    )

    child_maintenance_strings = dka_calculator.holliday_segar_advice(weight=weight)
    
    # calculate the maintenance fluid hourly rate
    child_maintenance_rate = daily_maintenance_volume / 24
    
    # calculate the fluid deficit hourly rate
    if child_request_parameters.shocked:        
        deficit_replacement_rate = child_deficit_volume_less_bolus_volume / 48
    else:
        deficit_replacement_rate = child_deficit_volume / 48
    

    starting_fluid_rate = deficit_replacement_rate + child_maintenance_rate
    
    try:
        insulin_infusion_rate = dka_calculator.calculated_insulin_rate(
            weight=weight,
            insulin_per_kg=child_request_parameters.insulin_infusion_rate
        )
    except Exception as error:
        raise error

    return  {
        "deficit_percentage":{
            "deficit_percentage_output": child_deficit_percentage,
            "deficit_percentage_working": f"[pH {child_request_parameters.pH}] is in range {dka_calculator.pH_ranges(child_request_parameters.pH)} ==> {child_deficit_percentage}%",
            "deficit_percentage_formula": "pH range [7.2 to 7.4 = 5%] or [7.1 to 7.2 = 5%] or [6.5 to 7.1 = 10%]"
        },
        "deficit_volume":{
            "deficit_volume_output": child_deficit_volume,
            "deficit_volume_working": f"[{child_deficit_percentage}%] x [{weight}kg] x 10 = {child_deficit_volume}mL",
            "deficit_volume_formula": "[Deficit percentage] x [Patient weight (kg)] x 10",
            "deficit_volume_limit": "7500mL (for 10% deficit)" # @dan-leach can you check this is correct?
        },
        "bolus_volume":{
            "bolus_volume_output": child_bolus_volume,
            "bolus_volume_working": f"[10mL/kg] x [{weight}kg] = {child_bolus_volume}mL",
            "bolus_volume_formula": "[10mL/kg] x [Patient weight (kg)]",
            "bolus_volume_limit": "750mL" # @dan-leach can you check this is correct?
        },
        "deficit_volume_less_bolus_volume":deficit_volume_stem,
        "daily_maintenance_volume":{
            "daily_maintenance_volume_output": daily_maintenance_volume,
            "daily_maintenance_volume_working": child_maintenance_strings["advice"],
            "daily_maintenance_volume_formula": child_maintenance_strings["formula"],
            "daily_maintenance_volume_limit": "2600" # @dan-leach can you check this is correct?
        },
        "maintenance_rate":{
            "maintenance_rate_output": child_maintenance_rate,
            "maintenance_rate_working": "[Daily maintenance volume] ÷ [24 hours]",
            "maintenance_rate_formula": f"[{daily_maintenance_volume}mL] ÷ [24 hours] = {child_maintenance_rate}mL/hour"
        },
        "starting_fluid_rate":{
            "starting_fluid_rate_output": starting_fluid_rate,
            "starting_fluid_rate_working": f"[{deficit_replacement_rate}mL/hour] + [{child_maintenance_rate}mL/hour] = 112.9mL/hour",
            "starting_fluid_rate_formula": "[Deficit replacement rate] + [Maintenance rate]"
        },
        "insulin_infusion_rate":{
            "insulin_infusion_rate_output": insulin_infusion_rate,
            "insulin_infusion_rate_working": f"{insulin_infusion_rate} Units/hour (for {child_request_parameters.insulin_infusion_rate} Units/kg/hour)",
            "insulin_infusion_rate_formula": "[Insulin rate (Units/kg/hour)] x [Patient weight]",
            "insulin_infusion_rate_limit": "3.75 Units/hour (for 0.05 Units/kg/hour)" # @dan-leach can you check this is correct?
        }
    }