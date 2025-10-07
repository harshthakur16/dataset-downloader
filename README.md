# Seekho Dataset Downloader

A tiny, shareable tool that downloads a CSV dataset from Seekho Analytics, saves it as `dataset.csv`, and expands the `adCreative` field into structured parts. It also converts **all CSV column names** from `snake_case` to **camelCase** for convenience.

## What it does
1. Downloads CSV from: `https://analytics.seekho.in/api/queries/41583/results.csv?api_key=YOUR_KEY`
2. Saves the file as `dataset.csv` in the same folder.
3. Preserves the original `ad_creative` as `adCreativeOriginal`.
4. Splits `adCreative` into: `category`, `scriptName`, `actorName`, `uploadDate`, `formatName`, `otherData`.
5. Converts **all** column names from `snake_case` → `camelCase` (e.g., `total_spend` → `totalSpend`).

> Works on Windows, macOS, and Linux. No Python knowledge required—just run the provided script for your OS.

---

## Quick Start (Zero Tech Steps)

### Windows
1. Double‑click `run-windows.bat` (or right‑click → Run).  
2. When asked for your API key, paste it and press Enter.  
3. It creates a local Python environment, installs everything, and runs the tool.  
4. Check the folder for `dataset.csv`.

### macOS & Linux
1. Open Terminal in this folder.
2. Run:
   ```bash
   chmod +x run-macos-linux.sh
   ./run-macos-linux.sh
   ```
3. When asked for your API key, paste it and press Enter.
4. Check the folder for `dataset.csv`.

> If you prefer, you can put your key into a `.env` file (see below) to avoid prompts.

---

## Using a `.env` file (optional)
1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
2. Fill in `SEEKHO_API_KEY=your_real_key_here`.
3. Re‑run the script.

---

## Advanced: Use as a CLI

After the first run (which sets up a virtual environment), you can call the tool directly:

```bash
# Windows
.venv\Scripts\python -m seekho_downloader --out dataset.csv

# macOS/Linux
. .venv/bin/activate
python -m seekho_downloader --out dataset.csv
```

You can also pass the key inline (not recommended for shared terminals):
```bash
python -m seekho_downloader --apiKey YOUR_KEY
```

### CLI options
- `--apiKey` — API key (or set `SEEKHO_API_KEY` in `.env`)
- `--out` — Output CSV path (default: `dataset.csv`)
- `--timeout` — HTTP timeout seconds (default: 60)

---

## Repo layout
```
seekho-dataset-downloader/
├─ .env.example
├─ README.md
├─ requirements.txt
├─ run-windows.bat
├─ run-macos-linux.sh
├─ pyproject.toml
└─ src/
   └─ seekho_downloader/
      ├─ __init__.py
      ├─ cli.py
      └─ utils.py
```

---

## Notes
- The parser tries to **detect date-like tokens** anywhere in `adCreative` (`14sep`, `2may`, `2024-09-14`, `14-09-2024`, `20240914`, etc.).
- If no date token is found, it falls back to positional parsing (`formatName` then `uploadDate`).
- You can tweak patterns in `utils.py` → `DATE_PATTERNS`.

---

## Uninstall
Just delete the folder to remove the tool and its virtual environment.
