#!/bin/bash

# 翼术师世界 - GitHub 部署脚本
# 使用方法: chmod +x deploy.sh && ./deploy.sh

set -e

echo "🪶 翼术师世界 - 部署到 GitHub"
echo "================================"
echo ""

# 颜色定义
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 检查是否在正确的目录
if [ ! -f "index.html" ]; then
    echo -e "${RED}错误: 请在项目根目录运行此脚本${NC}"
    exit 1
fi

echo -e "${BLUE}步骤 1/5: 检查 Git 状态${NC}"
if [ ! -d ".git" ]; then
    echo "初始化 Git 仓库..."
    git init
    echo -e "${GREEN}✓ Git 仓库已初始化${NC}"
else
    echo -e "${GREEN}✓ Git 仓库已存在${NC}"
fi
echo ""

echo -e "${BLUE}步骤 2/5: 添加所有文件${NC}"
git add .
echo -e "${GREEN}✓ 文件已添加${NC}"
echo ""

echo -e "${BLUE}步骤 3/5: 创建提交${NC}"
if git diff-index --quiet HEAD 2>/dev/null; then
    echo -e "${YELLOW}没有新的更改需要提交${NC}"
else
    read -p "请输入提交信息 (默认: 更新内容): " commit_message
    commit_message=${commit_message:-"更新内容"}
    git commit -m "$commit_message"
    echo -e "${GREEN}✓ 提交已创建${NC}"
fi
echo ""

echo -e "${BLUE}步骤 4/5: 配置远程仓库${NC}"
if git remote | grep -q "origin"; then
    echo -e "${GREEN}✓ 远程仓库已配置${NC}"
    git remote -v
else
    echo -e "${YELLOW}请输入您的 GitHub 仓库 URL${NC}"
    echo "格式: https://github.com/用户名/仓库名.git"
    read -p "仓库 URL: " repo_url
    
    if [ -z "$repo_url" ]; then
        echo -e "${RED}错误: 仓库 URL 不能为空${NC}"
        exit 1
    fi
    
    git remote add origin "$repo_url"
    echo -e "${GREEN}✓ 远程仓库已添加${NC}"
fi
echo ""

echo -e "${BLUE}步骤 5/5: 推送到 GitHub${NC}"
read -p "是否推送到 GitHub? (y/n): " confirm
if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
    echo "推送到 main 分支..."
    git branch -M main
    git push -u origin main
    echo -e "${GREEN}✓ 已推送到 GitHub${NC}"
else
    echo -e "${YELLOW}跳过推送${NC}"
fi
echo ""

echo "================================"
echo -e "${GREEN}🎉 部署脚本执行完成！${NC}"
echo ""
echo "📝 下一步操作:"
echo "1. 访问 https://github.com/你的用户名/仓库名"
echo "2. 进入 Settings → Pages"
echo "3. Source 选择: GitHub Actions"
echo "4. 等待几分钟后访问你的网站"
echo ""
echo "🔗 你的网站将在以下地址可用:"
echo "   https://你的用户名.github.io/仓库名/"
echo ""
echo -e "${BLUE}身无彩凤双飞翼，心有灵犀一点通${NC} ✨"
