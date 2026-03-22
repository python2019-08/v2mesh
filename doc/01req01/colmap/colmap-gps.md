# 1.如何 导入GPS轨迹或IMU数据**作为COLMAP的初始位姿

在COLMAP中导入GPS/IMU作为初始位姿，核心是通过**位姿先验（pose_priors）** 或**位置先验（tvec_prior）** 注入数据，再用于SfM初始化或模型对齐。以下是完整可执行流程（含GPS/IMU两种场景、GUI/命令行、坐标系转换）。

---

## 一、核心概念与数据准备
### 1. 位姿格式（COLMAP要求）
- **6DoF位姿**：`qw, qx, qy, qz, tx, ty, tz`（四元数+平移，**世界→相机**）
- **位置先验**：`X, Y, Z`（相机中心，WGS84或局部笛卡尔）
- **IMU数据**：需先融合为**6DoF位姿**（含旋转+平移），COLMAP原生不直接读IMU原始数据

### 2. 数据预处理（必做）
1. **时间戳对齐**：图像与GPS/IMU时间戳严格同步（误差<20ms）
2. **坐标系转换**
   - GPS：WGS84（经纬度+海拔）→ ECEF/ENU（笛卡尔）
   - IMU：IMU坐标系 → 相机坐标系（需外参标定）
3. **格式标准化**：生成**位姿先验文件**或**位置先验文件**

---

## 二、方法1：导入GPS位置先验（最常用）
### 方式A：从图像EXIF自动读取（推荐）
1. 图像EXIF包含`GPSLatitude`/`GPSLongitude`/`GPSAltitude`
2. COLMAP特征提取时自动读取，存入数据库`images`表
3. 用于：**空间匹配加速**、**模型地理对齐**

### 方式B：手动导入位置先验文件（无EXIF）
#### 1. 准备位置文件（`image_pos.txt`）
格式：`图像名 经度 纬度 海拔`（WGS84）或 `图像名 X Y Z`（笛卡尔）
```
image_001.jpg 116.3975 39.9080 50.0
image_002.jpg 116.3980 39.9085 51.2
...
```

#### 2. 命令行导入
```bash
colmap import_position \
  --database_path project/database.db \
  --image_pos_path image_pos.txt \
  --ref_is_gps 1  # 1=WGS84，0=笛卡尔
```
- 数据存入：`images.tvec_prior`（3D位置先验）

---

## 三、方法2：导入完整6DoF位姿先验（GPS+IMU融合）
### 1. 准备位姿先验文件（`pose_priors.txt`）
格式：`图像名 qw qx qy qz tx ty tz`（**世界→相机**）
```
image_001.jpg 0.98 0.01 0.02 0.15 10.0 20.0 5.0
image_002.jpg 0.97 0.03 0.01 0.20 15.0 25.0 5.5
...
```

### 2. 导入位姿先验（命令行）
#### 方案A：使用官方脚本（推荐）
```bash
# COLMAP源码目录下
python scripts/python/database_manipulation.py \
  --database_path project/database.db \
  --add_pose_priors \
  --pose_priors_path pose_priors.txt
```
- 数据存入：`pose_priors`表（image_id, qw, qx, qy, qz, tx, ty, tz）

#### 方案B：SQLite直接写入（进阶）
```sql
INSERT INTO pose_priors (image_id, qw, qx, qy, qz, tx, ty, tz)
VALUES (1, 0.98, 0.01, 0.02, 0.15, 10.0, 20.0, 5.0);
```

---

## 四、方法3：GUI操作导入（可视化）
1. 打开COLMAP GUI → 新建项目（指定数据库+图像路径）
2. **提取特征**：`Processing → Extract Features`（自动读EXIF GPS）
3. **导入位姿/位置先验**
   - 位置先验：`Processing → Import Positions` → 选择`image_pos.txt`
   - 位姿先验：`Database → Edit Pose Priors` → 手动添加或导入文件
4. **重建时启用先验**
   - 增量重建：`Reconstruction → Start` → 勾选`Use pose priors`
   - 模型对齐：`Reconstruction → Align Reconstruction` → 选择先验源

---

## 五、使用先验进行SfM与模型对齐
### 1. 增量SfM（用先验初始化）
#### 命令行
```bash
colmap incremental_mapper \
  --database_path project/database.db \
  --image_path images \
  --output_path sparse \
  --use_pose_priors 1  # 启用位姿先验
```

### 2. 模型地理对齐（GPS→真实世界坐标）
#### 命令行（model_aligner）
```bash
colmap model_aligner \
  --input_path sparse/0 \
  --output_path sparse/0_geo \
  --database_path project/database.db \
  --ref_is_gps 1 \
  --alignment_type ecef  # 或 enu
  --alignment_max_error 3.0  # 先验误差容忍（米）
```
- 效果：模型获得**真实尺度+地理坐标**

---

## 六、IMU数据特殊处理流程
COLMAP不直接读IMU原始数据，需先融合为6DoF位姿：
1. **IMU预积分**：用EKF/因子图融合IMU+GPS，得到**相机6DoF位姿**
2. **外参标定**：获取`T_cam_imu`（IMU→相机变换）
3. **坐标转换**：IMU位姿 → 相机位姿（世界→相机）
4. **生成`pose_priors.txt`**，按方法2导入

---

## 七、关键参数与常见问题
### 1. 重要参数
- `--use_pose_priors 1`：重建时启用位姿先验
- `--ref_is_gps 1`：先验为WGS84（需转笛卡尔）
- `--alignment_type ecef/enu`：地理对齐坐标系
- `--pose_prior_weight`：先验权重（默认1.0，越大越信任先验）

### 2. 常见问题
- **先验不生效**：检查`pose_priors`表是否有数据、`use_pose_priors`是否开启
- **坐标系错误**：确保位姿是**世界→相机**（非相机→世界）
- **GPS漂移**：用RTK-GPS提升精度，或增大`alignment_max_error`

---

## 八、完整工作流（推荐）
1. 数据采集：同步图像+GPS+IMU
2. 预处理：时间对齐+坐标转换→生成`pose_priors.txt`/`image_pos.txt`
3. 建库：`colmap feature_extractor` + 导入先验
4. 匹配：`colmap exhaustive_matcher`（或空间匹配）
5. 重建：`incremental_mapper --use_pose_priors 1`
6. 对齐：`model_aligner`（GPS场景）

需要我帮你写一个**GPS/IMU位姿转换+导入COLMAP**的Python脚本（含WGS84转ENU、时间戳对齐、生成pose_priors.txt）吗？

