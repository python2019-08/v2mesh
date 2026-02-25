import shutil
from pathlib import Path
import pycolmap

#  https://pypi.org/project/pycolmap/
# 
#  从运动恢复结构（Structure from Motion, SfM），它主要包含三个步骤：
# 
# 特征提取 (Feature Extraction)：在每张图像中检测独特的特征点（例如，使用 SIFT 算法）。
# 特征匹配 (Feature Matching)：在不同图像之间寻找并匹配相同的特征点。
# 增量重建 (Incremental Reconstruction)：利用匹配好的特征点，逐步地、稳健地计算出每张照片的相机位置和姿态，
#         并同时构建出场景的稀疏三维点云。Bundle Adjustment (光束法平差) 是这个过程中不断进行的优化步骤，
#         用于最小化三维点投影到图像上的误差，从而得到更精确的结果。

 
def sfm1_featureExtraction(dat_root: Path):
    """ 
    这个过程包括 [1/3].特征提取  
    """
 
    # 输入图像目录
    image_dir = dat_root / "frames_sharp"
    
    # COLMAP 工作区目录，用于存放数据库和重建结果
    colmap_workspace = dat_root / "colmap_workspace"
    
    # COLMAP 数据库文件路径
    database_path = colmap_workspace / "database.db"

    # --- 脚本主体 ---
    print("使用 PyCOLMAP 进行 SfM 重建: 1.特征提取...")

    # 0. 环境准备
    # 检查输入目录是否存在
    if not image_dir.is_dir() or not any(image_dir.iterdir()):
        print(f"错误：图像目录 {image_dir} 不存在或为空。")
        print("请先运行 s01... 系列脚本生成清晰的关键帧。")
        return

    # 清理并创建工作区
    if colmap_workspace.exists():
        print(f"清理已存在的工作区: {colmap_workspace}")
        shutil.rmtree(colmap_workspace)
    print(f"创建新的工作区: {colmap_workspace}")
    colmap_workspace.mkdir(parents=True)

    # 1. 特征提取 (Feature Extraction)
    # ------------------------------------
    # https://pypi.org/project/pycolmap/
    # 
    # 这一步会为每张图片提取 SIFT 特征，并将它们存储在 SQLite 数据库中。
    # pycolmap.extract_features 会自动创建数据库文件。
    print("\n[1/4] 正在提取特征...")
    try:      
        reader_options = pycolmap.ImageReaderOptions()
        reader_options.camera_model = "SIMPLE_RADIAL" 
        # 核心：1200是估算的像素焦距，960/540是主点，0是初始畸变
        # 1080p 的标准焦距约在 1200-1500 之间
        reader_options.camera_params = "1200, 960, 540, 0" 
        # 告诉 COLMAP 初始参数是准确的，不需要它乱猜
        # reader_options.prior_focal_length = True 

        # 1244張圖如果不限制，數據庫會輕鬆破 20GB
        # For pycolmap 3.13+, we must use FeatureExtractionOptions
        extraction_options = pycolmap.FeatureExtractionOptions()
        extraction_options.sift.max_num_features = 4096  # 關鍵：限制每張圖的特徵點數量
    

        # PINHOLE 模型不包含畸变参数。如果你的手机视频畸变很大，用 PINHOLE 会导致特征点对不齐，重投影误差极高，从而无法通过初始化的质量校验。
        # 建议：如果视频没经过预先去畸变，请改回 SIMPLE_RADIAL 或 OPENCV。
        pycolmap.extract_features(database_path,
                                  image_dir,
                                  camera_mode=pycolmap.CameraMode.SINGLE,
                                  camera_model='SIMPLE_RADIAL',
                                  reader_options     = reader_options,
                                  extraction_options = extraction_options)
        

        
        print("特征提取完成。")
    except Exception as e:
        print(f"特征提取过程中发生错误: {e}")
        print("请确保您已正确安装 COLMAP 及其依赖 (如 CUDA)。")
        exit(1)  # return
 
  

def sfm2_featureMatching(project_root : Path,dat_root: Path):
    """
    [2/3].特征匹配。
    """
 
    # 输入图像目录
    image_dir = dat_root / "frames_sharp"
    
    # COLMAP 工作区目录，用于存放数据库和重建结果
    colmap_workspace = dat_root / "colmap_workspace"
  
    # COLMAP 数据库文件路径
    database_path = colmap_workspace / "database.db"

    # --- 脚本主体 ---
    print("使用 PyCOLMAP 进行 SfM 重建: 2.特征匹配...")
 

    # ,check环境准备 
    if not colmap_workspace.exists():
        print(f" 不存在的工作区: {colmap_workspace}")
        return 
    
    if not (database_path).is_file():
        print(f" 不存在的數據庫文件: {database_path},特征提取  需要先完成!")
        return
 
    # 2. 特征匹配 (Feature Matching)
    # ---------------------------------
    # 这一步在所有图像对之间寻找匹配的特征点。
    # 'exhaustive' 匹配器会尝试匹配所有可能的图像对，适用于图像数量不多的情况。
    # 对于大量图像，需要考虑 'sequential' 或 'vocab_tree' 匹配器。
    print("\n[2/4] 正在进行特征匹配...")
    try:       
        # 不要用 exhaustive_matching，改用 match_sequential        
        # pycolmap.match_exhaustive(database_path, matching_options=matching_options)
        
        # 匹配器选项，用于设置重叠数量
        # overlap=20 表示每張圖只和前後20張匹配，這對 10米路面視頻最完美
        matching_options = pycolmap.FeatureMatchingOptions()
        matching_options.use_gpu = True 

        pairing_options= pycolmap.SequentialPairingOptions() 
        pairing_options.overlap = 20  
        pairing_options.loop_detection = True # 关键：开启回环检测，增强匹配稳定性

        # 关键：手动指定词汇树的路径，避免自动下载失败
        # wget https://github.com/colmap/colmap/releases/download/3.11.1/vocab_tree_faiss_flickr100K_words256K.bin
        vocab_tree_path = project_root / "dat/2models4sfm/vocab_tree_faiss_flickr100K_words256K.bin"
        pairing_options.vocab_tree_path = str(vocab_tree_path)
        # 调用函数，并使用 'device' 参数指定自动选择 GPU
        pycolmap.match_sequential(database_path, 
                                  matching_options = matching_options, 
                                  pairing_options  = pairing_options, 
                                  device=pycolmap.Device.auto) 
        print("特征匹配完成。")
    except Exception as e:
        print(f"特征匹配过程中发生错误: {e}")
        exit(2)  # return



def sfm3_sparseReconstruct(dat_root: Path):
    """
    [3/3]增量重建。
    """
 
    # 输入图像目录
    image_dir = dat_root / "frames_sharp"
    
    # COLMAP 工作区目录，用于存放数据库和重建结果
    colmap_workspace = dat_root / "colmap_workspace"
    
    # 输出的稀疏重建模型目录
    sparse_dir = colmap_workspace / "sparse"
    
    # COLMAP 数据库文件路径
    database_path = colmap_workspace / "database.db"

    # --- 脚本主体 ---
    print("开始使用 PyCOLMAP 进行 SfM 重建...")

    # ,check环境准备 
    if not image_dir.is_dir() or not any(image_dir.iterdir()):
        print(f"错误：图像目录 {image_dir} 不存在或为空。")
        print("请先运行 s01... 系列脚本生成清晰的关键帧。")
        return
        
    if not colmap_workspace.exists():
        print(f" 不存在的工作区: {colmap_workspace}")
        return 
    
    if not (database_path).is_file():
        print(f" 不存在的數據庫文件: {database_path},特征提取  需要先完成!")
        return
 
    # 3. 增量重建 (Incremental Reconstruction / SfM)
    # ------------------------------------------------
    # 这是 SfM 的核心步骤。COLMAP 会选择一个最佳的初始图像对，
    # 然后逐步地将其他图像加入到模型中，同时通过 Bundle Adjustment
    # 来优化相机位姿和三维点云的位置。
    print("\n[3/4] 正在运行增量重建 (SfM)...")
    try:

        # For pycolmap 3.13+, options are nested.
        # IncrementalPipelineOptions：负责整个重建流程的宏观控制
        pipeline_options = pycolmap.IncrementalPipelineOptions()
        pipeline_options.min_num_matches = 50 # 调低点，默认通常是 100），给初始化留更多余地。
        # Let COLMAP automatically find the best initial pair.
        # pipe_opts.mapper：对应 IncrementalMapperOptions，控制具体的三角化角度、重投影误差阈值、本地/全局 BA 的触发条件。
        pipeline_options.mapper.init_max_error = 8.0      # 稍微调大初始容忍误差  
        # 当f锁死在 1200 时，OpenMVS 在 Points weighted 阶段计算的投影坐标会落在 1753x986 的合理像素范围内
        # （比如 500, 400），而不再是产生万级别像素坐标导致的 buffer overflow。        
        # 2. 关键：禁止 BA 优化焦距 (f)
        # 将该属性设为 False，COLMAP 就会锁死你在数据库里存的 1200
        pipeline_options.ba_refine_focal_length = False        
        # 3. 可选：如果你觉得畸变参数也被带跑了，也可以关掉
        pipeline_options.ba_refine_extra_params = False        
        # pipe_opts.triangulation：对应 IncrementalTriangulatorOptions，控制 3D 点生成的质量要求。



        # `incremental_mapping` 函数需要一个输出目录来存放模型。
        # 它会返回一个 Reconstruction 对象，或者如果失败则返回 None。
        models = pycolmap.incremental_mapping(
            database_path, image_dir, sparse_dir, options=pipeline_options
        )
         

        if models and len(models) > 0:
            print("增量重建成功！")
            # 最大的模型通常是索引 0
            # reconstruction = model[0]
            # reconstruction.write_text(sparse_dir)      
            # 
            for idx, rec in models.items():
                print(f"model-#{idx} {rec.summary()}")                           
                # 打印出重建的一些基本信息
                print(f"  - model-#{idx}中包含 {len(rec.cameras)} 个相机。")
                print(f"  - model-#{idx}中包含 {len(rec.images)} 张注册成功的图像。")
                print(f"  - model-#{idx}中包含 {len(rec.points3D)} 个三维点。")
            
            # 你可以进一步处理 `model` 对象，例如导出为其他格式
            # model.write_text(colmap_workspace / "sparse_text")
            # print(f"稀疏模型已以文本格式导出到 {colmap_workspace / 'sparse_text'}")

        else:
            print("增量重建失败：未能生成任何有效的稀疏模型。")
            print("可能的原因包括：图像之间重叠度不足、特征匹配点太少、场景无纹理等。")
            print(f"请检查 {colmap_workspace} 中的日志以获取详细信息。")
            return
            
    except Exception as e:
        print(f"增量重建过程中发生错误: {e}")
        exit(3)  # return

    print(f"\nSfM 流程完成。稀疏重建结果已保存至: {sparse_dir}")

# -------------------------------------------------------------
# def sfm4_undistort_images(dat_root: Path):

#     # COLMAP 工作区目录，用于存放数据库和重建结果
#     colmap_workspace = dat_root / "colmap_workspace"

#     image_path  = dat_root / "frames_sharp"
#     input_path  = colmap_workspace / Path("sparse/0")
    

#     output_path = colmap_workspace / Path("sparse_undistort")
#     output_path.mkdir(exist_ok=True)

 
#     # 自动进行去畸变导出
#     # 这会生成可以直接给 OpenMVS 使用的 .mvs 或 colmap 格式文件
#     print("\n[4/4] 正在运行去畸变导出...")
#     pycolmap.undistort_images(
#         output_path= output_path,
#         input_path = input_path, # 传入刚才取出的第一个模型
#         image_path = image_path,
#         output_type="COLMAP"
#     )    
# -------------------------------------------------------------

def sfm4_undistort_images(dat_root: Path):
    colmap_workspace = dat_root / "colmap_workspace"
    image_path = dat_root / "frames_sharp"
    input_path = colmap_workspace / "sparse/0"
    output_path = colmap_workspace / "sparse_undistort"
    
    # 创建目录结构（OpenMVS 需要 sparse 子目錄）
    sparse_out_dir = output_path / "sparse"
    sparse_out_dir.mkdir(parents=True, exist_ok=True)

    reconstruction = pycolmap.Reconstruction(str(input_path))
    
    # 遍历所有相机进行转换（处理单相机或多相机）
    for camera_id, camera in reconstruction.cameras.items():
        if camera.model.name  == "PINHOLE":
            continue

        # 如果畸变参数为 0，直接手动转换为 PINHOLE
        if len(camera.params) >= 4 and camera.params[3] == 0:
            f, cx, cy = camera.params[0], camera.params[1], camera.params[2]
            new_params = [f, f, cx, cy]
            
            # 更新重建对象中的相机
            reconstruction.cameras[camera_id] = pycolmap.Camera(
                model="PINHOLE",
                width=camera.width,
                height=camera.height,
                params=new_params
            )
            print(f"相机 {camera_id} 已手动转换为 PINHOLE [f={f}]")
        else:
            # 存在畸变参数，必须运行真正的去畸变算法
            print(f"相机 {camera_id} 存在畸变参数，运行 pycolmap.undistort_images...")
            pycolmap.undistort_images(str(output_path), str(input_path), str(image_path))
            return # undistort_images 会处理整个目录，直接返回
    
    
    # 如果是手动转换的，保存结果
    reconstruction.write_binary(str(sparse_out_dir))
    
    # 同步复制图片（OpenMVS 转换需要图片在对应位置）
    img_out_dir = output_path / "images"
    if not img_out_dir.exists():
        shutil.copytree(str(image_path), str(img_out_dir))
        
    print(f"模型已准备就绪：{sparse_out_dir}")

 



if __name__ == "__main__":
    dat_rootPathStr = "/home/abner/Documents/jobs/task/task-blender/task03ai0img0modeling/dat"
 
    dat_root = Path(dat_rootPathStr).resolve()

    sfm1_featureExtraction(dat_root)
    sfm2_featureMatching(dat_root)
    sfm3_sparseReconstruct(dat_root)
    sfm4_undistort_images(dat_root)
