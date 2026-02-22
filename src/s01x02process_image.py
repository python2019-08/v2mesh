import cv2
import shutil
from pathlib import Path
 
import numpy as np
from PIL import Image, ExifTags
import os

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

def deblur(input_dir: Path,output_dir: Path):
    """
    遍历关键帧目录，检测并过滤模糊的图像。
    """ 
 
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


# ------------------------------------------------
def auto_rotate_to_landscape(image_path):
    """
    自动将图像旋转为横屏（宽>高），优先读取EXIF方向信息，无则按宽高比判断
    :param image_path: 输入图像路径
    :return: 旋转后的OpenCV格式图像（BGR）
    """
    # 第一步：用PIL读取EXIF方向信息
    try:
        pil_img = Image.open(image_path)
        # 获取EXIF方向标签
        exif = pil_img._getexif()
        orientation = None
        if exif is not None:
            for tag, value in exif.items():
                if ExifTags.TAGS.get(tag) == 'Orientation':
                    orientation = value
                    break
        
        # 根据EXIF Orientation值旋转图像
        if orientation == 1:
            # 正常方向，无需旋转
            rotated_pil = pil_img
        elif orientation == 2:
            # 水平翻转
            rotated_pil = pil_img.transpose(Image.FLIP_LEFT_RIGHT)
        elif orientation == 3:
            # 旋转180°
            rotated_pil = pil_img.transpose(Image.ROTATE_180)
        elif orientation == 4:
            # 垂直翻转
            rotated_pil = pil_img.transpose(Image.FLIP_TOP_BOTTOM)
        elif orientation == 5:
            # 先水平翻转再旋转90°顺时针
            rotated_pil = pil_img.transpose(Image.FLIP_LEFT_RIGHT).transpose(Image.ROTATE_90)
        elif orientation == 6:
            # 旋转90°顺时针（最常见：竖屏转横屏）
            rotated_pil = pil_img.transpose(Image.ROTATE_90)
        elif orientation == 7:
            # 先水平翻转再旋转90°逆时针
            rotated_pil = pil_img.transpose(Image.FLIP_LEFT_RIGHT).transpose(Image.ROTATE_270)
        elif orientation == 8:
            # 旋转90°逆时针
            rotated_pil = pil_img.transpose(Image.ROTATE_270)
        else:
            # 无明确方向，按宽高比判断
            width, height = pil_img.size
            if height > width:
                rotated_pil = pil_img.transpose(Image.ROTATE_90)
            else:
                rotated_pil = pil_img
        
        # 转换为OpenCV格式（PIL是RGB，OpenCV是BGR）
        rotated_cv = cv2.cvtColor(np.array(rotated_pil), cv2.COLOR_RGB2BGR)
        pil_img.close()
        rotated_pil.close()
        
    except Exception as e:
        # 无EXIF信息时的降级处理
        print(f"读取EXIF失败：{e}，按宽高比旋转")
        cv_img = cv2.imread(image_path)
        height, width = cv_img.shape[:2]
        if height > width:
            rotated_cv = cv2.rotate(cv_img, cv2.ROTATE_90_CLOCKWISE)
        else:
            rotated_cv = cv_img
    
    return rotated_cv

def enhance_image_quality(image):
    """
    图像质量提升：先去噪，再锐化
    :param image: OpenCV格式的BGR图像
    :return: 增强后的图像
    """
    # 第一步：彩色图像去噪（参数可根据需求调整）
    # h：去噪强度（1-10，值越大去噪越明显，细节丢失越多）
    # templateWindowSize：模板窗口大小（必须为奇数）
    # searchWindowSize：搜索窗口大小（必须为奇数）
    denoised = cv2.fastNlMeansDenoisingColored(
        image, 
        None, 
        h=8,               # 亮度通道去噪强度
        hColor=8,          # 颜色通道去噪强度
        templateWindowSize=7,
        searchWindowSize=21
    )
    
    # 第二步：锐化（自定义卷积核，避免过度锐化）
    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]])  # 简单锐化核
    # 也可以用拉普拉斯锐化：kernel = np.array([[0,1,0],[1,-4,1],[0,1,0]])
    sharpened = cv2.filter2D(denoised, -1, kernel)
    
    # 可选：调整对比度和亮度（进一步提升视觉效果）
    alpha = 1.1  # 对比度（1.0为原图，>1增强）
    beta = 5     # 亮度（0为原图，>0增亮）
    enhanced = cv2.convertScaleAbs(sharpened, alpha=alpha, beta=beta)
    
    return enhanced

def process_oneImage(input_path, output_path):
    """
    完整流程：读取→旋转→增强→保存
    :param input_path: 输入图像路径
    :param output_path: 输出图像路径
    """
    if not os.path.exists(input_path):
        print(f"输入文件不存在：{input_path}")
        return
    
    # 1. 自动旋转为横屏
    rotated_img = auto_rotate_to_landscape(input_path)
    
    # 2. 提升图像质量
    enhanced_img = enhance_image_quality(rotated_img)
    
    # 3. 保存结果
    cv2.imwrite(output_path, enhanced_img)
    print(f"处理完成，结果保存至：{output_path}")


def processImages(inputDirPath, outputDirPath):
    """
    批量处理图像：读取→旋转→增强→保存
    :param inputDirPath: 输入图像目录路径
    :param outputDirPath: 输出图像目录路径
    """
    if not os.path.exists(inputDirPath):
        print(f"输入目录不存在：{inputDirPath}")
        return
    if not os.path.exists(outputDirPath):
        os.makedirs(outputDirPath)
    
    # 遍历目录下所有图像文件
    for filename in os.listdir(inputDirPath):
        if not filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            continue

        input_file = os.path.join(inputDirPath, filename)
        output_file = os.path.join(outputDirPath, filename)
        
        # 处理单张图像
        process_oneImage(input_file, output_file)


def process_Images( aDatRoot : Path):
    # 输入目录 (包含关键帧)
    input_dir = aDatRoot / "frames"
    # 输出目录 (存放清晰的帧)
    output_dir = aDatRoot / "frames_sharp0"
    processImages( input_dir, output_dir)

    #  
    deblur_input_dir = aDatRoot / "frames_sharp0"     
    deblur_output_dir = aDatRoot / "frames_sharp"
    deblur(deblur_input_dir, deblur_output_dir)


if __name__ == "__main__":
    dat_rootPathStr = "/home/abner/Documents/jobs/task/task-blender/task03ai0img0modeling/dat"
 
 
    dat_root = Path(dat_rootPathStr).resolve()

    deblur(dat_root)
