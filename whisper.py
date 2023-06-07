import openai
openai.api_key='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'
audio_file= open("Grabacion.m4a", "rb")
transcript = openai.Audio.transcribe("whisper-1", audio_file)
print(transcript)