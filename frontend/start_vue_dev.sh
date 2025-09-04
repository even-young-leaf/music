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

# 启动开发服务器
echo "正在启动Vue开发服务器..."
npm run serve