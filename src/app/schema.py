from pydantic import BaseModel
from typing import List

class FeatureVector(BaseModel):
    features: List[float]
    label: float