# DocumentConverter 技术架构设计

## 1. 文档目标

本文档定义 DocumentConverter 项目的技术架构设计，基于 PRD 需求设计简洁高效的文档转换系统。

> **适用范围**：Python 项目开发，文档转换工具，版本化开发场景。

---

- **文档版本**：v3.0  
- **最后更新**：2025-07-29  
- **更新内容**：明确版本边界，锚定 1.0 MVP 开发范围

## 2. 架构设计概述

### 2.1 设计目标

基于 PRD 需求，设计一个简洁高效的文档转换系统，实现：

- **快速迭代**：MVP 优先，快速验证核心功能
- **函数式设计**：核心逻辑采用函数式编程范式
- **TDD 驱动**：测试先行，保证代码质量
- **渐进式演进**：从简单到复杂，避免过度设计

### 2.2 架构原则

- **YAGNI**：You Aren't Gonna Need It，不过度设计
- **KISS**：Keep It Simple, Stupid，保持简单
- **函数式优先**：纯函数，无副作用
- **测试驱动**：测试先行，快速反馈

### 2.3 技术栈选型

#### PDF 处理

- **pdfplumber**：PDF 内容解析（表格、文本、图片）
- **PyPDF2**：备用 PDF 文本提取

#### Word 文档处理

- **python-docx**：Word 文档读写

#### Markdown 处理

- **markdown**：Markdown 解析和渲染
- **markdownify**：HTML 转 Markdown

#### CLI 框架

- **click**：命令行界面框架
- **rich**：终端美化输出

#### 开发工具

- **pytest**：测试框架（TDD 驱动）
- **black**：代码格式化
- **flake8**：代码检查

#### 最小可行依赖

```python
# requirements.txt (MVP 版本)
click>=8.0.0
rich>=10.0.0
pdfplumber>=0.7.0
python-docx>=0.8.11
markdown>=3.3.0
pytest>=7.0.0
```

## 3. 系统架构设计

### 3.1 MVP 阶段：3层架构

```text
┌─────────────────┐
│   CLI Layer     │  # 命令行接口层
│                 │
│  - Command      │  # 命令处理
│  - Interface    │  # 用户交互
│  - Validation   │  # 输入验证
├─────────────────┤
│   Core Layer    │  # 核心业务层（函数式）
│                 │
│  - Parser       │  # 文档解析（纯函数）
│  - Converter    │  # 格式转换（纯函数）
│  - Generator    │  # 文档生成（纯函数）
├─────────────────┤
│  Utility Layer  │  # 工具层
│                 │
│  - Logger       │  # 日志记录
│  - Error Handler│  # 错误处理
│  - File I/O     │  # 文件操作
└─────────────────┘
```

### 3.2 核心函数设计

#### 解析器函数

```python
from typing import Dict, Any
from dataclasses import dataclass

@dataclass
class DocumentData:
    """简化的文档数据模型"""
    title: str
    content: str
    metadata: Dict[str, Any]

def parse_pdf(file_path: str) -> DocumentData:
    """解析PDF文件（纯函数）"""
    pass

def parse_word(file_path: str) -> DocumentData:
    """解析Word文件（纯函数）"""
    pass

def parse_markdown(file_path: str) -> DocumentData:
    """解析Markdown文件（纯函数）"""
    pass
```

#### 转换器函数

```python
def convert_to_markdown(document: DocumentData) -> str:
    """转换为Markdown格式（纯函数）"""
    pass

def convert_to_word(document: DocumentData) -> str:
    """转换为Word格式（纯函数）"""
    pass
```

#### 生成器函数

```python
def save_markdown(content: str, output_path: str) -> None:
    """保存Markdown文件"""
    pass

def save_word(content: str, output_path: str) -> None:
    """保存Word文件"""
    pass
```

#### 组合函数

```python
def convert_pdf_to_markdown(input_file: str, output_file: str) -> None:
    """PDF转Markdown的完整流程"""
    document = parse_pdf(input_file)
    markdown_content = convert_to_markdown(document)
    save_markdown(markdown_content, output_file)

def convert_word_to_markdown(input_file: str, output_file: str) -> None:
    """Word转Markdown的完整流程"""
    document = parse_word(input_file)
    markdown_content = convert_to_markdown(document)
    save_markdown(markdown_content, output_file)

def convert_markdown_to_word(input_file: str, output_file: str) -> None:
    """Markdown转Word的完整流程"""
    document = parse_markdown(input_file)
    word_content = convert_to_word(document)
    save_word(word_content, output_file)
```

## 4. 开发流程与测试策略

### 4.1 TDD 驱动开发

#### 测试先行策略

##### 第一步：写测试

```python
# test_converter.py
import pytest
from documentconverter.core import convert_pdf_to_markdown

def test_convert_pdf_to_markdown_basic():
    """测试PDF转Markdown基础功能"""
    # 准备测试数据
    input_file = "tests/data/sample.pdf"
    output_file = "tests/output/sample.md"
    
    # 执行转换
    convert_pdf_to_markdown(input_file, output_file)
    
    # 验证结果
    assert os.path.exists(output_file)
    with open(output_file, 'r') as f:
        content = f.read()
        assert "# Sample Title" in content
        assert "Sample content" in content

def test_parse_pdf_title():
    """测试PDF标题解析"""
    document = parse_pdf("tests/data/sample.pdf")
    assert document.title == "Sample Document"
    assert len(document.content) > 0
```

##### 第二步：写代码

```python
# core.py
def parse_pdf(file_path: str) -> DocumentData:
    """解析PDF文件"""
    import pdfplumber
    
    with pdfplumber.open(file_path) as pdf:
        pages = pdf.pages
        content = ""
        title = ""
        
        for page in pages:
            text = page.extract_text()
            if text:
                content += text + "\n"
        
        # 简单提取标题（第一行）
        lines = content.split('\n')
        title = lines[0] if lines else "Untitled"
        
        return DocumentData(
            title=title,
            content=content,
            metadata={"pages": len(pages)}
        )
```

##### 第三步：重构

```python
# 优化后的代码
def parse_pdf(file_path: str) -> DocumentData:
    """解析PDF文件（重构后）"""
    import pdfplumber
    
    with pdfplumber.open(file_path) as pdf:
        content = _extract_text_from_pages(pdf.pages)
        title = _extract_title_from_content(content)
        
        return DocumentData(
            title=title,
            content=content,
            metadata={"pages": len(pdf.pages)}
        )

def _extract_text_from_pages(pages) -> str:
    """提取页面文本"""
    return "\n".join(page.extract_text() or "" for page in pages)

def _extract_title_from_content(content: str) -> str:
    """从内容中提取标题"""
    lines = content.split('\n')
    return lines[0] if lines else "Untitled"
```

### 4.2 测试策略

#### 单元测试

- **解析器测试**：每个解析函数的独立测试
- **转换器测试**：格式转换的正确性测试
- **生成器测试**：文件生成和保存测试

#### 集成测试

- **端到端测试**：完整转换流程测试
- **文件格式测试**：不同格式文件的兼容性测试
- **性能测试**：大文件处理性能测试

#### 测试数据管理

```ini
tests/
├── data/                    # 测试数据
│   ├── sample.pdf
│   ├── sample.docx
│   └── sample.md
├── output/                  # 测试输出
├── test_parser.py
├── test_converter.py
└── test_generator.py
```

### 4.3 TDD 开发流程

1. **写测试** → **运行测试**（失败）
2. **写代码** → **运行测试**（通过）
3. **重构** → **运行测试**（通过）
4. **重复**

## 5. 项目实现与部署

### 5.1 项目目录结构

```ini
DocumentConverter/
├── src/
│   ├── __init__.py
│   ├── main.py              # 主入口
│   ├── cli/                 # 命令行接口
│   │   ├── __init__.py
│   │   └── commands.py
│   ├── core/                # 核心功能（函数式）
│   │   ├── __init__.py
│   │   ├── parser.py        # 解析函数
│   │   ├── converter.py     # 转换函数
│   │   ├── generator.py     # 生成函数
│   │   └── models.py        # 数据模型
│   └── utils/               # 工具函数
│       ├── __init__.py
│       ├── logger.py
│       └── file_utils.py
├── tests/                   # 测试目录
│   ├── __init__.py
│   ├── data/                # 测试数据
│   ├── test_parser.py
│   ├── test_converter.py
│   └── test_generator.py
├── docs/                    # 文档目录
├── requirements.txt         # 依赖文件
├── setup.py                 # 安装配置
└── README.md                # 项目说明
```

### 5.2 命令行接口设计

#### 简化命令

```python
# 主要命令
documentconverter convert <input_file> <output_file> [options]
documentconverter batch <input_dir> <output_dir> [options]

# 选项参数
--format, -f: 指定格式（pdf2md, word2md, md2word）
--verbose, -v: 详细输出
--quiet, -q: 静默模式
```

#### 实现示例

```python
import click
from rich.console import Console
from rich.progress import Progress

console = Console()

@click.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.argument('output_file', type=click.Path())
@click.option('--format', '-f', help='转换格式')
@click.option('--verbose', '-v', is_flag=True, help='详细输出')
def convert(input_file, output_file, format, verbose):
    """转换文档格式"""
    try:
        with Progress() as progress:
            task = progress.add_task("Converting...", total=100)
            
            # 根据文件扩展名自动判断格式
            if not format:
                format = _detect_format(input_file, output_file)
            
            # 执行转换
            _convert_file(input_file, output_file, format)
            
            progress.update(task, completed=100)
        
        console.print(f"✅ 转换完成: {output_file}", style="green")
        
    except Exception as e:
        console.print(f"❌ 转换失败: {e}", style="red")
        raise click.Abort()
```

### 5.3 错误处理机制

#### 错误分类

```python
class DocumentConverterError(Exception):
    """基础异常类"""
    pass

class FileNotFoundError(DocumentConverterError):
    """文件未找到"""
    pass

class UnsupportedFormatError(DocumentConverterError):
    """不支持的格式"""
    pass

class ConversionError(DocumentConverterError):
    """转换错误"""
    pass
```

#### 错误处理策略

```python
def safe_convert(input_file: str, output_file: str) -> bool:
    """安全的转换函数"""
    try:
        # 验证输入文件
        if not os.path.exists(input_file):
            raise FileNotFoundError(f"输入文件不存在: {input_file}")
        
        # 验证文件格式
        if not _is_supported_format(input_file):
            raise UnsupportedFormatError(f"不支持的格式: {input_file}")
        
        # 执行转换
        convert_pdf_to_markdown(input_file, output_file)
        return True
        
    except Exception as e:
        logger.error(f"转换失败: {e}")
        return False
```

### 5.4 性能优化策略

#### 基础优化

- **内存管理**：及时释放大对象
- **文件处理**：使用上下文管理器
- **错误恢复**：部分失败时继续处理

#### 渐进式优化

```python
# 第一版：基础实现
def parse_pdf(file_path: str) -> DocumentData:
    """基础PDF解析"""
    pass

# 第二版：添加缓存
@lru_cache(maxsize=128)
def parse_pdf(file_path: str) -> DocumentData:
    """带缓存的PDF解析"""
    pass

# 第三版：异步处理
async def parse_pdf_async(file_path: str) -> DocumentData:
    """异步PDF解析"""
    pass
```

## 6. 版本规划与开发边界

### 6.1 版本边界定义

#### 1.0 版本（MVP）- 核心功能

**开发边界**：

- ✅ **基础数据模型**：简单的 `DocumentData` 结构
- ✅ **核心转换功能**：PDF / Word ↔ Markdown 基础转换
- ✅ **命令行界面**：基础 CLI 功能
- ✅ **基础错误处理**：简单异常处理
- ✅ **基础测试覆盖**：核心功能测试

**技术约束**：

- 3 层架构（CLI、Core、Utility）
- 函数式设计，纯函数实现
- 最小依赖原则
- 同步处理，无异步支持
- 无缓存机制
- 无性能监控

#### 2.0 版本 - 功能完善

**新增功能**：

- 🔄 **增强数据模型**：结构化 `DocumentElement` 支持
- 🔄 **配置管理系统**：`ConversionConfig` 统一配置
- 🔄 **批量处理**：多文件批量转换
- 🔄 **格式优化**：更好的格式保持
- 🔄 **错误处理增强**：详细的错误信息和恢复机制

**技术升级**：

- 4 层架构（增加 Config 层）
- 配置驱动的转换流程
- 批量处理优化
- 更完善的测试覆盖

#### 3.0 版本 - 性能优化

**新增功能**：

- 🚀 **性能监控系统**：实时性能监控
- 🚀 **缓存策略**：智能缓存机制
- 🚀 **异步处理**：异步批量转换
- 🚀 **大文件优化**：流式处理支持
- 🚀 **内存优化**：内存使用优化

**技术升级**：

- 5 层架构（增加 Monitor 层）
- 异步处理能力
- 缓存和监控系统
- 性能基准测试

### 6.2 1.0 版本开发计划

#### 第一周：核心功能（MVP）

- [ ] 项目环境搭建
- [ ] PDF → Markdown 基础转换
- [ ] Word → Markdown 基础转换
- [ ] 基础命令行界面

#### 第二周：功能完善

- [ ] Markdown → Word 转换
- [ ] 基础错误处理机制
- [ ] 核心功能测试覆盖

#### 第三周：稳定和文档

- [ ] 功能稳定和 bug 修复
- [ ] 文档完善
- [ ] 用户测试和反馈收集

### 6.3 版本演进策略

#### 1.0 → 2.0 演进

```text
1.0 MVP (3层) → 2.0 功能完善 (4层)
```

**演进原则**：

- 保持 API 向后兼容
- 渐进式功能增强
- 配置驱动的架构升级

#### 2.0 → 3.0 演进

```text
2.0 功能完善 (4层) → 3.0 性能优化 (5层)
```

**演进原则**：

- 性能优先的架构升级
- 异步处理能力增强
- 监控和缓存系统集成

### 6.4 技术债务管理

#### 1.0 版本约束

- **功能边界**：严格控制在核心转换功能
- **性能边界**：基础性能，无高级优化
- **架构边界**：3 层架构，避免过度设计
- **依赖边界**：最小依赖集，避免技术债务

#### 版本间技术债务

- **定期重构**：每个版本结束后的代码重构
- **测试覆盖**：保持 > 80% 测试覆盖率
- **文档同步**：代码和文档同步更新
- **向后兼容**：新版本保持 API 兼容性

## 7. 核心要点

### 版本边界策略

- **1.0 MVP**：3 层架构，核心转换功能，最小依赖
- **2.0 功能完善**：4 层架构，配置管理，批量处理
- **3.0 性能优化**：5 层架构，异步处理，监控缓存

### 开发原则

- **功能边界**：严格控制在版本定义的功能范围内
- **TDD 驱动**：测试先行，保证代码质量
- **渐进式演进**：从简单到复杂的平滑过渡
- **向后兼容**：新版本保持 API 兼容性

### 技术约束

- **1.0 约束**：同步处理，无缓存，无监控，最小依赖
- **架构演进**：3 层 → 4 层 → 5 层，避免过度设计
- **性能边界**：基础性能 → 功能完善 → 性能优化

> **一句话总结**：通过明确的版本边界和渐进式架构演进，实现可控的文档转换工具开发。
