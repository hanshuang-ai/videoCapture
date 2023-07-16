const { exec } = require('child_process');
const path = require('path');
const fs = require('fs');

// 视频文件路径
const videoPath = './原视频/秘密.mp4';
// 片头视频文件路径
const introPath = './甲鱼不是鱼.mp4';
// 片尾视频文件路径
const outroPath = './甲鱼不是鱼.mp4';
// 输出目录
const outputDir = './截取';

// 执行视频分割的函数
function splitVideo(inputPath, outputDir, segmentDuration) {
    // 获取原视频的文件名和扩展名
    const videoName = path.basename(inputPath, path.extname(inputPath));

    console.log('输入视频路径:', inputPath);
    console.log('输出目录:', outputDir);

    // 定义视频分割的FFmpeg命令
    const segmentCommand = `ffmpeg -i ${inputPath} -c copy -f segment -segment_time ${segmentDuration} -reset_timestamps 1 -map 0 -segment_list "${outputDir}/${videoName}.m3u8" -segment_list_type m3u8 -segment_list_entry_prefix "${videoName}_" "${outputDir}/${videoName}_%03d.mp4"`;

    // 执行视频分割的命令
    const segmentProcess = exec(segmentCommand);
    segmentProcess.stdout.on('data', (data) => {
        console.log(`视频分割进度: ${data}`);
    });
    segmentProcess.stderr.on('data', (data) => {
        console.error(`视频分割错误: ${data}`);
    });
    segmentProcess.on('close', (code) => {
        if (code === 0) {
            console.log('视频分割完成！');
            // 获取分割后的视频段文件列表
            const segmentFiles = getSegmentFiles(outputDir, videoName);
            if (segmentFiles.length === 0) {
                console.error('未找到分割后的视频段文件！');
                return;
            }

            // 执行拼接视频的函数
            concatVideos(introPath, outroPath, outputDir, segmentFiles, videoName);
        } else {
            console.error(`视频分割失败，退出码: ${code}`);
        }
    });
}

// 获取分割后的视频段文件列表
function getSegmentFiles(outputDir, videoName) {
    const segmentFiles = fs.readdirSync(outputDir).filter((file) => {
        return file.startsWith(`${videoName}_`);
    });

    return segmentFiles.map((file) => path.join(outputDir, file));
}

// 执行视频拼接的函数
function concatVideos(introPath, outroPath, outputDir, segmentFiles, videoName) {
    console.log('开始拼接视频...');
    console.log('片头视频路径:', introPath);
    console.log('片尾视频路径:', outroPath);

    // 创建拼接列表文件
    const concatFilePath = path.join(outputDir, `${videoName}_concat.txt`);
    const concatContent = segmentFiles.map((file) => {
        return `file '${file.replace(outputDir + '/', '')}'`;
    }).join('\n');
    fs.writeFileSync(concatFilePath, concatContent, 'utf8');

    // 定义视频拼接的FFmpeg命令
    const concatCommand = `ffmpeg -f concat -safe 0 -i "${concatFilePath}" -c copy -fflags +genpts "${path.join(outputDir, `${videoName}_concat.mp4`)}"`;

    // 执行视频拼接的命令
    const concatProcess = exec(concatCommand);
    concatProcess.stdout.on('data', (data) => {
        console.log(`视频拼接进度: ${data}`);
    });
    concatProcess.stderr.on('data', (data) => {
        console.error(`视频拼接错误: ${data}`);
    });
    concatProcess.on('close', (code) => {
        if (code === 0) {
            console.log('视频拼接完成！');
        } else {
            console.error(`视频拼接失败，退出码: ${code}`);
        }
    });
}

// 调用视频分割函数
splitVideo(videoPath, outputDir, 120); // 每段2分钟，即120秒
