from typing import Literal

def derive_weight(age: float, sex=Literal['male', 'female']):
    # Returns weight against age and sex
    # This function is currently a placeholder which returns an estimated weight
    # based on the APLS calculation.
    # BSPED however uses a look up table which need to be implemented
    # Weight is capped at 75 kg
    weight =  (age + 4)*2

    if weight > 75:
        weight = 75

    return weight