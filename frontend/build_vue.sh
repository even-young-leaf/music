#!/bin/bash

# 确保脚本在frontend目录下执行
cd "$(dirname "$0")"

# 检查node和npm是否安装
if ! command -v node &> /dev/null; then
    echo "错误: 未找到node，请先安装Node.js"
    exit 1
fi

if ! command -v npm &> /dev/null; then
    echo "错误: 未找到npm，请先安装npm"
    exit 1
fi

# 安装依赖
echo "正在安装依赖..."
npm install

# 构建生产版本
echo "正在构建Vue应用..."
npm run build

echo "构建完成！"
echo "Vue应用已构建并部署到Django静态文件目录。"
echo "可以通过访问 http://localhost:8000/?vue=1 来查看Vue版本的应用。"