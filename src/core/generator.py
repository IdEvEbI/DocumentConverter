"""
文档生成器模块

提供不同格式文档的生成功能。
"""

from abc import ABC, abstractmethod

from .parser import DocumentStructure


class DocumentGenerator(ABC):
    """文档生成器基类"""

    @abstractmethod
    def generate(self, document: DocumentStructure, output_path: str) -> bool:
        """生成文档文件"""
        pass

    @abstractmethod
    def can_generate(self, output_path: str) -> bool:
        """检查是否可以生成指定格式"""
        pass


class MarkdownGenerator(DocumentGenerator):
    """Markdown 文档生成器"""

    def generate(self, document: DocumentStructure, output_path: str) -> bool:
        """生成 Markdown 文档"""
        # TODO: 实现 Markdown 生成逻辑
        raise NotImplementedError("Markdown 生成功能尚未实现")

    def can_generate(self, output_path: str) -> bool:
        """检查是否为 Markdown 文件"""
        return output_path.lower().endswith(".md")


class WordGenerator(DocumentGenerator):
    """Word 文档生成器"""

    def generate(self, document: DocumentStructure, output_path: str) -> bool:
        """生成 Word 文档"""
        # TODO: 实现 Word 生成逻辑
        raise NotImplementedError("Word 生成功能尚未实现")

    def can_generate(self, output_path: str) -> bool:
        """检查是否为 Word 文件"""
        return output_path.lower().endswith((".docx", ".doc"))
