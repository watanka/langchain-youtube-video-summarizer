from pydantic import BaseModel, HttpUrl


class UserRequest(BaseModel) :
    url : str

    #TODO validate url as an youtube link.
