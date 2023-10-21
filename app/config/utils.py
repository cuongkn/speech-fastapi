import asyncio
import os
import re
import uuid
import aiofiles
from pathlib import Path
from tempfile import NamedTemporaryFile

from fastapi import HTTPException


class Config:
    BASE_DIR = Path(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    SAVE_AUDIO_DIR = "/audio_files"


config = Config()


async def save_file_to_local_directory(audio_file):
    file_uuid = uuid.uuid4()
    save_file_path = os.path.join(config.BASE_DIR, "audio_files")

    if not os.path.exists(save_file_path):
        os.makedirs(save_file_path)

    save_file_path = os.path.join(save_file_path, f"{file_uuid}.wav")

    async with aiofiles.open(save_file_path, "wb") as out_file:
        content = await audio_file.read()
        await out_file.write(content)
        await out_file.close()

    return save_file_path


async def save_file_to_temporary_directory(audio_file):
    with NamedTemporaryFile(delete=True, suffix=".wav") as temp_file:
        content = await audio_file.read()
        temp_file.write(content)
        temp_file.seek(0)

        temp_path = temp_file.name

    return temp_path


async def subprocess_with_sox(save_file_path):
    cmd = f'sox --i "{save_file_path}"'

    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()

    print(stderr)

    sample_rate, duration = None, None
    if stdout:
        response = stdout.decode()
        sample_rate_pattern = r"Sample Rate\s+:\s(\d+)"
        duration_pattern = r"Duration\s+:\s(\d+)"

        sample_rate_str = re.search(sample_rate_pattern, response)
        if sample_rate_str is None:
            raise HTTPException(
                status_code=500,
                detail="Not found Sample Rate when dissecting .WAV file",
            )
        sample_rate = sample_rate_str.group(1)
        duration_str = re.search(duration_pattern, response)
        if duration_str is None:
            raise HTTPException(
                status_code=500,
                detail="Not found Duration when dissecting .WAV file",
            )
        duration = duration_str.group(1)
    if stderr:
        raise HTTPException(
            status_code=500,
            detail="There has been an error when dissecting .WAV file",
        )
    
    return sample_rate, duration


