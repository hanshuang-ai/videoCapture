const { exec } = require('child_process');
const path = require('path');

// 视频文件路径
const videoPath = './原视频/秘密.mp4';
// 输出目录
const outputDir = './截取';

// 执行视频分割的函数
function splitVideo(inputPath, outputDir, segmentDuration) {
  // 提取原视频的文件名（不包括扩展名）
  const videoName = path.parse(inputPath).name;

  // 定义FFmpeg命令
  const outputPattern = path.join(outputDir, `${videoName}_%03d.mp4`);
  const ffmpegCommand = `ffmpeg -i ${inputPath} -c copy -f segment -segment_time ${segmentDuration} -reset_timestamps 1 -map 0 "${outputPattern}"`;

  // 创建新的Promise对象
  return new Promise((resolve, reject) => {
    // 执行FFmpeg命令
    const childProcess = exec(ffmpegCommand, (error, stdout, stderr) => {
      if (error) {
        reject(`视频分割失败: ${error.message}`);
        return;
      }
      resolve();
    });

    // 监听FFmpeg命令的标准输出流
    childProcess.stdout.on('data', (data) => {
      console.log(data); // 打印输出信息
    });

    // 监听FFmpeg命令的标准错误流
    childProcess.stderr.on('data', (data) => {
      console.error(data); // 打印错误信息
    });
  })
  .then(() => {
    console.log('成功分割一段视频！');
  });
}

// 调用视频分割函数
splitVideo(videoPath, outputDir, 120) // 每段2分钟，即120秒
  .then(() => {
    console.log('视频分割完成！');
  })
  .catch((error) => {
    console.error(error);
  });
