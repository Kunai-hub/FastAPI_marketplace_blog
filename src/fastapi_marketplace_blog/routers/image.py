from fastapi import APIRouter, Query, HTTPException, status
import uuid


from src.fastapi_marketplace_blog.services.s3 import generate_presigned_url

image_router = APIRouter(prefix="/image", tags=["image"])


@image_router.get("/presigned")
async def get_presigned_url(filename: str = Query(...)):
    key = f"posts/{uuid.uuid4().hex}_{filename}"
    try:
        url = generate_presigned_url(key=key)

        return {"upload_url": url, "object_key": key, "file_url": f"{key}"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
