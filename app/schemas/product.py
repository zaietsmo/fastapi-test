from typing import Optional

from pydantic import BaseModel, field_validator


class Product(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    calories: Optional[int] = None
    fats: Optional[float] = None
    carbs: Optional[float] = None
    proteins: Optional[float] = None
    unsaturated_fats: Optional[float] = None
    sugar: Optional[float] = None
    salt: Optional[float] = None
    portion: Optional[int] = None

    @field_validator("calories", mode="before")
    @classmethod
    def parse_calories(cls, v):
        if v is None or v == "N/A":
            return None
        try:
            return int(float(v))
        except (ValueError, TypeError):
            return None

    @field_validator(
        "fats", "carbs", "proteins", "unsaturated_fats", "sugar", "salt", mode="before"
    )
    @classmethod
    def parse_float_fields(cls, v):
        if v is None or v == "N/A":
            return None
        try:
            return float(v)
        except (ValueError, TypeError):
            return None

    @field_validator("portion", mode="before")
    @classmethod
    def parse_portion(cls, v):
        if v is None or v == "N/A":
            return None
        try:
            return int(v)
        except (ValueError, TypeError):
            return None
