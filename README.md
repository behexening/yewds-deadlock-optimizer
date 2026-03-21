# OPTIMIZATIONLOCK CONFIGURATOR v1.4.3

A **Designer's Republic**–inspired GUI tool for editing Deadlock's `gameinfo.gi` without touching Notepad.

## Features

- **Visual editor** for all OptimizationLock ConVars — toggles, sliders, dropdowns
- **Categorized** into sections: FOV, Shadows, Lighting, Particles, LOD, etc.
- **Auto-backup** — saves a timestamped `.backup` of your original file before writing
- **Reads existing values** from your gameinfo.gi so you see what's currently set
- **Reset to defaults** — one click to revert all values to OptimizationLock config defaults
- **Helvetica Neue typography** (bundled fonts auto-loaded on Windows)

## Usage

### Run directly (requires Python 3.10+)
```
python optimizationlock_gui.py
```

### Build standalone .exe (Windows)
```
BUILD.bat
```
The exe will be in the `dist/` folder.

### Workflow
1. Click **► LOAD FILE** and navigate to your `gameinfo.gi`  
   (typically at `steamapps/common/deadlock/game/citadel/gameinfo.gi`)
2. A backup is automatically created alongside the original
3. Browse categories in the left sidebar, adjust values
4. Click **■ SAVE** to write changes back

## Notes

- The config's `gameinfo.gi` gets overwritten every major Deadlock update — you'll need to re-apply
- This tool includes the OptimizationLock reference config (`optimizationlock_gameinfo.gi`) if you need a fresh copy
- Based on [OptimizationLock v1.4.3](https://github.com/Sqooky/OptimizationLock)

## Credits

OptimizationLock by Sqooky, Dacoder_, Brullee, Kaizuchaneru, Artemon121, Jaden, Piggy  
Original config by Maihdenless (based on Dyson's config)
