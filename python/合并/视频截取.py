import os
from moviepy.editor import VideoFileClip

def split_video(video_path, output_path, segment_duration):
    # 创建输出文件夹
    os.makedirs(output_path, exist_ok=True)

    # 使用 VideoFileClip 加载视频文件
    video = VideoFileClip(video_path)

    # 提取原视频的文件名（不包括扩展名）
    video_filename = os.path.splitext(os.path.basename(video_path))[0]

    # 计算视频总时长（单位：秒）
    total_duration = video.duration

    # 计算每个分段的起始时间和结束时间
    start_times = [segment_duration * i for i in range(int(total_duration / segment_duration))]
    end_times = [start_time + segment_duration for start_time in start_times]
    end_times[-1] = min(end_times[-1], total_duration)  # 处理最后一个分段的结束时间

    # 分割视频并保存
    segment_count = 1
    for start_time, end_time in zip(start_times, end_times):
        output_filename = f'{video_filename}{segment_count}.mp4'
        output_path_segment = os.path.join(output_path, output_filename)
        segment = video.subclip(start_time, end_time)
        segment.write_videofile(output_path_segment, codec='libx264', audio_codec='aac')

        print(f'第 {segment_count} 个分割成功')
        segment_count += 1

    print(f'共 {segment_count - 1} 个小视频，已完成 {segment_count - 1} 个小视频')

    # 释放资源
    video.close()

# 示例用法
video_filename = '../../原视频/秘密.mp4'  # 输入视频文件名
output_foldername = 'output_segment'  # 输出分割后的小视频文件夹名

script_dir = os.path.dirname(os.path.abspath(__file__))
video_path = os.path.join(script_dir, video_filename)
output_path = os.path.join(script_dir, output_foldername)

segment_duration = 2 * 60  # 每段小视频的时长（单位：分钟）

split_video(video_path, output_path, segment_duration)
