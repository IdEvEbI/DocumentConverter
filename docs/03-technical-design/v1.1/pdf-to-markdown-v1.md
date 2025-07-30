# DocumentConverter PDF → Markdown 转换功能 v1.1 设计文档

## 1. 文档目标

本文档定义 DocumentConverter 项目 v1.1 版本的 PDF → Markdown 转换功能设计，实现 PDF 文档到 Markdown 格式的智能转换。

> **适用范围**：Python 项目开发，PDF 文档解析，Markdown 转换功能。

---

**文档版本**：v1.1  
**最后更新**：2025-07-30  
**更新内容**：创建 PDF → Markdown 转换功能设计文档

## 2. 设计概述

### 2.1 设计目标

基于 PRD 需求，实现 PDF → Markdown 转换功能，确保：

- **格式保持**：保持标题层级、段落结构、列表格式
- **内容完整**：完整提取文本、表格、图片、链接
- **性能优化**：支持大文件处理，转换速度 < 30 秒
- **错误处理**：优雅处理 PDF 解析异常和格式问题

### 2.2 设计原则

- **渐进式实现**：从基础文本提取开始，逐步完善功能
- **TDD 驱动**：测试先行，保证转换质量
- **函数式设计**：纯函数转换，无副作用
- **错误友好**：详细的错误信息和恢复建议

### 2.3 技术选型

#### PDF 解析技术栈

- **pdfplumber**：主要 PDF 解析库，支持表格和文本提取
- **pypdf**：备用 PDF 文本提取，处理复杂格式
- **PIL/Pillow**：图片处理和提取

#### Markdown 生成技术栈

- **markdown**：Markdown 语法验证
- **自定义生成器**：根据解析结果生成 Markdown

> 详细技术选型请参考：01-mvp-design.md

## 3. 详细设计

### 3.1 架构设计

#### PDF → Markdown 转换架构

```text
┌─────────────────┐
│   PDF Input     │  # PDF 文件输入
│                 │
│  - File I/O     │  # 文件读取
│  - Validation   │  # 格式验证
├─────────────────┤
│   PDF Parser    │  # PDF 解析层
│                 │
│  - Text Extract │  # 文本提取
│  - Table Parse  │  # 表格解析
│  - Image Extract│  # 图片提取
│  - Link Extract │  # 链接提取
├─────────────────┤
│   Content Model │  # 内容模型层
│                 │
│  - Document     │  # 文档结构
│  - Elements     │  # 元素数组
│  - Metadata     │  # 元数据
├─────────────────┤
│   Markdown Gen  │  # Markdown 生成层
│                 │
│  - Text Format  │  # 文本格式化
│  - Table Gen    │  # 表格生成
│  - Image Gen    │  # 图片生成
│  - Link Gen     │  # 链接生成
├─────────────────┤
│   Markdown Out  │  # Markdown 输出
│                 │
│  - File Write   │  # 文件写入
│  - Validation   │  # 输出验证
└─────────────────┘
```

### 3.2 接口设计

#### 核心转换接口

```python
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from pathlib import Path

@dataclass
class PDFConversionOptions:
    """PDF 转换选项"""
    extract_images: bool = True
    extract_tables: bool = True
    extract_links: bool = True
    preserve_formatting: bool = True
    code_block_detection: bool = True
    max_file_size: int = 50 * 1024 * 1024  # 50MB

@dataclass
class PDFElement:
    """PDF 元素模型"""
    element_type: str  # 'text', 'table', 'image', 'link'
    content: str
    position: Dict[str, float]
    metadata: Dict[str, Any]

@dataclass
class PDFDocument:
    """PDF 文档模型"""
    title: str
    elements: List[PDFElement]
    metadata: Dict[str, Any]
    page_count: int

def convert_pdf_to_markdown(
    input_file: Path,
    output_file: Path,
    options: Optional[PDFConversionOptions] = None
) -> bool:
    """PDF 转 Markdown 主函数"""
    pass

def parse_pdf_document(pdf_file: Path) -> PDFDocument:
    """解析 PDF 文档"""
    pass

def generate_markdown_content(document: PDFDocument) -> str:
    """生成 Markdown 内容"""
    pass
```

### 3.3 数据流设计

#### PDF → Markdown 数据流

```text
PDF 文件 → PDF 解析 → 内容模型 → Markdown 生成 → Markdown 文件
    ↓           ↓           ↓           ↓           ↓
  文件读取   元素提取    结构组织    格式转换    文件输出
```

#### 详细数据流

```python
def pdf_to_markdown_flow(pdf_path: Path, md_path: Path) -> bool:
    """PDF → Markdown 转换流程"""
    
    # 1. 文件验证
    validate_pdf_file(pdf_path)
    
    # 2. PDF 解析
    pdf_document = parse_pdf_document(pdf_path)
    
    # 3. 内容处理
    processed_elements = process_pdf_elements(pdf_document.elements)
    
    # 4. Markdown 生成
    markdown_content = generate_markdown_content(processed_elements)
    
    # 5. 文件输出
    write_markdown_file(md_path, markdown_content)
    
    return True
```

## 4. 实现计划

### 4.1 开发阶段

#### 第一阶段：基础文本转换（MVP）

- [ ] 实现 PDF 文本提取
  - [ ] 使用 pdfplumber 提取文本内容
  - [ ] 处理基本段落和标题
  - [ ] 实现简单的 Markdown 生成

- [ ] 实现基础格式转换
  - [ ] 标题层级识别和转换
  - [ ] 段落格式保持
  - [ ] 基础列表识别

#### 第二阶段：高级功能

- [ ] 实现表格转换
  - [ ] 表格结构识别
  - [ ] Markdown 表格生成
  - [ ] 表格样式优化

- [ ] 实现图片处理
  - [ ] 图片提取和保存
  - [ ] 图片链接生成
  - [ ] 图片格式验证

#### 第三阶段：优化和完善

- [ ] 实现链接处理
  - [ ] 链接提取和验证
  - [ ] Markdown 链接生成

- [ ] 实现代码块识别
  - [ ] 代码块检测算法
  - [ ] 代码块格式化

### 4.2 测试策略

#### 单元测试

```python
def test_pdf_text_extraction():
    """测试 PDF 文本提取"""
    pdf_path = "tests/data/sample.pdf"
    document = parse_pdf_document(pdf_path)
    
    assert document.title is not None
    assert len(document.elements) > 0
    assert any(e.element_type == 'text' for e in document.elements)

def test_markdown_generation():
    """测试 Markdown 生成"""
    elements = [
        PDFElement('text', '# Title', {'x': 0, 'y': 0}, {}),
        PDFElement('text', 'Paragraph content', {'x': 0, 'y': 50}, {})
    ]
    
    markdown = generate_markdown_content(elements)
    assert '# Title' in markdown
    assert 'Paragraph content' in markdown

def test_table_conversion():
    """测试表格转换"""
    table_element = PDFElement('table', 'table_data', {'x': 0, 'y': 0}, {})
    
    markdown = convert_table_to_markdown(table_element)
    assert '|' in markdown
    assert '-' in markdown
```

#### 集成测试

```python
def test_pdf_to_markdown_conversion():
    """测试完整转换流程"""
    input_file = "tests/data/sample.pdf"
    output_file = "tests/output/sample.md"
    
    result = convert_pdf_to_markdown(input_file, output_file)
    assert result is True
    assert output_file.exists()
    
    # 验证输出内容
    with open(output_file, 'r') as f:
        content = f.read()
        assert len(content) > 0
        assert '# ' in content  # 至少有一个标题
```

### 4.3 性能优化策略

#### 大文件处理

```python
def process_large_pdf(pdf_path: Path, chunk_size: int = 1024 * 1024):
    """大文件分块处理"""
    with open(pdf_path, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            process_pdf_chunk(chunk)
```

#### 内存优化

```python
def optimize_memory_usage():
    """内存使用优化"""
    # 使用生成器处理大文件
    def element_generator(pdf_document):
        for element in pdf_document.elements:
            yield process_element(element)
    
    # 流式处理
    for processed_element in element_generator(document):
        write_element_to_markdown(processed_element)
```

## 5. 风险评估

### 5.1 技术风险

#### PDF 解析复杂性

- **风险**：PDF 格式复杂，解析可能不完整
- **缓解措施**：使用成熟的 pdfplumber 库，实现备用解析方案

#### 格式兼容性

- **风险**：不同 PDF 版本格式差异
- **缓解措施**：充分测试不同格式，实现格式检测和适配

#### 性能瓶颈

- **风险**：大文件处理可能影响性能
- **缓解措施**：实现分块处理和内存优化

### 5.2 缓解措施

- 使用成熟的 PDF 解析库（pdfplumber + pypdf）
- 充分测试不同格式的兼容性
- 实现分块处理和内存优化
- 提供详细的错误信息和恢复建议

## 6. 核心要点

### 转换质量保证

- **格式保持**：保持标题层级、段落结构、列表格式
- **内容完整**：完整提取文本、表格、图片、链接
- **性能优化**：支持大文件处理，转换速度 < 30 秒
- **错误处理**：优雅处理 PDF 解析异常和格式问题

### 技术约束

- **MVP 约束**：基础文本转换，无高级格式
- **性能边界**：支持 50MB 以下文件，转换时间 < 30 秒
- **格式边界**：支持主流 PDF 格式

### 开发策略

- **渐进式开发**：从基础文本提取开始，逐步完善功能
- **TDD 驱动**：测试先行，保证转换质量
- **性能监控**：持续监控转换性能和内存使用

> **一句话总结**：通过成熟的 PDF 解析技术和智能的 Markdown 生成算法，实现高质量的 PDF → Markdown 转换功能。
