from typing import Optional
from pydantic import BaseModel, Field


class Calculator(BaseModel):
    age: float = Field(ge=0, lt=19)
    pH: float = Field(ge=6.2, lt=7.5)
    bicarbonate: Optional[float] = Field(ge=0, lt=35)
    weight: float = Field(ge=0.5, lt=150)
    shock: bool
    insulinDose: Optional[float] = Field(default=0.05, ge=0.05, le=0.1)

    def fluidMaintenanceVolume(self):
        if self.weight < 10:
            x = self.weight*100
        elif self.weight <20:
            x = ((self.weight-10)*50)+1000
        else:
            x = ((self.weight-20)*20)+1500
        return x
    
    def fluidMaintenanceRate(self):
        return self.fluidMaintenanceVolume() / 24
    
    def fluidDeficitPercentage(self):
        if self.pH >= 7.2:
            x = 5
        elif self.pH >= 7.1:
            x = 7
        else:
            x = 10
        return x

    def fluidDeficitVolume(self):
        x = self.fluidDeficitPercentage() * self.weight * 10
        if not self.shock:
            x = x - (self.weight * 10)
        return x
    
    def fluidDeficitRate(self):
        return self.fluidDeficitVolume() / 48

    def fluidTotalRate(self):
        return self.fluidMaintenanceRate() + self.fluidDeficitRate()

    def insulinRate(self):
        return self.insulinDose * self.weight
