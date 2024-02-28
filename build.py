import subprocess
from pathlib import Path

spec = Path('./base.spec')
if spec.exists():
    subprocess.run(['pyinstaller', './base.spec'])
else:
    subprocess.run(
        [
            'pyinstaller',
            '--onefile',
            '--name',
            'Sprite Cut Tool',
            '--icon',
            'Icon.ico',
            '--version-file',
            'build_info.txt',
            '--add-data',
            'Icon.ico;.',
            '--add-data',
            'head.png;.',
            '--add-data',
            './venv/Lib/site-packages/tkinterdnd2;tkinterdnd2/',
            '--exclude',
            'altgraph',
            '--exclude',
            'packaging',
            '--exclude',
            'pefile',
            '--exclude',
            'pip',
            '--exclude',
            'pyinstaller',
            '--exclude',
            'pyinstaller-hooks-contrib',
            '--exclude',
            'pywin32-ctypes',
            '--exclude',
            'setuptools',
            'base.py',
        ]
    )
