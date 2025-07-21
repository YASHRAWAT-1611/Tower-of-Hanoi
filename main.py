import pygame
import sys
import time
import os

pygame.init()
pygame.mixer.init()

# Sound effects
move_sound = pygame.mixer.Sound("move.wav")
win_sound = pygame.mixer.Sound("win.wav")

# Configuration
WIDTH, HEIGHT = 900, 600
ROD_WIDTH = 20
ROD_HEIGHT = 300
DISK_HEIGHT = 30
NUM_DISKS = 4
MAX_DISKS = 8
MIN_DISKS = 3
FPS = 60
MOVE_DELAY = 0.5  # seconds between auto moves

# Colors
LIGHT_THEME = {
    "bg": (255, 255, 255),
    "text": (0, 0, 0),
    "button": (200, 0, 0),
    "button_hover": (255, 0, 0),
    "green": (0, 200, 0)
}
DARK_THEME = {
    "bg": (30, 30, 30),
    "text": (255, 255, 255),
    "button": (100, 0, 0),
    "button_hover": (150, 0, 0),
    "green": (0, 255, 0)
}
theme = LIGHT_THEME

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tower of Hanoi")
clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 48)

rod_x = [200, 450, 700]
rod_y = HEIGHT - ROD_HEIGHT

highscore_file = "highscore.txt"

game_state = "menu"  # "menu", "howto", "game"

# Disk class
class Disk:
    def __init__(self, size, rod):
        self.size = size
        self.width = 40 + size * 30
        self.color = (50 + size * 20, 100, 255 - size * 20)
        self.rod = rod
        self.x = 0
        self.y = 0
        self.dragging = False

    def update_position(self):
        stack = rods[self.rod]
        index = stack.index(self)
        self.x = rod_x[self.rod] - self.width // 2
        self.y = HEIGHT - (index + 1) * DISK_HEIGHT

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, DISK_HEIGHT))

def draw_button(rect, text, hover=False):
    color = theme["button_hover"] if hover else theme["button"]
    pygame.draw.rect(screen, color, rect)
    label = font.render(text, True, theme["text"])
    screen.blit(label, (rect.x + (rect.width - label.get_width()) // 2, rect.y + 5))

def load_highscore():
    if os.path.exists(highscore_file):
        with open(highscore_file, "r") as f:
            try:
                return int(f.readline().strip())
            except:
                return None
    return None

def save_highscore(time_seconds):
    with open(highscore_file, "w") as f:
        f.write(str(time_seconds))

def create_disks():
    rods[0].clear()
    rods[1].clear()
    rods[2].clear()
    disks.clear()
    for i in range(current_disks):
        disk = Disk(current_disks - i - 1, 0)
        rods[0].append(disk)
        disk.update_position()
        disks.append(disk)

# Hanoi recursive generator for moves
def auto_solve(n, source, target, auxiliary):
    if n == 1:
        yield (source, target)
    else:
        yield from auto_solve(n - 1, source, auxiliary, target)
        yield (source, target)
        yield from auto_solve(n - 1, auxiliary, target, source)

def move_disk(src, dst):
    disk = rods[src].pop()
    disk.rod = dst
    rods[dst].append(disk)
    disk.update_position()

# Game state
rods = [[], [], []]
disks = []
current_disks = NUM_DISKS
create_disks()

dragged_disk = None
offset_x = 0
offset_y = 0
move_count = 0
start_time = time.time()
game_won = False
best_time = load_highscore()

# Buttons
restart_btn = pygame.Rect(WIDTH - 160, 20, 140, 40)
increase_btn = pygame.Rect(30, HEIGHT - 60, 40, 40)
decrease_btn = pygame.Rect(80, HEIGHT - 60, 40, 40)
theme_toggle_btn = pygame.Rect(WIDTH - 160, HEIGHT - 60, 140, 40)
auto_solve_btn = pygame.Rect(WIDTH - 320, 20, 140, 40)

# Main menu buttons
start_btn = pygame.Rect(WIDTH//2 - 100, 250, 200, 50)
howto_btn = pygame.Rect(WIDTH//2 - 100, 320, 200, 50)
exit_btn = pygame.Rect(WIDTH//2 - 100, 390, 200, 50)
back_btn = pygame.Rect(20, HEIGHT - 60, 140, 40)

def toggle_theme():
    global theme
    theme = DARK_THEME if theme == LIGHT_THEME else LIGHT_THEME

# Auto solver variables
auto_solving = False
move_generator = None
last_move_time = 0

# Main loop
running = True
while running:
    clock.tick(FPS)
    screen.fill(theme["bg"])
    mouse_pos = pygame.mouse.get_pos()

    if game_state == "menu":
        title = big_font.render("Tower of Hanoi", True, theme["text"])
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 150))

        draw_button(start_btn, "Start Game", start_btn.collidepoint(mouse_pos))
        draw_button(howto_btn, "How to Play", howto_btn.collidepoint(mouse_pos))
        draw_button(exit_btn, "Exit", exit_btn.collidepoint(mouse_pos))

    elif game_state == "howto":
        lines = [
            "Goal: Move all disks from the left rod to the right rod.",
            "Rules:",
            "- Only one disk can be moved at a time.",
            "- Only the top disk can be moved.",
            "- No larger disk on top of a smaller one.",
            "",
            "Click and drag disks to move them.",
            "Use + / - to change number of disks.",
            "Press 'T' or use button to toggle theme.",
        ]
        for i, line in enumerate(lines):
            line_render = font.render(line, True, theme["text"])
            screen.blit(line_render, (50, 100 + i * 40))
        draw_button(back_btn, "Back", back_btn.collidepoint(mouse_pos))

    elif game_state == "game":
        elapsed_time = int(time.time() - start_time)
        minutes = elapsed_time // 60
        seconds = elapsed_time % 60

        # Draw rods
        for i in range(3):
            pygame.draw.rect(screen, theme["text"], (rod_x[i] - ROD_WIDTH//2, rod_y, ROD_WIDTH, ROD_HEIGHT))

        # Draw buttons
        draw_button(restart_btn, "Restart", restart_btn.collidepoint(mouse_pos))
        draw_button(increase_btn, "+", increase_btn.collidepoint(mouse_pos))
        draw_button(decrease_btn, "-", decrease_btn.collidepoint(mouse_pos))
        draw_button(theme_toggle_btn, "Theme", theme_toggle_btn.collidepoint(mouse_pos))
        draw_button(auto_solve_btn, "Auto-Solve", auto_solve_btn.collidepoint(mouse_pos))

        # Disks
        for disk in disks:
            if disk != dragged_disk:
                disk.update_position()
            disk.draw(screen)
        if dragged_disk:
            dragged_disk.draw(screen)

        screen.blit(font.render(f"Moves: {move_count}", True, theme["text"]), (20, 20))
        screen.blit(font.render(f"Time: {minutes:02}:{seconds:02}", True, theme["text"]), (20, 60))
        screen.blit(font.render(f"Disks: {current_disks}", True, theme["text"]), (140, HEIGHT - 50))

        if best_time:
            bt_min = best_time // 60
            bt_sec = best_time % 60
            screen.blit(font.render(f"Best: {bt_min:02}:{bt_sec:02}", True, theme["green"]), (20, 100))

        if len(rods[2]) == current_disks and not game_won:
            game_won = True
            win_sound.play()
            win_text = big_font.render("You Win!", True, theme["green"])
            screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, 50))
            if best_time is None or elapsed_time < best_time:
                save_highscore(elapsed_time)
                best_time = elapsed_time

        # Auto solving animation
        if auto_solving:
            if time.time() - last_move_time > MOVE_DELAY:
                try:
                    src, dst = next(move_generator)
                    move_disk(src, dst)
                    move_sound.play()
                    move_count += 1
                    last_move_time = time.time()
                except StopIteration:
                    auto_solving = False
                    game_won = True
                    win_sound.play()
                    # Update highscore if better
                    elapsed_time = int(time.time() - start_time)
                    if best_time is None or elapsed_time < best_time:
                        save_highscore(elapsed_time)
                        best_time = elapsed_time

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_state == "menu":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_btn.collidepoint(event.pos):
                    # Reset game variables
                    current_disks = NUM_DISKS
                    create_disks()
                    move_count = 0
                    start_time = time.time()
                    game_won = False
                    auto_solving = False
                    game_state = "game"
                elif howto_btn.collidepoint(event.pos):
                    game_state = "howto"
                elif exit_btn.collidepoint(event.pos):
                    running = False

        elif game_state == "howto":
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_btn.collidepoint(event.pos):
                    game_state = "menu"

        elif game_state == "game":
            if auto_solving:
                # Ignore user input while auto solving
                continue

            if event.type == pygame.MOUSEBUTTONDOWN:
                if restart_btn.collidepoint(event.pos):
                    create_disks()
                    move_count = 0
                    start_time = time.time()
                    game_won = False
                    auto_solving = False
                    dragged_disk = None

                elif increase_btn.collidepoint(event.pos):
                    if current_disks < MAX_DISKS:
                        current_disks += 1
                        create_disks()
                        move_count = 0
                        start_time = time.time()
                        game_won = False
                        auto_solving = False
                        dragged_disk = None

                elif decrease_btn.collidepoint(event.pos):
                    if current_disks > MIN_DISKS:
                        current_disks -= 1
                        create_disks()
                        move_count = 0
                        start_time = time.time()
                        game_won = False
                        auto_solving = False
                        dragged_disk = None

                elif theme_toggle_btn.collidepoint(event.pos):
                    toggle_theme()

                elif auto_solve_btn.collidepoint(event.pos):
                    # Start auto solving
                    move_generator = auto_solve(current_disks, 0, 2, 1)
                    auto_solving = True
                    move_count = 0
                    start_time = time.time()
                    game_won = False
                    dragged_disk = None

                else:
                    # Check if clicked on a top disk to drag
                    for rod_index in range(3):
                        if rods[rod_index]:
                            top_disk = rods[rod_index][-1]
                            rect = pygame.Rect(top_disk.x, top_disk.y, top_disk.width, DISK_HEIGHT)
                            if rect.collidepoint(event.pos):
                                dragged_disk = top_disk
                                offset_x = event.pos[0] - top_disk.x
                                offset_y = event.pos[1] - top_disk.y
                                break

            elif event.type == pygame.MOUSEBUTTONUP and dragged_disk:
                # Drop disk
                # Find which rod mouse is over
                for rod_index in range(3):
                    rod_rect = pygame.Rect(rod_x[rod_index] - 50, rod_y, 100, ROD_HEIGHT)
                    if rod_rect.collidepoint(event.pos):
                        # Check if move is valid
                        if rods[rod_index]:
                            if rods[rod_index][-1].size < dragged_disk.size:
                                # Invalid move
                                dragged_disk.update_position()
                                dragged_disk = None
                                break
                        # Valid move
                        old_rod = dragged_disk.rod
                        rods[old_rod].remove(dragged_disk)
                        dragged_disk.rod = rod_index
                        rods[rod_index].append(dragged_disk)
                        dragged_disk.update_position()
                        move_count += 1
                        move_sound.play()
                        dragged_disk = None
                        break
                else:
                    # Not dropped on any rod, reset position
                    dragged_disk.update_position()
                    dragged_disk = None

            elif event.type == pygame.MOUSEMOTION and dragged_disk:
                dragged_disk.x = event.pos[0] - offset_x
                dragged_disk.y = event.pos[1] - offset_y

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_t:
                    toggle_theme()

    pygame.display.flip()

pygame.quit()
sys.exit()
