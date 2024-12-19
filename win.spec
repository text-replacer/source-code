# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['D:\\_VSCODE_Git\\text-auto-replacer-by-drquochoai\\main.py'],
    pathex=['D:\\_VSCODE_Git\\text-auto-replacer-by-drquochoai'],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=['d:\\_VSCODE_Git\\text-auto-replacer-by-drquochoai\\.venv\\lib\\site-packages\\pyupdater\\hooks'],
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
    [],
    exclude_binaries=True,
    name='win',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='win',
)
