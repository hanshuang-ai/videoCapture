const { exec } = require('child_process');

// 视频文件路径
const videoPath = './秘密.mp4';
// 输出目录
const outputDir = './截取';

// 执行视频分割的函数
function splitVideo(inputPath, outputDir, segmentDuration) {
    // 定义FFmpeg命令
    const ffmpegCommand = `ffmpeg -i ${inputPath} -c copy -f segment -segment_time ${segmentDuration} -reset_timestamps 1 -map 0 "${outputDir}/output%03d.mp4"`;

    // 执行FFmpeg命令
    exec(ffmpegCommand, (error, stdout, stderr) => {
        if (error) {
            console.error(`视频分割失败: ${error.message}`);
            return;
        }
        console.log('视频分割完成！');
    });
}

// 调用视频分割函数
splitVideo(videoPath, outputDir, 120); // 每段2分钟，即120秒
