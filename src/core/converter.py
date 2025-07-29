"""
文档转换器核心模块

提供文档格式转换的核心功能和数据模型。
"""

from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class ConversionOptions:
    """转换选项配置"""

    preserve_formatting: bool = True
    include_images: bool = True
    include_tables: bool = True
    code_block_detection: bool = True


@dataclass
class ConversionResult:
    """转换结果模型"""

    success: bool
    output_file: str
    error_message: Optional[str] = None
    conversion_stats: Optional[Dict[str, Any]] = None


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
