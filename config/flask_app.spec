# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['src\\flask_app.py'],
    pathex=['D:\\Programming\\Projects\\AI-image-upscaler\\src'],
    binaries=[],
    datas=[
        ('D:\\Programming\\Projects\\AI-image-upscaler\\src\\models\\DSRCNN.keras', 'models'),
        ('D:\\Programming\\Projects\\AI-image-upscaler\\src\\static', 'static'),
        ('D:\\Programming\\Projects\\AI-image-upscaler\\src\\templates', 'templates'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='flask_app',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
