"""环境验证测试"""

import pytest


def test_python_version():
    """测试 Python 版本"""
    import sys

    assert sys.version_info >= (3, 12), "Python 版本需要 3.12+"


def test_required_packages():
    """测试必需包的导入"""
    import click
    import docx
    import markdown  # type: ignore
    import markdownify  # type: ignore
    import pdfplumber
    import PyPDF2
    import rich

    # 验证包已正确安装（只检查可以导入的包）
    # 注意：某些包可能没有 __version__ 属性，这里只验证导入成功
    assert click is not None
    assert rich is not None
    assert pdfplumber is not None
    assert PyPDF2 is not None
    assert docx is not None
    assert markdown is not None
    assert markdownify is not None


def test_dev_packages():
    """测试开发包的导入"""
    import black
    import flake8  # type: ignore
    import pytest

    # 验证开发包已正确安装（只检查可以导入的包）
    assert pytest is not None
    assert black is not None
    assert flake8 is not None


def test_project_structure():
    """测试项目目录结构"""
    import os

    # 检查必需的目录
    required_dirs = [
        "src",
        "src/cli",
        "src/core",
        "src/utils",
        "tests",
        "tests/data",
        "scripts",
        ".vscode",
    ]

    for dir_path in required_dirs:
        assert os.path.exists(dir_path), f"目录 {dir_path} 不存在"

    # 检查必需的文件
    required_files = [
        "src/__init__.py",
        "src/cli/__init__.py",
        "src/core/__init__.py",
        "src/utils/__init__.py",
        "tests/__init__.py",
        "requirements.txt",
        "requirements-dev.txt",
        "pyproject.toml",
        "setup.py",
        ".vscode/settings.json",
        ".vscode/extensions.json",
        "scripts/setup_env.sh",
        "scripts/run_tests.sh",
    ]

    for file_path in required_files:
        assert os.path.exists(file_path), f"文件 {file_path} 不存在"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
