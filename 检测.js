const { exec } = require('child_process');

function detectVideoFormat(filePath) {
    return new Promise((resolve, reject) => {
        const command = `ffprobe -v error -select_streams v:0 -show_entries stream=codec_name -of default=noprint_wrappers=1:nokey=1 ${filePath}`;

        exec(command, (error, stdout, stderr) => {
            if (error) {
                reject(error);
                return;
            }

            const format = stdout.trim();
            resolve(format);
        });
    });
}

// 示例用法
// const filePath = './拼接/0000.mp4';
const filePath = './拼接/0.mp4';
detectVideoFormat(filePath)
    .then(format => {
        console.log(`视频格式: ${format}`);
    })
    .catch(error => {
        console.error(`发生错误: ${error}`);
    });
