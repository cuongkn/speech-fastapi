from fastapi import UploadFile
from pydub import AudioSegment
from tempfile import NamedTemporaryFile

from app.config.utils import *
from app.models.audio import AudioMeta


async def process_audio_with_tool(audio_file: UploadFile, save_file_after_process: bool) -> AudioMeta:
    if save_file_after_process:
        save_file_path = await save_file_to_local_directory(audio_file)
        sample_rate, duration = await subprocess_with_sox(save_file_path)
    
    else:
        with NamedTemporaryFile(delete=True, suffix=".wav") as temp_file:
            content = await audio_file.read()
            temp_file.write(content)
            temp_file.seek(0)

            save_file_path = temp_file.name

            audio = AudioSegment.from_file(save_file_path)
            duration = len(audio) / 1000  
            sample_rate = audio.frame_rate

    return AudioMeta(sample_rate=sample_rate, duration=duration)


async def process_audio_with_bin(audio_file: UploadFile) -> AudioMeta:
    def parse_binary_wav(content):
        if len(content) < 44:
            raise ValueError("Invalid WAV file")
        
        riff_header = content[:4]
        if riff_header != b'RIFF':
            raise ValueError("Invalid WAV file")
        
        sample_rate = int.from_bytes(content[24:28], byteorder='little')
        content_size = int.from_bytes(content[40:44], byteorder='little') / 2 
        duration = content_size / sample_rate
        
        return sample_rate, duration
    
    content = await audio_file.read()

    sample_rate, duration = parse_binary_wav(content=content)

    return AudioMeta(sample_rate=sample_rate, duration=duration)
