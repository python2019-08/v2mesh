# 1. MVE 和 TexRecon的官方代码库链接
根据您的技术方案表格，您提到的 **MVE（Multi-View Environment）** 和 **TexRecon** 的官方代码库链接如下：

### 1. MVE（Multi-View Environment）
- **GitHub 仓库**：https://github.com/simonfuhrmann/mve
- **说明**：这是由 Simon Fuhrmann 维护的官方仓库。MVE 是达姆施塔特工业大学（TU Darmstadt）开发的多视图重建环境，包含完整的 SfM、MVS 和表面重建管线，其底层库和命令行工具非常适合集成到自动化流程中。

### 2. TexRecon（纹理重建工具）
- **GitHub 仓库**：https://github.com/nmoehrle/mvs-texturing
- **说明**：该项目通常被称为 `mvs-texturing`，其中的可执行程序即为 `texrecon`。它专门用于为已有的网格模型生成高质量、无缝的纹理贴图，通过全局能量最小化算法有效消除多视角合成时的阴影、接缝和反光问题。

### 使用建议
在您的流水线中，可以：
1. 使用 **MVE** 的 `makescene` 等工具进行数据准备和格式转换。
2. 使用 **TexRecon** 对 OpenMVS 生成的网格进行纹理映射，获得视觉效果统一的最终模型。

这两个项目都是学术和工业界广泛使用的开源标准工具，文档和社区支持都比较完善。