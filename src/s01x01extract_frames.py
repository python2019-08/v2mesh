#!/usr/bin/python3
import os
import subprocess
import shutil
from pathlib import Path



def extractVideoFrames(aDatRoot: Path):
    """
    从视频文件中提取帧。
    """
    # --- 配置 ---
    # 输入视频文件路径 (相对于项目根目录)
    # input_video_rel = "e01.mp4"   #"20260118-143016.mov"
    input_video_rel = "20260118-143016.mov"
    input_video = aDatRoot / input_video_rel

    # 输出关键帧的目录 (相对于项目根目录)
    # output_dir_rel = "frames_0"
    output_dir_rel = "frames"
    output_dir = aDatRoot / output_dir_rel
 

    # 检查输入视频是否存在
    if not input_video.is_file():
        print(f"错误：输入视频文件未找到于 {input_video}")
        exit(1)

    # 如果输出目录不存在，则创建它
    if not output_dir.is_dir():
        print(f"创建输出目录于 {output_dir_rel}")
        output_dir.mkdir(parents=True, exist_ok=True)

    # ----------------------------------------------
    # 构建 FFmpeg 命令
    # -i: 输入文件
    # -vf "select=eq(pict_type\,I)": 选择所有 I-frame (关键帧)
    # -vsync vfr: 使用可变帧率，防止重复帧
    # -q:v 2: 设置输出图像的质量 (2-5 是一个很好的范围，2是高质量)
    # -loglevel error: 只显示错误信息
    # command = [
    #     "ffmpeg",
    #     "-i", str(input_video),
    #     "-vf", "select=eq(pict_type\\,I)",
    #     "-vsync", "vfr",
    #     "-q:v", "2",
    #     "-loglevel", "error",
    #     f"{output_dir}/keyframe_%04d.jpg"
    # ]
    # ----------------------------------------------
    # 按固定间隔抽帧，比如 每 10 帧抽 1 张
    # mod(n\,10) → 每 10 帧取 1 张
    # ffmpeg -i video.mp4 -vf "select=not(mod(n\,10))" -q:v 2 frames/%04d.jpg
    # ----------------------------------------------
    # 
    # 按每秒多少张抽帧，比如 每秒 10 张
    # ffmpeg -i video.mp4 -r 10 frames/%04d.jpg
    command = [
        "ffmpeg",
        "-i", str(input_video), 
        "-r", "4", 
        f"{output_dir}/frame_%04d.jpg"
    ]

    # 执行 FFmpeg 命令
    print(f"正在从 {input_video_rel} 提取帧...")
    try:
        subprocess.run(command, check=True)
        print(f"关键帧提取完成。文件已保存至 {output_dir_rel}")
    except FileNotFoundError:
        print("错误: 'ffmpeg' 命令未找到。请确保 FFmpeg 已安装并位于您的系统 PATH 中。")
        exit(1)
    except subprocess.CalledProcessError as e:
        print(f"执行 FFmpeg 时出错: {e}")
        exit(1)

 
def extractFrames2(aDatRoot: Path):
    # 设置源目录和目标目录
    src_dir = aDatRoot / "frames_0"
    dst_dir = aDatRoot / "frames"
    dst_dir.mkdir(exist_ok=True)

    # 每隔 3 张取一帧 (1244 -> 约 415 张)
    all_images = sorted( list(  src_dir.glob("*.jpg")  ))
    subset = all_images[::2] 

    for img in subset:
        shutil.copy(img, dst_dir / img.name)

    print(f"抽稀完成：从 {len(all_images)} 张缩减至 {len(subset)} 张")

if __name__ == "__main__":
    # 获取项目根目录 (假定此脚本位于 code/ 目录下)
    # dat_root = Path(__file__).resolve().parent.parent
    dat_rootPathStr = "/home/abner/Documents/jobs/task/task-blender/task03ai0img0modeling/dat"
    ddd = dat_rootPathStr + "/ddd"
    print(ddd)

    # 调用函数 
    dat_root = Path(dat_rootPathStr).resolve()
    extractVideoFrames(dat_root)

    extractFrames2(dat_root)

    
