const ffmpeg = require('fluent-ffmpeg');

/// 指定视频文件路径
const videoPath = './截取/秘密_000.mp4';

// 指定片头和片尾文件路径
const introPath = './甲鱼不是鱼.mp4';
const outroPath = './甲鱼不是鱼.mp4';

// 指定输出文件路径
const outputPath = './111.mp4';

// 创建 ffmpeg 命令对象
const command = ffmpeg();

// 添加片头
command.input(introPath);

// 添加视频
command.input(videoPath);

// 添加片尾
command.input(outroPath);

// 使用复杂滤镜将片头、视频和片尾连接起来
command.complexFilter([
    '[0:v] [0:a] [1:v] [1:a] [2:v] [2:a] concat=n=3:v=1:a=1 [v] [a]',
], ['v', 'a']);

// 指定输出编码和设置
command.output(outputPath)
    .videoCodec('mpeg4')
    .audioCodec('aac')
    .outputOptions(['-movflags +faststart'])
    .on('end', () => {
        console.log('Video processing completed successfully.');
    })
    .on('error', (err) => {
        console.error('Error:', err);
    })
    .run();
