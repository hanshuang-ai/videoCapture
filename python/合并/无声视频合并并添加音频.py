import os
from moviepy.editor import VideoFileClip, concatenate_videoclips, AudioFileClip

def merge_videos_and_audio(video_files, audio_file, output_file):
    # 创建一个空白的视频片段列表
    video_clips = []

    # 依次加载每个视频文件并添加到视频片段列表
    for video_file in video_files:
        video = VideoFileClip(video_file)
        # 去除音频
        video = video.without_audio()
        video_clips.append(video)

    # 将视频片段列表合并为一个视频
    merged_video = concatenate_videoclips(video_clips)

    # 加载音频文件
    audio = AudioFileClip(audio_file)

    # 将音频与视频进行合并
    merged_video = merged_video.set_audio(audio)

    # 生成最终文件名
    output_filename = os.path.splitext(video_files[1])[0] + "_" + os.path.basename(output_file)

    # 保存合并后的视频文件
    merged_video.write_videofile(output_filename, codec="libx264", audio_codec="aac")
    print(f"已合并视频文件保存为 {output_filename}")

    # 删除第一段代码的中间产物
    for video_file in video_files:
        os.remove(video_file)

# 视频文件列表
video_files = ["video1.mp4", "video2.mp4", "video3.mp4"]

# 合并后的输出文件
output_file = "merged_video_audio.mp4"

# 音频文件路径
audio_file = "video2.mp3"

# 调用合并视频和音频函数
merge_videos_and_audio(video_files, audio_file, output_file)
