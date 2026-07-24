from pydantic import BaseModel

class SceneRequest(BaseModel):

    scene: int | str

    image: str

    audio: str