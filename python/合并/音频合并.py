from pydub import AudioSegment

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

# 音频文件列表
audio_files = ["video1.mp3", "video2.mp3", "video3.mp3"]

# 合并后的输出文件
output_file = "merged_audio.mp3"

# 调用合并音频函数
merge_audios(audio_files, output_file)
