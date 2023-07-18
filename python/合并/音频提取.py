from moviepy.editor import VideoFileClip, AudioFileClip
import os

def extract_audio(video_path):
    # 检查视频文件是否存在
    if not os.path.exists(video_path):
        print(f"视频文件 {video_path} 不存在")
        return

    video = VideoFileClip(video_path)

    # 检查视频是否有音频
    if video.audio is None:
        # 创建与视频等长的空白音频
        audio = AudioFileClip(duration=video.duration)
        # 保存空白音频
        audio_path = os.path.splitext(video_path)[0] + ".mp3"
        audio.write_audiofile(audio_path)
        print(f"已生成空白音频文件 {audio_path}")
    else:
        # 提取视频的音频
        audio = video.audio
        # 保存音频文件
        audio_path = os.path.splitext(video_path)[0] + ".mp3"
        audio.write_audiofile(audio_path)
        print(f"已提取音频文件 {audio_path}")

    # 关闭视频和音频对象
    video.close()
    audio.close()

# 视频文件列表
video_files = ["video1.mp4", "video2.mp4", "video3.mp4"]

for video_file in video_files:
    extract_audio(video_file)
