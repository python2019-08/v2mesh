# fatal error: glad/glad.h: 没有那个文件或目录

```sh
In file included from /mnt/disk2/abner/zdev/jobs/task/blender/task03v2mesh/3rd/openMVS/make02/apps/Viewer/CMakeFiles/Viewer.dir/cmake_pch.hxx:5,
                 from <command-line>:
/mnt/disk2/abner/zdev/jobs/task/blender/task03v2mesh/3rd/openMVS/apps/Viewer/Common.h:42:10: fatal error: glad/glad.h: 没有那个文件或目录
   42 | #include <glad/glad.h>
      |          ^~~~~~~~~~~~~
compilation terminated.
```

### 核心需求理解
你在编译OpenMVS的Viewer模块时，编译器提示找不到`glad/glad.h`头文件，这是因为glad的头文件路径未被正确添加到Viewer模块的编译包含目录中，导致编译器无法定位到该头文件。需要修正CMake配置，确保Viewer模块能识别glad的头文件路径。
  
#### 步骤1：重新生成完整的glad代码 
如果`glad.h`缺失，重新生成glad（确保包含核心头文件）：

<!-- https://github.com/Dav1dde/glad?tab=readme-ov-file -->

glad1 generator:   https://glad.dav1d.de/

##### 步骤2：3rd/openMVS/3rd/glad/CMakeLists.txt
```sh
CMAKE_MINIMUM_REQUIRED(VERSION 3.18)

PROJECT(OpenMVS LANGUAGES C)

# 配置编译选项
set(CMAKE_C_STANDARD 99)
set(CMAKE_C_STANDARD_REQUIRED ON)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

if(CMAKE_CROSSCOMPILING)
  message(STATUS "Cross-compiling: "
    "${CMAKE_HOST_SYSTEM_NAME}/${CMAKE_HOST_SYSTEM_PROCESSOR} -> "
    "${CMAKE_SYSTEM_NAME}/${CMAKE_SYSTEM_PROCESSOR}")
else()
  message(STATUS "**NOT** Cross-compiling: "
    "${CMAKE_HOST_SYSTEM_NAME}/${CMAKE_HOST_SYSTEM_PROCESSOR} -> "
    "${CMAKE_SYSTEM_NAME}/${CMAKE_SYSTEM_PROCESSOR}")    
endif()

# ----------------------------------------------------
include(GNUInstallDirs)
set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/${CMAKE_INSTALL_LIBDIR})
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/${CMAKE_INSTALL_LIBDIR})
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/${CMAKE_INSTALL_BINDIR})

# ----------------------------------------------------
set(CUDA_ENABLED OFF)
# 手动指定glad的头文件和源码路径
MESSAGE(STATUS "glad-path==${CMAKE_SOURCE_DIR}")
set(GLAD_INCLUDE_DIR "${CMAKE_SOURCE_DIR}/include")
set(GLAD_SRC "${CMAKE_SOURCE_DIR}/src/glad.c")

# 生成glad静态库
add_library(glad STATIC ${GLAD_SRC})
target_include_directories(glad PUBLIC ${GLAD_INCLUDE_DIR})
```

##### 步骤3：修正Viewer模块的CMake配置（强制添加glad包含路径）
编辑`3rd/openMVS/apps/Viewer/CMakeLists.txt`，在glad配置后**手动添加glad的包含路径到Viewer目标**（兜底保障）：
```sh
set(CUDA_ENABLED OFF)
# 1. 指定已编译好的glad库路径（关键：指向单独编译的libglad.a）
MESSAGE(STATUS "glad-path==${CMAKE_SOURCE_DIR}/3rd/glad")
set(GLAD_INCLUDE_DIR "${CMAKE_SOURCE_DIR}/3rd/glad/include") 
set(GLAD_LIB "${CMAKE_SOURCE_DIR}/3rd/glad/build/lib/libglad.a")
# 2. 验证库文件是否存在（避免链接错误）
if(NOT EXISTS ${GLAD_LIB})
    message(FATAL_ERROR "Precompiled glad library not found at: ${GLAD_LIB}")
endif()
# 3. 创建IMPORTED目标（链接外部已编译的glad库）
add_library(glad::glad STATIC IMPORTED GLOBAL)
# 指定已编译的库文件路径
set_target_properties(glad::glad PROPERTIES
    IMPORTED_LOCATION "${GLAD_LIB}"
    INTERFACE_INCLUDE_DIRECTORIES "${GLAD_INCLUDE_DIR}"  # 传递头文件路径
    LINKER_LANGUAGE C  # 强制C语言链接
    CUDA_RESOLVE_DEVICE_SYMBOLS OFF  # 彻底禁用CUDA
    CUDA_ARCHITECTURES ""
)
# 4. 标记glad已找到，兼容原有逻辑
set(glad_FOUND TRUE)
MESSAGE(STATUS "GLAD (precompiled static lib) found: ${GLAD_LIB}")
# Find required packages
# FIND_PACKAGE(glad QUIET)
if(glad_FOUND)
	MESSAGE(STATUS "GLAD ${glad_VERSION} found")
else()
	MESSAGE("-- Can't find GLAD. Continuing without it.")
	RETURN()
endif()
```

<!-- 

```cmake
# 原有glad配置（保留）
set(GLAD_INCLUDE_DIR "${CMAKE_SOURCE_DIR}/3rd/glad/include")
add_library(glad INTERFACE)
target_include_directories(glad INTERFACE ${GLAD_INCLUDE_DIR})
add_library(glad::glad ALIAS glad)
set(glad_FOUND TRUE) 

# 新增：手动将glad包含路径添加到Viewer模块的全局包含目录
include_directories(${GLAD_INCLUDE_DIR})

# 后续原有代码...
FIND_PACKAGE(GLFW3 QUIET)
# ...其他依赖配置...

# 找到Viewer目标的定义处（通常是cxx_executable_with_flags），确保链接glad::glad
# 示例：如果Viewer目标是这样定义的，确保链接glad
# cxx_executable_with_flags(Viewer "Apps" ${SOURCE_FILES} ${LINK_LIBRARIES} glad::glad)
``` 
-->

##### 步骤4：编译glad

3rd/openMVS/3rd/glad/build-glad.sh的内容
```sh
# 3rd/openMVS/3rd/glad/build-glad.sh
BuildDIR_lib=build     
CMAKE_BUILD_TYPE=Release
cmake -S. -B ${BuildDIR_lib} \
        -DCMAKE_INSTALL_PREFIX=${CMAKE_BINARY_DIR}/install_zstd  \
        -DCMAKE_POSITION_INDEPENDENT_CODE=ON \
        -DCMAKE_BUILD_TYPE=${CMAKE_BUILD_TYPE}   \
        -DBUILD_SHARED_LIBS=OFF     \
        -DCMAKE_C_FLAGS="-fPIC" \
        -DCMAKE_CXX_FLAGS="-fPIC" 

echo "-------------------------"
cmake --build ${BuildDIR_lib} -j$(nproc)  -v
```

```sh
cd 3rd/openMVS/3rd/glad/
./build-glad.sh
```

##### 步骤4：清理缓存并重新编译
```bash
# 进入构建目录
cd  task03v2mesh/3rd/openMVS/make02

# 彻底清理缓存
rm -rf CMakeCache.txt CMakeFiles/

# 重新配置CMake（建议暂时禁用Viewer，先确保核心库编译通过）
cmake .. \
-DCMAKE_PREFIX_PATH=/usr/lib/x86_64-linux-gnu \
-DCMAKE_BUILD_TYPE=Release \
-DVCG_ROOT=/home/abner/zdev/jobs/task/blender/task03v2mesh/3rd/openMVS/libs/vcglib \
-DCMAKE_CXX_STANDARD=17 \
-DCMAKE_CXX_FLAGS="-w" \
-DBUILD_SHARED_LIBS=OFF \
-DOpenMVS_USE_CUDA=ON \
-DOpenMVS_BUILD_APPS=ON \
-DOpenMVS_BUILD_VIEWER=OFF  # 先禁用Viewer，编译核心库

# 编译核心库
cmake --build . -j8
```
 
<!-- ------------------------------------------ -->
====================================================

# 2.glad/glad.h

你想了解的是 `glad/glad.h` 这个头文件相关的知识，它是 OpenGL 开发中非常核心的一个工具头文件，主要用于加载 OpenGL 的函数指针。

### 一、什么是 glad/glad.h
`glad` 是一个开源的 OpenGL 加载库（替代了老旧的 GLEW），`glad/glad.h` 是它的核心头文件，作用是：
1. 自动检测你的系统/显卡支持的 OpenGL 版本；
2. 加载对应版本的 OpenGL 核心函数指针（因为 OpenGL 的核心函数不会直接暴露在标准头文件中，需要手动加载）；
3. 替代原生的 `GL/gl.h`/`GL/glu.h`，避免重复定义冲突。

简单来说：没有 glad，你无法直接调用 OpenGL 3.0+ 的核心函数（比如 `glCreateShader`、`glGenVertexArrays` 等）。

### 二、如何使用 glad/glad.h
#### 1. 前置准备
- 先从 [Glad 官方生成器](https://glad.dav1d.de/) 下载适配的 glad 源码：
  - 选择 OpenGL 版本（比如 4.6）、核心模式（Core）；
  - 勾选 "Generate loader"；
  - 点击 "Generate" 下载压缩包。
- 解压后，将 `include/glad` 和 `include/KHR` 复制到你的项目头文件目录，将 `src/glad.c` 添加到项目源码中。

#### 2. 核心使用示例（C/C++）
```cpp
// 第一步：必须先包含 glad.h，再包含 GLFW/SDL 等窗口库的头文件（避免冲突）
#include <glad/glad.h>
// 以 GLFW 为例（窗口创建库）
#include <GLFW/glfw3.h>

#include <iostream>

// 窗口大小改变时的回调函数
void framebuffer_size_callback(GLFWwindow* window, int width, int height) {
    glViewport(0, 0, width, height);
}

int main() {
    // 初始化 GLFW
    glfwInit();
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 4);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 6);
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);

    // 创建窗口
    GLFWwindow* window = glfwCreateWindow(800, 600, "Glad Example", NULL, NULL);
    if (window == NULL) {
        std::cout << "Failed to create GLFW window" << std::endl;
        glfwTerminate();
        return -1;
    }
    glfwMakeContextCurrent(window);
    glfwSetFramebufferSizeCallback(window, framebuffer_size_callback);

    // 第二步：初始化 glad（核心步骤，加载 OpenGL 函数指针）
    if (!gladLoadGLLoader((GLADloadproc)glfwGetProcAddress)) {
        std::cout << "Failed to initialize GLAD" << std::endl;
        return -1;
    }

    // 第三步：正常使用 OpenGL 函数（此时才可以调用 glXXX 函数）
    while (!glfwWindowShouldClose(window)) {
        // 清屏
        glClearColor(0.2f, 0.3f, 0.3f, 1.0f);
        glClear(GL_COLOR_BUFFER_BIT);

        // 交换缓冲区、处理事件
        glfwSwapBuffers(window);
        glfwPollEvents();
    }

    // 清理资源
    glfwTerminate();
    return 0;
}
```
 
<!-- ------------------------------------------------ -->
=============================================================
# 3. 关键变量（如CMAKE_C_CREATE_STATIC_LIBRARY）未配置

```txt
CMake内部变量未正确设置
问题：关键变量（如CMAKE_C_CREATE_STATIC_LIBRARY）未配置，常见于自定义工具链或交叉编译场景。

解决：
检查CMakeLists.txt中的编译器和平台设置。
若使用自定义工具链文件（toolchain.cmake），确保其完整且路径正确。
清理构建目录并重新配置
```
