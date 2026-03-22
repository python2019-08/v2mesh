# 使用 OpenMVS 对 COLMAP 的稀疏重建结果进行稠密重建和网格化。
import subprocess
import shutil
from pathlib import Path

def run_command(command, cwd):
    """
    执行一个 shell 命令并处理可能的错误。
    :param command: 要执行的命令列表。
    :param cwd: 命令执行的工作目录。
    """
    print(f"\n[执行命令] {' '.join(command)}")
    try:
        # 使用 Popen 实时打印输出
        process = subprocess.Popen(command, 
                                   cwd=cwd, 
                                   stdout=subprocess.PIPE, 
                                   stderr=subprocess.STDOUT, 
                                   text=True, 
                                   bufsize=1)
        for line in iter(process.stdout.readline, ''):
            print(line, end='')
        process.wait()
        
        if process.returncode != 0:
            raise subprocess.CalledProcessError(process.returncode, command)
        
        print(f"[成功] 命令 {' '.join(command)} 执行完毕。")
    except FileNotFoundError:
        print(f"错误: 命令 '{command[0]}' 未找到。")
        print("请确保 OpenMVS 的可执行文件目录已添加到系统的 PATH 环境变量中。")
        exit(1)
    except subprocess.CalledProcessError as e:
        print(f"错误: 命令 {' '.join(command)} 执行失败，返回码 {e.returncode}。")
        exit(1)

# project_root = Path(__file__).resolve().parent.parent
class DenseReconstruction:       
    def __init__(self, project_root: Path, dat_root: Path):
        self._projectRoot = project_root
        self._datRoot = dat_root
        
        if not self._projectRoot.exists():
            print(f"错误：未找到 文件目录于 {self._projectRoot}") 
            exit(-1000)  


        self._openmvs_binDir = self._projectRoot / "3rd/openMVS/make02/bin"
        if not self._openmvs_binDir.exists():
            print(f"错误：未找到 OpenMVS 可执行文件目录于 {self._openmvs_binDir}")
            print("请先成功编译 OpenMVS。")
            exit(-1001)

        self._mvsWorkspace = self._datRoot / "mvs" 
        self._sceneMvs_file = self._mvsWorkspace / "scene.mvs"
        
        # 定义稠密点云文件的路径
        self._dense_mvs = self._mvsWorkspace / "dense_pt_cloud.mvs"

        # 定义重建网格文件的路径
        self._reconstructMesh_mvs = self._mvsWorkspace / "reconstruct_mesh.mvs"
        self._reconstructMesh_ply = self._mvsWorkspace / "reconstruct_mesh.ply"
        
        # 定义精炼网格文件的路径
        self._refineMesh_mvs = self._mvsWorkspace / "refine_mesh.mvs"
        self._refineMesh_ply = self._mvsWorkspace / "refine_mesh.ply"
        
        # 定义纹理网格文件的路径
        self._textureMesh_mvs = self._mvsWorkspace / "textured_mesh.mvs"
        self._textureMesh_ply = self._mvsWorkspace / "textured_mesh.ply"
        
    #=================================
    def _init_mvsWorkspace(self):
        # OpenMVS workspace   # 清理并创建 OpenMVS 工作区 
        if self._mvsWorkspace.exists():
            print(f"清理已存在的 OpenMVS 工作区: {self._mvsWorkspace}")
            shutil.rmtree(self._mvsWorkspace)
        print(f"创建新的 OpenMVS 工作区: {self._mvsWorkspace}")
        self._mvsWorkspace.mkdir(parents=True)

    # ================================
    def step1_makeMvs(self) ->None:
        """
        
        """  
        print("step1_makeMvs().....................")           
        # COLMAP 工作区 (包含稀疏重建结果)
        colmap_workspace = self._datRoot / "colmap_workspace/sparse_undistort"
        # 检查 COLMAP 的输出是否存在
        if not (colmap_workspace).exists():
            print(f"错误：未找到 COLMAP 稀疏重建结果于 {colmap_workspace}")
            print("请先成功运行 s02_run_sfm.py 脚本。")
            exit( -1002)

        self._init_mvsWorkspace()
 

        # 1. 将 COLMAP 格式转换为 OpenMVS 格式
        # -----------------------------------------
        # InterfaceCOLMAP 工具读取 COLMAP 的输出并生成一个 .mvs 文件，
        # 该文件包含了所有相机、位姿和稀疏点云信息。
        print("\n[1/5] 转换 COLMAP 模型到 OpenMVS 格式...")
        cmd_interface = [
            str(self._openmvs_binDir / "InterfaceCOLMAP"),
            "--input-file",   str(colmap_workspace),
            "--image-folder", str(colmap_workspace / "images"),
            "--output-file",  str(self._sceneMvs_file)        
        ]
        run_command(cmd_interface, self._mvsWorkspace)

    # ====================================
    def check_mvsWorkspace(self):
        # OpenMVS 工作区 
        if not self._mvsWorkspace.exists():
            print(f"请先创建 OpenMVS 工作区: {self._mvsWorkspace}")  
            exit(-1011)       
                 
    # ====================================
    def check_sceneMvs_file(self):
        # 检查 OpenMVS 工作区
        if not self._sceneMvs_file.exists():
            print(f"请先创建 OpenMVS 场景文件: {self._sceneMvs_file}") 
            exit(-1012)                         

    # =====================================
    def step2_densifyPointCloud(self):
        """
        生成 *.dmap 
        """ 
        print("step2x1_makeDmap().....................")   
        self.check_mvsWorkspace()   
        self.check_sceneMvs_file()
        # 2. 稠密点云重建 (DensifyPointCloud)
        # ------------------------------------
        # 这是 MVS 的核心步骤，计算量非常大。
        # 它会为场景生成一个密集的 3D 点云。
        if True :        
            print("\n[2/5] 正在生成dmap 和 稠密点云...")

            cmd_createDmap = [
                str(self._openmvs_binDir / "DensifyPointCloud"),
                "--input-file", str(self._sceneMvs_file),
                "--output-file", str(self._dense_mvs),
                "--working-folder", str(self._mvsWorkspace),   
                "--max-threads","2",               # 仅2线程，避免内存竞争
                "--cuda-device","-2"               # 禁用GPU，强制CPU（核心修复溢出）                             
                # "--resolution-level","2",         # 核心：图像缩到1/4，降低内存
                # "--max-resolution","480",        # 深度图最大分辨率480p
                # "--min-resolution","240",        # 深度图最小分辨率240p
                # "--number-views","4",           # 仅用4个视图估计深度（减少计算）
                # "--number-views-fuse","1",      # 最低1个视图融合（适配稀疏点云）
                # "--iters","2",                     # 减少深度匹配迭代次数
                # "--geometric-iters","0",           # 禁用几何一致性迭代（避免溢出）
                # "--estimate-normals","0",          # 禁用法线估计（减少内存）
                # "--estimate-scale","0",            # 禁用尺度估计（减少内存）
                # "--fusion-mode","0",               # 0=深度图+融合（v2.3.0默认，稳定）
                # "--verbosity","1",                 # 低日志级别，减少输出内存占用
                # "--postprocess-dmaps","0",         # 禁用深度图后处理（简化计算）
                # "--filter-point-cloud","0",        # 禁用点云过滤（避免额外计算）
                # "--estimate-colors","1"            # 仅最终估计颜色（减少计算，保留颜色）
            ]
            run_command(cmd_createDmap, self._mvsWorkspace)
  
    # =========================================

    # def step2x2_densifyPointCloud(self):
    #     """
    #     既然 .dmap 文件已经生成在 mvs_ws 目录中，稠密重建最耗时的“计算”阶段已经完成了。
    #     """    
    #     print("step2x2_densifyPointCloud().....................") 
    #     self.check_mvsWorkspace()   

    #     self.check_sceneMvs_file()           
        # 2. 稠密点云重建 (DensifyPointCloud)
        # ------------------------------------
        # 这是 MVS 的核心步骤，计算量非常大。
        # 它会为场景生成一个密集的 3D 点云。
        # -----------------------------------
        # print("\n[2.2/4] 正在生成稠密点云 ...")
        # cmd_densify = [
        #     str(self._openmvs_binDir / "DensifyPointCloud"),
        #     "--input-file", str(self._sceneMvs_file),
        #     "--working-folder", str(self._mvsWorkspace),
        #     "--output-file", str(self._dense_mvs),
        #     "--fusion-mode", "0" , # 从fusion-mode=2（高复杂度）降到1（基础融合）
        #     "--max-resolution", "480",  # 深度图分辨率缩到480p（960x540→480x270）
        #     "--min-resolution", "240", 
        #     "--max-threads", "2",  # 极致降低线程数，避免内存竞争
        #     "--cuda-device", "-2",  # 禁用GPU，改用CPU（GPU易触发缓冲区溢出）               
        # ]
        # run_command(cmd_densify, self._mvsWorkspace)   
  
    def check_dense_mvs(self):
        # 检查 OpenMVS 工作区
        if not self._dense_mvs.exists():
            print(f"请先创建 OpenMVS 稠密场景文件: {self._dense_mvs}") 
            exit(-1013)                             

    def step3_reconstructMesh(self):
        """
        使用 OpenMVS 对 COLMAP 的稀疏重建结果进行稠密重建和网格化。
        """   
        print( "step3_reconstructMesh()....................." )   
        self.check_mvsWorkspace()
        self.check_sceneMvs_file()                 
        # 3. 网格重建 (ReconstructMesh)
        # --------------------------------
        if True:
            # 
            # ----使用泊松表面重建算法从稠密点云创建 3D 网格。    
            print("\n[3/5] 正在从稠密点云重建网格...")
            self.check_dense_mvs()
            cmd_reconstruct = [
                str(self._openmvs_binDir / "ReconstructMesh"),
                "--input-file", str(self._dense_mvs),
                "--working-folder", str(self._mvsWorkspace),
                "--output-file",    str(self._reconstructMesh_mvs),
                "--cuda-device", "-2"  # 禁用GPU，改用CPU（GPU易触发缓冲区溢出）   
                # "--min-point-distance", "0"                
            ]
            run_command(cmd_reconstruct, self._mvsWorkspace)
        else:
            # 
            # ----直接从稀疏点云重建网格 
            print("\n[3/4] 正在从稀疏点云融合深度图并重建网格...")
        
            cmd_reconstruct = [
                str(self._openmvs_binDir / "ReconstructMesh"),
                "--input-file",     str(self._sceneMvs_file),
                "--working-folder", str(self._mvsWorkspace),
                "--output-file",    str(self._reconstructMesh_mvs),
                "--cuda-device", "-2",  # 禁用GPU，改用CPU（GPU易触发缓冲区溢出）   
                "--min-point-distance", "0"
            ]    
            run_command(cmd_reconstruct, self._mvsWorkspace)

    # ==================================================
    def step4_RefineMesh(self):
        """
        RefineMesh 。
        """           
        # 4. (RefineMesh)
        # ----------------------------
        #  
        #  
        print("\n[4/5] 正在为网格生成纹理...")
        refineMesh_inputFile : Path = self._reconstructMesh_mvs
        if not refineMesh_inputFile.exists():
            print(f"refineMesh_inputFile={refineMesh_inputFile} not exist, try use denseMvs_file={self._dense_mvs}") 
            refineMesh_inputFile = self._dense_mvs    

        if not refineMesh_inputFile.exists():
            print(f"refineMesh_inputFile={refineMesh_inputFile} not exist, exit") 
            exit(-1014)             


        # cmd_texture = [
        #     str(self._openmvs_binDir / "RefineMesh"),
        #     "--input-file", str(refineMesh_inputFile),
        #     "--mesh-file",  str(self._reconstructMesh_ply), 
        #     "--output-file",    str(self._refineMesh_mvs),
        #     "--working-folder", str(self._mvsWorkspace),
        #     "--max-threads", "4" , # 降低线程数（减少内存占用）
        #     "--cuda-device", "-2"  # 禁用GPU，改用CPU（核心修复）
        # ]
        # run_command(cmd_texture, self._mvsWorkspace)        
 
    # ==================================================
    def check_reconstructMesh_ply(self):
        if not self._reconstructMesh_mvs.exists():
            print(f"_reconstructMesh_mvs 文件: {self._reconstructMesh_mvs} not generated, ignore it") 

        # 检查_reconstructMesh_ply
        if not self._reconstructMesh_ply.exists():
            print(f"请先创建 OpenMVS 网格文件: {self._reconstructMesh_ply}") 
            exit(-1015)     


    # ==================================================
    def step5_textureMesh(self):
        """
        使用 OpenMVS 对 COLMAP 的稀疏重建结果进行稠密重建和网格化。
        """              
        print("\nstep4_textureMesh().....................")
        self.check_mvsWorkspace()
        self.check_reconstructMesh_ply()

        # 4. 网格纹理化 (TextureMesh)
        # ----------------------------
        # 为 3D 网格生成纹理贴图，使其看起来更真实。
        # 输出是一个标准的 .obj 文件，可以在大多数 3D 查看器中打开。
        print("\n[5/5] 正在为网格生成纹理...")
        cmd_texture = [
            str(self._openmvs_binDir / "TextureMesh"),
            "--input-file", str(self._dense_mvs),
            "--mesh-file",  str(self._reconstructMesh_ply), 
            "--working-folder", str(self._mvsWorkspace),
            # 可选：导出为 glb /obj 格式
            "--export-type", "glb" ,
            "--output-file", str(self._textureMesh_mvs),
            "--max-threads", "4" , # 降低线程数（从20→8，减少内存占用）
            "--cuda-device", "-2",  # 禁用GPU，改用CPU（核心修复）
            "--resolution-level", "1",  # 图像缩放到1/2（降低纹理计算量）
            "--min-resolution", "320",  # 降低最小分辨率阈值
            "--max-texture-size", "2048",  # 降低最大纹理尺寸（从4096→2048）
            "--sharpness-weight", "0.6",  # 降低锐化（减少计算复杂度）
            "--outlier-threshold", "0.1",
            "--cost-smoothness-ratio", "1.0",  # 降低平滑度权重（减少计算）
            "--close-holes", "50",  # 降低孔洞修复阈值（减少计算）
            "--decimate", "1.0",  # 保持原始网格比例（无下采样）
            "--virtual-face-images", "0",  # 降低虚拟面数量（从3→2）
            "--global-seam-leveling", "0",  #  全局接缝平整（减少计算）
            "--local-seam-leveling", "0",  # 关闭局部接缝平整（减少计算）
            "-v", "2"  # 降低日志详细度（减少内存输出）

        ]
        run_command(cmd_texture, self._mvsWorkspace)

        final_model_path = self._mvsWorkspace / "scene_dense_mesh_textured.glb"
        print(f"\n处理完成！")
        print(f"最终的带纹理三维模型已保存至: {final_model_path}")    

if __name__ == "__main__":
    project_rootPathStr = "/home/abner/Documents/jobs/task/task-blender/task03ai0img0modeling/"
    project_root = Path(project_rootPathStr).resolve()

    dat_rootPathStr = "~/0model"
    dat_root = Path(dat_rootPathStr).resolve()

    drObj = DenseReconstruction()
    drObj.step1_makeMvs(project_root, dat_root)
    drObj.step2x1_makeDmap(project_root, dat_root)
    drObj.step2x2_densifyPointCloud(project_root, dat_root)
    drObj.step3_reconstructMesh( )
    drObj.step4_textureMesh( )
