from moviepy.editor import VideoFileClip, concatenate_videoclips

def merge_videos(video_files, output_file):
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

    # 保存合并后的视频文件
    merged_video.write_videofile(output_file, codec="libx264")
    print(f"已合并视频文件保存为 {output_file}")

# 视频文件列表
video_files = ["video1.mp4", "video2.mp4", "video3.mp4"]

# 合并后的输出文件
output_file = "merged_video.mp4"

# 调用合并视频函数
merge_videos(video_files, output_file)
