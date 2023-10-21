from fastapi import APIRouter, Query, Response, UploadFile, Depends

from app.services.audio import *

router = APIRouter()


def param_dependency(mode: int, 
                     save_file_after_process: bool = Query(None)):
    if mode == 1 and save_file_after_process is None:
        raise ValueError("'save_file_after_process' is required when 'mode' is 1.")
    return mode, save_file_after_process

@router.post("/upload")
async def upload_file(audio_file: UploadFile, mode_save_file_after_process: tuple = Depends(param_dependency)) -> Response:
    mode, save_file_after_process = mode_save_file_after_process
    if mode == 1:
        response = await process_audio_with_tool(audio_file, save_file_after_process)
    elif mode == 2:
        response = await process_audio_with_bin(audio_file)
    else:
        raise ValueError("Invalid mode. Only 1 or 2 is available.")
    return response
