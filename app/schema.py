import pydantic


class CreateAds(pydantic.BaseModel):
    title: str
    description: str
    owner_id: int


class UpdateAds(pydantic.BaseModel):
    title: str
    description: str
    
           
