from PyInstaller.utils.hooks import collect_submodules
import os

hidden_imports = collect_submodules('keras')

block_cipher = None

a = Analysis(
    ['flask_app.py'],
    pathex=['D:\\Programming\\Projects\\Image-upscaler'],
    binaries=[],
    datas=[
        ('D:\\Programming\\Projects\\Image-upscaler\\models\\DSRCNN.keras', 'models'),
        ('D:\\Programming\\Projects\\Image-upscaler\\static', 'static'),
        ('D:\\Programming\\Projects\\Image-upscaler\\templates', 'templates'),
    ],
    hiddenimports=hidden_imports,
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='flask_app',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='flask_app',
)