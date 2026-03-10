from pytube import YouTube

def download_youtube_video(url, path_to_save):
    try:
        # Khởi tạo đối tượng YouTube với URL của video
        yt = YouTube(url)
        
        # Chọn stream với chất lượng cao nhất
        video_stream = yt.streams.get_highest_resolution()
        
        # Tải video về đường dẫn đã chỉ định
        print(f"Đang tải video: {yt.title}")
        video_stream.download(output_path=path_to_save)
        
        print("Tải video thành công!")
    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")

# Ví dụ sử dụng
video_url = "https://www.youtube.com/watch?v=AbI--MaIh-k"
save_path = "/Users/hopee/Downloads/python/download-video/"
download_youtube_video(video_url, save_path)
