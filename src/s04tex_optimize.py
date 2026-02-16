#  纹理优化（多视角混合）:MVE（Multi-View Environment）/ TexRecon ;
# 使用TexRecon，调用其全局能量最小化算法（Global Color Adjustment），自动消除多角度纹理合成时的阴影重叠、接缝、反光问题。

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
        process = subprocess.Popen(command, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
        for line in iter(process.stdout.readline, ''):
            print(line, end='')
        process.wait()
        if process.returncode != 0:
            raise subprocess.CalledProcessError(process.returncode, command)
        print(f"[成功] 命令 {' '.join(command)} 执行完毕。")
    except FileNotFoundError:
        print(f"错误: 命令 '{command[0]}' 未找到。")
        print("请确保 MVE (包含 colmap2mve 和 texrecon) 的可执行文件目录已添加到系统的 PATH 环境变量中。")
        exit(1)
    except subprocess.CalledProcessError as e:
        print(f"错误: 命令 {' '.join(command)} 执行失败，返回码 {e.returncode}。")
        exit(1)


def do_texture_optimization(project_root: Path):
    """
    使用 MVE/TexRecon 对 OpenMVS 生成的网格进行纹理优化。
    """
    # --- 配置 ---
    project_root = Path(__file__).resolve().parent.parent
    
    # 输入：COLMAP 工作区 (用于转换)
    colmap_workspace = project_root / "dat/colmap_workspace"
    
    # 输入：OpenMVS 生成的带纹理的网格
    input_mesh = project_root / "dat/openmvs_workspace/scene_dense_mesh_textured.obj"
    
    # MVE 工作区 (用于存放转换后的场景和优化结果)
    mve_workspace = project_root / "dat/mve_workspace"
    
    # 输出：优化后的模型文件名前缀
    output_prefix = mve_workspace / "optimized_model"

    # --- 脚本主体 ---
    print("开始使用 MVE/TexRecon 进行纹理优化...")

    # 0. 环境准备
    # 检查输入文件是否存在
    if not (colmap_workspace / "sparse").exists():
        print(f"错误：未找到 COLMAP 稀疏重建结果于 {colmap_workspace}")
        print("请先成功运行 s02_run_sfm.py 脚本。")
        return
    if not input_mesh.is_file():
        print(f"错误：未找到 OpenMVS 网格文件于 {input_mesh}")
        print("请先成功运行 s0301reconstruct.py 脚本。")
        return

    # 清理并创建 MVE 工作区
    if mve_workspace.exists():
        print(f"清理已存在的 MVE 工作区: {mve_workspace}")
        shutil.rmtree(mve_workspace)
    print(f"创建新的 MVE 工作区: {mve_workspace}")
    mve_workspace.mkdir(parents=True)

    # 1. 将 COLMAP 格式转换为 MVE 场景格式
    # -----------------------------------------
    # `colmap2mve` 是一个实用工具，它读取 COLMAP 项目并生成一个 MVE 场景，
    # 其中包含一个 `views` 目录（存放每个视角的图像和元数据）。
    print("\n[1/2] 转换 COLMAP 项目到 MVE 场景格式...")
    cmd_convert = [
        "colmap2mve",
        "--input", str(colmap_workspace),
        "--output", str(mve_workspace)
    ]
    run_command(cmd_convert, mve_workspace)

    # 2. 运行 TexRecon 进行纹理优化
    # ------------------------------------
    # 这是核心步骤。TexRecon 读取 MVE 场景、输入的网格，并生成一个新的优化纹理。
    print("\n[2/2] 运行 TexRecon 进行全局纹理优化...")
    cmd_texrecon = [
        "texrecon",
        # --- 关键优化选项 ---
        # 启用全局和局部接缝平滑，这是消除颜色差异的关键。
        "--global-seam-leveling",
        "--local-seam-leveling",
        # 使用高斯钳位去除颜色异常值，有助于处理反光。
        "--outlier-removal=gauss_clamping",
        # 确保最终生成带纹理的 .obj 文件。
        "--write-atlases",
        # --- 输入和输出 ---
        # 输入 MVE 场景目录
        str(mve_workspace),
        # 输入要进行纹理优化的网格文件
        str(input_mesh),
        # 输出优化后模型的文件名前缀
        str(output_prefix)
    ]
    run_command(cmd_texrecon, mve_workspace)

    final_model_path = output_prefix.with_suffix(".obj")
    print(f"\n纹理优化完成！")
    print(f"最终的优化后三维模型已保存至: {final_model_path}")

if __name__ == "__main__":
    project_rootPathStr = "/home/abner/Documents/jobs/task/task-blender/task03ai0img0modeling/"
    
 
    project_root = Path(project_rootPathStr).resolve()
    do_texture_optimization(project_root)
