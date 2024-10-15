import subprocess
from pathlib import Path

# fmt: off
target_file_name = './Sprite_Cut_Tool'
spec = Path(f'{target_file_name}.spec')
if spec.exists():
    subprocess.run(['pyinstaller', f'{target_file_name}.spec', '--clean'])
else:
    subprocess.run(
        [
            'pyinstaller', '--onefile', '--name', 'Sprite Cut Tool',
            '--icon', 'Icon.ico',
            '--version-file', 'build_info.txt',
            '--add-data', 'Icon.ico;.', # 添加图标
            '--add-data', 'head.png;.', # 添加图片资源
            '--add-data', './venv/Lib/site-packages/tkinterdnd2;tkinterdnd2/', # 添加 tkinterdnd2 库
            '--exclude-module', 'altgraph', # 过滤不需要的库
            '--exclude-module', 'packaging',
            '--exclude-module', 'pefile',
            '--exclude-module', 'pip',
            '--exclude-module', 'pyinstaller',
            '--exclude-module', 'pyinstaller-hooks-contrib',
            '--exclude-module', 'pywin32-ctypes',
            '--exclude-module', 'setuptools',
            '--exclude-module','nuitka',
            '--exclude-module','zstandard',
            # '--exclude-module','tkinterdnd2',
            # '--exclude-module','pillow',
            '--noconsole',  # 不显示控制台
            '--strip',  # 删除调试信息，减小体积
            '--clean',  # 清理之前生成的文件
            f'{target_file_name}.py'
        ]
    )
