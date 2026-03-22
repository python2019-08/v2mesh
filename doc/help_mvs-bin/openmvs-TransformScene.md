# 1.TransformScene -h

```sh
$ TransformScene -h
23:23:03 [App     ] OpenMVS x64 v2.3.0
23:23:03 [App     ] Build date: Feb 12 2026, 14:43:45
23:23:04 [App     ] CPU: Intel(R) Core(TM) i9-10900K CPU @ 3.70GHz (20 cores)
23:23:04 [App     ] RAM: 62.53GB Physical Memory 8.00GB Virtual Memory
23:23:04 [App     ] OS: Linux 6.17.0-14-generic (x86_64)
23:23:04 [App     ] Disk: 1023.83GB (1.79TB) space
23:23:04 [App     ] SSE & AVX compatible CPU & OS detected
23:23:04 [App     ] Command line: TransformScene -h
23:23:04 [App     ] Available options:

Generic options:
  -h [ --help ]                         produce this help message
  -w [ --working-folder ] arg           working directory (default current 
                                        directory)
  -c [ --config-file ] arg (=TransformScene.cfg)
                                        file name containing program options
  --export-type arg (=ply)              file type used to export the 3D scene 
                                        (ply, obj, glb or gltf)
  --archive-type arg (=4294967295)      project archive type: -1-interface, 
                                        0-text, 1-binary, 2-compressed binary
  --process-priority arg (=-1)          process priority (below normal by 
                                        default)
  --max-threads arg (=0)                maximum number of threads (0 for using 
                                        all available cores)
  -v [ --verbosity ] arg (=2)           verbosity level

Main options:
  -i [ --input-file ] arg               input scene filename
  -p [ --pointcloud-file ] arg          dense point-cloud with views file name 
                                        to transform (overwrite existing 
                                        point-cloud)
  -m [ --mesh-file ] arg                mesh file name to transform (overwrite 
                                        existing mesh)
  -o [ --output-file ] arg              output filename for storing the scene
  -a [ --align-file ] arg               input scene filename to which the scene
                                        will be cameras aligned
  -t [ --transform-file ] arg           input transform filename by which the 
                                        scene will transformed
  --transfer-texture-file arg           input mesh filename to which the 
                                        texture of the scene's mesh will be 
                                        transfered to (the two meshes should be
                                        aligned and the new mesh to have 
                                        UV-map)
  --indices-file arg                    input indices filename to be used with 
                                        ex. texture transfer to select a subset
                                        of the scene's mesh
  --compute-volume arg (=0)             compute the volume of the given 
                                        watertight mesh, or else try to 
                                        estimate the ground plane and assume 
                                        the mesh is bounded by it
  --plane-threshold arg (=0)            threshold used to estimate the ground 
                                        plane (<0 - disabled, 0 - auto, >0 - 
                                        desired threshold)
  --sample-mesh arg (=-300000)          uniformly samples points on a mesh (0 -
                                        disabled, <0 - number of points, >0 - 
                                        sample density per square unit)
  --max-resolution arg (=0)             make sure image resolution are not not 
                                        larger than this (0 - disabled)
  --up-axis arg (=2)                    scene axis considered to point upwards 
                                        (0 - x, 1 - y, 2 - z23:23:04 [App     ] MEMORYINFO: {
23:23:04 [App     ] 	VmPeak:	  249308 kB
23:23:05 [App     ] 	VmSize:	  249272 kB
23:23:05 [App     ] } ENDINFO
```

你现在展示的是 OpenMVS 中 `TransformScene` 工具的帮助信息，核心是想搞懂这个工具的功能、参数含义和实际用法，对吧？我先帮你把这些参数拆解清楚，再结合实际场景告诉你怎么用。

---
<!-- ------------------------------------- -->
<!-- -----------------doubaoAI-------------------- -->
## 一、核心功能总结
`TransformScene` 是 OpenMVS（多视图立体视觉库）的核心工具之一，主要作用是：
1. 对 3D 场景（包括相机位姿、点云、网格）进行**空间变换**（平移、旋转、缩放）；
2. 将一个场景的相机/点云/网格**对齐**到另一个参考场景；
3. 辅助处理：计算网格体积、采样网格点云、纹理迁移、调整场景坐标轴等；
4. 导出不同格式的 3D 场景文件（ply/obj/glb/gltf）。

简单说：它是 OpenMVS 里用来“调整 3D 场景空间姿态/格式”的工具。

---

## 二、关键参数详解（按用途分类，新手重点看标★的）
### 1. 基础通用参数（所有场景都可能用到）
| 参数 | 含义 | 实用说明 |
|------|------|----------|
| `-h / --help` | 显示帮助信息 | 就是你执行的这个命令，查参数用 |
| `-w / --working-folder` | 工作目录 | 指定临时文件/输出文件的路径，默认当前目录 |
| `-v / --verbosity` | 日志详细程度（默认2） | 0=极简，3=最详细（调试时用） |
| `--max-threads` | 最大线程数（默认0） | 0=用全部核心，建议设为CPU核心数（比如你的20核就设20） |
| `--export-type` | 导出文件格式（默认ply） | 常用：ply（点云/网格）、obj（带纹理网格）、glb/gltf（轻量化3D格式） |

### 2. ★核心输入输出参数（必须掌握）
| 参数 | 含义 | 实用说明 |
|------|------|----------|
| `-i / --input-file` | 输入的 OpenMVS 场景文件（.mvs/.mvsc） | **必选**：要处理的原始3D场景文件 |
| `-o / --output-file` | 输出的场景文件名 | **必选**：处理后的场景保存路径 |
| `-p / --pointcloud-file` | 要变换的稠密点云文件 | 用外部点云替换场景中原有的点云，并同步变换 |
| `-m / --mesh-file` | 要变换的网格文件 | 用外部网格替换场景中原有的网格，并同步变换 |

### 3. ★空间变换/对齐参数（核心功能）
| 参数 | 含义 | 实用说明 |
|------|------|----------|
| `-a / --align-file` | 参考场景文件 | 将 `-i` 的场景**对齐**到这个参考场景（比如把两个重建的场景拼在一起） |
| `-t / --transform-file` | 变换矩阵文件 | 用预定义的变换矩阵（4x4矩阵，txt格式）对场景做平移/旋转/缩放 |

### 4. 辅助功能参数（按需使用）
| 参数 | 含义 | 实用说明 |
|------|------|----------|
| `--compute-volume` | 计算网格体积（默认0） | 输入1：计算封闭网格的体积；输入2：估算地面平面后计算体积 |
| `--plane-threshold` | 地面平面估算阈值 | 配合`--compute-volume`用，0=自动估算，>0=自定义阈值 |
| `--sample-mesh` | 网格均匀采样点云 | 比如设为 `-100000`：从网格上采样10万个点生成点云 |
| `--up-axis` | 场景“向上”的坐标轴（默认2） | 0=x轴，1=y轴，2=z轴（匹配不同软件的坐标系，比如Blender用z轴向上） |
| `--transfer-texture-file` | 纹理迁移的目标网格 | 将原场景网格的纹理迁移到新网格（要求两个网格对齐且新网格有UV） |

---

## 三、新手常用示例（直接复制用）
### 示例1：将场景对齐到参考场景并导出OBJ格式
```bash
# 把 input.mvs 对齐到 reference.mvs，输出为 aligned_scene.mvs，同时导出OBJ格式
TransformScene -i input.mvs -a reference.mvs -o aligned_scene.mvs --export-type obj --max-threads 20
```

### 示例2：用变换矩阵调整场景并替换点云
```bash
# 用 transform.txt 里的4x4矩阵变换场景，替换为新的点云，输出新场景
TransformScene -i input.mvs -t transform.txt -p new_pointcloud.ply -o transformed_scene.mvs
```

### 示例3：计算网格体积（需网格是封闭的）
```bash
# 输入带网格的场景，计算体积并输出
TransformScene -i mesh_scene.mvs -o volume_scene.mvs --compute-volume 1 --plane-threshold 0
```

---

## 四、关键注意事项
1. 输入文件必须是 OpenMVS 格式（.mvs 或 .mvsc），不能直接输入ply/obj（需先用 `ConvertScene` 转换）；
2. 变换矩阵文件（`--transform-file`）是纯文本，格式为4行4列的浮点数（示例）：
   ```
   1.0 0.0 0.0 0.0
   0.0 1.0 0.0 0.0
   0.0 0.0 1.0 0.0
   0.0 0.0 0.0 1.0
   ```
   （这是单位矩阵，无变换；修改数值可实现平移/旋转/缩放）；
3. 对齐功能（`-a`）要求两个场景有重叠的相机/点云，否则对齐会失败；
4. 你的环境是 Linux + 20核i9 + 64G内存，适合处理大场景，建议`--max-threads`设为20以提速。

---

### 总结
1. `TransformScene` 核心是**空间变换/对齐** OpenMVS 3D场景，兼顾格式导出/体积计算等辅助功能；
2. 新手先掌握 `-i/-o/-a/-t` 核心参数，再按需用辅助功能；
3. 输入需是.mvs/.mvsc格式，变换矩阵需符合4x4格式，线程数建议设为CPU核心数。

如果你的目标是具体场景（比如“把两个重建的场景拼在一起”“调整场景坐标系”），可以告诉我，我直接给你对应的完整命令和参数配置。


