# 1.ply是什么格式

简单来说，PLY (Polygon File Format) 是一种专门为存储 3D 扫描数据（点云或多边形网格）而设计的标准文件格式。
在你目前的 OpenMVS/COLMAP 流程中，它是最核心的中间产物。以下是它的 3 个关键特征：
1. 它能存什么？
点云 (Point Cloud)：仅包含 3D 坐标 
，通常带有 RGB 颜色、法线（方向）和置信度。
网格 (Mesh)：除了点，还记录了哪些点连接成了三角形（面）。
自定义属性：它可以扩展存储任何数据，比如 OpenMVS 在稠密重建时会存入每个点的“可见视角数量”。
2. 两种存储形式
ASCII 模式：可以用记事本直接打开阅读。
特点：直观易读，但文件极大，读取慢。
Binary（二进制）模式：不可读。
特点：体积小，读取极快。COLMAP 和 OpenMVS 默认生成这种格式，因为它能高效处理你那 10 万个以上的 3D 点。
3. 在你工作流中的位置
COLMAP 输出：points3D.bin 导出后通常就是 sparse.ply。
OpenMVS 输出：DensifyPointCloud 产生的 scene_dense.ply 是带颜色的点云；ReconstructMesh 产生的 scene_mesh.ply 是带形状的网格。
互操作性：它是 3D 软件的“通用货币”。
Blender：直接导入查看形状。
MeshLab：查看点云质量、进行平滑处理的最强工具。
CloudCompare：比较不同算法生成的点云差异。