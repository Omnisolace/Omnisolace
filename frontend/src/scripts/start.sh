#!/bin/bash

# Omnisolace 项目启动脚本
# 用于快速启动开发环境

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 项目信息
PROJECT_NAME="Omnisolace"
PROJECT_VERSION="1.0.0"

echo -e "${BLUE}"
echo "=================================================="
echo "  $PROJECT_NAME v$PROJECT_VERSION"
echo "  全年龄段 AI 心理疏导机器人"
echo "=================================================="
echo -e "${NC}"

# 检查 Node.js 版本
check_node() {
    echo -e "${YELLOW}正在检查 Node.js 环境...${NC}"
    
    if ! command -v node &> /dev/null; then
        echo -e "${RED}错误: 未找到 Node.js，请先安装 Node.js (建议版本 18+)${NC}"
        exit 1
    fi
    
    NODE_VERSION=$(node -v | cut -d'v' -f2)
    MAJOR_VERSION=$(echo $NODE_VERSION | cut -d'.' -f1)
    
    if [ $MAJOR_VERSION -lt 16 ]; then
        echo -e "${RED}错误: Node.js 版本过低 ($NODE_VERSION)，请升级到 16+ 版本${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✓ Node.js 版本: $NODE_VERSION${NC}"
}

# 检查包管理器
check_package_manager() {
    if command -v pnpm &> /dev/null; then
        PACKAGE_MANAGER="pnpm"
    elif command -v yarn &> /dev/null; then
        PACKAGE_MANAGER="yarn"
    elif command -v npm &> /dev/null; then
        PACKAGE_MANAGER="npm"
    else
        echo -e "${RED}错误: 未找到包管理器 (npm/yarn/pnpm)${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✓ 使用包管理器: $PACKAGE_MANAGER${NC}"
}

# 安装依赖
install_dependencies() {
    echo -e "${YELLOW}正在安装项目依赖...${NC}"
    
    if [ ! -d "node_modules" ]; then
        echo -e "${BLUE}首次运行，安装依赖可能需要几分钟...${NC}"
    fi
    
    case $PACKAGE_MANAGER in
        "pnpm")
            pnpm install
            ;;
        "yarn")
            yarn install
            ;;
        "npm")
            npm install
            ;;
    esac
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ 依赖安装完成${NC}"
    else
        echo -e "${RED}✗ 依赖安装失败${NC}"
        exit 1
    fi
}

# 检查环境变量
check_env() {
    echo -e "${YELLOW}正在检查环境配置...${NC}"
    
    if [ ! -f ".env.local" ] && [ ! -f ".env" ]; then
        if [ -f "env.example" ]; then
            echo -e "${BLUE}创建环境配置文件...${NC}"
            cp env.example .env.local
            echo -e "${GREEN}✓ 已创建 .env.local 文件${NC}"
            echo -e "${YELLOW}提示: 请根据需要修改 .env.local 中的配置${NC}"
        else
            echo -e "${YELLOW}警告: 未找到环境配置文件${NC}"
        fi
    else
        echo -e "${GREEN}✓ 环境配置文件存在${NC}"
    fi
}

# 启动开发服务器
start_dev_server() {
    echo -e "${YELLOW}正在启动开发服务器...${NC}"
    echo -e "${BLUE}服务器将在 http://localhost:5173 启动${NC}"
    echo -e "${BLUE}按 Ctrl+C 停止服务器${NC}"
    echo ""
    
    case $PACKAGE_MANAGER in
        "pnpm")
            pnpm dev
            ;;
        "yarn")
            yarn dev
            ;;
        "npm")
            npm run dev
            ;;
    esac
}

# 显示帮助信息
show_help() {
    echo -e "${BLUE}使用方法:${NC}"
    echo "  ./scripts/start.sh [选项]"
    echo ""
    echo -e "${BLUE}选项:${NC}"
    echo "  -h, --help     显示帮助信息"
    echo "  -c, --clean    清理缓存后启动"
    echo "  -b, --build    构建生产版本"
    echo "  -p, --preview  预览生产版本"
    echo ""
    echo -e "${BLUE}示例:${NC}"
    echo "  ./scripts/start.sh          # 启动开发服务器"
    echo "  ./scripts/start.sh --clean  # 清理缓存后启动"
    echo "  ./scripts/start.sh --build  # 构建生产版本"
}

# 清理缓存
clean_cache() {
    echo -e "${YELLOW}正在清理缓存...${NC}"
    
    # 清理 node_modules
    if [ -d "node_modules" ]; then
        rm -rf node_modules
        echo -e "${GREEN}✓ 清理 node_modules${NC}"
    fi
    
    # 清理构建缓存
    if [ -d "dist" ]; then
        rm -rf dist
        echo -e "${GREEN}✓ 清理构建文件${NC}"
    fi
    
    # 清理包管理器缓存
    case $PACKAGE_MANAGER in
        "pnpm")
            pnpm store prune
            ;;
        "yarn")
            yarn cache clean
            ;;
        "npm")
            npm cache clean --force
            ;;
    esac
    
    echo -e "${GREEN}✓ 缓存清理完成${NC}"
}

# 构建生产版本
build_production() {
    echo -e "${YELLOW}正在构建生产版本...${NC}"
    
    case $PACKAGE_MANAGER in
        "pnpm")
            pnpm build
            ;;
        "yarn")
            yarn build
            ;;
        "npm")
            npm run build
            ;;
    esac
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ 构建完成，文件位于 dist 目录${NC}"
    else
        echo -e "${RED}✗ 构建失败${NC}"
        exit 1
    fi
}

# 预览生产版本
preview_production() {
    echo -e "${YELLOW}正在启动生产版本预览...${NC}"
    
    if [ ! -d "dist" ]; then
        echo -e "${YELLOW}未找到构建文件，正在构建...${NC}"
        build_production
    fi
    
    case $PACKAGE_MANAGER in
        "pnpm")
            pnpm preview
            ;;
        "yarn")
            yarn preview
            ;;
        "npm")
            npm run preview
            ;;
    esac
}

# 主函数
main() {
    # 解析命令行参数
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_help
                exit 0
                ;;
            -c|--clean)
                CLEAN_MODE=true
                shift
                ;;
            -b|--build)
                BUILD_MODE=true
                shift
                ;;
            -p|--preview)
                PREVIEW_MODE=true
                shift
                ;;
            *)
                echo -e "${RED}未知选项: $1${NC}"
                show_help
                exit 1
                ;;
        esac
    done
    
    # 执行检查
    check_node
    check_package_manager
    
    # 处理不同模式
    if [ "$CLEAN_MODE" = true ]; then
        clean_cache
    fi
    
    if [ "$BUILD_MODE" = true ]; then
        install_dependencies
        check_env
        build_production
        exit 0
    fi
    
    if [ "$PREVIEW_MODE" = true ]; then
        install_dependencies
        check_env
        preview_production
        exit 0
    fi
    
    # 默认启动开发服务器
    install_dependencies
    check_env
    start_dev_server
}

# 错误处理
trap 'echo -e "\n${RED}启动被中断${NC}"; exit 1' INT TERM

# 运行主函数
main "$@"
