import os
import openai
from pydub import AudioSegment

def check_api_key():
    if not os.environ["OPENAI_API_KEY"]:
        raise Exception("OPENAI_API_KEY not found in environment variables")
    if not openai.api_key:
        openai.api_key = os.environ["OPENAI_API_KEY"]

def convert_audio_to_text(audio_file_path):
    check_api_key() # this should not be necessary, but somehow it is
    print("OPENAI_API_KEY", os.environ["OPENAI_API_KEY"]) 
    input_file =  extract_audio(audio_file_path)
    file_root, file_ext = os.path.splitext(input_file)

    output_dir = os.path.join(file_root + 'output_chunks')
    chunk_size = 25  # 25 MB
    transcript_output_file = os.path.join(file_root + '_transcript.txt')
    transcripts = split_audio(input_file, output_dir, chunk_size)

    return "\n".join(transcripts)

    # save_transcripts(transcripts, transcript_output_file)

def extract_audio(file):
    output_file = file.split('.')[0] + '.wav' # change file extension to .wav
    os.system(f"ffmpeg -i {file} -vn -acodec pcm_s16le -ar 44100 -ac 2 {output_file}")
    return output_file

def process_audio_chunk(chunk_path):
    with open(chunk_path, "rb") as audio_file:
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
    return transcript['text']

def split_audio(input_file, output_dir, chunk_size_mb):
    audio = AudioSegment.from_wav(input_file)
    
    bytes_per_second = audio.frame_width * audio.frame_rate
    chunk_duration_ms = (chunk_size_mb * 1000 * 1000) // bytes_per_second * 1000

    total_duration_ms = len(audio)
    num_chunks = total_duration_ms // chunk_duration_ms + 1

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    transcripts = []

    for i in range(num_chunks):
        start_time = i * chunk_duration_ms
        end_time = min((i + 1) * chunk_duration_ms, total_duration_ms)
        chunk = audio[start_time:end_time]
        chunk_path = os.path.join(output_dir, f"chunk_{i}.mp3")
        chunk.export(chunk_path, format="mp3")

        transcript = process_audio_chunk(chunk_path)
        print(transcript)
        transcripts.append(transcript)

    return transcripts

def save_transcripts(transcripts, output_file):
    with open(output_file, "w") as f:
        for transcript in transcripts:
            f.write(transcript + "\n")
