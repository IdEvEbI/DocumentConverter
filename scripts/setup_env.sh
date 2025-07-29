#!/bin/bash
# scripts/setup_env.sh

echo "🚀 开始搭建 DocumentConverter 开发环境..."

# 1. 检查 Python 版本
echo "📋 检查 Python 版本..."
python_version=$(python3 --version 2>&1 | grep -o '3\.[0-9]\+')
if [[ "$python_version" < "3.12" ]]; then
    echo "❌ Python 版本过低，需要 3.12+"
    exit 1
fi
echo "✅ Python 版本检查通过: $(python3 --version)"

# 2. 创建虚拟环境
echo "📦 创建虚拟环境..."
python3 -m venv venv
source venv/bin/activate

# 3. 升级 pip
echo "⬆️ 升级 pip..."
pip install --upgrade pip

# 4. 安装依赖
echo "📚 安装项目依赖..."
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 5. 创建项目目录结构
echo "📁 创建项目目录结构..."
mkdir -p src/{cli,core,utils}
mkdir -p tests/data
mkdir -p scripts
mkdir -p .vscode

# 6. 创建基础文件
echo "📄 创建基础文件..."
touch src/__init__.py
touch src/cli/__init__.py
touch src/core/__init__.py
touch src/utils/__init__.py
touch tests/__init__.py

# 7. 配置 VSCode
echo "⚙️ 配置 VSCode..."
cat > .vscode/settings.json << EOF
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.formatting.provider": "black",
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.organizeImports": true
    }
}
EOF

cat > .vscode/extensions.json << EOF
{
    "recommendations": [
        "ms-python.python",
        "ms-python.black-formatter",
        "ms-python.flake8",
        "ms-python.mypy-type-checker"
    ]
}
EOF

echo "✅ 环境搭建完成！"
echo "📝 使用说明："
echo "   1. 激活虚拟环境: source venv/bin/activate"
echo "   2. 运行测试: python -m pytest"
echo "   3. 格式化代码: black src/"
echo "   4. 检查代码: flake8 src/" 