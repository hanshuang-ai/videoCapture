const { exec } = require('child_process');
const path = require('path');

// 视频文件路径
const videoPath = './原视频/秘密.mp4';
// 输出目录
const outputDir = './截取';

// 执行视频分割的函数
function splitVideo(inputPath, outputDir, segmentDuration) {
    // 获取原视频的文件名和扩展名
    const videoName = path.basename(inputPath, path.extname(inputPath));

    // 定义FFmpeg命令，使用原视频文件名作为输出文件名
    const ffmpegCommand = `ffmpeg -i ${inputPath} -c copy -f segment -segment_time ${segmentDuration} -reset_timestamps 1 -map 0 "${outputDir}/${videoName}%03d.mp4"`;

    // 执行FFmpeg命令
    const ffmpegProcess = exec(ffmpegCommand);

    ffmpegProcess.stderr.on('data', (data) => {
        const output = data.toString();
        // 提取进度信息
        const regex = /time=(\d+:\d+:\d+)/;
        const matches = output.match(regex);
        if (matches && matches[1]) {
            const currentTime = matches[1];
            console.log(`当前处理进度：${currentTime}`);
        }
    });

    ffmpegProcess.on('close', (code) => {
        if (code === 0) {
            console.log('视频分割完成！');
        } else {
            console.error(`视频分割失败，退出码：${code}`);
        }
    });
}

// 调用视频分割函数
splitVideo(videoPath, outputDir, 120); // 每段2分钟，即120秒
