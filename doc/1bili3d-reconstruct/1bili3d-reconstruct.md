# 1.三维重建(小白版) | OpenMVS环境配置+数据测试（VS2019+CMake+Colmap）

2023-04-03 18:37:09
https://www.bilibili.com/video/BV16h41137JK/?spm_id_from=333.1387.favlist.content.click&vd_source=4212b105520112daf65694a1e5944e23
利用开源OpenMVS框架进行三维重建，本视频记录纯依赖CMake进行第三方库的环境配置，并在数据集上进行测试，还包含部分debug过程。
上传仅为记录，有误地方请大家批评指正！

================================================
## x.0.openmvs github
![alt text](img/01openmv00-github.png)

<!-- ----------------------------------------- -->
==================================================
<!-- ----------------------------------------- -->

## x.1 openmvs cmakegui
![alt text](img/01openmv01-cmakegui01.png)
![alt text](img/01openmv01-cmakegui02.png)
![alt text](img/01openmv01-cmakegui03.png)
![alt text](img/01openmv01-cmakegui04.png)

<!-- ----------------------------------------- -->
==================================================
<!-- ----------------------------------------- -->
## x.2 openmvs + visual studio

![alt text](img/01openmv02-01vs.png)

![alt text](img/01openmv02-02cmake-modules.png)

![alt text](img/01openmv02-03bin-dir.png)

<!-- ----------------------------------------- -->
==================================================
<!-- ----------------------------------------- -->
## x.3 colmap-3.8-windows-no-cuda
![alt text](img/02colmap00-01win-no-cuda00.png)

![alt text](img/02colmap00-02workspace.png)
### x.3.1 create-db
![alt text](img/02colmap01create-db.png)

### x.3.2 Feature-extract
![alt text](img/02colmap02Feature-extract.png)
### x.3.3 Feature-matching
![alt text](img/02colmap03Feature-matching.png)
### x.3.3 reconstruct
![alt text](img/02colmap04reconstruct01.png)
![alt text](img/02colmap04reconstruct02.png)
![alt text](img/02colmap04reconstruct03.png)
![alt text](img/02colmap04reconstruct04.png)
![alt text](img/02colmap04reconstruct05.png)
![alt text](img/02colmap04reconstruct06.png)

### x.3.4 export-model
![alt text](img/02colmap05export-model01.png)
![alt text](img/02colmap05export-model02nvm.png)
![alt text](img/02colmap05export-model03txt.png)

<!-- ----------------------------------------- -->
==================================================
<!-- ----------------------------------------- -->

## x.4 openmvs
### x.4.1 InterfaceCOLMAP
![alt text](img/03openmvs01InterfaceCOLMAP.png)
### x.4.2 DensifyPointCloud
![alt text](img/03openmvs02DensifyPointCloud01.png)
![alt text](img/03openmvs02DensifyPointCloud02.png)
![alt text](img/03openmvs02DensifyPointCloud03.png)
### x.4.3 ReconstructMesh
![alt text](img/03openmvs03ReconstructMesh01.png)
![alt text](img/03openmvs03ReconstructMesh02.png)
![alt text](img/03openmvs03ReconstructMesh03.png)
![alt text](img/03openmvs03ReconstructMesh04.png)
### x.4.4 RefineMesh
![alt text](img/03openmvs04RefineMesh01.png)
![alt text](img/03openmvs04RefineMesh02.png)
![alt text](img/03openmvs04RefineMesh03.png)
### x.4.5 TextureMesh
![alt text](img/03openmvs05TextureMesh01.png)
![alt text](img/03openmvs05TextureMesh02.png)

























