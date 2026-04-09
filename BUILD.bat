@echo off
echo ═══════════════════════════════════════════════
echo   YEWD'S OPTIMIZER - BUILD SCRIPT
echo ═══════════════════════════════════════════════
echo.
echo   [1] Nuitka  (recommended - fewer antivirus false positives)
echo   [2] PyInstaller  (fallback)
echo.
set /p choice="Select build method (1 or 2): "

python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Install Python 3.10+ from python.org
    pause
    exit /b 1
)

if "%choice%"=="1" goto nuitka
if "%choice%"=="2" goto pyinstaller
echo Invalid choice.
pause
exit /b 1

:nuitka
echo.
echo Installing Nuitka + ordered-set...
pip install nuitka ordered-set
echo.
echo Building with Nuitka (this takes a few minutes)...
echo.
python -m nuitka ^
    --standalone ^
    --onefile ^
    --windows-console-mode=disable ^
    --windows-icon-from-ico=icon.ico ^
    --enable-plugin=tk-inter ^
    --include-data-dir=fonts=fonts ^
    --include-data-files=icon.ico=icon.ico ^
    --include-data-files=icon.png=icon.png ^
    --include-data-files=optimizationlock_gameinfo.gi=optimizationlock_gameinfo.gi ^
    --output-filename=Yewds_Optimizer.exe ^
    optimizationlock_gui.py

echo.
if exist "Yewds_Optimizer.exe" (
    echo ════════════════════════════════════════
    echo   BUILD SUCCESSFUL [Nuitka]
    echo   Output: Yewds_Optimizer.exe
    echo ════════════════════════════════════════
) else (
    echo [ERROR] Build failed. Check output above.
    echo.
    echo Common fixes:
    echo   - Install a C compiler: MinGW64 or Visual Studio Build Tools
    echo   - Nuitka needs a C compiler to work
    echo   - Run: pip install ordered-set
)
echo.
pause
exit /b 0

:pyinstaller
echo.
echo Installing PyInstaller...
pip install pyinstaller
echo.
echo Building with PyInstaller...
echo.
pyinstaller --onefile --noconsole ^
    --name "Yewds_Optimizer" ^
    --icon "icon.ico" ^
    --add-data "fonts;fonts" ^
    --add-data "icon.ico;." ^
    --add-data "icon.png;." ^
    --add-data "optimizationlock_gameinfo.gi;." ^
    optimizationlock_gui.py

echo.
if exist "dist\Yewds_Optimizer.exe" (
    echo ════════════════════════════════════════
    echo   BUILD SUCCESSFUL [PyInstaller]
    echo   Output: dist\Yewds_Optimizer.exe
    echo ════════════════════════════════════════
) else (
    echo [ERROR] Build failed. Check output above.
)
echo.
pause
exit /b 0
