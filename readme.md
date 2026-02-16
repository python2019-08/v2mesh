# <<v2mesh>>

# 1. how to setup env

```sh
$ conda create -n img-modeling python=3.10
# $ conda create -n road39modeling python=3.9
## ref: doc/Imagebased-modeling-solution2.md

#                                                                                            
# To activate this environment, use  
#             
$ conda activate img-modeling      
#
# To deactivate an active environment, use
#
# $ conda deactivate

$  python ./src/main_modeling.py

```

# 2. 3rd/ 
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
