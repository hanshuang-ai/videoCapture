const { exec } = require('child_process');

// 指定视频文件路径
const videoPath = './截取/秘密_000.mp4';

// 指定片头和片尾文件路径
const introPath = './甲鱼不是鱼.mp4';
const outroPath = './甲鱼不是鱼.mp4';

// 指定输出文件路径
const outputPath = './111.mp4';

// 生成ffmpeg命令
const command = `ffmpeg -i "${introPath}" -i "${videoPath}" -i "${outroPath}" -filter_complex \
"[0:v] [0:a] [1:v] [1:a] [2:v] [2:a] concat=n=3:v=1:a=1 [v] [a]" \
-map "[v]" -map "[a]" -c:v libx264 -c:a aac -movflags +faststart "${outputPath}"`;

// 执行ffmpeg命令
exec(command, (error, stdout, stderr) => {
    if (error) {
        console.error('Error:', error);
        return;
    }
    console.log('Video processing completed successfully.');
});
