import requests

def transcribe_audio(file_path, beam_size=5):
    url = "http://192.168.157.67:31655/transcribe"
    params = {"beam_size": beam_size}
    with open(file_path, "rb") as file:
        files = {"file": (file_path, file, "audio/mpeg")}
        response = requests.post(url, params=params, files=files)

    if response.status_code == 200:
        result = response.json()
        print(f"Detected language: {result['language']} (probability: {result['language_probability']:.2f})")
        print(f"Used beam size: {result.get('beam_size_used', 'default')}")
        
        # 合并所有分段文本
        full_text = " ".join(segment["text"] for segment in result["transcription"])
        print("\n完整转录内容:")
        print(full_text)
    else:
        print(f"Error: {response.json().get('error', 'Unknown error')}")

if __name__ == "__main__":
    transcribe_audio("/root/sample-0.wav")
    transcribe_audio("/root/record2.m4a", beam_size=2)
