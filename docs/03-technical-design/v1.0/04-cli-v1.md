# DocumentConverter 命令行接口 v1.0 设计文档

## 1. 文档目标

本文档定义 DocumentConverter 项目 v1.0 MVP 版本的命令行界面设计，专注用户交互和命令结构。

> **适用范围**：Python 项目开发，命令行工具。

---

**文档版本**：v1.0  
**最后更新**：2025-07-30  
**更新内容**：精简内容，专注 CLI 设计，删除重复内容

## 2. 设计概述

### 2.1 设计目标

基于 PRD 需求，设计简洁高效的命令行接口，实现：

- **简单易用**：直观的命令结构，清晰的参数说明
- **功能完整**：支持所有核心转换功能
- **错误友好**：清晰的错误提示和帮助信息
- **进度显示**：转换进度和状态反馈
- **批量处理**：支持批量文件转换

### 2.2 设计原则

- **KISS 原则**：保持简单，避免复杂参数
- **一致性**：统一的命令结构和参数格式
- **可扩展性**：易于添加新功能和选项
- **用户友好**：清晰的帮助信息和错误提示

### 2.3 技术选型

#### CLI 框架

- **click**：功能强大的命令行界面框架
- **rich**：终端美化输出和进度显示

#### 参数处理

- **typer**：类型提示和参数验证
- **pathlib**：路径处理和验证

## 3. 详细设计

### 3.1 架构设计

#### CLI 模块架构

```text
┌─────────────────┐
│   CLI Layer     │  # 命令行接口层
│                 │
│  - Commands     │  # 命令定义
│  - Interface    │  # 用户交互
│  - Validation   │  # 输入验证
├─────────────────┤
│   Core Layer    │  # 核心业务层
│                 │
│  - Converter    │  # 转换器调用
│  - File I/O     │  # 文件操作
│  - Progress     │  # 进度显示
├─────────────────┤
│  Utility Layer  │  # 工具层
│                 │
│  - Logger       │  # 日志记录
│  - Error Handler│  # 错误处理
│  - Help System  │  # 帮助系统
└─────────────────┘
```

### 3.2 接口设计

#### 主要命令结构

```python
import click
from rich.console import Console
from rich.progress import Progress

@click.group()
@click.version_option(version="1.0.0")
def cli():
    """DocumentConverter - 智能文档转换工具"""
    pass

@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.argument('output_file', type=click.Path())
@click.option('--format', '-f', 
              type=click.Choice(['pdf2md', 'word2md', 'md2word']),
              help='转换格式')
@click.option('--verbose', '-v', is_flag=True, help='详细输出')
@click.option('--quiet', '-q', is_flag=True, help='静默模式')
def convert(input_file, output_file, format, verbose, quiet):
    """转换单个文件"""
    pass

@cli.command()
@click.argument('input_dir', type=click.Path(exists=True))
@click.argument('output_dir', type=click.Path())
@click.option('--format', '-f', 
              type=click.Choice(['pdf2md', 'word2md', 'md2word']),
              help='转换格式')
@click.option('--recursive', '-r', is_flag=True, help='递归处理子目录')
def batch(input_dir, output_dir, format, recursive):
    """批量转换文件"""
    pass

@cli.command()
def list_formats():
    """列出支持的格式"""
    pass

@cli.command()
@click.argument('file_path', type=click.Path(exists=True))
def info(file_path):
    """显示文件信息"""
    pass
```

### 3.3 命令设计

#### 转换命令

```bash
# 基础转换
documentconverter convert input.pdf output.md --format pdf2md

# 自动格式检测
documentconverter convert input.docx output.md

# 详细输出
documentconverter convert input.pdf output.md -v

# 静默模式
documentconverter convert input.pdf output.md -q
```

#### 批量转换命令

```bash
# 批量转换
documentconverter batch input_dir output_dir --format pdf2md

# 递归处理
documentconverter batch input_dir output_dir -r

# 自动格式检测
documentconverter batch input_dir output_dir
```

#### 信息命令

```bash
# 列出支持格式
documentconverter list-formats

# 显示文件信息
documentconverter info sample.pdf
```

### 3.4 用户交互设计

#### 进度显示

```python
def show_progress(total_files: int):
    """显示转换进度"""
    with Progress() as progress:
        task = progress.add_task("转换中...", total=total_files)
        
        for i in range(total_files):
            # 执行转换
            convert_file(files[i])
            progress.update(task, advance=1)
```

#### 错误处理

```python
def handle_error(error: Exception, context: str):
    """统一错误处理"""
    console = Console()
    
    if isinstance(error, FileNotFoundError):
        console.print(f"[red]错误[/red]: 文件未找到 - {context}")
    elif isinstance(error, UnsupportedFormatError):
        console.print(f"[red]错误[/red]: 不支持的文件格式 - {context}")
    else:
        console.print(f"[red]错误[/red]: {str(error)}")
    
    sys.exit(1)
```

#### 帮助信息

```python
def show_help():
    """显示帮助信息"""
    console = Console()
    
    console.print("""
[bold blue]DocumentConverter[/bold blue] - 智能文档转换工具

[bold]用法:[/bold]
  documentconverter convert <input> <output> [options]
  documentconverter batch <input_dir> <output_dir> [options]

[bold]支持的格式:[/bold]
  pdf2md  - PDF 转 Markdown
  word2md - Word 转 Markdown
  md2word - Markdown 转 Word

[bold]示例:[/bold]
  documentconverter convert sample.pdf sample.md
  documentconverter batch docs/ converted/ --format pdf2md
    """)
```

## 4. 实现计划

### 4.1 开发阶段

#### 第一阶段：基础命令（MVP）

- [ ] 实现 convert 命令
  - [ ] 文件路径验证
  - [ ] 格式检测和转换
  - [ ] 基础错误处理
  - [ ] 简单进度显示

- [ ] 实现 list-formats 命令
  - [ ] 格式列表显示
  - [ ] 格式说明信息

#### 第二阶段：功能完善

- [ ] 实现 batch 命令
  - [ ] 目录遍历
  - [ ] 批量转换
  - [ ] 递归处理

- [ ] 实现 info 命令
  - [ ] 文件信息显示
  - [ ] 格式检测

#### 第三阶段：用户体验

- [ ] 进度显示优化
- [ ] 错误处理完善
- [ ] 帮助信息完善
- [ ] 日志系统集成

### 4.2 测试策略

#### CLI 测试

```python
def test_convert_command_basic():
    """测试基础转换命令"""
    runner = CliRunner()
    result = runner.invoke(cli, ['convert', 'test.pdf', 'test.md'])
    
    assert result.exit_code == 0
    assert "转换完成" in result.output

def test_convert_command_invalid_file():
    """测试无效文件处理"""
    runner = CliRunner()
    result = runner.invoke(cli, ['convert', 'nonexistent.pdf', 'test.md'])
    
    assert result.exit_code == 1
    assert "文件未找到" in result.output

def test_batch_command():
    """测试批量转换命令"""
    runner = CliRunner()
    result = runner.invoke(cli, ['batch', 'test_dir', 'output_dir'])
    
    assert result.exit_code == 0
    assert "批量转换完成" in result.output
```

### 4.3 错误处理策略

#### 输入验证

```python
def validate_input_file(file_path: str) -> bool:
    """验证输入文件"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"文件不存在: {file_path}")
    
    if not os.path.isfile(file_path):
        raise ValueError(f"不是文件: {file_path}")
    
    return True

def validate_output_file(file_path: str) -> bool:
    """验证输出文件"""
    output_dir = os.path.dirname(file_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    
    return True

def detect_format(file_path: str) -> str:
    """自动检测文件格式"""
    ext = os.path.splitext(file_path)[1].lower()
    
    format_map = {
        '.pdf': 'pdf2md',
        '.docx': 'word2md',
        '.doc': 'word2md',
        '.md': 'md2word'
    }
    
    if ext not in format_map:
        raise UnsupportedFormatError(f"不支持的文件格式: {ext}")
    
    return format_map[ext]
```

## 5. 风险评估

### 5.1 技术风险

#### 用户体验

- **风险**：命令行界面可能不够友好
- **缓解措施**：提供详细的帮助信息和错误提示

#### 参数复杂性

- **风险**：参数过多可能导致使用复杂
- **缓解措施**：保持参数简洁，提供合理的默认值

#### 错误处理

- **风险**：错误信息可能不够清晰
- **缓解措施**：实现统一的错误处理和用户友好的错误信息

### 5.2 缓解措施

- 提供详细的帮助文档和示例
- 实现统一的错误处理机制
- 进行充分的用户测试
- 提供多种输出模式（详细/简洁）

## 6. 核心要点

### CLI 设计原则

- **简单易用**：直观的命令结构，清晰的参数说明
- **一致性**：统一的命令结构和参数格式
- **可扩展性**：易于添加新功能和选项
- **用户友好**：清晰的帮助信息和错误提示

### 技术约束

- **MVP 约束**：基础命令功能，无高级选项
- **性能边界**：基础性能，支持单文件和批量处理
- **格式边界**：支持主流文档格式

### 开发策略

- **渐进式开发**：从基础命令开始，逐步完善功能
- **用户测试**：持续收集用户反馈，优化用户体验
- **文档驱动**：详细的帮助文档和示例

> **一句话总结**：通过简洁的命令结构和友好的用户交互，提供易用的文档转换工具。
