# pycolmap的api文档在哪里

目前 pycolmap 官方没有像 OpenCV 或 PyTorch 那样独立的网页版 HTML 文档。它的 API 主要通过 pybind11 直接从 C++ 映射到 Python。

你可以通过以下三个渠道获取最准确的参数说明：
### 1. 官方 GitHub 示例（最推荐）
官方仓库的 scripts/ 文件夹包含了最权威的调用范例：
pycolmap/scripts/python：涵盖了从特征提取到增量重建的全流程脚本。
### 2. Python 内置 help() 或 dir()
由于是动态绑定的，直接在终端查看对象属性是最快的方法：
```python
import pycolmap

# 查看所有可用的类和函数
print(dir(pycolmap))

# 查看具体配置项的参数（非常有用！）
help(pycolmap.ImageReaderOptions)
help(pycolmap.IncrementalPipelineOptions)
```

### 3. 查看 C++ 源码头文件
如果 Python 层的注释不够清晰，直接看对应的 C++ 绑定定义。
搜索 py::class_ 关键字，你可以看到每个 Python 类对应的 C++ 成员变量名称，这通常与 Options 对象中的属性完全一致。

### 特别提醒：PINHOLE 设置失效的根源
如果你在 ImageReaderOptions 中设置了 camera_model = 'PINHOLE' 但结果还是 SIMPLE_RADIAL，请检查：
是否删除了 database.db：COLMAP 极其依赖数据库缓存。
函数调用位置：必须在 extract_features 这一步传入 reader_options。
你需要我帮你查询某个具体函数（例如 incremental_mapping）的所有可选参数列表吗？