import subprocess
from pydub import AudioSegment
import os
from moviepy.editor import VideoFileClip, concatenate_videoclips, AudioFileClip
import shutil

def extract_audio(video_path, audio_path, fade_duration):
    cmd = ['ffmpeg', '-i', video_path, '-vn', '-c:a', 'libmp3lame', '-q:a', '2', '-af', f'afade=t=in:ss=0:d={fade_duration},afade=t=out:st={duration-fade_duration}:d={fade_duration}', audio_path]
    subprocess.call(cmd)

def get_video_duration(video_path):
    cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', video_path]
    output = subprocess.check_output(cmd).decode('utf-8').strip()
    duration = float(output)
    return duration

def merge_audios(audio_files, output_file):
    # 创建一个空白音频对象用于存储合并的音频
    merged_audio = AudioSegment.silent(duration=0)

    # 依次加载每个音频文件并进行合并
    for audio_file in audio_files:
        audio = AudioSegment.from_file(audio_file)
        merged_audio += audio

    # 保存合并后的音频文件
    merged_audio.export(output_file, format="mp3")
    print(f"已合并音频文件保存为 {output_file}")

    # 删除中间生成的音频文件
    for audio_file in audio_files:
        os.remove(audio_file)

    print("中间音频文件已删除。")

# 提取多个视频的音频并应用淡入淡出效果或生成空白音频
video_paths = ['video1.mp4', 'video2.mp4', 'video3.mp4']
fade_duration = 3  # 淡入淡出时长（秒）
audio_files = []

for i, video_path in enumerate(video_paths):
    audio_path = f'audio{i+1}.mp3'
    print("Processing video:", video_path)
    try:
        duration = get_video_duration(video_path)
        if duration > 0:
            extract_audio(video_path, audio_path, fade_duration)
            print("Audio extracted with fade effect successfully.")
        else:
            cmd = ['ffmpeg', '-f', 'lavfi', '-i', 'anullsrc=channel_layout=stereo:sample_rate=44100', '-t', str(duration), audio_path]
            subprocess.call(cmd)
            print("Blank audio generated successfully.")
        audio_files.append(audio_path)
    except Exception as e:
        print("Error extracting audio or generating blank audio:", str(e))

# 音频文件列表
audio_output_file = os.path.join(os.path.dirname(video_paths[1]), os.path.splitext(video_paths[1])[0] + ".mp3")

# 调用合并音频函数
merge_audios(audio_files, audio_output_file)



# 合并视频和音频
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
    video2_filename = os.path.splitext(video_files[1])[0]
    output_filename = f"{video2_filename}.mp4"

    # 最终视频文件保存路径
    output_folder = os.path.join(os.path.dirname(video_files[1]), "视频")
    os.makedirs(output_folder, exist_ok=True)
    output_path = os.path.join(output_folder, output_filename)

    # 保存合并后的视频文件
    merged_video.write_videofile(output_path, codec="libx264", audio_codec="aac")
    print(f"已合并视频文件保存为 {output_path}")

# 视频文件列表
video_files = ["video1.mp4", "video2.mp4", "video3.mp4"]

# 合并后的输出文件夹
output_folder = os.path.join(os.path.dirname(video_files[1]), "视频")
os.makedirs(output_folder, exist_ok=True)

# 调用合并视频和音频函数
merge_videos_and_audio(video_files, audio_output_file, output_folder)

print("中间音频文件已删除。")


# 移动音频文件到音频文件夹
audio_folder = os.path.join(os.path.dirname(video_paths[1]), "音频")
os.makedirs(audio_folder, exist_ok=True)
shutil.move(audio_output_file, os.path.join(audio_folder, os.path.basename(audio_output_file)))

print("中间音频文件已移动。")
