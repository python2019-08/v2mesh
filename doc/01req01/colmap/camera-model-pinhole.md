# 1.COLMAP 的 PINHOLE 或 SIMPLE_PINHOLE 相机模型

COLMAP 中的 **SIMPLE_PINHOLE** 和 **PINHOLE** 是两种最基础的**无畸变针孔相机模型**，适用于**已去畸变**的图像（如标定后、鱼眼校正后）。它们的核心区别在于**参数数量与假设**：**SIMPLE_PINHOLE 更简单、参数更少**；**PINHOLE 更通用、自由度更高**。

---

### 一、核心定义与参数

#### 1. SIMPLE_PINHOLE（ID: 0）
- **模型假设**：
  - 无任何镜头畸变（径向/切向）
  - **主点在图像中心**：`cx = width/2`，`cy = height/2`
  - **x/y 焦距相等**：`fx = fy = f`
- **参数数量**：**3 个**
  ```
  [f, cx, cy]
  ```
- **适用场景**：
  - 图像已严格去畸变
  - 相机为**标准画幅、无明显畸变**
  - 快速重建、参数少、不易过拟合

#### 2. PINHOLE（ID: 1）
- **模型假设**：
  - 无任何镜头畸变
  - **允许 fx ≠ fy**（非正方形像素/传感器）
  - **主点可自由估计**（不一定在中心）
- **参数数量**：**4 个**
  ```
  [fx, fy, cx, cy]
  ```
- **适用场景**：
  - 图像已去畸变，但**像素非正方形**
  - 主点可能偏离中心
  - 需要更精确的内参建模

---

### 二、参数对比表

| 模型 | ID | 参数个数 | 核心假设 | 适用图像 |
|---|---|---|---|---|
| **SIMPLE_PINHOLE** | 0 | 3 | fx=fy，cx=w/2，cy=h/2，无畸变 | 已去畸变、标准相机 |
| **PINHOLE** | 1 | 4 | fx≠fy 允许，cx/cy 自由，无畸变 | 已去畸变、非正方形像素 |

---

### 三、在 COLMAP 中的使用

#### 1. 命令行指定
```bash
# SIMPLE_PINHOLE
colmap feature_extractor --camera_model SIMPLE_PINHOLE ...

# PINHOLE
colmap feature_extractor --camera_model PINHOLE ...
```

#### 2. cameras.txt 格式示例
```text
# camera_id, model, width, height, params
1 SIMPLE_PINHOLE 1920 1080 2500.0 960.0 540.0
2 PINHOLE 1920 1080 2500.0 2498.0 958.0 542.0
```

---

### 四、选择建议

- **优先用 SIMPLE_PINHOLE**：
  - 图像已去畸变
  - 相机是普通手机/单反，像素接近正方形
  - 希望**少参数、快收敛、稳定**
- **改用 PINHOLE**：
  - 图像去畸变后仍有明显**非正方形像素**效应
  - 主点明显偏离中心（如工业相机、裁剪图）
  - SIMPLE_PINHOLE 重建结果**焦距/主点异常**
- **绝对不要用**：
  - 图像**有明显径向/切向畸变**（应改用 SIMPLE_RADIAL / RADIAL / OPENCV）

---

### 五、与其他模型的关系
- 两者均为**无畸变**模型，不包含 `k1, k2, p1, p2` 等畸变参数
- 若图像有畸变，直接用这两个模型会导致**重建精度下降、漂移**
- 更复杂的模型（如 SIMPLE_RADIAL、OPENCV）是在 PINHOLE 基础上增加畸变项

---

需要我帮你写一段可直接运行的 **COLMAP 命令行脚本**，自动按 **SIMPLE_PINHOLE / PINHOLE** 做特征提取与稀疏重建吗？