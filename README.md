# Arma 3 Modpack Updater

A Python GUI application that automates downloading and deploying Arma 3 workshop mods.

## Features

- Import HTML modlists exported from the Arma 3 launcher
- Download missing mods using SteamCMD
- Flatten the Steam workshop folder structure
- Deploy mods to another directory using symlinks or file copies
- Remembers folders and Steam username between sessions

## Requirements

- Python 3.8 or newer
- [SteamCMD](https://developer.valvesoftware.com/wiki/SteamCMD)
- `beautifulsoup4` Python package

## Installation

Clone this repository and install the Python dependency:

```bash
git clone https://github.com/yourname/arma3-modpack-updater.git
cd arma3-modpack-updater
pip install -r requirements.txt
```

Make sure SteamCMD is installed and the path is correct. The default path in `steamcmd.py` is `C:\SteamCMD\steamcmd.exe` on Windows.

## Usage

Run the GUI:

```bash
python main.py
```

1. **Import Modlist** – Select an HTML modlist exported from the Arma 3 launcher.
2. **Download Mods** – Enter your Steam credentials, choose a download folder and start the download. Mods are fetched with SteamCMD and flattened automatically.
3. **Deploy Mods** – Choose a deployment directory and deploy the downloaded mods. The program creates symlinks (or copies) of each mod into the target directory.

Folder paths and your username are saved to `config.json` when you close the program.

## License

This project is licensed under the GPL-3.0-or-later. See [LICENSE.md](LICENSE.md) for details.
