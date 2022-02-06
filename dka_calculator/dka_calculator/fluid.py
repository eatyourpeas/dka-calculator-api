"""
This file contains the functions for calculating:
1. fluid deficit
2. fluid maintenance
3. fluid bolus
"""

# Boluses
def crystalloid_bolus(
    weight: float, 
    volume_per_kilogram: int
    )->float:

    """
    This returns a volume of crystalloid to administer per kg body weight.
    It can be used to calculate individual boluses or retrospectively to calculate total fluid given
    volumes/kg are expected as ml/kg
    weights are expected in kg
    """

    if weight is None:
        raise Exception("No weight supplied")
    if volume_per_kilogram is None:
        raise Exception("No volume/kg supplied")

    return weight * volume_per_kilogram

# Maintenance
def holliday_segar_volume(
    weight: float
    ):
    """
    This returns the maintenance rate for fluids based on weight.
    It uses the Holliday-Segar equation and returns a rate in ml/hr
    """

    if weight is None:
        raise Exception("No weight supplied")

    if weight > 75:
        # note that the upper limit for this equation is 75 kg
        weight = 75

    if weight > 20:
        return 1500 + ((weight-20) * 20)
    elif weight > 10:
        return 1000 + ((weight-10) * 50)
    else:
        return weight * 100

def holliday_segar_rate(
    weight: float
    )-> float:
    """
    This returns the maintenance rate for fluids based on weight.
    It uses the Holliday-Segar equation and returns a rate in ml/hr
    """
    
    total_volume = holliday_segar_volume(weight)
    return total_volume/24

def holliday_segar_advice(
        weight: float
    ):
    """
    This returns values for the advice strings
    """
    if weight is None:
        raise Exception("No weight supplied")

    formula = "[100mL/kg for 0-10kg] + [50mL/kg for 10-20kg] + [20mL/kg for >20kg]"

    if weight > 75:
        # note that the upper limit for this equation is 75 kg
        weight = 75
        advice = "Weight has been capped at 75kg."
        formula = "Weight is capped at 75kg."
    if weight > 20:
        volume = 1500 + ((weight-20) * 20)
        advice = f"(([{weight}kg] - 20kg) x 20mL) + 1500mL = {volume}mL"
    elif weight > 10:
        volume = 1000 + ((weight-10) * 50)
        advice = f"(([{weight}kg] - 10kg) x 50mL) + 1000mL = {volume}mL"
    else:
        volume = weight * 100
        advice = f"([{weight}kg] x 100mL) = {volume}mL"
    return {
        "volume": volume,
        "advice": advice,
        "formula": formula
    }

# deficit
def deficit_percentage(pH: float)->float:
    """
    Return percentage deficit based on pH
    """

    if pH is None:
        raise Exception("No volume/kg supplied")
    if pH <= 6.5:
        raise Exception(f"A pH of {pH} is very low. Please check accuracy.")
    
    if pH < 7.1:
        percentage_deficit = 10
    elif pH < 7.2:
        percentage_deficit = 5
    else:
        percentage_deficit = 0
    
    return percentage_deficit

def pH_ranges(pH: float)->str:
    if pH<=7.1:
        return "less than 7.1"
    elif pH <= 7.2:
        return "7.1 to 7.2"
    elif pH <=7.4:
        return "7.2 to 7.4"
    else:
        return ">7.4"

def deficit_volume(percentage_deficit: float, weight: float):
    """
    Return volume deficit based on and weight (kg)
    """
    if weight is None or weight < 0:
        raise Exception("No valid weight supplied")
    if percentage_deficit is None or percentage_deficit < 0:
        raise Exception("No valid percentage deficit value supplied")
    return percentage_deficit * weight * 10

def forty_eight_hour_total_fluid_replacement(
    bolus_total: float,
    deficit: float,
    maintenance_volume: float,
    shocked: bool = False
    ):
    """
    Returns total 48 hour volume of recommended fluid replacement in ml
    """

    total_fluids_over_forty_eight_hours = (maintenance_volume * 2) + deficit

    if shocked:
        total_fluids_over_forty_eight_hours -= bolus_total
    
    return total_fluids_over_forty_eight_hours    