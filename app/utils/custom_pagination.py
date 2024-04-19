from fastapi import Query
from fastapi_pagination import Page, Params
from fastapi_pagination.customization import CustomizedPage, UseParams


class PageParams(Params):
    # id: int = Query(None, default=1, description="id", alias="id")
    pass


PageParams = CustomizedPage[Page, UseParams(PageParams)]
