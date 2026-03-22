# 1.TextureMesh -h

```sh
3rd/openMVS/make02/bin$ ./TextureMesh -h
23:02:52 [App     ] OpenMVS x64 v2.4.0
23:02:52 [App     ] Build date: Feb 22 2026, 20:37:13
23:02:52 [App     ] CPU: Intel(R) Core(TM) i9-10900K CPU @ 3.70GHz (20 cores)
23:02:52 [App     ] RAM: 62.53GB Physical Memory 8.00GB Virtual Memory
23:02:52 [App     ] OS: Linux 6.17.0-14-generic (x86_64)
23:02:52 [App     ] Disk: 1020.29GB (1.79TB) space
23:02:52 [App     ] SSE & AVX compatible CPU & OS detected
23:02:52 [App     ] Command line: TextureMesh -h
23:02:52 [App     ] Available options:

Generic options:
  -h [ --help ]                         produce this help message
  -w [ --working-folder ] arg           working directory (default current 
                                        directory)
  -c [ --config-file ] arg (=TextureMesh.cfg)
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
  --cuda-device arg (=-1)               CUDA device number to be used to 
                                        texture the mesh (-2 - CPU processing, 
                                        -1 - best GPU, >=0 - device index)

Texture options:
  -i [ --input-file ] arg               input filename containing camera poses 
                                        and image list
  -m [ --mesh-file ] arg                mesh file name to texture (overwrite 
                                        existing mesh)
  -o [ --output-file ] arg              output filename for storing the mesh
  --decimate arg (=1)                   decimation factor in range [0..1] to be
                                        applied to the input surface before 
                                        refinement (0 - auto, 1 - disabled)
  --close-holes arg (=30)               try to close small holes in the input 
                                        surface (0 - disabled)
  --resolution-level arg (=0)           how many times to scale down the images
                                        before mesh refinement
  --min-resolution arg (=640)           do not scale images lower than this 
                                        resolution
  --outlier-threshold arg (=0.0599999987)
                                        threshold used to find and remove 
                                        outlier face textures (0 - disabled)
  --cost-smoothness-ratio arg (=0.100000001)
                                        ratio used to adjust the preference for
                                        more compact patches (1 - best 
                                        quality/worst compactness, ~0 - worst 
                                        quality/best compactness)
  --virtual-face-images arg (=0)        generate texture patches using virtual 
                                        faces composed of coplanar triangles 
                                        sharing at least this number of views 
                                        (0 - disabled, 3 - good value)
  --global-seam-leveling arg (=1)       generate uniform texture patches using 
                                        global seam leveling
  --local-seam-leveling arg (=1)        generate uniform texture patch borders 
                                        using local seam leveling
  --texture-size-multiple arg (=0)      texture size should be a multiple of 
                                        this value (0 - power of two)
  --patch-packing-heuristic arg (=3)    specify the heuristic used when 
                                        deciding where to place a new patch (0 
                                        - best fit, 3 - good speed, 100 - best 
                                        speed)
  --empty-color arg (=16744231)         color used for faces not covered by any
                                        image
  --sharpness-weight arg (=0.5)         amount of sharpness to be applied on 
                                        the texture (0 - disabled)
  --orthographic-image-resolution arg (=0)
                                        orthographic image resolution to be 
                                        generated from the textured mesh - the 
                                        mesh is expected to be already 
                                        geo-referenced or at least properly 
                                        oriented (0 - disabled)
  --ignore-mask-label arg (=-1)         label value to ignore in the image 
                                        mask, stored in the MVS scene or next 
                                        to each image with '.mask.png' 
                                        extension (-1 - auto estimate mask for 
                                        lens distortion, -2 - disabled)
  --max-texture-size arg (=8192)        maximum texture size, split it in 
                                        multiple textures of this size if 
                                        needed (0 - unbounded23:02:52 [App     ] MEMORYINFO: {
23:02:52 [App     ] 	VmPeak:	  253440 kB
23:02:52 [App     ] 	VmSize:	  253404 kB
23:02:52 [App     ] } ENDINFO
```

<!-- ------------------doubaoAI--------------------------- -->
你现在展示的是 OpenMVS 中 `TextureMesh` 工具的帮助信息，核心是想搞懂这个工具的功能、关键参数含义，以及如何用它给你生成的 mesh 贴纹理（解决 960x540 视频重建后 mesh 无纹理/纹理差的问题）。我会按「核心功能→关键参数→实战命令→调优技巧」的逻辑讲，完全贴合你之前的低分辨率视频重建场景。

---

## 一、核心功能总结
`TextureMesh` 是 OpenMVS 中**给 3D 网格（mesh）贴纹理**的核心工具，也是重建流程的最后一步，核心作用：
> 1. 从原始图像（视频抽帧）中提取纹理，映射到生成的 mesh 表面；
> 2. 优化纹理拼接（消除接缝、均匀亮度）；
> 3. 修复 mesh 小孔洞、简化网格（降面数）；
> 4. 导出带纹理的 mesh（ply/obj/glb/gltf 格式），可直接用于 Blender/Unity 等软件。

简单说：它能让你之前生成的 `scene_dense_mesh.ply` 从“灰色网格”变成“带真实图像纹理的彩色网格”。

---

## 二、关键参数详解（按用途分类，低分辨率场景重点看标★的）
### 1. 基础通用参数（和其他 OpenMVS 工具一致）
| 参数 | 含义 | 实用说明（960x540 场景） |
|------|------|--------------------------|
| `-h / --help` | 显示帮助 | 你执行的命令，查参数用 |
| `-w / --working-folder` | 工作目录 | 指定临时文件/输出路径，建议设为你的 mvs 目录：`/home/abner/1v2m/mvs` |
| `--max-threads` | 最大线程数 | 设为 20（你的 CPU 核心数），提速明显 |
| `--cuda-device` | CUDA 设备 | -1=自动选最佳 GPU（有 GPU 必开，纹理映射速度快10倍+）；-2=纯 CPU |
| `--export-type` | 导出格式 | 优先选 `obj`（带纹理，Blender 兼容最好），其次 `glb`（轻量化） |
| `-v / --verbosity` | 日志详细度 | 设为 3（调试时看详细日志，定位纹理问题） |

### 2. ★核心输入输出参数（必须指定）
| 参数 | 含义 | 实用说明 |
|------|------|----------|
| `-i / --input-file` | 输入 MVS 场景文件 | 必选：你的场景文件 `scene_dense_mesh.mvs`（关联相机位姿和原始图像） |
| `-m / --mesh-file` | 要贴纹理的 mesh 文件 | 可选：如果想替换场景中的 mesh，指定你的 `scene_dense_mesh.ply`；不指定则用场景内的 mesh |
| `-o / --output-file` | 输出带纹理的 mesh 文件 | 必选：比如 `scene_textured.mvs`，最终会生成对应的 `scene_textured.ply/obj` |

### 3. ★纹理质量/适配低分辨率的关键参数（重点调）
| 参数 | 含义 | 960x540 场景推荐值 | 作用 |
|------|------|--------------------|------|
| `--resolution-level` | 图像缩放倍数（0=原图） | 0 | 低分辨率视频别缩放，用原始 960x540 图像（缩放会丢失纹理细节） |
| `--min-resolution` | 图像最小分辨率 | 540 | 确保图像不被缩到低于 540p（匹配你的视频分辨率） |
| `--max-texture-size` | 最大纹理尺寸 | 4096 | 低分辨率场景设 4096 足够（默认 8192 会浪费内存），超出会自动分块 |
| `--sharpness-weight` | 纹理锐化权重 | 0.8 | 增大锐化（默认 0.5），弥补低分辨率图像的细节不足 |
| `--outlier-threshold` | 纹理离群值阈值 | 0.1 | 放宽阈值（默认 0.06），保留更多弱纹理（低分辨率易被判定为离群） |
| `--cost-smoothness-ratio` | 纹理块紧凑度 | 0.5 | 增大比值（默认 0.1），优先纹理质量而非块紧凑度（低分辨率需优先保质量） |

### 4. 网格修复/优化参数（适配稀疏 mesh）
| 参数 | 含义 | 推荐值 | 作用 |
|--------------------------|------------|--------|------|
| `--close-holes`          | 关闭小孔洞   | 50     | 增大阈值（默认 30），修复低分辨率重建的 mesh 孔洞 |
| `--decimate`             | 网格简化因子 | 1.0    | 设为 1（禁用简化），低分辨率 mesh 本身面数少，无需简化 |
| `--global-seam-leveling` | 全局接缝平整 | 1      | 开启（默认 1），消除纹理拼接的明显接缝 |
| `--local-seam-leveling`  | 局部接缝平整 | 1      | 开启（默认 1），优化纹理块边缘的亮度均匀性 |

### 5. 其他实用参数
| 参数 | 含义 | 说明 |
|------|------|------|
| `--empty-color` | 无纹理区域颜色 | 默认值即可（浅灰色），低分辨率场景可能有少量无纹理区域 |
| `--virtual-face-images` | 虚拟面纹理 | 3 | 设为 3，用多视图合成虚拟纹理，填补纹理空缺 |

---

## 三、实战命令（适配你的场景，直接复制运行）
针对你之前生成的 `scene_dense_mesh.ply`，执行以下命令给 mesh 贴纹理：
```bash
# 给低分辨率重建的 mesh 贴纹理（适配 960x540 视频）
/mnt/disk2/abner/zdev/jobs/task/blender/task03v2mesh/3rd/openMVS/make/bin/TextureMesh \
  --input-file /home/abner/1v2m/mvs/scene_dense_mesh.mvs \
  --output-file /home/abner/1v2m/mvs/scene_textured.mvs \
  --working-folder /home/abner/1v2m/mvs \
  --export-type obj \  # 导出 obj 格式（带纹理，方便后续使用）
  --max-threads 20 \
  --cuda-device -1 \  # 用 GPU 加速（有 GPU 必开）
  --resolution-level 0 \
  --min-resolution 540 \
  --max-texture-size 4096 \
  --sharpness-weight 0.8 \
  --outlier-threshold 0.1 \
  --cost-smoothness-ratio 0.5 \
  --close-holes 50 \
  --decimate 1.0 \
  --virtual-face-images 3 \
  --global-seam-leveling 1 \
  --local-seam-leveling 1 \
  -v 3  # 输出详细日志，方便排查问题
```

### 命令执行后会生成的文件：
1. `scene_textured.mvs`：场景配置文件；
2. `scene_textured.obj`：带纹理的 mesh（核心文件，可直接导入 Blender）；
3. `scene_textured_0.jpg`（或 png）：纹理贴图文件（和 obj 配套）；
4. 若纹理尺寸超 4096，会生成 `scene_textured_1.jpg`/`scene_textured_2.jpg` 等分块纹理。

---

## 四、低分辨率场景调优技巧（纹理差/无纹理时用）
如果执行后纹理模糊/有黑块/缺失，按以下顺序调参：
1. **纹理模糊**：增大 `--sharpness-weight` 到 1.0，同时确保 `--resolution-level=0`；
2. **纹理有接缝**：将 `--global-seam-leveling` 和 `--local-seam-leveling` 都设为 2；
3. **部分区域无纹理**：增大 `--virtual-face-images` 到 5，放宽 `--outlier-threshold` 到 0.15；
4. **mesh 有孔洞导致纹理断裂**：先运行 `RefineMesh` 修复孔洞，再执行 `TextureMesh`；
5. **速度慢/内存不足**：降低 `--max-texture-size` 到 2048，`--max-threads` 降到 16。

---

## 五、常见问题排查
1. **提示“no images found”**：检查 `scene_dense_mesh.mvs` 是否关联了原始图像（抽帧后的增强图像），确保图像路径正确；
2. **纹理全黑/全灰**：`--empty-color` 被触发，说明纹理映射失败，需重新检查 COLMAP 稀疏重建的相机位姿是否正确；
3. **GPU 报错**：将 `--cuda-device` 设为 -2（纯 CPU 运行），虽然慢但稳定。

---

### 总结
1. `TextureMesh` 核心是给 mesh 贴纹理，低分辨率场景需**禁用图像缩放、增大锐化、放宽离群阈值**；
2. 实战命令优先选 `obj` 导出格式，开启 GPU 加速，修复 mesh 孔洞；
3. 纹理质量差时，先检查相机位姿，再按“锐化→接缝→虚拟纹理”的顺序调参；
4. 最终生成的 `scene_textured.obj` + 配套纹理图，是可直接使用的带纹理 3D 模型。

如果需要将“生成 mesh→修复 mesh→贴纹理”整合成一个一键执行的 bash 脚本，我可以帮你写好，直接运行就能完成全流程。

<!-- ---------------------------------------------- -->
=======================================================
<!-- ---------------------------------------------- -->
# 2.TextureMesh 命令需要输入 .mvs 场景文件，但目前只有 scene_dense_mesh.ply

你现在的核心问题是：`TextureMesh` 命令需要输入 `.mvs` 场景文件，但目前只有 `scene_dense_mesh.ply` 网格文件，我先告诉你**两种解决方法**（优先用方法1，简单且适配你的场景），确保能顺利执行纹理贴图。

---

## 核心原因
`.mvs` 文件是 OpenMVS 的**场景描述文件**，包含相机位姿、图像路径、点云/网格关联信息；而 `.ply` 只是纯几何文件（顶点/面），没有纹理映射所需的“图像-网格”关联信息。
解决思路：要么**重建 `.mvs` 场景文件**，要么**直接指定 `.ply` 作为输入网格**。

---

## 方法1：最简方案（直接指定 ply 网格，无需 mvs 文件）
修改 `TextureMesh` 命令，用 `-m/--mesh-file` 参数直接指定 `scene_dense_mesh.ply`，同时将原始的 `scene.mvs`（稠密重建前的场景文件）作为输入（这个文件你一定有，包含相机和图像信息）。

### 修正后的完整命令（直接复制运行）
```bash
/mnt/disk2/abner/zdev/jobs/task/blender/task03v2mesh/3rd/openMVS/make/bin/TextureMesh \
  --input-file /home/abner/1v2m/mvs/scene.mvs \  # 用原始场景文件（含相机/图像信息）
  --mesh-file /home/abner/1v2m/mvs/scene_dense_mesh.ply \  # 直接指定ply网格
  --output-file /home/abner/1v2m/mvs/scene_textured.mvs \
  --working-folder /home/abner/1v2m/mvs \
  --export-type obj \
  --max-threads 20 \
  --cuda-device -1 \
  --resolution-level 0 \
  --min-resolution 540 \
  --max-texture-size 4096 \
  --sharpness-weight 0.8 \
  --outlier-threshold 0.1 \
  --cost-smoothness-ratio 0.5 \
  --close-holes 50 \
  --decimate 1.0 \
  --virtual-face-images 3 \
  --global-seam-leveling 1 \
  --local-seam-leveling 1 \
  -v 3
```

### 关键修改说明：
1. `--input-file`：改为你最初的 `scene.mvs`（稠密重建前的场景文件，包含相机位姿、原始图像路径，这是纹理映射的核心）；
2. `--mesh-file`：新增参数，直接指定你的 `scene_dense_mesh.ply` 网格文件；
3. 其他参数不变，保持适配低分辨率场景的优化配置。

---

## 方法2：手动生成 .mvs 场景文件（备用方案）
如果方法1提示“找不到相机信息”，先通过 `ConvertScene` 工具将 `ply` 网格整合到 `scene.mvs` 中，生成包含网格的新 `.mvs` 文件：

### 步骤1：生成带网格的 .mvs 文件
```bash
/mnt/disk2/abner/zdev/jobs/task/blender/task03v2mesh/3rd/openMVS/make/bin/ConvertScene \
  --input-file /home/abner/1v2m/mvs/scene.mvs \
  --output-file /home/abner/1v2m/mvs/scene_with_mesh.mvs \
  --mesh-file /home/abner/1v2m/mvs/scene_dense_mesh.ply \
  --working-folder /home/abner/1v2m/mvs
```

### 步骤2：执行 TextureMesh（用新生成的 .mvs 文件）
```bash
/mnt/disk2/abner/zdev/jobs/task/blender/task03v2mesh/3rd/openMVS/make/bin/TextureMesh \
  --input-file /home/abner/1v2m/mvs/scene_with_mesh.mvs \
  --output-file /home/abner/1v2m/mvs/scene_textured.mvs \
  --working-folder /home/abner/1v2m/mvs \
  --export-type obj \
  --max-threads 20 \
  --cuda-device -1 \
  --resolution-level 0 \
  --min-resolution 540 \
  --max-texture-size 4096 \
  --sharpness-weight 0.8 \
  --outlier-threshold 0.1 \
  --cost-smoothness-ratio 0.5 \
  --close-holes 50 \
  --decimate 1.0 \
  --virtual-face-images 3 \
  --global-seam-leveling 1 \
  --local-seam-leveling 1 \
  -v 3
```

---

## 关键验证：确保 scene.mvs 有效
执行命令前，先确认 `scene.mvs` 存在且包含图像信息：
```bash
# 查看 scene.mvs 的内容（确认有图像路径）
cat /home/abner/1v2m/mvs/scene.mvs | grep "Image"
```
如果输出中有类似 `Image path="enhanced_frames/frame_000000.jpg"` 的行，说明 `scene.mvs` 有效；如果没有，需重新检查 COLMAP 转 OpenMVS 的步骤（确保图像路径正确）。

---

## 常见问题排查
1. **提示“mesh has no texture coordinates”**：正常，`TextureMesh` 会自动为 ply 网格生成 UV 纹理坐标，无需额外处理；
2. **纹理映射失败/全黑**：
   - 检查 `scene.mvs` 中的图像路径是否是绝对路径（低分辨率场景建议用绝对路径，避免找不到图像）；
   - 确保抽帧后的图像（enhanced_frames）都存在，且路径无中文/空格；
3. **GPU 报错**：将 `--cuda-device` 改为 -2（纯 CPU 运行），虽然速度慢，但能避开 GPU 驱动问题。

---

### 总结
1. 核心解决方案：用 `--mesh-file` 直接指定 `scene_dense_mesh.ply`，同时将原始 `scene.mvs` 作为 `--input-file`（提供相机/图像信息）；
2. 备用方案：先通过 `ConvertScene` 将 ply 整合到 mvs 场景文件中，再执行纹理贴图；
3. 关键前提：`scene.mvs` 必须包含正确的相机位姿和图像路径，否则纹理映射会失败。

执行修正后的命令后，会生成 `scene_textured.obj` 和配套的纹理贴图，这就是你需要的带纹理的 3D 模型。