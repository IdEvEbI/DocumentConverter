# DocumentConverter 测试框架 v1.0 设计文档

## 1. 文档目标

本文档定义 DocumentConverter 项目 v1.0 MVP 版本的测试框架设计，确保代码质量和功能可靠性。

> **适用范围**：Python 项目开发，TDD 驱动开发，MVP 快速迭代场景。

---

**文档版本**：v1.0  
**最后更新**：2025-07-29  
**更新内容**：创建测试框架设计文档，定义测试策略和实现方案

## 2. 设计概述

### 2.1 设计目标

基于 TDD 驱动开发理念，设计完善的测试框架，实现：

- **测试先行**：先写测试，再写代码
- **全面覆盖**：单元测试、集成测试、功能测试
- **快速反馈**：快速执行测试，及时发现问题
- **质量保证**：确保代码质量和功能可靠性
- **持续集成**：支持 CI/CD 流程

### 2.2 设计原则

- **TDD 驱动**：测试先行，保证代码质量
- **全面覆盖**：核心功能 100% 测试覆盖
- **快速执行**：测试执行时间 < 30 秒
- **易于维护**：清晰的测试结构和文档
- **可重复性**：测试结果稳定可靠

### 2.3 技术选型

#### 测试框架

- **pytest**：功能强大的 Python 测试框架
- **pytest-cov**：测试覆盖率统计
- **pytest-mock**：Mock 和 Stub 支持

#### 测试工具

- **factory-boy**：测试数据生成
- **faker**：假数据生成
- **responses**：HTTP 请求 Mock

## 3. 详细设计

### 3.1 架构设计

#### 测试框架架构

```text
┌─────────────────┐
│   Test Layer    │  # 测试层
│                 │
│  - Unit Tests   │  # 单元测试
│  - Integration  │  # 集成测试
│  - Functional   │  # 功能测试
├─────────────────┤
│   Test Data     │  # 测试数据层
│                 │
│  - Fixtures     │  # 测试夹具
│  - Factories    │  # 数据工厂
│  - Mocks        │  # Mock 对象
├─────────────────┤
│   Test Utils    │  # 测试工具层
│                 │
│  - Helpers      │  # 测试辅助函数
│  - Assertions   │  # 自定义断言
│  - Generators   │  # 数据生成器
└─────────────────┘
```

### 3.2 测试分类设计

#### 单元测试

```python
# 测试核心转换函数
def test_convert_pdf_to_markdown():
    """测试PDF转Markdown核心功能"""
    # 准备测试数据
    input_data = "Sample PDF content"
    expected_output = "# Sample Title\n\nSample content"
    
    # 执行转换
    result = convert_pdf_to_markdown(input_data)
    
    # 验证结果
    assert result == expected_output

def test_convert_word_to_markdown():
    """测试Word转Markdown核心功能"""
    # 准备测试数据
    input_data = "Sample Word content"
    expected_output = "# Sample Title\n\nSample content"
    
    # 执行转换
    result = convert_word_to_markdown(input_data)
    
    # 验证结果
    assert result == expected_output
```

#### 集成测试

```python
# 测试文件转换流程
def test_file_conversion_workflow():
    """测试完整的文件转换流程"""
    # 准备测试文件
    input_file = "tests/data/sample.pdf"
    output_file = "tests/output/sample.md"
    
    # 执行转换
    result = convert_file(input_file, output_file)
    
    # 验证结果
    assert result.success
    assert os.path.exists(output_file)
    
    # 验证输出内容
    with open(output_file, 'r') as f:
        content = f.read()
        assert "# Sample Title" in content

def test_cli_integration():
    """测试CLI集成"""
    runner = CliRunner()
    result = runner.invoke(cli, ['convert', 'test.pdf', 'test.md'])
    
    assert result.exit_code == 0
    assert "转换完成" in result.output
```

#### 功能测试

```python
# 测试不同格式转换
def test_pdf_to_markdown_conversion():
    """测试PDF转Markdown功能"""
    test_cases = [
        ("simple.pdf", "simple.md"),
        ("with_tables.pdf", "with_tables.md"),
        ("with_images.pdf", "with_images.md")
    ]
    
    for input_file, output_file in test_cases:
        result = convert_pdf_to_markdown(input_file, output_file)
        assert result.success

def test_word_to_markdown_conversion():
    """测试Word转Markdown功能"""
    test_cases = [
        ("simple.docx", "simple.md"),
        ("with_formatting.docx", "with_formatting.md"),
        ("with_tables.docx", "with_tables.md")
    ]
    
    for input_file, output_file in test_cases:
        result = convert_word_to_markdown(input_file, output_file)
        assert result.success
```

### 3.3 测试数据管理

#### 测试夹具设计

```python
import pytest
from pathlib import Path

@pytest.fixture
def sample_pdf_file():
    """提供测试用PDF文件"""
    return "tests/data/sample.pdf"

@pytest.fixture
def sample_docx_file():
    """提供测试用Word文件"""
    return "tests/data/sample.docx"

@pytest.fixture
def sample_md_file():
    """提供测试用Markdown文件"""
    return "tests/data/sample.md"

@pytest.fixture
def temp_output_dir(tmp_path):
    """提供临时输出目录"""
    return tmp_path / "output"

@pytest.fixture
def conversion_options():
    """提供转换选项配置"""
    return {
        "preserve_formatting": True,
        "include_images": True,
        "include_tables": True
    }
```

#### 测试数据生成

```python
from faker import Faker
import factory

fake = Faker()

class DocumentDataFactory(factory.Factory):
    """文档数据工厂"""
    class Meta:
        model = dict
    
    title = factory.LazyFunction(lambda: fake.sentence())
    content = factory.LazyFunction(lambda: fake.text())
    metadata = factory.LazyFunction(lambda: {
        "author": fake.name(),
        "created_date": fake.date()
    })

def generate_test_pdf_content():
    """生成测试PDF内容"""
    return {
        "title": fake.sentence(),
        "content": fake.text(),
        "tables": [
            {"headers": ["Name", "Age"], "rows": [["John", "25"], ["Jane", "30"]]}
        ]
    }

def generate_test_word_content():
    """生成测试Word内容"""
    return {
        "title": fake.sentence(),
        "content": fake.text(),
        "formatting": {
            "bold": ["important text"],
            "italic": ["emphasized text"]
        }
    }
```

### 3.4 测试工具设计

#### 自定义断言

```python
def assert_markdown_structure(content: str):
    """断言Markdown结构正确"""
    assert "#" in content  # 包含标题
    assert "\n\n" in content  # 包含段落分隔
    assert len(content) > 0  # 非空内容

def assert_conversion_success(result):
    """断言转换成功"""
    assert result.success
    assert result.output_file is not None
    assert os.path.exists(result.output_file)

def assert_file_content_contains(file_path: str, expected_content: str):
    """断言文件内容包含指定文本"""
    with open(file_path, 'r') as f:
        content = f.read()
        assert expected_content in content
```

#### 测试辅助函数

```python
def create_test_file(file_path: str, content: str):
    """创建测试文件"""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as f:
        f.write(content)

def cleanup_test_files(file_paths: list):
    """清理测试文件"""
    for file_path in file_paths:
        if os.path.exists(file_path):
            os.remove(file_path)

def compare_files(file1: str, file2: str, ignore_whitespace: bool = True):
    """比较两个文件内容"""
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        content1 = f1.read()
        content2 = f2.read()
        
        if ignore_whitespace:
            content1 = ' '.join(content1.split())
            content2 = ' '.join(content2.split())
        
        return content1 == content2
```

## 4. 实现计划

### 4.1 开发阶段

#### 第一阶段：基础测试框架（MVP）

- [ ] 设置测试环境
  - [ ] 配置 pytest
  - [ ] 配置测试覆盖率
  - [ ] 创建测试目录结构

- [ ] 实现核心单元测试
  - [ ] PDF 转换函数测试
  - [ ] Word 转换函数测试
  - [ ] 工具函数测试

#### 第二阶段：集成测试

- [ ] 实现文件转换测试
  - [ ] 完整转换流程测试
  - [ ] 错误处理测试
  - [ ] 性能测试

- [ ] 实现 CLI 测试
  - [ ] 命令执行测试
  - [ ] 参数验证测试
  - [ ] 错误处理测试

#### 第三阶段：功能测试

- [ ] 实现端到端测试
  - [ ] 真实文件转换测试
  - [ ] 批量转换测试
  - [ ] 边界条件测试

### 4.2 测试策略

#### TDD 开发流程

##### 第一步：写测试

```python
def test_convert_pdf_to_markdown_basic():
    """测试PDF转Markdown基础功能"""
    # 准备测试数据
    input_file = "tests/data/sample.pdf"
    output_file = "tests/output/sample.md"
    
    # 执行转换
    result = convert_pdf_to_markdown(input_file, output_file)
    
    # 验证结果
    assert result.success
    assert os.path.exists(output_file)
    
    with open(output_file, 'r') as f:
        content = f.read()
        assert "# Sample Title" in content
        assert "Sample content" in content
```

##### 第二步：写代码

```python
def convert_pdf_to_markdown(input_file: str, output_file: str) -> ConversionResult:
    """PDF转Markdown实现"""
    try:
        # 读取PDF文件
        with pdfplumber.open(input_file) as pdf:
            content = ""
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    content += text + "\n"
        
        # 转换为Markdown格式
        markdown_content = convert_to_markdown(content)
        
        # 写入输出文件
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w') as f:
            f.write(markdown_content)
        
        return ConversionResult(success=True, output_file=output_file)
    except Exception as e:
        return ConversionResult(success=False, error_message=str(e))
```

##### 第三步：重构

```python
def convert_pdf_to_markdown(input_file: str, output_file: str) -> ConversionResult:
    """PDF转Markdown实现（重构后）"""
    try:
        # 解析PDF
        content = parse_pdf_content(input_file)
        
        # 转换为Markdown
        markdown_content = convert_to_markdown(content)
        
        # 写入文件
        write_output_file(output_file, markdown_content)
        
        return ConversionResult(success=True, output_file=output_file)
    except Exception as e:
        return ConversionResult(success=False, error_message=str(e))

def parse_pdf_content(file_path: str) -> str:
    """解析PDF内容"""
    with pdfplumber.open(file_path) as pdf:
        return "\n".join(page.extract_text() or "" for page in pdf.pages)

def convert_to_markdown(content: str) -> str:
    """转换为Markdown格式"""
    # 实现Markdown转换逻辑
    pass

def write_output_file(file_path: str, content: str):
    """写入输出文件"""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as f:
        f.write(content)
```

### 4.3 测试配置

#### pytest 配置

```ini
# pytest.ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = -v --tb=short --strict-markers
markers =
    unit: 单元测试
    integration: 集成测试
    functional: 功能测试
    slow: 慢速测试
```

#### 测试覆盖率配置

```ini
# .coveragerc
[run]
source = src
omit = 
    */tests/*
    */venv/*
    setup.py

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
```

## 5. 风险评估

### 5.1 技术风险

#### 测试稳定性

- **风险**：测试可能不稳定，影响开发效率
- **缓解措施**：使用稳定的测试数据和 Mock 对象

#### 测试性能

- **风险**：测试执行时间过长
- **缓解措施**：优化测试结构，使用并行执行

#### 测试维护

- **风险**：测试代码难以维护
- **缓解措施**：清晰的测试结构和文档

### 5.2 缓解措施

- 建立完善的测试数据管理
- 实现测试并行执行
- 提供详细的测试文档
- 定期重构测试代码

## 6. 核心要点

### 测试框架设计原则

- **TDD 驱动**：测试先行，保证代码质量
- **全面覆盖**：核心功能 100% 测试覆盖
- **快速执行**：测试执行时间 < 30 秒
- **易于维护**：清晰的测试结构和文档
- **可重复性**：测试结果稳定可靠

### 技术约束

- **MVP 约束**：基础测试功能，无高级测试工具
- **性能边界**：测试执行时间控制在合理范围内
- **覆盖边界**：核心功能 100% 覆盖

### 开发策略

- **测试先行**：先写测试，再写代码
- **渐进式开发**：从单元测试开始，逐步完善
- **持续集成**：支持 CI/CD 流程

> **一句话总结**：通过 TDD 驱动和全面测试覆盖，确保代码质量和功能可靠性。
