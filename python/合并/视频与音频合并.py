from moviepy.editor import VideoFileClip, AudioFileClip

def merge_video_audio(video_file, audio_file, output_file):
    # 加载视频和音频文件
    video = VideoFileClip(video_file)
    audio = AudioFileClip(audio_file)

    # 将音频与视频进行合并
    video = video.set_audio(audio)

    # 保存合并后的视频文件
    video.write_videofile(output_file, codec="libx264", audio_codec="aac")
    print(f"已合并视频文件保存为 {output_file}")

# 视频文件路径
video_file = "merged_video.mp4"

# 音频文件路径
audio_file = "merged_audio.mp3"

# 合并后的输出文件
output_file = "merged_video_audio.mp4"

# 调用合并视频和音频函数
merge_video_audio(video_file, audio_file, output_file)
