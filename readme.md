# <<v2mesh>>

# 1. how to setup  env

## 1.1 how to setup python env
```sh
$ conda create -n img-modeling python=3.10
# $ conda create -n road39modeling python=3.9
## ref: doc/Imagebased-modeling-solution2.md # 8.how-to-setup-env

#                                                                                            
# To activate this environment, use  
#             
$ conda activate img-modeling      
#
# To deactivate an active environment, use
#
# $ conda deactivate
# ------------------------------------------------------------
## 1. 核心算法庫環境 (Python 3.8 - 3.10)
# 基礎數值計算與圖像處理
# pip install open3d==0.17.0 numpy==1.23.5 pycolmap==0.6.1
pip install numpy==1.23.5
pip install opencv-python==4.8.0.76
pip install opencv-contrib-python==4.8.0.76  # 包含 SIFT/SURF 專利算法


# 核心 3D 處理與表面重建 (取代手寫泊松重建)
pip install open3d==0.17.0

# 學術級 SfM 接口 (COLMAP 的 Python 綁定)
# pip install pycolmap==0.4.0
# 如果 0.4.0 無法安裝或報錯，建議使用這個更現代的版本
# pip uninstall pycolmap -y
# pip install pycolmap==0.6.1
 pip install pycolmap-cuda==3.13.0.dev2


# 點雲與網格的高級操作 (輔助 Open3D)
pip install trimesh[easy]==3.23.5
pip install plyfile==1.0.1

# ------------------------------------------------------------
## 2. GPU 加速依賴 (關鍵)
# 重建算法极度依赖 CUDA，需先安装匹配版本的 NVIDIA 驱动，再安装以下库：
# 注意：cu121 完美兼容你的 12.8 驅動，是目前最推薦的穩定組合
pip install torch==2.1.0 torchvision==0.16.0 torchaudio==2.1.0 --index-url https://download.pytorch.org/whl/cu121

# 修正 2：CuPy 的安裝
# 雖然 12.8 是驅動版本，但 CuPy 官方目前最高對標是 cuda12x（對應 12.0-12.7）
# 它在 12.8 下通常可以運行，若報錯，需手動指定版本
pip install cupy-cuda12x==12.2.0
# ------------------------------------------------------------
## 3. 數據管理與可視化 (開發調試用)
pip install matplotlib==3.7.2
 # 進度條顯示
pip install tqdm==4.66.1 
# 矩陣平差輔助
pip install scipy==1.10.1  
# ------------------------------------------------------------
```

## 1.2 how to build openmvs
doc/build_openmvs.md


<!-- -------------------------------------------------- -->
# 2 how to run
```sh
$ python src/main_modeling.py
```

<!-- -------------------------------------------------- -->
# 3. 3rd/ 
```sh
(img-modeling) abner@abner-XPS:~/Documents/jobs/task/task-blender/task03v2mesh$ ls
3rd  dat  doc  docker  readme.md  src  t1.txt  t2.txt  tools 
(img-modeling) abner@abner-XPS:~/Documents/jobs/task/task-blender/task03v2mesh$ ls -l 3rd/
总计 36
drwxrwxr-x 11 abner abner 4096  2月 13 14:23 colmap
drwxrwxr-x 18 abner abner 4096  2月  9 12:29 eigen
-rw-rw-r--  1 abner abner   85  2月  8 14:49 git-urls
drwxrwxr-x  8 abner abner 4096  2月 12 07:40 openMVG--
drwxrwxr-x 12 abner abner 4096  2月 12 14:20 openMVS
drwxrwxr-x  4 abner abner 4096  2月 14 12:31 openMVS_sample
-rw-------  1 abner abner 4944  2月 15 14:13 ReconstructMesh-260215141323958FEC.log
drwxrwxr-x 10 abner abner 4096  2月 11 23:46 vcglib-- 
```


### git repositories of 3rd
https://github.com/colmap/colmap.git  

https://gitlab.com/libeigen/eigen.git  

https://github.com/cnr-isti-vclab/vcglib.git 

https://github.com/cdcseacave/openMVS.git

https://github.com/cdcseacave/openMVS_sample.git



