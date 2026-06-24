# Project Setup Script for Patent Review Skill

"""
项目安装和设置脚本
"""

import os
import sys
import subprocess
import shutil


def print_step(step_num, message):
    """打印步骤信息"""
    print(f"\n{'='*60}")
    print(f"步骤 {step_num}: {message}")
    print('='*60)


def check_python_version():
    """检查Python版本"""
    print_step(1, "检查Python版本")
    
    version = sys.version_info
    print(f"当前Python版本: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("错误: 需要 Python 3.8 或更高版本")
        return False
    
    print("Python版本检查通过")
    return True


def install_dependencies():
    """安装依赖"""
    print_step(2, "安装依赖包")
    
    requirements_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "requirements.txt"
    )
    
    if not os.path.exists(requirements_file):
        print(f"错误: 找不到 {requirements_file}")
        return False
    
    print("正在安装依赖包...")
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", requirements_file
        ])
        print("依赖安装成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"错误: 依赖安装失败 - {e}")
        return False


def create_directories():
    """创建必要的目录"""
    print_step(3, "创建目录结构")
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    directories = [
        "output",
        "logs",
        "cache",
        "tests/output"
    ]
    
    for directory in directories:
        dir_path = os.path.join(base_dir, directory)
        os.makedirs(dir_path, exist_ok=True)
        print(f"创建目录: {directory}")
    
    print("目录创建完成")
    return True


def verify_installation():
    """验证安装"""
    print_step(4, "验证安装")
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 检查关键文件
    required_files = [
        "patent-workflow/SKILL.md",
        "patent-workflow/workflow/patent-review-workflow.json",
        "patent-workflow/workflow/node-prompts.md",
        "scripts/case_matcher.py"
    ]
    
    all_exist = True
    for file_path in required_files:
        full_path = os.path.join(base_dir, file_path)
        if os.path.exists(full_path):
            print(f"✓ {file_path}")
        else:
            print(f"✗ {file_path} - 缺失")
            all_exist = False
    
    return all_exist


def run_tests():
    """运行测试"""
    print_step(5, "运行测试")
    
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "tests/", "-v", "--tb=short"],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        
        print(result.stdout)
        
        if result.returncode == 0:
            print("\n所有测试通过！")
            return True
        else:
            print("\n部分测试失败，请检查输出")
            return False
            
    except Exception as e:
        print(f"测试运行失败: {e}")
        return False


def print_usage():
    """打印使用说明"""
    print_step(6, "安装完成 - 使用说明")
    
    print("""
欢迎使用 Patent Review Skill！

安装成功！现在您可以：

1. 运行案例匹配:
   $ python scripts/case_matcher.py --features "深度学习,神经网络"

2. 运行测试:
   $ pytest tests/ -v

3. 查看文档:
   $ cat docs/GETTING_STARTED.md

4. 查看示例:
   $ cat docs/EXAMPLES.md

更多信息请访问: https://github.com/your-org/patent-review-skill
""")


def main():
    """主函数"""
    print("\n" + "="*60)
    print("Patent Review Skill - 安装程序")
    print("="*60)
    
    steps = [
        ("检查Python版本", check_python_version),
        ("安装依赖", install_dependencies),
        ("创建目录", create_directories),
        ("验证安装", verify_installation),
        ("运行测试", run_tests),
    ]
    
    for i, (name, func) in enumerate(steps, 1):
        if not func():
            print(f"\n安装过程中断于: {name}")
            sys.exit(1)
    
    print_usage()


if __name__ == "__main__":
    main()
