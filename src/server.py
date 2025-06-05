from fastapi import FastAPI, File, UploadFile, Query
from faster_whisper import WhisperModel
import os
import tempfile
import uvicorn

app = FastAPI()

# Load the model once at startup
model_size = os.getenv("WHISPER_MODEL_SIZE", "large-v3")
model_path = f"/opt/whisper/models/Systran-faster-whisper-{model_size}"
model = WhisperModel(model_path, device="cuda", compute_type="float16")

@app.post("/transcribe")
async def transcribe_audio(
        file: UploadFile = File(...),
        beam_size: int = Query(default=5, description="lower for quicker, higher for more accurate", ge=1, le=5)
):
    # Validate file type
    if not file.filename.endswith((".mp3", ".wav", ".m4a")):
        return {"error": "Unsupported file format. Use mp3, wav, or m4a."}

    # Create a temporary file to store the uploaded audio
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
        temp_file.write(await file.read())
        temp_file_path = temp_file.name

    try:
        # Transcribe the audio file with the provided beam_size
        segments, info = model.transcribe(temp_file_path, beam_size=beam_size)

        # Collect transcription results
        transcription = [
            {
                "start": segment.start,
                "end": segment.end,
                "text": segment.text
            } for segment in segments
        ]

        # Prepare response
        response = {
            "language": info.language,
            "language_probability": info.language_probability,
            "transcription": transcription,
            "beam_size_used": beam_size  # Include the beam size in the response
        }

        return response

    finally:
        # Clean up the temporary file
        os.unlink(temp_file_path)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)