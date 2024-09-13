"""
Script to re-encode mp3 files from the nasty 440Hz to the benevolent 528Hz.
"""
import os
from typing import List
import librosa
import numpy as np
from pydub import AudioSegment


def convert_440hz_to_528hz_v2(input_file, output_file):
    # Load the MP3 file
    audio = AudioSegment.from_file(input_file, format="mp3")

    # Convert audio to raw data for processing with librosa
    audio_data = np.array(audio.get_array_of_samples(), dtype=np.float32)
    sample_rate = audio.frame_rate

    # Normalize audio data
    audio_data /= np.max(np.abs(audio_data))

    # Calculate the pitch shift factor (528/440)
    pitch_shift = np.log2(528 / 440) * 12

    # Pitch shift using librosa
    shifted_audio_data = librosa.effects.pitch_shift(audio_data, sr=sample_rate, n_steps=pitch_shift)

    # Convert back to the original format and scale to the original range
    shifted_audio_data *= 32767 / np.max(np.abs(shifted_audio_data))
    shifted_audio_data = shifted_audio_data.astype(np.int16)

    # Create a new AudioSegment with the shifted audio
    shifted_audio = AudioSegment(
        shifted_audio_data.tobytes(),
        frame_rate=sample_rate,
        sample_width=shifted_audio_data.dtype.itemsize,
        channels=audio.channels
    )

    # Export the shifted audio as a new MP3 file
    shifted_audio.export(output_file, format="mp3")

def process_directory_v2(input_directory, output_directory):
    # Ensure the output directory exists
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Loop through all files in the input directory
    for filename in os.listdir(input_directory):
        if filename.endswith(".mp3"):
            input_file = os.path.join(input_directory, filename)
            output_file = os.path.join(output_directory, f"528hz_{filename}")
            print(f"Processing {input_file} -> {output_file}")
            convert_440hz_to_528hz_v2(input_file, output_file)


def convert_440_to_528(audio_files: List, audio_data=None) -> None:
    """
    Convert the mp3 file from 440Hz to 528Hz.
    """
    try:
        print(f"[INFO] Files to process: {len(audio_files)}")
        for file in audio_files:
            print(f"[INFO] Processing file: {file}")
            audio = AudioSegment.from_file(file, format="mp3")
            sample_rate = audio.frame_rate

            # Normalize the audio data
            audio_data /= np.max(np.abs(audio_data))
            # Pitch shift the audio data
            pitch_sift = np.log2(528 / 440) * 12
            # Pitch shift using librosa
            shifted_audio_data = librosa.effects.pitch_shift(audio_data, sr=sample_rate, n_steps=pitch_sift)

            # Covert back to the original format and scale to the original range
            shifted_audio_data *= np.max(np.abs(shifted_audio_data))
            shifted_audio_data = shifted_audio_data.astype(np.int16)

            # Create a new AudioSegment object
            shifted_audio = AudioSegment(
                shifted_audio_data.tobytes(),
                frame_rate=sample_rate,
                sample_width=2,
                channels=1
            )
            shifted_audio.export(f"{file}_528Hz.mp3", format="mp3")
            print(f"[INFO] File {file} processed successfully!")

        print("Done!")
    except Exception as e:
        print(f"[ERROR] An error occurred: {e}")


def process_directory(input_dir, output_dir):
    """
    Process all the mp3 files in the input directory and save the converted files in the output directory.
    """
    try:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        filenames = os.listdir(input_dir)
        audio_files = [f for f in filenames if f.endswith(".mp3")]
        convert_440_to_528(audio_files)
    except Exception as e:
        print(f"[ERROR] An error occurred: {e}")


if __name__ == "__main__":
    input_directory = "/home/juliobriones/Music/country"
    sub_dir = input_directory.split("/")[-1]
    output_directory = f"/home/juliobriones/Music/528hz{sub_dir}"
    process_directory_v2(
        input_directory=input_directory,
        output_directory=output_directory
    )
