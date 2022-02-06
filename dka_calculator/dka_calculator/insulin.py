def calculated_insulin_rate(weight: float, insulin_per_kg: float):
    """
    Returns the actual ml/hr of insulin, based on 50 U of actrapid made up with 50 U dextrose 10%
    Note has very limited error handling - no safety built in
    """

    if weight is None:
        raise Exception("No weight supplied")
    if insulin_per_kg is None:
        raise Exception("No u/kg/hr supplied")

    
    return insulin_per_kg * weight