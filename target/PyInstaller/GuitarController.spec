# -*- mode: python -*-

block_cipher = None


a = Analysis(['/Users/lfarritor3/Documents/GitHub/guitar-gui-pyqt/src/main/python/main.py'],
             pathex=['/Users/lfarritor3/Documents/GitHub/guitar-gui-pyqt/target/PyInstaller'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=['/Library/Frameworks/Python.framework/Versions/3.8/lib/python3.8/site-packages/fbs/freeze/hooks'],
             runtime_hooks=['/Users/lfarritor3/Documents/GitHub/guitar-gui-pyqt/target/PyInstaller/fbs_pyinstaller_hook.py'],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='GuitarController',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=False,
          console=False , icon='/Users/lfarritor3/Documents/GitHub/guitar-gui-pyqt/target/Icon.icns')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=False,
               name='GuitarController')
app = BUNDLE(coll,
             name='GuitarController.app',
             icon='/Users/lfarritor3/Documents/GitHub/guitar-gui-pyqt/target/Icon.icns',
             bundle_identifier=None)
