import cv2
import shutil
from pathlib import Path

def variance_of_laplacian(image_path):
    """
    计算图像的拉普拉斯算子的方差。
    :param image_path: 图像文件的路径。
    :return: 拉普拉斯方差值。
    """
    # 以灰度模式读取图像
    image = cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE)
    # 计算拉普拉斯算子，并指定数据类型为64位浮点数以避免溢出
    laplacian = cv2.Laplacian(image, cv2.CV_64F)
    # 计算方差
    variance = laplacian.var()
    return variance

def deblur(aDatRoot: Path):
    """
    遍历关键帧目录，检测并过滤模糊的图像。
    """ 

    # 输入目录 (包含关键帧)
    input_dir = aDatRoot / "frames"

    # 输出目录 (存放清晰的帧)
    output_dir = aDatRoot / "frames_sharp"

    # 方差阈值，低于此值的图像被认为是模糊的。
    # 这个值可能需要根据实际图像进行调整。100.0 是一个常见的起始点。
    blur_threshold = 100.0

    # --- 脚本主体 ---
    # 检查输入目录是否存在
    if not input_dir.is_dir():
        print(f"错误：输入目录未找到于 {input_dir}")
        return

    # 清理并创建输出目录
    if output_dir.exists():
        print(f"清理已存在的输出目录: {output_dir}")
        shutil.rmtree(output_dir)
    print(f"创建输出目录: {output_dir}")
    output_dir.mkdir(parents=True)

    print(f"开始处理目录 {input_dir} 中的图像...")
    print(f"模糊检测阈值 = {blur_threshold}\n")

    # 遍历输入目录中的所有 jpg 文件
    image_files = sorted(list(input_dir.glob("*.jpg")))
    if not image_files:
        print("未在输入目录中找到 .jpg 图像。")
        return
        
    total_images = len(image_files)
    sharp_count = 0

    for i, image_path in enumerate(image_files):
        # 计算图像的模糊度 (拉普拉斯方差)
        variance = variance_of_laplacian(image_path)

        # 检查方差是否低于阈值
        if variance < blur_threshold:
            print(f"  - 丢弃: {image_path.name} (方差: {variance:.2f} < {blur_threshold})")
        else:
            print(f"  + 保留: {image_path.name} (方差: {variance:.2f} >= {blur_threshold})")
            # 将清晰的图像复制到输出目录
            shutil.copy(image_path, output_dir / image_path.name)
            sharp_count += 1
    
    print(f"\n处理完成。")
    print(f"总共处理了 {total_images} 张图像。")
    print(f"保留了 {sharp_count} 张清晰图像，已保存至 {output_dir}")


if __name__ == "__main__":
    dat_rootPathStr = "/home/abner/Documents/jobs/task/task-blender/task03ai0img0modeling/dat"
 
 
    dat_root = Path(dat_rootPathStr).resolve()

    deblur(dat_root)
