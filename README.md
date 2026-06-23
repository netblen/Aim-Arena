# Aim Arena

## Student Name
Anabella Miranda

## Project Title
Shooter Practice Game

## Overview
Aim Arena is a Flask web app with short mouse-skill mini games. Players can practice clicking speed, aim, reaction time, and target tracking, then see their best recorded score for each mode.

## Features
- Hamburger navigation menu shared across all pages
- Mini games for Click Speed, Shoot Test, Re-center, Hold Ball, Horizontal Hold, Vertical Hold, and Reaction Time
- Score saving through Flask routes
- Best-score panels for each game
- Scoreboard page and shared styling

## How To Run
Start the app with `uv`, which installs and runs the needed packages:

```powershell
uv run --with flask --with cryptography --with python-dotenv app.py
```

Open this in a browser:

```text
http://localhost:5000
```

Keep the terminal open while using the site. Press `Ctrl+C` in the terminal to stop the server. The app creates a local `.env` file for the encryption key if one does not already exist.

## Project Files
- `app.py`: Flask routes, score handling, and encryption setup
- `templates/`: HTML pages and shared components
- `static/css/site.css`: Main visual styling
- `static/js/`: Navigation and score display scripts
- `proposal.md`: Project proposal
- `project_exploration.ipynb`: Early project exploration
