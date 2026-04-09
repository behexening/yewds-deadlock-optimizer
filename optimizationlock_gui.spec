# -*- mode: python ; coding: utf-8 -*-
import os

block_cipher = None

font_dir = os.path.join('build_dir', 'fonts')
font_files = [(os.path.join(font_dir, f), 'fonts') for f in os.listdir(font_dir)]

a = Analysis(
    ['optimizationlock_gui.py'],
    pathex=[],
    binaries=[],
    datas=font_files,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='OptimizationLock_Configurator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
