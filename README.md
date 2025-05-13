# USAPatchNotes  
_Game-style patch notes for America._
**USAPatchNotes** is a satirical, auto-updating project that scrapes Executive Orders from the Federal Register and transforms them into update logs—just like your favorite video game's patch notes. Buffs, nerfs, meta shifts—except it's the federal government.

## What It Does
- Fetches newly signed Executive Orders from the White House via the Federal Register API  
- Converts them into readable, humorous "patch notes" using a local open-source language model  
- Supports customization and future automation for social media or newsletter delivery  

## Project Structure
```
/data/raw/         → Raw JSON data from Federal Register  
/data/processed/   → Stylized EO patch notes  
/src/fetch_eos.py  → Pulls new EOs by date  
/src/summarize.py  → Generates patch notes using a local AI model  
/templates/        → Prompt and style formats (optional for advanced use)  
```

## Getting Started

### 1. Install dependencies
```bash
pip install -r requirements.txt
```
### 2. Fetch today's Executive Orders
```bash
python src/fetch_eos.py
```
### 3. Generate stylized patch notes using a local open-source model
```bash
python src/summarize.py
```
> Note: This uses `tiiuae/falcon-rw-1b`, a free transformer model that may run slowly on CPU. A GPU is recommended for faster performance.

## Automation
A GitHub Actions workflow can be added to run this daily.  
Future roadmap includes integration with X (Twitter), Discord, or Substack for automated publishing.

## Humor Engine
Patch notes are styled using a lightweight prompt that mimics video game changelogs:  
- Slight humor  
- Game balance tone  
- Names Executive Orders like gameplay tweaks  

## License
This project is licensed under the MIT License.
