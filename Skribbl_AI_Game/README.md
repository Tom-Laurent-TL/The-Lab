# Skribbl AI Game

A Pygame-based drawing game where you try to make an AI guess what you are drawing in real time!

## How It Works
- You are shown a word to draw (in French) on a fullscreen Pygame canvas.
- As you draw, an AI (using the Mistral API) tries to guess your drawing from the image.
- Your goal: get the AI to guess as many words as possible within the time limit.
- Use color shortcuts, brush size, and jokers to skip hard words.

## Features
- Real-time AI guessing using image-to-text via Mistral LLM.
- Fullscreen, responsive drawing interface with color and brush controls.
- Score tracking and animated feedback when the AI guesses correctly.
- French vocabulary challenge (words are in French).
- Jokers to skip words you don't want to draw.

## Controls
- **[N]** Noir (Black)
- **[R]** Rouge (Red)
- **[V]** Vert (Green)
- **[J]** Jaune (Yellow)
- **[B]** Bleu (Blue)
- **[C]** Effacer (Clear)
- **[↑/↓]** Changer la taille du pinceau (Brush size)
- **[P]** Passer (Joker)
- **[Q]** Quitter
- **[Espace]** Démarrer/Revenir au menu

## Requirements
- Python 3.8+
- Pygame
- Pillow
- python-dotenv
- mistralai

Install dependencies:
```bash
pip install pygame pillow python-dotenv mistralai
```

## Setup
1. Get a Mistral API key and set it in a `.env` file:
   ```env
   MISTRAL_API_KEY=your_api_key_here
   ```
2. Run the game:
   ```bash
   python skribbl_game.py
   ```

## Gameplay
- Draw the given word as clearly as possible.
- The AI will guess after each drawing action or when you clear the canvas.
- Try to maximize your score before the timer runs out!

---
Inspired by Skribbl.io, but with an AI twist!
