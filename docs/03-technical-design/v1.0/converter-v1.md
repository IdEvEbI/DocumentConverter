# DocumentConverter 转换器 v1.0 设计文档

## 1. 文档目标

本文档定义 DocumentConverter 项目 v1.0 MVP 版本的转换器模块设计，实现文档格式转换的核心功能。

> **适用范围**：Python 项目开发，文档转换功能，MVP 快速迭代场景。

---

**文档版本**：v1.0  
**最后更新**：2025-07-29  
**更新内容**：创建转换器设计文档，定义核心转换功能和数据流

## 2. 设计概述

### 2.1 设计目标

基于 PRD 需求，设计简洁高效的文档转换器，实现：

- **PDF → Markdown**：PDF 文档内容提取和格式转换
- **Word → Markdown**：Word 文档解析和 Markdown 生成
- **Markdown → Word**：Markdown 渲染和 Word 文档生成
- **函数式设计**：纯函数实现，无副作用
- **TDD 驱动**：测试先行，保证转换质量

### 2.2 设计原则

- **单一职责**：每个转换器只负责一种格式转换
- **纯函数**：转换函数无副作用，易于测试
- **渐进式**：从基础转换开始，逐步完善功能
- **错误处理**：优雅处理转换失败和格式异常

### 2.3 技术选型

#### PDF 转换

- **pdfplumber**：PDF 内容解析和表格提取
- **PyPDF2**：备用文本提取

#### Word 转换

- **python-docx**：Word 文档读写和格式处理

#### Markdown 转换

- **markdown**：Markdown 解析和渲染
- **markdownify**：HTML 转 Markdown

## 3. 详细设计

### 3.1 架构设计

#### 转换器模块架构

```text
┌─────────────────┐
│   Converter     │  # 转换器主模块
│                 │
│  - PDF2MD      │  # PDF → Markdown
│  - Word2MD     │  # Word → Markdown  
│  - MD2Word     │  # Markdown → Word
├─────────────────┤
│   Parser        │  # 解析器模块
│                 │
│  - PDF Parser  │  # PDF 解析
│  - Word Parser │  # Word 解析
│  - MD Parser   │  # Markdown 解析
├─────────────────┤
│   Generator     │  # 生成器模块
│                 │
│  - MD Gen      │  # Markdown 生成
│  - Word Gen    │  # Word 生成
└─────────────────┘
```

### 3.2 接口设计

#### 核心转换接口

```python
from typing import Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class ConversionOptions:
    """转换选项配置"""
    preserve_formatting: bool = True
    include_images: bool = True
    include_tables: bool = True
    code_block_detection: bool = True

def convert_pdf_to_markdown(
    input_file: str, 
    output_file: str, 
    options: Optional[ConversionOptions] = None
) -> bool:
    """PDF 转 Markdown"""
    pass

def convert_word_to_markdown(
    input_file: str, 
    output_file: str, 
    options: Optional[ConversionOptions] = None
) -> bool:
    """Word 转 Markdown"""
    pass

def convert_markdown_to_word(
    input_file: str, 
    output_file: str, 
    options: Optional[ConversionOptions] = None
) -> bool:
    """Markdown 转 Word"""
    pass
```

### 3.3 数据流设计

#### PDF → Markdown 数据流

```text
PDF 文件 → PDF Parser → 结构化数据 → Markdown Generator → Markdown 文件
    ↓           ↓              ↓              ↓              ↓
  读取文件   提取文本/表格    数据模型      格式转换      输出文件
```

#### Word → Markdown 数据流

```text
Word 文件 → Word Parser → 结构化数据 → Markdown Generator → Markdown 文件
    ↓           ↓              ↓              ↓              ↓
  读取文件   提取内容/格式    数据模型      格式转换      输出文件
```

#### Markdown → Word 数据流

```text
Markdown 文件 → MD Parser → 结构化数据 → Word Generator → Word 文件
      ↓           ↓              ↓              ↓              ↓
    读取文件   解析语法/结构    数据模型      格式转换      输出文件
```

### 3.4 数据模型设计

#### 文档数据模型

```python
from typing import List, Dict, Any
from dataclasses import dataclass

@dataclass
class DocumentElement:
    """文档元素基类"""
    content: str
    element_type: str
    attributes: Dict[str, Any] = None

@dataclass
class DocumentStructure:
    """文档结构模型"""
    title: str
    elements: List[DocumentElement]
    metadata: Dict[str, Any] = None

@dataclass
class ConversionResult:
    """转换结果模型"""
    success: bool
    output_file: str
    error_message: str = None
    conversion_stats: Dict[str, Any] = None
```

## 4. 实现计划

### 4.1 开发阶段

#### 第一阶段：基础转换功能（MVP）

- [ ] PDF → Markdown 基础转换
  - [ ] 文本提取和段落处理
  - [ ] 标题层级识别
  - [ ] 基础列表转换
  - [ ] 简单表格转换

- [ ] Word → Markdown 基础转换
  - [ ] 文档内容提取
  - [ ] 标题样式识别
  - [ ] 段落和列表转换
  - [ ] 基础表格转换

#### 第二阶段：功能完善

- [ ] 图片和链接处理
- [ ] 代码块识别
- [ ] 复杂表格转换
- [ ] 样式模板支持

#### 第三阶段：Markdown → Word

- [ ] Markdown 解析
- [ ] Word 文档生成
- [ ] 样式应用
- [ ] 图片嵌入

### 4.2 测试策略

#### TDD 驱动开发

##### PDF 转换测试

```python
def test_convert_pdf_to_markdown_basic():
    """测试PDF转Markdown基础功能"""
    input_file = "tests/data/sample.pdf"
    output_file = "tests/output/sample.md"
    
    result = convert_pdf_to_markdown(input_file, output_file)
    
    assert result.success
    assert os.path.exists(output_file)
    
    with open(output_file, 'r') as f:
        content = f.read()
        assert "# Sample Title" in content
        assert "Sample content" in content

def test_convert_pdf_to_markdown_with_tables():
    """测试PDF表格转换"""
    input_file = "tests/data/table.pdf"
    output_file = "tests/output/table.md"
    
    result = convert_pdf_to_markdown(input_file, output_file)
    
    assert result.success
    with open(output_file, 'r') as f:
        content = f.read()
        assert "|" in content  # 表格标记
```

##### Word 转换测试

```python
def test_convert_word_to_markdown_basic():
    """测试Word转Markdown基础功能"""
    input_file = "tests/data/sample.docx"
    output_file = "tests/output/sample.md"
    
    result = convert_word_to_markdown(input_file, output_file)
    
    assert result.success
    assert os.path.exists(output_file)
    
    with open(output_file, 'r') as f:
        content = f.read()
        assert "# Sample Title" in content
        assert "Sample content" in content
```

### 4.3 错误处理策略

#### 转换错误处理

```python
class ConversionError(Exception):
    """转换错误基类"""
    pass

class FileNotFoundError(ConversionError):
    """文件未找到错误"""
    pass

class UnsupportedFormatError(ConversionError):
    """不支持格式错误"""
    pass

class ConversionFailedError(ConversionError):
    """转换失败错误"""
    pass

def safe_convert(func):
    """转换函数装饰器，提供错误处理"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError:
            return ConversionResult(success=False, error_message="文件未找到")
        except UnsupportedFormatError:
            return ConversionResult(success=False, error_message="不支持的文件格式")
        except Exception as e:
            return ConversionResult(success=False, error_message=str(e))
    return wrapper
```

## 5. 风险评估

### 5.1 技术风险

#### PDF 解析复杂性

- **风险**：PDF 格式复杂，解析可能不完整
- **缓解措施**：使用成熟的 PDF 解析库，充分测试不同格式

#### Word 格式兼容性

- **风险**：不同 Word 版本格式差异
- **缓解措施**：充分测试不同格式的兼容性

#### 转换质量

- **风险**：格式转换可能丢失信息
- **缓解措施**：建立转换质量评估机制

### 5.2 缓解措施

- 使用成熟的文档处理库
- 建立完善的测试覆盖
- 实现转换质量验证
- 提供转换选项配置

## 6. 核心要点

### 转换器设计原则

- **单一职责**：每个转换器只负责一种格式转换
- **纯函数**：转换函数无副作用，易于测试
- **渐进式**：从基础转换开始，逐步完善功能
- **错误处理**：优雅处理转换失败和格式异常

### 技术约束

- **MVP 约束**：基础转换功能，无高级优化
- **性能边界**：基础性能，支持小文件处理
- **格式边界**：支持主流文档格式

### 开发策略

- **TDD 驱动**：测试先行，保证转换质量
- **渐进式开发**：从简单到复杂的平滑过渡
- **质量优先**：转换质量优先于功能数量

> **一句话总结**：通过函数式设计和 TDD 驱动，实现高质量、可测试的文档转换功能。
