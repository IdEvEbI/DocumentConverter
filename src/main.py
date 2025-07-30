"""
DocumentConverter 主入口模块

提供命令行工具的入口点。
"""

from .cli import cli


def main():
    """主函数"""
    cli()


if __name__ == "__main__":
    main()
