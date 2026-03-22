#!/bin/bash

openmvsBinDirPath=/home/abner/Documents/jobs/task/blender/task03v2mesh/3rd/openMVS/make02/bin
export PATH=$openmvsBinDirPath:$PATH

dataDirPath=/home/abner/0m/01

# -------------------------------
# 是否跳过  , true ,false
isSkip_InterfaceCOLMAP=true
isSkip_DensifyPointCloud=false
isSkip_ReconstructMesh=true
isSkip_RefineMesh=true
isSkip_TextureMesh=true

# -------------------------------
if [ "$isSkip_InterfaceCOLMAP" = "false" ]; then
    ${openmvsBinDirPath}/InterfaceCOLMAP   -w  ${dataDirPath}  \
                -i  ${dataDirPath}/frames_sharp  \
                -o  ${dataDirPath}/scene.mvs
fi
# -------------------------------
if [ "$isSkip_DensifyPointCloud" = "false" ]; then
    ${openmvsBinDirPath}/DensifyPointCloud  --cuda-device  -2  -w  ${dataDirPath}  \
            -i  ${dataDirPath}/scene.mvs  \
            -o  ${dataDirPath}/dense.mvs
fi 

# -------------------------------
if [ "$isSkip_ReconstructMesh" = "false" ]; then
    ${openmvsBinDirPath}/ReconstructMesh  --cuda-device  -2   -w  ${dataDirPath}  \
            -i  ${dataDirPath}/dense.mvs  \
            -o  ${dataDirPath}/mesh.mvs
fi 

# -------------------------------
if [ "$isSkip_RefineMesh" = "false" ]; then
    ${openmvsBinDirPath}/RefineMesh  --cuda-device  -2  -w  ${dataDirPath}  \
            -i  ${dataDirPath}/mesh.mvs  \
            -o  ${dataDirPath}/refinemesh.mvs
fi  

# -------------------------------
if [ "$isSkip_TextureMesh" = "false" ]; then
    ${openmvsBinDirPath}/TextureMesh  --cuda-device  -2  -w  ${dataDirPath}  \
            -i  ${dataDirPath}/refinemesh.mvs  \
            -o  ${dataDirPath}/texturedmesh.mvs
fi  