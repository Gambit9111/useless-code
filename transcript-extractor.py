from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter

def extract_transcript(youtube_url, file_number):
    # Extract the video ID from the URL
    video_id = youtube_url.split("watch?v=")[-1]

    # Fetch the transcript
    transcript = YouTubeTranscriptApi.get_transcript(video_id)

    # Format the transcript into plain text
    formatter = TextFormatter()
    text_transcript = formatter.format_transcript(transcript)

    # Remove newline characters to make the transcript in one line
    text_transcript = text_transcript.replace('\n', ' ')

    # Write the transcript to a text file
    file_name = f"youtube_transcripts/strategy_transcript{file_number}.txt"
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(text_transcript)

    print(f"Transcript for {youtube_url} saved as {file_name}")

# Read the YouTube links from the file
with open('youtube_links.txt', 'r') as file:
    youtube_links = file.readlines()

# Loop through the YouTube links and create transcripts
for index, link in enumerate(youtube_links):
    
    try:
        extract_transcript(link.strip(), index + 1)
    except Exception as e:
        print(f"Error: {e}")
        continue