const { exec } = require('child_process');
const path = require('path');

// 视频文件路径
const videoPath = '/path/to/video.mp4';
// 片头视频文件路径
const introPath = '/path/to/intro.mp4';
// 片尾视频文件路径
const outroPath = '/path/to/outro.mp4';
// 输出目录
const outputDir = '/path/to/output';

// 执行视频分割的函数
function splitVideo(inputPath, introPath, outroPath, outputDir, segmentDuration) {
    // 创建临时目录用于保存分割后的视频段
    const tempDir = `${outputDir}/temp`;

    // 获取原始视频的文件名
    const videoName = path.basename(inputPath, path.extname(inputPath));

    // 定义FFmpeg命令：将片头与每个分割段合并，并使用原始视频名称作为输出文件名
    const mergeCommand = `ffmpeg -i ${introPath} -c copy -bsf:v h264_mp4toannexb -f mpegts ${tempDir}/intro.ts && ` +
        `ffmpeg -i ${inputPath} -c copy -bsf:v h264_mp4toannexb -f mpegts ${tempDir}/input.ts && ` +
        `ffmpeg -i ${outroPath} -c copy -bsf:v h264_mp4toannexb -f mpegts ${tempDir}/outro.ts && ` +
        `ffmpeg -i "concat:${tempDir}/intro.ts|${tempDir}/input.ts|${tempDir}/outro.ts" -c copy -bsf:a aac_adtstoasc "${outputDir}/${videoName}.mp4" && ` +
        `ffmpeg -i "${outputDir}/${videoName}.mp4" -c copy -f segment -segment_time ${segmentDuration} -reset_timestamps 1 -map 0 "${outputDir}/${videoName}%03d.mp4"`;

    // 执行FFmpeg命令
    exec(mergeCommand, (error, stdout, stderr) => {
        if (error) {
            console.error(`视频分割失败: ${error.message}`);
            return;
        }
        console.log('视频分割完成！');
    });
}

// 调用视频分割函数
splitVideo(videoPath, introPath, outroPath, outputDir, 120); // 每段2分钟，即120秒
