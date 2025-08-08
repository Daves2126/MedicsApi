from pydantic import BaseModel, Field

class Doctor(BaseModel):
    name: str
    doctor_id: int = Field(alias='id')
    specialtyCode: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
