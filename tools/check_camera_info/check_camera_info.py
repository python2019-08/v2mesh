import pycolmap
from pathlib import Path



def check_camera_info(aProjectRoot: Path, aSparsePath: str):
    # 1. 加载 aSparsePath 文件夹中的模型
    # 注意：路径应指向包含 cameras.bin, images.bin, points3D.bin 的父目录 
    #  
    reconstruction = pycolmap.Reconstruction(str(aProjectRoot / aSparsePath))
    print(reconstruction.summary())
    # 2. 遍历所有相机查看模型名称
    print(f"{aSparsePath}, Total cameras: {len(reconstruction.cameras)}")
    for camera_id, camera in reconstruction.cameras.items():
        print(f"Camera ID: {camera_id}")
        print(f"  Model Name: {camera.model.name}")   # 例如: SIMPLE_RADIAL, PINHOLE
        print(f"  Model ID: {camera.model.value}")       # 对应的内部枚举 ID
        print(f"  Width/Height: {camera.width}x{camera.height}")
        print(f"  Parameters: {camera.params}")       # [f, cx, cy, k, ...] 具体取决于模型
        
    # 顺便检查一下有多少张图被成功注册到了这个模型
    print(f"{aSparsePath}, 成功注册的图像数: {len(reconstruction.images)}")

if __name__ == "__main__":
    project_rootPathStr = "/home/abner/Documents/jobs/task/task-blender/task03ai0img0modeling/"
    
    
    # 调用函数提取关键帧
    print( "*" * 40)
    project_root = Path(project_rootPathStr).resolve()
    rel_path_sparse = "dat/colmap_workspace/sparse/0"
    check_camera_info(project_root, rel_path_sparse)

    print( "*" * 40)
    rel_path_sparse_undistort = "dat/colmap_workspace/sparse_undistort/sparse"
    check_camera_info(project_root, rel_path_sparse_undistort)


 