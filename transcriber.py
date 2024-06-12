import pandas as pd
import assemblyai as aai
from datetime import timedelta

# Set your AssemblyAI API key
aai.settings.api_key = "b356af60b44c483987c0061448812214"

# Define the audio file path and transcription configuration
audio_url = "/Users/amaris/Desktop/transcriber/speech-to-text-assembly/christmas.mp3"
config = aai.TranscriptionConfig(
  speaker_labels=True,
  speakers_expected=2
)

# Transcribe the audio file
transcript = aai.Transcriber().transcribe(audio_url, config)

# Create a list of dictionaries from the transcript
transcript_data = [{
    "Speaker": utterance.speaker,
    "Text": utterance.text,
    "Start": utterance.start,
    "End": utterance.end
} for utterance in transcript.utterances]
print(transcript_data)

# Generate the time intervals
# Set the variables needed for the intervals
time_intervals = []
start_time = timedelta(seconds=0)
end_time = timedelta(minutes=15)
increment = timedelta(seconds=5)

# Sreate the intervalz
current_time = start_time
while current_time < end_time:
    next_time = current_time + increment
    interval = f"{current_time.seconds//60}:{str(current_time.seconds%60).zfill(2)}-" \
               f"{next_time.seconds//60}:{str(next_time.seconds%60).zfill(2)}"
    time_intervals.append(interval)
    current_time = next_time

# Create a new list for DataFrame including the intervals and corresponding speech
formatted_transcript = []

for interval in time_intervals:
    start_seconds = int(interval.split('-')[0].split(':')[0]) * 60 + int(interval.split('-')[0].split(':')[1])
    print(interval, interval.split('-')[0], int(interval.split('-')[0].split(':')[0]) * 60 + int(interval.split('-')[0].split(':')[1]))
    end_seconds = int(interval.split('-')[1].split(':')[0]) * 60 + int(interval.split('-')[1].split(':')[1])

    # Find all utterances within the current time interval
    utterances_in_interval = [
    {
        "Time": interval,
        "Speech": f"({entry['Start'] // 1000 // 60}:{str(entry['Start'] // 1000 % 60).zfill(2)}) {entry['Speaker']}: {entry['Text']}"
    }
    for entry in transcript_data if entry['Start'] / 1000 >= start_seconds and entry['End'] / 1000 < end_seconds
]

    formatted_transcript.extend(utterances_in_interval)

    # formatted_transcript.append({
    #     "Time": interval,
    #     "Speech": "\n".join(utterances_in_interval)
    # })

# Convert the list of dictionaries to a DataFrame
df = pd.DataFrame(formatted_transcript)

# Save the DataFrame to an Excel file
output_file = "transcript.xlsx"
df.to_excel(output_file, index=False)

print(f"Transcript saved to {output_file}")
