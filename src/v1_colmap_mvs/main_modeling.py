# =======================================
# conda activate img-modeling
# python ./src/main_modeling.py
# =======================================

from s01x01extract_frames import extractVideoFrames

from s01x02process_image import deblur,process_Images

import s02sfm as sfm

import s03dense as dense
from s04tex_optimize import do_texture_optimization

from pathlib import Path


if __name__ == "__main__":
    # 获取项目根目录 (假定此脚本位于 code/ 目录下)
    # project_root = Path(__file__).resolve().parent.parent
    # input parameters (1/3)
    project_rootPathStr = "/home/abner/Documents/jobs/task/blender/task03v2mesh/"
    print(project_rootPathStr)
    project_root = Path(project_rootPathStr).resolve()
    if not project_root.is_dir():
        print(f"错误：项目根目录未找到于 {project_root}")
        exit(1)


    # v2m : video to mesh
    # ----input parameters (2/3)
    dat_rootPathStr = "/home/abner/0m/my04playground"
    dat_root = Path(dat_rootPathStr).resolve()

    # ----input parameters (3/3)
    # video_relativePath = "m.mov" ## "20260118-143016.mov"
    video_relativePath = "playgr.mp4"     
    # ----------------------------------------
    # 控制是否跳过每个步骤，方便调试和分阶段运行  False  True
    isSkip_extractVideoFrames = False
    isSkip_process_Images = False

    isSkip_sfm1featureExtract = False
    isSkip_sfm2featureMatching = False
    isSkip_sfm3sparseReconstruct = False
    isSkip_sfm4undistort_images = False
 
    isSkip_step1_makeMvs = False
    isSkip_step2_densifyPointCloud = False 
    isSkip_step3_reconstructMesh = False
    # isSkip_step4_refineMesh  = True
    isSkip_step5_textureMesh = False

    isSkip_optimize_texture = True

    # ----------------------------------------
    # 调用函数提取关键帧    
    if not isSkip_extractVideoFrames:
        extractVideoFrames(dat_root, video_relativePath)
        # extractFrames2(project_root)
 
    # ----------------------------------------
    # 调用函数进行去模糊处理
    if not isSkip_process_Images:
        process_Images(dat_root)

 
    # ----------------------------------------
    # 调用函数进行SFM重建
    if not isSkip_sfm1featureExtract:
        sfm.sfm1_featureExtraction(dat_root)
    
    if not isSkip_sfm2featureMatching:
        sfm.sfm2_featureMatching(project_root, dat_root)

    if not isSkip_sfm3sparseReconstruct: 
        sfm.sfm3_sparseReconstruct(dat_root)

    if not isSkip_sfm4undistort_images: 
        sfm.sfm4_undistort_images(dat_root)

    # ----------------------------------------
    # 调用函数进行稠密重建
    drObj = dense.DenseReconstruction(project_root, dat_root)
    if not isSkip_step1_makeMvs:
        drObj.step1_makeMvs( )

    if not isSkip_step2_densifyPointCloud:
        drObj.step2_densifyPointCloud( ) 

    if not isSkip_step3_reconstructMesh:
        drObj.step3_reconstructMesh( )

    # if not isSkip_step4_refineMesh :
    #     drObj.step4_RefineMesh()

    if not isSkip_step5_textureMesh:
        drObj.step5_textureMesh( )

    # ----------------------------------------
    # 调用函数进行纹理优化
    if not isSkip_optimize_texture:
        do_texture_optimization(project_root)

    
