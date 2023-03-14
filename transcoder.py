import io
import os
import pathlib
import requests
import subprocess

from logging import info

AWS_LAMBDA_FUNCTION_NAME_ENV = 'AWS_LAMBDA_FUNCTION_NAME'
IN_AWS_LAMBDA = AWS_LAMBDA_FUNCTION_NAME_ENV in os.environ


def transcode_opus_ogg_to_wav(source_url: str) -> io.BytesIO:
    info('start')
    if IN_AWS_LAMBDA:
        response = requests.get(source_url)
        ogg_bytes_io = response.content
        opus_path = pathlib.Path('opus_linux', 'opusdec')
        result = subprocess.run([str(opus_path), 
                                '--force-wav', 
                                '-', 
                                '-'],
                                input=ogg_bytes_io,
                                stdout=subprocess.PIPE
                            )

    else:
        opus_path = pathlib.Path('opus_win', 'opusdec.exe')
        result = subprocess.run([str(opus_path), 
                                '--force-wav', 
                                source_url, 
                                '-'],
                                stdout=subprocess.PIPE
                            )
    voice_wav_bytes: bytes = result.stdout
    voice_wav_bytes_io = io.BytesIO(voice_wav_bytes)
    voice_wav_bytes_io.name = 'my_voice_message.wav'
    
    info('finish')    
    return voice_wav_bytes_io