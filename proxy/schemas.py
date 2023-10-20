from pydantic import BaseModel, HttpUrl


class SummaryRequest(BaseModel) :
    url : str

    #TODO validate url as an youtube link.
