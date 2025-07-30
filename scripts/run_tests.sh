#!/bin/bash
# scripts/run_tests.sh

echo "🧪 运行测试套件..."

# 激活虚拟环境
source venv/bin/activate

# 运行测试
echo "📋 运行单元测试..."
python -m pytest tests/ -v

# 运行代码质量检查
echo "🔍 运行代码质量检查..."
black --check src/
flake8 src/

echo "✅ 测试完成！" 