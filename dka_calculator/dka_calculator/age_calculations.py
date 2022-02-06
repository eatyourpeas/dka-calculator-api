from datetime import date, datetime
from datetime import timedelta

def age_to_nearest_year(birth_date: date, observation_date: datetime) -> float:

    """
    Calculates a decimal age from two dates supplied as raw dates without times.
    Returns value floating point
    :param birth_date: date of birth
    :param observation_date: date observation made
    """

    days_between = observation_date - birth_date
    chronological_decimal_age = days_between.days / 365.25
    return round(chronological_decimal_age)