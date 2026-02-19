"""
打包脚本：将应用打包为独立可执行文件
使用 PyInstaller 打包人生倒计时应用
"""

import os
import shutil
import subprocess
import sys


def clean_build():
    """清理之前的构建文件"""
    dirs_to_remove = ['build', 'dist']
    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            print(f"正在清理 {dir_name}/...")
            shutil.rmtree(dir_name)
    
    # 清理 spec 文件
    for file in os.listdir('.'):
        if file.endswith('.spec'):
            print(f"正在删除 {file}...")
            os.remove(file)
    print("清理完成！\n")


def build_app():
    """使用 PyInstaller 打包应用"""
    print("开始打包应用...")
    
    # PyInstaller 命令参数
    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--name=人生计时器',           # 应用名称
        '--windowed',                  # 不显示控制台窗口
        '--onefile',                   # 打包为单个可执行文件
        '--icon=assets/app.ico',                 # 可以添加图标: --icon=app.ico
        '--clean',                     # 清理缓存
        # 添加数据文件
        '--add-data', f'settings.json{os.pathsep}.',
        '--add-data', f'assets{os.pathsep}assets',
        # 隐藏导入（确保模块被包含）
        '--hidden-import=core.settings',
        '--hidden-import=core.calculator',
        '--hidden-import=ui.main_window',
        '--hidden-import=ui.settings_dialog',
        # 主程序入口
        'main.py'
    ]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=False)
        print("\n✅ 打包成功！")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ 打包失败: {e}")
        return False
    except FileNotFoundError:
        print("\n❌ 未找到 PyInstaller，请先安装: uv add --dev pyinstaller")
        return False


def copy_output():
    """复制输出文件到根目录"""
    exe_name = '人生计时器.exe' if sys.platform == 'win32' else '人生计时器'
    src = os.path.join('dist', exe_name)
    dst = exe_name
    
    if os.path.exists(src):
        shutil.copy2(src, dst)
        print(f"\n📦 可执行文件已生成: {dst}")
        print(f"   文件大小: {os.path.getsize(dst) / 1024 / 1024:.1f} MB")


def main():
    """主函数"""
    print("=" * 50)
    print("人生计时器 - 打包工具")
    print("=" * 50 + "\n")
    
    # 步骤1: 清理
    clean_build()
    
    # 步骤2: 打包
    if build_app():
        # 步骤3: 复制输出
        copy_output()
        print("\n" + "=" * 50)
        print("打包完成！请查看生成的可执行文件。")
        print("=" * 50)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
