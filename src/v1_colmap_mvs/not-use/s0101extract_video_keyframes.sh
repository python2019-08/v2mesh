#!/bin/bash
set -e

# --- 配置 ---
# 输入视频文件路径
INPUT_VIDEO="dat/2026-01-18 143016.mov"
# 输出关键帧的目录
OUTPUT_DIR="dat/keyframes"


# --- 脚本主体 ---
# 获取项目根目录 (假定此脚本位于 code/ 目录下)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_ROOT="$SCRIPT_DIR/.."

# 切换到项目根目录执行
cd "$PROJECT_ROOT"

# 检查输入视频是否存在
if [ ! -f "$INPUT_VIDEO" ]; then
    echo "错误：输入视频文件未找到于 $INPUT_VIDEO"
    exit 1
fi

# 如果输出目录不存在，则创建它
echo "创建输出目录于 $OUTPUT_DIR"
mkdir -p "$OUTPUT_DIR"

# 使用 FFmpeg 提取关键帧 (I-frame)
echo "正在从 $INPUT_VIDEO 提取关键帧..."
ffmpeg -i "$INPUT_VIDEO" -vf "select=eq(pict_type\,I)" -vsync vfr -q:v 2 "$OUTPUT_DIR/keyframe_%04d.jpg"

echo "关键帧提取完成。文件已保存至 $OUTPUT_DIR"