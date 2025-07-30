"""
文件工具模块

提供文件操作和路径处理功能。
"""

import os


def validate_file_path(file_path: str) -> bool:
    """验证文件路径"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"文件不存在: {file_path}")

    if not os.path.isfile(file_path):
        raise ValueError(f"不是文件: {file_path}")

    return True


def create_output_dir(output_path: str) -> bool:
    """创建输出目录"""
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)

    return True


def detect_format(file_path: str) -> str:
    """自动检测文件格式"""
    ext = os.path.splitext(file_path)[1].lower()

    format_map = {
        ".pdf": "pdf2md",
        ".docx": "word2md",
        ".doc": "word2md",
        ".md": "md2word",
    }

    if ext not in format_map:
        raise ValueError(f"不支持的文件格式: {ext}")

    return format_map[ext]


def get_file_size(file_path: str) -> int:
    """获取文件大小（字节）"""
    return os.path.getsize(file_path)


def get_file_info(file_path: str) -> dict:
    """获取文件信息"""
    stat = os.stat(file_path)
    return {"size": stat.st_size, "modified": stat.st_mtime, "created": stat.st_ctime}
