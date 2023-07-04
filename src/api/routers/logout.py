from fastapi import APIRouter
from fastapi.param_functions import Depends
from fastapi.responses import Response
from starlette import status

from src.core.depends import AuthJWT, authorization
from src.schemas import ApplicationResponse, RouteReturn
from src.utils.cookies import unset_jwt_cookies

router = APIRouter()


@router.delete(
    path="/",
    dependencies=[Depends(authorization)],
    summary="WORKS (need X-CSRF-TOKEN in headers):logout (token removal).",
    response_model=ApplicationResponse[bool],
    status_code=status.HTTP_200_OK,
)
async def logout_user(
    response: Response,
    authorize: AuthJWT,
) -> RouteReturn:

    unset_jwt_cookies(response=response, authorize=authorize)

    return {
        "ok": True,
        "result": True,
    }
