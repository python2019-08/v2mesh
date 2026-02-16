# =======================================
# conda activate img-modeling
# python ./src/main_modeling.py
# =======================================

from s01x01extract_frames import extractVideoFrames

from s01x02deblur import deblur

import s02sfm as sfm

import s03dense as dense
from s04tex_optimize import do_texture_optimization

from pathlib import Path


if __name__ == "__main__":
    # 获取项目根目录 (假定此脚本位于 code/ 目录下)
    # project_root = Path(__file__).resolve().parent.parent
    project_rootPathStr = "/home/abner/Documents/jobs/task/task-blender/task03ai0img0modeling/"
    print(project_rootPathStr)
    project_root = Path(project_rootPathStr).resolve()

    if not project_root.is_dir():
        print(f"错误：项目根目录未找到于 {project_root}")
        exit(1)
    # v2m : video to mesh
    dat_rootPathStr = "/0v2m"
    dat_root = Path(dat_rootPathStr).resolve()

    # ----------------------------------------
    # 控制是否跳过每个步骤，方便调试和分阶段运行  False  True
    isSkip_extractVideoFrames = True
    isSkip_deblur = True

    isSkip_sfm1featureExtract = True
    isSkip_sfm2featureMatching = True
    isSkip_sfm3sparseReconstruct = True
    isSkip_sfm4undistort_images = True
 
    isSkip_step1_makeMvs = True
    isSkip_step2x1_makeDmap = True
    isSkip_step2x2_densifyPointCloud = False
    isSkip_step3_reconstructMesh = False
    isSkip_step4_textureMesh = False

    isSkip_optimize_texture = True

    # ----------------------------------------
    # 调用函数提取关键帧    
    if not isSkip_extractVideoFrames:
        extractVideoFrames(dat_root)
        # extractFrames2(project_root)
 
    # ----------------------------------------
    # 调用函数进行去模糊处理
    if not isSkip_deblur:
        deblur(dat_root)

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

    if not isSkip_step2x1_makeDmap:
        drObj.step2x1_makeDmap( )

    # if not isSkip_step2x2_densifyPointCloud:
    #     drObj.step2x2_densifyPointCloud(  )

    if not isSkip_step3_reconstructMesh:
        drObj.step3_reconstructMesh( )

    if not isSkip_step4_textureMesh:
        drObj.step4_textureMesh( )

    # ----------------------------------------
    # 调用函数进行纹理优化
    if not isSkip_optimize_texture:
        do_texture_optimization(project_root)

    
