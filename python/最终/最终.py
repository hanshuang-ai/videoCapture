import subprocess
from pydub import AudioSegment
import os
from moviepy.editor import VideoFileClip, concatenate_videoclips, AudioFileClip
import shutil

def extract_audio(video_path, audio_path, fade_duration):
    duration = get_video_duration(video_path)
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
    merged_audio.export(os.path.join(temp_folder, output_file), format="mp3")
    print(f"已合并音频文件保存为 {os.path.join(temp_folder, output_file)}")

    # 删除中间生成的音频文件
    for audio_file in audio_files:
        os.remove(audio_file)

    print("中间音频文件已删除。")

# 视频文件的路径
video1_path = os.path.join("片头片尾", "片头.mp4")
video2_folder = "剪切后"
video3_path = os.path.join("片头片尾", "片尾.mp4")

# 设置淡入淡出时长（秒）
fade_duration = 3

# 临时文件目录
temp_folder = os.path.dirname(video1_path)

# 从视频1中提取音频
audio1_path = os.path.join(temp_folder, "audio1.mp3")
extract_audio(video1_path, audio1_path, fade_duration)
print("片头视频音频提取成功。")

# 从视频2中提取音频
video2_files = os.listdir(video2_folder)
audio2_files = []
for file in video2_files:
    video2_path = os.path.join(video2_folder, file)
    audio2_path = os.path.join(temp_folder, f"audio2_{os.path.splitext(file)[0]}.mp3")
    extract_audio(video2_path, audio2_path, fade_duration)
    print(f"剪切视频 {file} 的音频提取成功。")
    audio2_files.append(audio2_path)

# 从视频3中提取音频
audio3_path = os.path.join(temp_folder, "audio3.mp3")
extract_audio(video3_path, audio3_path, fade_duration)
print("片尾视频音频提取成功。")

# 合并音频文件
audio_files = [audio1_path] + audio2_files + [audio3_path]
audio_output_path = os.path.join(temp_folder, "merged_audio.mp3")
merge_audios(audio_files, "merged_audio.mp3")

# 合并视频和音频
output_folder = os.path.join(video2_folder, "视频")
os.makedirs(output_folder, exist_ok=True)
output_filename = os.path.splitext(video2_files[0])[0] + ".mp4"
output_path = os.path.join(output_folder, output_filename)

video_files = [video1_path] + [os.path.join(video2_folder, file) for file in video2_files] + [video3_path]

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
audio = AudioFileClip(audio_output_path)

# 将音频与视频进行合并
merged_video = merged_video.set_audio(audio)

# 保存合并后的视频文件
merged_video.write_videofile(output_path, codec="libx264", audio_codec="aac")
print(f"已合并视频文件保存为 {output_path}")

# 将音频文件移动到音频文件夹
# audio_folder = os.path.join(video2_folder, "音频")
# os.makedirs(audio_folder, exist_ok=True)
# shutil.move(audio_output_path, os.path.join(audio_folder, os.path.basename(audio_output_path)))
# print("中间音频文件已移动。")

# 将音频文件移动到音频文件夹并重命名为video2的名字
audio_folder = os.path.join(video2_folder, "音频")
os.makedirs(audio_folder, exist_ok=True)
audio_output_filename = os.path.splitext(video2_files[0])[0] + ".mp3"
audio_output_newpath = os.path.join(audio_folder, audio_output_filename)
shutil.move(audio_output_path, audio_output_newpath)
print(f"中间音频文件已移动到 {audio_output_newpath}")