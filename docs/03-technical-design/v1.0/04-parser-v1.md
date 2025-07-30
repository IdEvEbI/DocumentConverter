# DocumentConverter 解析器 v1.0 设计文档

## 1. 文档目标

本文档定义 DocumentConverter 项目 v1.0 MVP 版本的解析器模块设计，专注文档解析和数据结构。

> **适用范围**：Python 项目开发，文档解析功能。

---

**文档版本**：v1.0  
**最后更新**：2025-07-30  
**更新内容**：精简内容，专注解析设计，删除重复内容

## 2. 设计概述

### 2.1 设计目标

实现简洁高效的文档解析功能，支持：

- **PDF 解析**：提取文本、表格、图片内容
- **Word 解析**：提取文本、格式、图片内容
- **Markdown 解析**：解析 Markdown 语法结构
- **统一接口**：提供一致的解析接口

### 2.2 设计原则

- **函数式设计**：纯函数，无副作用
- **错误处理**：优雅的错误处理和恢复
- **性能优化**：内存友好的解析策略
- **可扩展性**：支持新格式的快速集成

### 2.3 技术选型

#### PDF 解析

- **pdfplumber**：主要解析库，支持表格和文本提取
- **PyPDF2**：备用解析库，纯文本提取

#### Word 解析

- **python-docx**：Word 文档解析和读写

#### Markdown 解析

- **markdown**：Markdown 解析和渲染
- **markdownify**：HTML 转 Markdown

## 3. 详细设计

### 3.1 核心数据模型

```python
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum

class ElementType(Enum):
    """文档元素类型"""
    TITLE = "title"
    PARAGRAPH = "paragraph"
    LIST = "list"
    TABLE = "table"
    IMAGE = "image"
    CODE = "code"

@dataclass
class DocumentElement:
    """文档元素"""
    type: ElementType
    content: str
    level: int = 1
    attributes: Optional[Dict[str, Any]] = None

@dataclass
class DocumentData:
    """文档数据模型"""
    title: str
    elements: List[DocumentElement]
    metadata: Dict[str, Any]
```

### 3.2 解析器接口设计

```python
from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseParser(ABC):
    """解析器基类"""
    
    @abstractmethod
    def parse(self, file_path: str) -> DocumentData:
        """解析文档"""
        pass
    
    @abstractmethod
    def validate_file(self, file_path: str) -> bool:
        """验证文件格式"""
        pass

def parse_pdf(file_path: str) -> DocumentData:
    """PDF 解析函数（纯函数）"""
    pass

def parse_word(file_path: str) -> DocumentData:
    """Word 解析函数（纯函数）"""
    pass

def parse_markdown(file_path: str) -> DocumentData:
    """Markdown 解析函数（纯函数）"""
    pass
```

### 3.3 具体实现设计

#### PDF 解析实现

```python
import pdfplumber
from typing import List, Dict, Any

def parse_pdf(file_path: str) -> DocumentData:
    """解析PDF文件（纯函数）"""
    try:
        with pdfplumber.open(file_path) as pdf:
            elements = []
            title = ""
            
            for page_num, page in enumerate(pdf.pages):
                # 提取文本
                text = page.extract_text()
                if text:
                    # 解析页面内容
                    page_elements = _parse_pdf_text(text, page_num)
                    elements.extend(page_elements)
                    
                    # 提取标题（第一页第一行）
                    if page_num == 0 and not title:
                        lines = text.split('\n')
                        title = lines[0] if lines else "Untitled"
                
                # 提取表格
                tables = page.extract_tables()
                for table in tables:
                    table_element = _create_table_element(table)
                    elements.append(table_element)
            
            return DocumentData(
                title=title,
                elements=elements,
                metadata={"pages": len(pdf.pages), "format": "pdf"}
            )
    except Exception as e:
        raise DocumentParseError(f"PDF解析失败: {e}")

def _parse_pdf_text(text: str, page_num: int) -> List[DocumentElement]:
    """解析PDF文本内容"""
    elements = []
    lines = text.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # 判断标题（简单规则：短行且以数字开头）
        if len(line) < 100 and line[0].isdigit():
            elements.append(DocumentElement(
                type=ElementType.TITLE,
                content=line,
                level=1
            ))
        else:
            elements.append(DocumentElement(
                type=ElementType.PARAGRAPH,
                content=line,
                level=1
            ))
    
    return elements

def _create_table_element(table: List[List[str]]) -> DocumentElement:
    """创建表格元素"""
    # 将表格转换为Markdown格式
    markdown_table = _convert_table_to_markdown(table)
    
    return DocumentElement(
        type=ElementType.TABLE,
        content=markdown_table,
        level=1,
        attributes={"rows": len(table), "columns": len(table[0]) if table else 0}
    )

def _convert_table_to_markdown(table: List[List[str]]) -> str:
    """将表格转换为Markdown格式"""
    if not table:
        return ""
    
    markdown_lines = []
    
    # 表头
    header = "| " + " | ".join(str(cell) for cell in table[0]) + " |"
    markdown_lines.append(header)
    
    # 分隔线
    separator = "| " + " | ".join("---" for _ in table[0]) + " |"
    markdown_lines.append(separator)
    
    # 数据行
    for row in table[1:]:
        row_line = "| " + " | ".join(str(cell) for cell in row) + " |"
        markdown_lines.append(row_line)
    
    return "\n".join(markdown_lines)
```

#### Word 解析实现

```python
from docx import Document
from typing import List, Dict, Any

def parse_word(file_path: str) -> DocumentData:
    """解析Word文件（纯函数）"""
    try:
        doc = Document(file_path)
        elements = []
        title = ""
        
        for paragraph in doc.paragraphs:
            text = paragraph.text.strip()
            if not text:
                continue
            
            # 判断标题（基于样式）
            if paragraph.style.name.startswith('Heading'):
                level = int(paragraph.style.name[-1]) if paragraph.style.name[-1].isdigit() else 1
                elements.append(DocumentElement(
                    type=ElementType.TITLE,
                    content=text,
                    level=level
                ))
                
                # 提取主标题
                if not title and level == 1:
                    title = text
            else:
                elements.append(DocumentElement(
                    type=ElementType.PARAGRAPH,
                    content=text,
                    level=1
                ))
        
        # 处理表格
        for table in doc.tables:
            table_data = []
            for row in table.rows:
                row_data = [cell.text for cell in row.cells]
                table_data.append(row_data)
            
            table_element = _create_table_element(table_data)
            elements.append(table_element)
        
        return DocumentData(
            title=title or "Untitled",
            elements=elements,
            metadata={"paragraphs": len(doc.paragraphs), "format": "docx"}
        )
    except Exception as e:
        raise DocumentParseError(f"Word解析失败: {e}")
```

#### Markdown 解析实现

```python
import markdown
from typing import List, Dict, Any

def parse_markdown(file_path: str) -> DocumentData:
    """解析Markdown文件（纯函数）"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        elements = []
        lines = content.split('\n')
        title = ""
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # 判断标题（# 开头）
            if line.startswith('#'):
                level = len(line) - len(line.lstrip('#'))
                text = line.lstrip('#').strip()
                elements.append(DocumentElement(
                    type=ElementType.TITLE,
                    content=text,
                    level=level
                ))
                
                # 提取主标题
                if not title and level == 1:
                    title = text
            # 判断列表
            elif line.startswith(('-', '*', '+')):
                elements.append(DocumentElement(
                    type=ElementType.LIST,
                    content=line,
                    level=1
                ))
            # 判断代码块
            elif line.startswith('```'):
                elements.append(DocumentElement(
                    type=ElementType.CODE,
                    content=line,
                    level=1
                ))
            else:
                elements.append(DocumentElement(
                    type=ElementType.PARAGRAPH,
                    content=line,
                    level=1
                ))
        
        return DocumentData(
            title=title or "Untitled",
            elements=elements,
            metadata={"lines": len(lines), "format": "markdown"}
        )
    except Exception as e:
        raise DocumentParseError(f"Markdown解析失败: {e}")
```

## 4. 实现计划

### 4.1 开发阶段

#### 第一周：基础解析功能

- [ ] PDF 文本解析
- [ ] Word 文本解析
- [ ] Markdown 基础解析
- [ ] 统一数据模型

#### 第二周：高级解析功能

- [ ] PDF 表格解析
- [ ] Word 表格解析
- [ ] 图片处理
- [ ] 格式保持

#### 第三周：优化和测试

- [ ] 错误处理优化
- [ ] 性能优化
- [ ] 单元测试
- [ ] 集成测试

### 4.2 测试策略

#### 单元测试

```python
# test_parser.py
import pytest
from documentconverter.core.parser import parse_pdf, parse_word, parse_markdown

def test_parse_pdf_basic():
    """测试PDF基础解析"""
    result = parse_pdf("tests/data/sample.pdf")
    assert result.title == "Sample Document"
    assert len(result.elements) > 0
    assert result.metadata["format"] == "pdf"

def test_parse_word_basic():
    """测试Word基础解析"""
    result = parse_word("tests/data/sample.docx")
    assert result.title == "Sample Document"
    assert len(result.elements) > 0
    assert result.metadata["format"] == "docx"

def test_parse_markdown_basic():
    """测试Markdown基础解析"""
    result = parse_markdown("tests/data/sample.md")
    assert result.title == "Sample Document"
    assert len(result.elements) > 0
    assert result.metadata["format"] == "markdown"
```

### 4.3 部署计划

#### 文件结构

```ini
src/core/
├── __init__.py
├── parser.py          # 解析器主模块
├── pdf_parser.py      # PDF 解析器
├── word_parser.py     # Word 解析器
├── markdown_parser.py # Markdown 解析器
└── models.py          # 数据模型
```

## 5. 风险评估

### 5.1 技术风险

#### PDF 解析复杂性

- **风险**：PDF 格式复杂，解析可能不完整
- **缓解措施**：使用成熟的 PDF 解析库，充分测试

#### 格式兼容性

- **风险**：不同 Word 版本格式差异
- **缓解措施**：充分测试不同格式的兼容性

#### 性能瓶颈

- **风险**：大文件处理可能影响性能
- **缓解措施**：实现分块处理和内存优化

### 5.2 缓解措施

- 使用成熟的解析库
- 充分测试不同格式
- 实现错误恢复机制
- 建立完善的测试覆盖

## 6. 核心要点

### 设计原则

- **函数式设计**：纯函数，无副作用
- **统一接口**：一致的解析接口
- **错误处理**：优雅的错误处理和恢复
- **可扩展性**：支持新格式的快速集成

### 技术约束

- **MVP 约束**：基础解析功能，无高级优化
- **性能边界**：支持 < 10MB 文件，< 30 秒解析时间
- **内存约束**：< 500MB 内存使用

### 开发策略

- **TDD 驱动**：测试先行，保证代码质量
- **渐进式开发**：从简单到复杂
- **错误优先**：优先处理异常情况

> **一句话总结**：通过函数式设计和统一接口，实现简洁高效的文档解析功能。
