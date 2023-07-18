import subprocess

def extract_audio(video_path, audio_path, fade_duration):
    cmd = ['ffmpeg', '-i', video_path, '-vn', '-c:a', 'libmp3lame', '-q:a', '2', '-af', f'afade=t=in:ss=0:d={fade_duration},afade=t=out:st={duration-fade_duration}:d={fade_duration}', audio_path]
    subprocess.call(cmd)

def get_video_duration(video_path):
    cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', video_path]
    output = subprocess.check_output(cmd).decode('utf-8').strip()
    duration = float(output)
    return duration

# 提取多个视频的音频并应用淡入淡出效果或生成空白音频
video_paths = ['video1.mp4', 'video2.mp4', 'video3.mp4']
fade_duration = 3  # 淡入淡出时长（秒）

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
    except Exception as e:
        print("Error extracting audio or generating blank audio:", str(e))
