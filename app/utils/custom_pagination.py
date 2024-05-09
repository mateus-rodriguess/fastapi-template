from fastapi_pagination import Page, Params
from fastapi_pagination.customization import CustomizedPage, UseParams


class PageParams(Params):
    # uuid: UUID = Query(None, description="uuid", alias="uuid")
    pass


PageParams = CustomizedPage[Page, UseParams(PageParams)]
