# 1.三维重建进展：从传统到深度学习方法全面梳理（上）
2021-06-06 18:25:40
https://www.bilibili.com/video/BV1wB4y1g7LH/?spm_id_from=333.337.search-card.all.click&vd_source=4212b105520112daf65694a1e5944e23

 

![alt text](< 3D-Reconstruction-advance01-img/02.3d-reconstruction-Overview.png>)

## 1.1 -3d重建的传统方法

### 1.1.1 rgbd
rgbd是指rgb和深度图的结合，深度图可以用深度传感器或者结构光等方法来获取。

![alt text](< 3D-Reconstruction-advance01-img/03rgbd04open-src-solutions.png>)

### 1.1.2 mvs
remark: 基于视频的多视图重建的位姿估计，可以用slam来估计，因为视频是序列化的图片所以。当然也可以用sfm来估计。
        对于从网上收集来的图片，因为没有时间序列所以不能用slam来估计位姿，只能用sfm来估计位姿。
![alt text](< 3D-Reconstruction-advance01-img/04mvs00.png>)        


* colmap
colmap包含sfm完整功能，以及部分mvs的功能。
![alt text](< 3D-Reconstruction-advance01-img/04mvs02fw01colmap00_sfm-mvs.png>)


* **openmvs**

![04mvs02fw02openmvs01](< 3D-Reconstruction-advance01-img/04mvs02fw02openmvs01.png>)


## 1.2 -3d重建的深度学习方法

### 1.2.1 单帧图像重建mesh 

 ![alt text](< 3D-Reconstruction-advance01-img/05dl00single-frame_reconstruct-mesh.png>)