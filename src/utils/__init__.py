"""
DocumentConverter 工具模块

提供通用工具函数和辅助功能。
"""

from .file_utils import create_output_dir, validate_file_path
from .logger import setup_logger

__all__ = ["setup_logger", "validate_file_path", "create_output_dir"]
