@echo off
setlocal enabledelayedexpansion

REM Omnisolace 项目启动脚本 (Windows版本)
REM 用于快速启动开发环境

title Omnisolace - 全年龄段AI心理疏导机器人

echo ================================================== 
echo   Omnisolace v1.0.0
echo   全年龄段 AI 心理疏导机器人
echo ==================================================
echo.

REM 检查 Node.js 版本
:check_node
echo 正在检查 Node.js 环境...

where node >nul 2>nul
if %errorlevel% neq 0 (
    echo [错误] 未找到 Node.js，请先安装 Node.js (建议版本 18+)
    echo 下载地址: https://nodejs.org/
    pause
    exit /b 1
)

for /f "tokens=1 delims=v" %%i in ('node -v') do set NODE_VERSION=%%i
for /f "tokens=1 delims=." %%i in ("%NODE_VERSION:v=%") do set MAJOR_VERSION=%%i

if %MAJOR_VERSION% lss 16 (
    echo [错误] Node.js 版本过低 (%NODE_VERSION%)，请升级到 16+ 版本
    pause
    exit /b 1
)

echo [√] Node.js 版本: %NODE_VERSION%

REM 检查包管理器
:check_package_manager
where pnpm >nul 2>nul
if %errorlevel% equ 0 (
    set PACKAGE_MANAGER=pnpm
    goto :package_manager_found
)

where yarn >nul 2>nul
if %errorlevel% equ 0 (
    set PACKAGE_MANAGER=yarn
    goto :package_manager_found
)

where npm >nul 2>nul
if %errorlevel% equ 0 (
    set PACKAGE_MANAGER=npm
    goto :package_manager_found
)

echo [错误] 未找到包管理器 (npm/yarn/pnpm)
pause
exit /b 1

:package_manager_found
echo [√] 使用包管理器: %PACKAGE_MANAGER%

REM 处理命令行参数
set CLEAN_MODE=false
set BUILD_MODE=false
set PREVIEW_MODE=false

:parse_args
if "%1"=="" goto :args_parsed
if "%1"=="-h" goto :show_help
if "%1"=="--help" goto :show_help
if "%1"=="-c" set CLEAN_MODE=true
if "%1"=="--clean" set CLEAN_MODE=true
if "%1"=="-b" set BUILD_MODE=true
if "%1"=="--build" set BUILD_MODE=true
if "%1"=="-p" set PREVIEW_MODE=true
if "%1"=="--preview" set PREVIEW_MODE=true
shift
goto :parse_args

:args_parsed

REM 清理模式
if "%CLEAN_MODE%"=="true" (
    echo 正在清理缓存...
    if exist node_modules (
        rmdir /s /q node_modules
        echo [√] 清理 node_modules
    )
    if exist dist (
        rmdir /s /q dist
        echo [√] 清理构建文件
    )
    
    if "%PACKAGE_MANAGER%"=="pnpm" (
        pnpm store prune
    ) else if "%PACKAGE_MANAGER%"=="yarn" (
        yarn cache clean
    ) else (
        npm cache clean --force
    )
    echo [√] 缓存清理完成
)

REM 构建模式
if "%BUILD_MODE%"=="true" (
    call :install_dependencies
    call :check_env
    call :build_production
    pause
    exit /b 0
)

REM 预览模式
if "%PREVIEW_MODE%"=="true" (
    call :install_dependencies
    call :check_env
    call :preview_production
    pause
    exit /b 0
)

REM 默认启动开发服务器
call :install_dependencies
call :check_env
call :start_dev_server
goto :end

REM 安装依赖
:install_dependencies
echo 正在安装项目依赖...

if not exist node_modules (
    echo 首次运行，安装依赖可能需要几分钟...
)

if "%PACKAGE_MANAGER%"=="pnpm" (
    pnpm install
) else if "%PACKAGE_MANAGER%"=="yarn" (
    yarn install
) else (
    npm install
)

if %errorlevel% equ 0 (
    echo [√] 依赖安装完成
) else (
    echo [×] 依赖安装失败
    pause
    exit /b 1
)
goto :eof

REM 检查环境变量
:check_env
echo 正在检查环境配置...

if not exist .env.local (
    if not exist .env (
        if exist env.example (
            echo 创建环境配置文件...
            copy env.example .env.local >nul
            echo [√] 已创建 .env.local 文件
            echo [提示] 请根据需要修改 .env.local 中的配置
        ) else (
            echo [警告] 未找到环境配置文件
        )
    ) else (
        echo [√] 环境配置文件存在
    )
) else (
    echo [√] 环境配置文件存在
)
goto :eof

REM 启动开发服务器
:start_dev_server
echo 正在启动开发服务器...
echo 服务器将在 http://localhost:5173 启动
echo 按 Ctrl+C 停止服务器
echo.

if "%PACKAGE_MANAGER%"=="pnpm" (
    pnpm dev
) else if "%PACKAGE_MANAGER%"=="yarn" (
    yarn dev
) else (
    npm run dev
)
goto :eof

REM 构建生产版本
:build_production
echo 正在构建生产版本...

if "%PACKAGE_MANAGER%"=="pnpm" (
    pnpm build
) else if "%PACKAGE_MANAGER%"=="yarn" (
    yarn build
) else (
    npm run build
)

if %errorlevel% equ 0 (
    echo [√] 构建完成，文件位于 dist 目录
) else (
    echo [×] 构建失败
    exit /b 1
)
goto :eof

REM 预览生产版本
:preview_production
echo 正在启动生产版本预览...

if not exist dist (
    echo 未找到构建文件，正在构建...
    call :build_production
)

if "%PACKAGE_MANAGER%"=="pnpm" (
    pnpm preview
) else if "%PACKAGE_MANAGER%"=="yarn" (
    yarn preview
) else (
    npm run preview
)
goto :eof

REM 显示帮助信息
:show_help
echo 使用方法:
echo   start.bat [选项]
echo.
echo 选项:
echo   -h, --help     显示帮助信息
echo   -c, --clean    清理缓存后启动
echo   -b, --build    构建生产版本
echo   -p, --preview  预览生产版本
echo.
echo 示例:
echo   start.bat          # 启动开发服务器
echo   start.bat --clean  # 清理缓存后启动
echo   start.bat --build  # 构建生产版本
echo.
pause
exit /b 0

:end
pause
