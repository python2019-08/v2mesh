# 1.ReconstructMesh -h

```sh
~$ ReconstructMesh  -h
17:44:12 [App     ] OpenMVS x64 v2.3.0
17:44:12 [App     ] Build date: Feb 12 2026, 14:43:45
17:44:12 [App     ] CPU: Intel(R) Core(TM) i9-10900K CPU @ 3.70GHz (20 cores)
17:44:12 [App     ] RAM: 62.53GB Physical Memory 8.00GB Virtual Memory
17:44:12 [App     ] OS: Linux 6.17.0-14-generic (x86_64)
17:44:12 [App     ] Disk: 275.75GB (936.79GB) space
17:44:12 [App     ] SSE & AVX compatible CPU & OS detected
17:44:12 [App     ] Command line: ReconstructMesh -h
17:44:12 [App     ] Available options:

Generic options:
  -h [ --help ]                         produce this help message
  -w [ --working-folder ] arg           working directory (default current 
                                        directory)
  -c [ --config-file ] arg (=ReconstructMesh.cfg)
                                        file name containing program options
  --export-type arg (=ply)              file type used to export the 3D scene 
                                        (ply or obj)
  --archive-type arg (=4294967295)      project archive type: -1-interface, 
                                        0-text, 1-binary, 2-compressed binary
  --process-priority arg (=-1)          process priority (below normal by 
                                        default)
  --max-threads arg (=0)                maximum number of threads (0 for using 
                                        all available cores)
  -v [ --verbosity ] arg (=2)           verbosity level
  --cuda-device arg (=-1)               CUDA device number to be used to 
                                        reconstruct the mesh (-2 - CPU  processing, 
                                        -1 - best GPU, >=0 - device index)

Reconstruct options:
  -i [ --input-file ] arg               input filename containing camera poses 
                                        and image list
  -p [ --pointcloud-file ] arg          dense point-cloud with views file name 
                                        to reconstruct (overwrite existing 
                                        point-cloud)
  -o [ --output-file ] arg              output filename for storing the mesh
  -d [ --min-point-distance ] arg (=2.5)
                                        minimum distance in pixels between the 
                                        projection of two 3D points to consider
                                        them different while triangulating (0 -
                                        disabled)
  --integrate-only-roi arg (=0)         use only the points inside the ROI
  --constant-weight arg (=1)            considers all view weights 1 instead of
                                        the available weight
  -f [ --free-space-support ] arg (=0)  exploits the free-space support in 
                                        order to reconstruct weakly-represented
                                        surfaces
  --thickness-factor arg (=1)           multiplier adjusting the minimum 
                                        thickness considered during visibility 
                                        weighting
  --quality-factor arg (=1)             multiplier adjusting the quality weight
                                        considered during graph-cut

Clean options:
  --decimate arg (=1)                   decimation factor in range (0..1] to be
                                        applied to the reconstructed surface (1
                                        - disabled)
  --target-face-num arg (=0)            target number of faces to be applied to
                                        the reconstructed surface. (0 - 
                                        disabled)
  --remove-spurious arg (=20)           spurious factor for removing faces with
                                        too long edges or isolated components 
                                        (0 - disabled)
  --remove-spikes arg (=1)              flag controlling the removal of spike 
                                        faces
  --close-holes arg (=30)               try to close small holes in the 
                                        reconstructed surface (0 - disabled)
  --smooth arg (=2)                     number of iterations to smooth the 
                                        reconstructed surface (0 - disabled)
  --edge-length arg (=0)                remesh such that the average edge 
                                        length is this size (0 - disabled)
  --roi-border arg (=0)                 add a border to the region-of-interest 
                                        when cropping the scene (0 - disabled, 
                                        >0 - percentage, <0 - absolute)
  --crop-to-roi arg (=1)                crop scene using the region-of-interes17:44:12 [App     ] MEMORYINFO: {
17:44:12 [App     ] 	VmPeak:	  249564 kB
17:44:12 [App     ] 	VmSize:	  249532 kB
17:44:12 [App     ] } ENDINFO
```

<!-- yuanbaoAI -->
 

`ReconstructMesh` 是从稠密点云生成网格模型的核心工具，它使用泊松表面重建算法将点云转换为三角网格。

## 📋 命令核心参数解析

### 一、基础输入输出参数
| 参数 | 简写 | 说明 | 示例值 |
|------|------|------|--------|
| `--input-file`      | `-i` | **必需**，输入场景文件（包含相机姿态和图像列表） | `scene.mvs` |
| `--pointcloud-file` | `-p` | 稠密点云文件（可选，会覆盖现有点云） | `dense.ply` |
| `--output-file`     | `-o` | 输出网格文件 | `mesh.ply` 或 `mesh.obj` |
| `--export-type`     | -    | 导出文件类型 | `ply`（默认）或 `obj` |
| `--working-folder`  | `-w` | 工作目录    | `./data/` |

### 二、表面重建核心参数
| 参数 | 简写 | 说明 | 推荐值 | 作用 |
|------|------|------|--------|------|
| `--min-point-distance` | `-d` | 三角化时两点投影的最小像素距离 | `2.5` | 值越大，网格越简化；0=禁用 |
| `--free-space-support` | `-f` | 利用自由空间支持重建弱表面     | `0` | 1=启用，有助于重建纹理弱区域 |
| `--thickness-factor`   | -    | 可见性权重中最小厚度的乘数     | `1` | >1 增加厚度，<1 减小厚度 |
| `--quality-factor`     | -    | 图割中质量权重的乘数          | `1` | 影响网格平滑度 |
| `--cuda-device`        | -    | CUDA设备                    | `-1` | -1=自动选择最佳GPU |

### 三、网格后处理（清理）参数
| 参数 | 说明 | 推荐值 | 作用 |
|------|------|--------|------|
| `--decimate` | 网格简化因子 | `0.5`-`1` | (0,1]，1=不简化 |
| `--target-face-num` | 目标面片数 | `0` | 0=禁用，>0 时尝试简化到该面数 |
| `--remove-spurious` | 移除长边和孤立组件的阈值 | `20` | 0=禁用，值越大移除越少 |
| `--remove-spikes` | 移除尖峰面片 | `1` | 0=禁用，1=启用 |
| `--close-holes` | 闭合小孔的最大边数 | `30` | 0=禁用，值越大闭合的孔越大 |
| `--smooth` | 平滑迭代次数 | `2` | 0=禁用，值越大越平滑 |
| `--edge-length` | 重新网格化的目标边长 | `0` | 0=禁用，>0 时按此边长重新网格化 |
| `--crop-to-roi` | 使用ROI裁剪场景 | `1` | 0=禁用，1=启用 |

## 🚀 常用配置方案

### 方案1：快速预览（低细节，快速）
```bash
ReconstructMesh \
  -i scene.mvs \
  -o mesh_fast.ply \
  --decimate 0.3 \
  --smooth 1 \
  --close-holes 10 \
  --max-threads 8
```

### 方案2：标准质量（平衡速度与质量）
```bash
ReconstructMesh \
  -i scene.mvs \
  -o mesh_standard.ply \
  --min-point-distance 2.5 \
  --decimate 0.7 \
  --remove-spurious 15 \
  --remove-spikes 1 \
  --close-holes 20 \
  --smooth 2 \
  --cuda-device 0 \
  --max-threads 0
```

### 方案3：高质量（细节优先，速度较慢）
```bash
ReconstructMesh \
  -i scene.mvs \
  -o mesh_high_quality.ply \
  --min-point-distance 1.5 \
  --free-space-support 1 \
  --decimate 0.9 \
  --remove-spurious 10 \
  --remove-spikes 1 \
  --close-holes 30 \
  --smooth 3 \
  --quality-factor 1.2 \
  --cuda-device 0 \
  --max-threads 0
```

### 方案4：保留原始细节（不简化）
```bash
ReconstructMesh \
  -i scene.mvs \
  -o mesh_full_detail.ply \
  --min-point-distance 1.0 \
  --decimate 1.0 \          # 不简化
  --remove-spurious 5 \     # 轻微清理
  --remove-spikes 1 \
  --close-holes 50 \        # 闭合中等孔洞
  --smooth 1 \              # 轻微平滑
  --cuda-device 0
```

## 🔧 完整三维重建工作流

### 步骤1：稀疏重建（使用OpenMVG）
```bash
# OpenMVG流程
openMVG_main_SfMInit_ImageListing -i ./images/ -o ./matches/
openMVG_main_ComputeFeatures -i ./matches/sfm_data.json -o ./matches/
openMVG_main_ComputeMatches -i ./matches/sfm_data.json -o ./matches/
openMVG_main_IncrementalSfM -i ./matches/sfm_data.json -o ./reconstruction/
openMVG_main_openMVG2openMVS -i ./reconstruction/sfm_data.bin -o ./mvs/scene.mvs
```

### 步骤2：稠密重建（OpenMVS）
```bash
# 稠密点云生成
DensifyPointCloud -i ./mvs/scene.mvs -o ./mvs/dense.ply

# 网格重建
ReconstructMesh -i ./mvs/scene.mvs -o ./mvs/mesh.ply

# 可选：网格优化
RefineMesh -i ./mvs/mesh.ply -o ./mvs/mesh_refined.ply

# 可选：纹理映射
TextureMesh -i ./mvs/mesh_refined.ply -o ./mvs/mesh_textured.obj
```

## ⚡ 性能优化技巧

### 1. 内存管理（处理大型场景）
```bash
# 简化网格以减少内存使用
--decimate 0.3
--target-face-num 1000000  # 目标100万个面

# 分块处理大型点云
# 首先用DensifyPointCloud的--sub-scene-area参数分割场景
```

### 2. GPU加速
```bash
# 检查CUDA可用性
ReconstructMesh --cuda-device -1 -i test.mvs --help

# 使用指定GPU
--cuda-device 0  # 使用第一个GPU
```

### 3. 并行处理
```bash
# 使用所有CPU核心
--max-threads 0

# 或预留2个核心给系统
--max-threads $(($(nproc) - 2))
```

## 🐛 常见问题与解决方案

### 问题1：内存不足（大型场景）
```
错误：内存分配失败，进程被终止
```
**解决方案：**
```bash
# 大幅简化网格
--decimate 0.2
--target-face-num 500000
--remove-spurious 50  # 更积极的清理

# 或先分割场景
# 1. 先用DensifyPointCloud的--sub-scene-area分割点云
# 2. 分别重建每个子场景的网格
# 3. 最后合并网格
```

### 问题2：网格过于粗糙
```
重建的网格丢失了太多细节
```
**解决方案：**
```bash
# 减少简化，增加细节
--min-point-distance 1.0  # 更小的值保留更多细节
--decimate 0.9           # 减少简化程度
--free-space-support 1   # 启用自由空间支持

# 增加平滑迭代
--smooth 1              # 减少平滑，保留特征
```

### 问题3：网格中有孔洞
```
重建的网格有很多孔洞
```
**解决方案：**
```bash
# 增强孔洞闭合
--close-holes 50        # 增大值以闭合更大的孔洞
--free-space-support 1  # 启用自由空间支持

# 在DensifyPointCloud阶段生成更稠密的点云
# 返回并调整DensifyPointCloud参数：
# --number-views-fuse 2 (降低融合阈值)
# --resolution-level 0 (使用最高分辨率)
```

### 问题4：处理时间过长
```
网格重建需要数小时
```
**解决方案：**
```bash
# 增加简化，减少计算量
--decimate 0.4
--target-face-num 500000
--min-point-distance 3.0

# 使用GPU加速
--cuda-device 0

# 降低质量因子
--quality-factor 0.8
```

## 📊 参数调优建议表

| 场景类型 | decimate | min-point-distance | close-holes | smooth | 备注 |
|----------|----------|-------------------|-------------|--------|------|
| **建筑外观** | 0.4-0.6 | 2.5-3.0 | 30-50 | 2-3 | 大尺度，需要简化 |
| **室内场景** | 0.7-0.9 | 1.5-2.0 | 20-30 | 1-2 | 复杂结构，需保留细节 |
| **文物数字化** | 0.9-1.0 | 1.0-1.5 | 10-20 | 1 | 高细节要求，最小简化 |
| **人脸/肖像** | 0.8-0.9 | 1.0-1.5 | 10-15 | 1 | 需要平滑但保留特征 |
| **地形/景观** | 0.3-0.5 | 3.0-4.0 | 50-100 | 3 | 大范围，高度简化 |

## 🔍 网格质量评估与优化

### 评估网格质量
```bash
# 使用meshlab检查网格
meshlab mesh.ply

# 检查统计信息：
# 1. 面片数量（应适中，通常50万-200万）
# 2. 非流形边（应为0）
# 3. 孔洞数量
# 4. 自相交面片
```

### 迭代优化流程
```bash
# 第一次尝试：快速预览
ReconstructMesh -i scene.mvs -o mesh_v1.ply --decimate 0.3

# 检查结果，如果细节不足：
ReconstructMesh -i scene.mvs -o mesh_v2.ply --decimate 0.7 --min-point-distance 2.0

# 如果仍有孔洞：
ReconstructMesh -i scene.mvs -o mesh_v3.ply --decimate 0.7 --close-holes 40 --free-space-support 1

# 如果太粗糙：
ReconstructMesh -i scene.mvs -o mesh_v4.ply --decimate 0.9 --min-point-distance 1.5
```

## 📝 配置文件示例

创建`ReconstructMesh.cfg`：
```ini
# ReconstructMesh 配置文件
min-point-distance=2.5
decimate=0.7
remove-spurious=15
remove-spikes=1
close-holes=20
smooth=2
free-space-support=0
quality-factor=1.0
max-threads=0
cuda-device=0
export-type=ply
```

使用配置文件：
```bash
ReconstructMesh -i scene.mvs -c ReconstructMesh.cfg -o mesh.ply
```

## 💡 最佳实践建议

1. **从简化版本开始**：先用高简化系数（`--decimate 0.3`）快速查看整体效果，再逐步增加细节。

2. **关注关键参数**：`--min-point-distance` 和 `--decimate` 对结果影响最大，优先调整这两个参数。

3. **利用GPU加速**：如果可用，CUDA可以显著加速泊松重建过程。

4. **分阶段处理**：对于超大场景，考虑使用`DensifyPointCloud`的`--sub-scene-area`参数分割处理。

5. **后续处理**：`ReconstructMesh`生成的网格通常需要进一步优化：
   ```bash
   # 1. 网格细化（增加细节）
   RefineMesh -i mesh.ply -o mesh_refined.ply
   
   # 2. 纹理映射
   TextureMesh -i mesh_refined.ply -o mesh_textured.obj
   
   # 3. 简化（如果需要）
   # 使用Meshlab或Blender进行更精细的简化
   ```

6. **验证输入点云**：在网格重建前，确保点云质量良好：
   - 点云足够稠密
   - 没有明显的噪声和离群点
   - 法线方向一致

7. **监控进度**：使用`-v 3`获取更详细的进度信息：
   ```bash
   ReconstructMesh -i scene.mvs -o mesh.ply -v 3
   ```

通过合理调整这些参数，你可以在重建速度、内存使用和最终网格质量之间找到最佳平衡点。根据具体应用需求（实时渲染、3D打印、存档等）选择不同的参数组合。