const fs = require('fs');
const {exec} = require('child_process');

// 视频文件路径
const filePath = './原视频/秘密.mp4';
// const filePath = './拼接/甲鱼不是鱼.mp4';
// 片头文件路径
const introFilePath = './拼接/0000.mp4';
// const introFilePath = './拼接/0.mp4';
// 片尾文件路径
const outroFilePath = './拼接/0000.mp4';
// const outroFilePath = './拼接/0.mp4';
// 分割时间间隔（以秒为单位）
// const segmentDuration = 60*10;
const segmentDuration = 120;

// 获取视频文件的总时长
function getVideoDuration(filePath) {
    return new Promise((resolve, reject) => {
        const command = `ffprobe -i "${filePath}" -show_entries format=duration -v quiet -of csv="p=0"`;

        exec(command, (error, stdout) => {
            if (error) {
                reject(error);
            } else {
                const duration = parseFloat(stdout.trim());
                resolve(duration);
            }
        });
    });
}

// 分割视频文件
function splitVideo(filePath, segmentDuration) {
    return new Promise((resolve, reject) => {
        const command = `ffmpeg -i "${filePath}" -c copy -map 0 -segment_time ${segmentDuration} -f segment "%d.mp4"`;
        exec(command, (error) => {
            if (error) {
                reject(error);
            } else {
                resolve();
            }
        });
    });
}

// 添加片头和片尾到视频文件
function addIntroAndOutro(filePath, introFilePath, outroFilePath) {
    return new Promise((resolve, reject) => {
        const tempFilePath = 'temp.mp4';
        // const command = `ffmpeg -i "${introFilePath}" -i "${filePath}" -i "${outroFilePath}" -filter_complex "[0:v:0][0:a:0][1:v:0][1:a:0][2:v:0][2:a:0]concat=n=3:v=1:a=1[outv][outa]" -map "[outv]" -map "[outa]" "${tempFilePath}"`;
        // const command = `ffmpeg -i "${introFilePath}" -i "${filePath}" -i "${outroFilePath}" -filter_complex "[0:v:0][0:a:0][1:v:0][1:a:0][2:v:0][2:a:0]concat=n=3:v=1:a=1[outv][outa]" -map "[outv]" -map "[outa]" "${tempFilePath}"`;
        const command = `ffmpeg -i "${introFilePath}" -i "${filePath}" -i "${outroFilePath}" -filter_complex "[0:v:0][0:a:0][1:v:0][1:a:0][2:v:0][2:a:0]concat=n=3:v=1:a=1[outv][outa]" -map "[outv]" -map "[outa]" "${tempFilePath}"`;
        console.log('command',command)
        exec(command, (error) => {
            if (error) {
                console.log('error',error)
                reject(error);
            } else {
                console.log('处理中')
                // 删除原始视频文件
                fs.unlinkSync(filePath);
                // 重命名临时文件为原始文件名
                fs.renameSync(tempFilePath, filePath);
                resolve();
            }
        });
    });
}

async function main() {
    try {
        const videoDuration = await getVideoDuration(filePath);
        const segmentCount = Math.ceil(videoDuration / segmentDuration);

        console.log('开始分割视频...');

        await splitVideo(filePath, segmentDuration);

        console.log('视频分割完成！');
        console.log('开始添加片头和片尾...');

        for (let i = 0; i < segmentCount; i++) {
            const segmentFilePath = `${i}.mp4`;
            console.log('segmentFilePath',segmentFilePath)
            console.log(`正在处理第 ${i + 1} 个分割视频文件...`);

            await addIntroAndOutro(segmentFilePath, introFilePath, outroFilePath);

            console.log(`第 ${i + 1} 个分割视频文件处理完成！`);
        }

        console.log('片头和片尾添加完成！');
        console.log('所有任务完成！');
    } catch (error) {
        console.error('出现错误：', error);
    }
}

main();
