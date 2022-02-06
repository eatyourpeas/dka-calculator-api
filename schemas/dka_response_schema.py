# standard imports
from datetime import date, datetime
from typing import Optional, Literal, Union, List

# third party imports
from pydantic import BaseModel, Field, validator

class DeficitPercentage(BaseModel):
    deficit_percentage_output: float
    deficit_percentage_working: str
    deficit_percentage_formula: str

class DeficitVolume(BaseModel):
    deficit_volume_output: float
    deficit_volume_working: str
    deficit_volume_formula: str
    deficit_volume_limit: str

class BolusVolume(BaseModel):
    bolus_volume_output: float
    bolus_volume_working: str
    bolus_volume_formula: str
    bolus_volume_limit: str

class DeficitVolumeLessBolusVolume(BaseModel):
    deficit_volume_less_bolus_volume_output: float
    deficit_volume_less_bolus_volume_working: str
    deficit_volume_less_bolus_volume_formula: str

class DeficitVolumeReplacementRate(BaseModel):
    deficit_volume_replacement_rate_output: float
    deficit_volume_replacement_rate_working: str
    deficit_volume_replacement_rate_formula: str

class DailyMaintenanceVolume(BaseModel):
    daily_maintenance_volume_output: float
    daily_maintenance_volume_working: str
    daily_maintenance_volume_formula: str
    daily_maintenance_volume_limit: str

class MaintenanceRate(BaseModel):
    maintenance_rate_output: float
    maintenance_rate_working: str
    maintenance_rate_formula: str

class StartingFluidRate(BaseModel):
    starting_fluid_rate_output: float
    starting_fluid_rate_working: str
    starting_fluid_rate_formula: str

class InsulinInfusionRate(BaseModel):
    insulin_infusion_rate_output: float
    insulin_infusion_rate_working: str
    insulin_infusion_rate_formula: str
    insulin_infusion_rate_limit: str

class DKACalculationResponse(BaseModel):
    deficit_percentage: DeficitPercentage
    deficit_volume: DeficitVolume
    bolus_volume: BolusVolume
    deficit_volume_less_bolus_volume: DeficitVolumeLessBolusVolume
    daily_maintenance_volume: DailyMaintenanceVolume
    maintenance_rate: MaintenanceRate
    starting_fluid_rate: StartingFluidRate
    insulin_infusion_rate: InsulinInfusionRate





