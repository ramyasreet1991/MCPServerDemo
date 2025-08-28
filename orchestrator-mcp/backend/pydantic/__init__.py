class BaseModel:
    def __init__(self, **data):
        for k, v in data.items():
            setattr(self, k, v)

    def dict(self):
        return self.__dict__

    @classmethod
    def model_validate(cls, data):
        return cls(**data)


class BaseSettings(BaseModel):
    pass
