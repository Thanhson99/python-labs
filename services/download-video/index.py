from pytube import YouTube

def download_youtube_video(url, path_to_save):
    try:
        # Initialize YouTube object with the target video URL
        yt = YouTube(url)
        
        # Select the highest quality stream
        video_stream = yt.streams.get_highest_resolution()
        
        # Download video to the specified directory
        print(f"Downloading video: {yt.title}")
        video_stream.download(output_path=path_to_save)
        
        print("Video downloaded successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
video_url = "https://www.youtube.com/watch?v=AbI--MaIh-k"
save_path = "/Users/hopee/Downloads/python/download-video/"
download_youtube_video(video_url, save_path)
