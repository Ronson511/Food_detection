from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import FileResponse
import os

router = APIRouter()

from mylinebot.utils import ipath

@router.get("/{filename}")
def images(filename):
    try:
        src = os.path.join(ipath, filename)
        return FileResponse(src, media_type='image/jpeg')
    except IOError as ex:
        return str(ex)

