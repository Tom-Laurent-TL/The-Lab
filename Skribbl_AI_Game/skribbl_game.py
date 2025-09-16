"""
Skribbl AI Challenge Game (Pygame Drawing Version)

Draw the word shown in the Pygame window. The AI will try to guess what you are drawing in real time.
Your goal is to make the AI guess as many words as possible within the time limit!
"""
import os
import time
import random
import threading
import base64
from io import BytesIO
from PIL import Image
from dotenv import load_dotenv
import pygame
from mistralai import Mistral
import ctypes

# Set process DPI awareness (Windows only)
try:
    ctypes.windll.user32.SetProcessDPIAware()
except Exception:
    pass

# --- AI and Game Setup ---
load_dotenv()
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
MISTRAL_MODEL = "mistral-small-latest"
client = Mistral(api_key=MISTRAL_API_KEY)

challenge_words = [
    "chat", "maison", "voiture", "arbre", "chien", "vélo", "pomme", "étoile", "poisson", "fleur",
    "bateau", "téléphone", "livre", "soleil", "lune", "nuage", "chaussure", "tasse", "chaise", "horloge",
    "ordinateur", "montagne", "plage", "oiseau", "fromage", "camion", "gâteau", "clé", "porte", "fenêtre",
    "ballon", "crayon", "main", "pied", "nez", "bouche", "main", "arbre", "forêt", "route", "pont",
    "train", "avion", "serpent", "grenouille", "papillon", "fourmi", "abeille", "banane", "orange", "citron",
    "chapeau", "vache", "mouton", "cochon", "poule", "canard", "lapin", "tigre", "lion", "éléphant",
    "girafe", "zèbre", "souris", "singe", "ours", "requin", "dauphin", "baleine", "escargot", "araignée",
    "pizza", "hamburger", "glace", "bonbon", "carotte", "tomate", "salade", "pain", "lait", "eau",
    "feu", "glace", "vent", "pluie", "neige", "orage", "arc", "épée", "bouclier", "robot"
]
GAME_DURATION = 60  # seconds
AI_PROMPT = "Qu'est-ce que l'utilisateur dessine ? Répondez avec un seul mot en français. S'il n'y a pas de dessin, répondez 'rien'."

# --- Pygame Drawing Setup ---
pygame.init()
pygame.display.init()
infoObject = pygame.display.Info()
WIDTH, HEIGHT = infoObject.current_w, infoObject.current_h  # Use actual screen size
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 200, 0)
YELLOW = (255, 255, 0)
BRUSH_SIZE = 6

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Skribbl AI Challenge - Lite Paint!")
font = pygame.font.SysFont("Segoe UI Symbol", 26)
clock = pygame.time.Clock()

# Force event loop to help window appear
for _ in range(10):
    pygame.event.pump()
    time.sleep(0.05)
print("Pygame window should now be visible. If not, check for errors in the terminal.")

# --- Drawing Functions ---
def get_canvas_image():
    """Capture the pygame drawing area as a base64 PNG image (excluding the UI area)."""
    # Crop only the drawing area (below UI)
    sub_surface = screen.subsurface(pygame.Rect(0, 50, WIDTH, HEIGHT-50)).copy()
    data = pygame.image.tostring(sub_surface, 'RGB')
    img = pygame.image.fromstring(data, (WIDTH, HEIGHT-50), 'RGB')
    buffered = BytesIO()
    pygame.image.save(img, buffered)
    buffered.seek(0)
    image = base64.b64encode(buffered.read()).decode("utf-8")
    return image

def image_to_text_guess(client, model, prompt, image):
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image}"}}
            ]
        }
    ]
    response = client.chat.complete(model=model, messages=messages, temperature=0.0)
    return response.choices[0].message.content.strip().lower()

# --- Game Logic ---
def draw_text(surface, text, pos, color=BLACK):
    img = font.render(text, True, color)
    surface.blit(img, pos)

class TextBox:
    def __init__(self, text, font, pos, color, bg_color, padding_x=18, padding_y=6, border_radius=12, align="topleft"):
        self.text = text
        self.font = font
        self.pos = pos  # (x, y)
        self.color = color
        self.bg_color = bg_color
        self.padding_x = padding_x
        self.padding_y = padding_y
        self.border_radius = border_radius
        self.align = align  # 'topleft', 'topright', 'center', etc.
        self.surface = self.font.render(self.text, True, self.color)
        self.rect = self.surface.get_rect()
        # Set rect position based on alignment
        setattr(self.rect, self.align, self.pos)
        self.bg_rect = pygame.Rect(
            self.rect.left - self.padding_x,
            self.rect.top - self.padding_y,
            self.rect.width + 2*self.padding_x,
            self.rect.height + 2*self.padding_y
        )

    def draw(self, surface):
        pygame.draw.rect(surface, self.bg_color, self.bg_rect, border_radius=self.border_radius)
        surface.blit(self.surface, self.rect)

def main():
    while True:
        # --- Main Menu Screen ---
        menu = True
        while menu:
            screen.fill((40, 44, 52))  # Dark background
            pygame.draw.rect(screen, (60, 63, 65), (WIDTH//2-350, HEIGHT//2-150, 700, 300), border_radius=30)
            # Centered main menu texts
            menu_font = pygame.font.SysFont("Segoe UI Symbol", 32, bold=True)
            menu_items = [
                ("Jeu Skribbl IA (Édition Pygame)", (0, 180, 255)),
                ("Dessinez le mot dans la fenêtre Pygame.", (220, 220, 220)),
                ("[C] Effacer  [B] Noir  [R] Rouge  [G] Vert  [Y] Jaune  [Q] Quitter", (200, 200, 200)),
                (f"Durée : {GAME_DURATION} secondes", (200, 200, 200)),
                ("Appuyez sur [ESPACE] pour commencer", (255, 140, 0)),
            ]
            y_start = HEIGHT//2 - 110
            for i, (text, color) in enumerate(menu_items):
                surf = menu_font.render(text, True, color)
                rect = surf.get_rect(center=(WIDTH//2, y_start + i*50))
                screen.blit(surf, rect)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        menu = False
                    if event.key == pygame.K_q:
                        pygame.quit()
                        return
        # --- Game Loop ---
        score = 0
        words_guessed = []
        start_time = time.time()
        running = True
        drawing = False
        last_ai_guess = ""
        challenge_word = random.choice(challenge_words)
        ai_guess = ""
        ai_guess_time = 0
        word_start = time.time()
        guessed = False
        brush_color = BLACK
        brush_size = BRUSH_SIZE
        jokers_left = 3  # Add joker counter
        screen.fill((245, 245, 245))
        pygame.draw.rect(screen, (60, 63, 65), (0,0,WIDTH,60), border_radius=0)

        guess_requested = threading.Event()

        def ai_guess_thread():
            nonlocal last_ai_guess, guessed, score
            ui_bar_height = 60
            help_bar_height = 50
            drawing_height = HEIGHT - ui_bar_height - help_bar_height
            while running and (time.time() - start_time) < GAME_DURATION:
                guess_requested.wait()  # Wait until user requests a guess
                if not running:
                    break
                # Capture only the drawing area (exclude top and bottom UI bars)
                sub_surface = screen.subsurface(pygame.Rect(0, ui_bar_height, WIDTH, drawing_height)).copy()
                data = pygame.image.tostring(sub_surface, 'RGB')
                img = Image.frombytes('RGB', (WIDTH, drawing_height), data)
                buffered = BytesIO()
                img.save(buffered, format="PNG")
                buffered.seek(0)
                image = base64.b64encode(buffered.read()).decode("utf-8")
                guess = image_to_text_guess(client, MISTRAL_MODEL, AI_PROMPT, image)
                print(f"Mot à deviner: {challenge_word} | Réponse de l'IA: {guess}")
                last_ai_guess = guess
                if challenge_word.lower() in guess:
                    guessed = True
                    score += 1
                guess_requested.clear()  # Reset for next action

        t = threading.Thread(target=ai_guess_thread, daemon=True)
        t.start()

        # Main game loop
        while running and (time.time() - start_time) < GAME_DURATION:
            pygame.event.pump()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and event.pos[1] > 60:
                        drawing = True
                        last_pos = pygame.mouse.get_pos()
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        drawing = False
                        if 'last_pos' in locals():
                            del last_pos
                        guess_requested.set()  # Request AI guess after drawing
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        running = False
                        pygame.quit()
                        return
                    if event.key == pygame.K_c:
                        screen.fill(WHITE)
                        pygame.draw.rect(screen, (230,230,230), (0,0,WIDTH,60))
                        guess_requested.set()  # Request AI guess after clear
                    if event.key == pygame.K_r:
                        brush_color = RED
                    if event.key == pygame.K_n:
                        brush_color = BLACK
                    if event.key == pygame.K_v:
                        brush_color = GREEN
                    if event.key == pygame.K_j:
                        brush_color = YELLOW
                    if event.key == pygame.K_b:
                        brush_color = BLUE
                    if event.key == pygame.K_UP:
                        brush_size = min(brush_size+2, 40)
                    if event.key == pygame.K_DOWN:
                        brush_size = max(2, brush_size-2)
                    if event.key == pygame.K_p and jokers_left > 0:
                        # Use a joker to skip the word
                        jokers_left -= 1
                        words_guessed.append(f"(joker) {challenge_word}")
                        available_words = [w for w in challenge_words if w not in words_guessed]
                        if not available_words:
                            running = False
                            break
                        challenge_word = random.choice(available_words)
                        guessed = False
                        last_ai_guess = ""
                        screen.fill(WHITE)
                        pygame.draw.rect(screen, (230,230,230), (0,0,WIDTH,60))
                        word_start = time.time()

            if drawing:
                mx, my = pygame.mouse.get_pos()
                if my > 60:
                    if 'last_pos' in locals():
                        pygame.draw.line(screen, brush_color, last_pos, (mx, my), brush_size)
                    else:
                        pygame.draw.circle(screen, brush_color, (mx, my), brush_size // 2)
                    last_pos = (mx, my)
            else:
                if 'last_pos' in locals():
                    del last_pos

            # Draw all previous lines (already drawn on the screen)
            # UI bar
            pygame.draw.rect(screen, (60, 63, 65), (0,0,WIDTH,60), border_radius=0)
            # Center vertical for all top UI texts (bar height = 60)
            ui_bar_height = 60
            # Mot à dessiner
            mot_box = TextBox(
                f"Mot à dessiner : {challenge_word}", font, (30, (ui_bar_height - font.get_height())//2),
                (0, 180, 255), (40, 44, 52), 18, 6, 12, align="topleft"
            )
            mot_box.draw(screen)

            # Timer, Score, Jokers (right-aligned, with consistent gap)
            gap = 18
            timer_font = pygame.font.SysFont("Segoe UI Symbol", 32, bold=True)
            timer_text = f"⏰ {max(0, int(GAME_DURATION - (time.time() - start_time)))}s"
            score_text = f"Score : {score}"
            jokers_text = f"Jokers : {jokers_left}"
            # Render surfaces to get widths
            timer_surf = timer_font.render(timer_text, True, (255, 140, 0))
            score_surf = font.render(score_text, True, (0, 200, 0))
            jokers_surf = font.render(jokers_text, True, (255, 80, 80) if jokers_left == 0 else (0, 180, 255))
            timer_width = timer_surf.get_width() + 2*18  # padding_x
            score_width = score_surf.get_width() + 2*18
            jokers_width = jokers_surf.get_width() + 2*18
            # Positions (right-aligned)
            timer_x = WIDTH - 30
            score_x = timer_x - timer_width - gap
            jokers_x = score_x - score_width - gap
            # Draw timer
            timer_box = TextBox(
                timer_text, timer_font, (timer_x, (ui_bar_height - timer_font.get_height())//2),
                (255, 140, 0), (40, 44, 52), 18, 6, 12, align="topright"
            )
            timer_box.draw(screen)
            # Draw score
            score_box = TextBox(
                score_text, font, (score_x, (ui_bar_height - font.get_height())//2),
                (0, 200, 0), (40, 44, 52), 18, 6, 12, align="topright"
            )
            score_box.draw(screen)
            # Draw jokers
            joker_box = TextBox(
                jokers_text, font, (jokers_x, (ui_bar_height - font.get_height())//2),
                (255, 80, 80) if jokers_left == 0 else (0, 180, 255), (40, 44, 52), 18, 6, 12, align="topright"
            )
            joker_box.draw(screen)

            # Réponse IA (centered horizontally, vertically in bar)
            ai_guess_color = (255, 80, 80) if last_ai_guess == challenge_word.lower() else (255, 255, 0)
            ai_guess_font = pygame.font.SysFont("Segoe UI Symbol", 32, bold=True)
            ai_guess_box = TextBox(
                f"Réponse IA : {last_ai_guess}", ai_guess_font, (WIDTH//2, ui_bar_height//2),
                ai_guess_color, (60, 63, 65), 24, 8, 12, align="center"
            )
            ai_guess_box.draw(screen)

            # Controls (help) at the bottom of the screen
            help_bar_height = 50
            help_font = pygame.font.SysFont("Segoe UI Symbol", 24)
            pygame.draw.rect(screen, (60, 63, 65), (0, HEIGHT-help_bar_height, WIDTH, help_bar_height), border_radius=0)

            # Draw color shortcuts with swatches and selected indicator
            color_shortcuts = [
                ("[N]", BLACK, pygame.K_n),  # Noir (Black)
                ("[R]", RED, pygame.K_r),
                ("[V]", GREEN, pygame.K_v),  # Vert (Green)
                ("[J]", YELLOW, pygame.K_j), # Jaune (Yellow)
                ("[B]", BLUE, pygame.K_b),   # Bleu (Blue)
            ]
            color_shortcut_width = 90 * len(color_shortcuts)
            other_help = "[C] Effacer   [↑/↓] Taille   [P] Passer (joker)   [Q] Quitter"
            other_surf = help_font.render(other_help, True, (200, 200, 200))
            other_width = other_surf.get_width()
            total_width = color_shortcut_width + 20 + other_width
            x_start = (WIDTH - total_width) // 2
            x = x_start
            y = HEIGHT - help_bar_height // 2 - 10
            for key, color, kcode in color_shortcuts:
                surf = help_font.render(key, True, (220, 220, 220))
                screen.blit(surf, (x, y))
                rect = pygame.Rect(x + 45, y + 5, 28, 18)
                pygame.draw.rect(screen, color, rect, border_radius=4)
                # Draw border if this color is selected
                if brush_color == color:
                    pygame.draw.rect(screen, (255, 255, 255), rect.inflate(6, 6), 3, border_radius=6)
                x += 90
            # Draw other controls text, centered after color shortcuts
            other_rect = other_surf.get_rect(midleft=(x + 20, HEIGHT - help_bar_height // 2))
            screen.blit(other_surf, other_rect)

            pygame.display.update()
            clock.tick(60)

            if guessed:
                # --- Reward Animation: Flashing guessed word and confetti (restricted to drawing area) ---
                animation_duration = 1000  # milliseconds
                animation_start = pygame.time.get_ticks()
                confetti_count = 40
                ui_bar_height = 60
                help_bar_height = 50
                drawing_top = ui_bar_height
                drawing_bottom = HEIGHT - help_bar_height
                drawing_height = drawing_bottom - drawing_top
                confetti = [
                    {
                        'x': random.randint(0, WIDTH),
                        'y': random.randint(drawing_top, drawing_bottom),
                        'color': random.choice([(255,0,0),(0,255,0),(0,180,255),(255,255,0),(255,80,80),(255,140,0),(0,200,0)]),
                        'radius': random.randint(8, 18),
                        'speed': random.uniform(2, 6)
                    }
                    for _ in range(confetti_count)
                ]
                while pygame.time.get_ticks() - animation_start < animation_duration:
                    # Redraw only the drawing area (not UI bars)
                    pygame.draw.rect(screen, (245,245,245), (0, drawing_top, WIDTH, drawing_height))
                    # Draw confetti in drawing area only
                    for c in confetti:
                        if drawing_top <= c['y'] <= drawing_bottom:
                            pygame.draw.circle(screen, c['color'], (int(c['x']), int(c['y'])), c['radius'])
                        c['y'] += c['speed']
                        if c['y'] > drawing_bottom:
                            c['y'] = random.randint(drawing_top, drawing_top + drawing_height//2)
                            c['x'] = random.randint(0, WIDTH)
                    # Flashing guessed word centered in drawing area
                    if ((pygame.time.get_ticks() - animation_start) // 200) % 2 == 0:
                        word_font = pygame.font.SysFont("Segoe UI Symbol", 72, bold=True)
                        word_surf = word_font.render(last_ai_guess.upper(), True, (255, 200, 0))
                        word_rect = word_surf.get_rect(center=(WIDTH//2, drawing_top + drawing_height//2))
                        screen.blit(word_surf, word_rect)
                    # Redraw UI bars on top
                    pygame.draw.rect(screen, (60, 63, 65), (0,0,WIDTH,ui_bar_height), border_radius=0)
                    pygame.draw.rect(screen, (60, 63, 65), (0, HEIGHT-help_bar_height, WIDTH, help_bar_height), border_radius=0)
                    pygame.display.update()
                    clock.tick(60)
                pygame.time.wait(300)
                words_guessed.append(challenge_word)
                # Pick a new word
                available_words = [w for w in challenge_words if w not in words_guessed]
                if not available_words:
                    running = False
                    break
                challenge_word = random.choice(available_words)
                guessed = False
                last_ai_guess = ""
                screen.fill(WHITE)
                pygame.draw.rect(screen, (230,230,230), (0,0,WIDTH,60))
                word_start = time.time()

        # After game ends, show end screen and wait for user to return to menu
        screen.fill((40, 44, 52))
        pygame.draw.rect(screen, (60, 63, 65), (WIDTH//2-375, HEIGHT//2-140, 750, 280), border_radius=20)
        end_font = pygame.font.SysFont("Segoe UI Symbol", 28, bold=True)
        end_items = [
            ("Partie terminée !", (255, 80, 80)),
            (f"Votre score : {score} mot(s) devinés par l'IA en {GAME_DURATION} secondes.", (220, 220, 220)),
        ]
        if score > 0:
            mots_devines = [w for w in words_guessed if not w.startswith("(joker)")]
            if mots_devines:
                end_items.append((f"Mots devinés : {', '.join(mots_devines)}", (0, 200, 0)))
            else:
                end_items.append(("Aucun mot deviné (hors jokers).", (255, 80, 80)))
        else:
            end_items.append(("L'IA n'a deviné aucun mot. Réessayez !", (255, 80, 80)))
        end_items.append(("Appuyez sur [ESPACE] pour revenir au menu", (0, 180, 255)))
        y_start = HEIGHT//2 - 80
        for i, (text, color) in enumerate(end_items):
            surf = end_font.render(text, True, color)
            rect = surf.get_rect(center=(WIDTH//2, y_start + i*48))
            screen.blit(surf, rect)
        pygame.display.update()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        waiting = False
                        # Loop back to menu
                        break
                    if event.key == pygame.K_q:
                        pygame.quit()
                        return

if __name__ == "__main__":
    main()
