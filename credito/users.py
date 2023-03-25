from fastapi import APIRouter, HTTPException, Header
from credito.auth_jwt import check_jwt
from credito.models import UserData

from credito.types import UserInfoData


user_routes = APIRouter()


@user_routes.put("/info")
async def update_user_info(user_info: UserInfoData, authentication: str = Header(...)):
    try:
        token = await check_jwt(authentication)
        user_data = await UserData.from_jwt(token)
        await user_data.update_registration(user_info)
        return {
            "status": "success",
        }
    except ValueError as v:
        raise HTTPException(status_code=404, detail=str(v))
    except HTTPException as h:
        raise h
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@user_routes.get("/info", tags=["user"])
async def get_user_info(authentication: str = Header(...)):
    """Get Information about the currently logged in User"""
    try:
        token = await check_jwt(authentication)
        return await UserData.from_jwt(token)
    except ValueError as v:
        raise HTTPException(status_code=404, detail=str(v))
