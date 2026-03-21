# Yewd's Optimizer

A GUI config editor for [Deadlock](https://store.steampowered.com/app/1422450/Deadlock/) that lets you tweak `gameinfo.gi` and `video.txt` without opening Notepad. Based on [OptimizationLock v1.4.3](https://github.com/Sqooky/OptimizationLock).

![Python](https://img.shields.io/badge/python-3.10+-blue) ![Platform](https://img.shields.io/badge/platform-Windows-lightgrey) ![License](https://img.shields.io/badge/license-MIT-green)

---

## Download

Grab the latest release from the [Releases](../../releases) page. Unzip the folder and run `Yewds_Optimizer.exe` — no install required.

---

## What it does

**GAMEINFO.GI** — 90+ convars across 18 categories:

FOV, Outlines, HUD, Lighting, Skybox, FPS Caps, Shadows, Deep Lighting, UI, Visual Clarity, Models, Particles, Culling, LOD, Ropes, Ragdolls, Grass, System

**VIDEO.TXT** — full video settings editor across 7 categories:

Device (VendorID/DeviceID), Display, Performance, Upscaling (DLSS/FSR), Graphics, Particles, Misc

The tool auto-detects your Deadlock install, reads your current values from both files, backs up the originals on first run, and writes changes directly. Toggle between the two files using the tab bar.

---

## Install

### Option A — Pre-built (recommended)

1. Download the latest `.zip` from [Releases](../../releases)
2. Extract the folder anywhere
3. Run `Yewds_Optimizer.exe`

Your Deadlock install at `steamapps/common/Deadlock/game/citadel` is auto-detected. If it's on an unusual drive, click **LOCATE** and point it to your `citadel` folder.

Since the exe lives in Program Files territory, you may need to **right-click → Run as Administrator** for the save to work.

### Option B — Run from source

Requires Python 3.10+ (tkinter is included with the standard Windows Python install).

```
git clone https://github.com/behexening/yewds-deadlock-optimizer.git
cd yewds-deadlock-optimizer
python optimizationlock_gui.py
```

No dependencies beyond the standard library.

### Option C — Build the exe yourself

1. Clone the repo
2. Install a C compiler (Visual Studio Build Tools — select "Desktop development with C++")
3. Run:

```
pip install nuitka ordered-set
python -m nuitka --standalone --windows-console-mode=disable --windows-icon-from-ico=icon.ico --enable-plugin=tk-inter --include-data-dir=fonts=fonts --include-data-files=icon.ico=icon.ico --include-data-files=icon.png=icon.png --include-data-files=optimizationlock_gameinfo.gi=optimizationlock_gameinfo.gi --output-filename=Yewds_Optimizer.exe optimizationlock_gui.py
```

Or just run `BUILD.bat` and pick option 1 (Nuitka) or 2 (PyInstaller).

The output folder is `optimizationlock_gui.dist/` — zip it up and distribute.

---

## Usage

1. Launch the app — it finds your `gameinfo.gi` and `video.txt` automatically
2. Switch between **GAMEINFO.GI** and **VIDEO.TXT** tabs at the top
3. Browse categories in the left sidebar
4. Flip toggles, change dropdowns, or type values directly
5. Click **SAVE** — both files are written in place
6. Hit **DEFAULTS** to reset everything back to the OptimizationLock recommended values

Backups of your original files are saved as `gameinfo.gi.backup_original` and `video.txt.backup_original` alongside the originals. These are only created once, so you can always revert.

---

## Notes

- Deadlock overwrites `gameinfo.gi` on major updates — you'll need to re-apply after patches
- `video.txt` can also be overwritten if you change in-game graphics settings
- VendorID and DeviceID are read from your existing `video.txt` and are never touched by the reset button
- The bundled `optimizationlock_gameinfo.gi` is included as a reference copy if you need a clean starting point

---

## Credits

- [OptimizationLock](https://github.com/Sqooky/OptimizationLock) by Sqooky, Dacoder_, Brullee, Kaizuchaneru, Artemon121, Jaden, Piggy
- Original config by Maihdenless (based on Dyson's config)
- [Deadlock Competitive Config](https://github.com/SHR1KN/Deadlock-Competitive-Config) for video.txt reference
- Vibecoded with Claude
