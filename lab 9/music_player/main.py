import pygame
import os

pygame.init()
pygame.mixer.init()

# Window
WIDTH, HEIGHT = 700, 350
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Music Player")

# Colors
WHITE = (245, 245, 245)
BLACK = (20, 20, 20)
GRAY = (180, 180, 180)
BLUE = (60, 120, 220)

font_big = pygame.font.SysFont("Arial", 32, bold=True)
font = pygame.font.SysFont("Arial", 24)

# Music folder
BASE_DIR = os.path.dirname(__file__)
MUSIC_DIR = os.path.join(BASE_DIR, "music")

# Load playlist
playlist = [
    file for file in os.listdir(MUSIC_DIR)
    if file.endswith(".mp3") or file.endswith(".wav")
]

current_index = 0
is_playing = False
start_ticks = 0
paused_position = 0


def load_track(index):
    """Load selected track."""
    track_path = os.path.join(MUSIC_DIR, playlist[index])
    pygame.mixer.music.load(track_path)


def play_track():
    """Play current track."""
    global is_playing, start_ticks, paused_position
    load_track(current_index)
    pygame.mixer.music.play()
    is_playing = True
    paused_position = 0
    start_ticks = pygame.time.get_ticks()


def stop_track():
    """Stop music."""
    global is_playing, paused_position
    pygame.mixer.music.stop()
    is_playing = False
    paused_position = 0


def next_track():
    """Go to next track."""
    global current_index
    current_index = (current_index + 1) % len(playlist)
    play_track()


def previous_track():
    """Go to previous track."""
    global current_index
    current_index = (current_index - 1) % len(playlist)
    play_track()


def draw_ui():
    """Draw player interface."""
    screen.fill(WHITE)

    title = font_big.render("Music Player", True, BLACK)
    screen.blit(title, (250, 30))

    track_text = font.render(f"Track: {playlist[current_index]}", True, BLACK)
    screen.blit(track_text, (40, 100))

    status = "Playing" if is_playing else "Stopped"
    status_text = font.render(f"Status: {status}", True, BLACK)
    screen.blit(status_text, (40, 140))

    # Playback position
    if is_playing:
        position = (pygame.time.get_ticks() - start_ticks) // 1000
    else:
        position = 0

    pos_text = font.render(f"Position: {position} sec", True, BLACK)
    screen.blit(pos_text, (40, 180))

    # Progress bar imitation
    pygame.draw.rect(screen, GRAY, (40, 230, 600, 20))
    progress_width = min(position * 10, 600)
    pygame.draw.rect(screen, BLUE, (40, 230, progress_width, 20))

    controls = font.render("P = Play   S = Stop   N = Next   B = Back   Q = Quit", True, BLACK)
    screen.blit(controls, (40, 280))


# Check playlist
if not playlist:
    print("No music files found in music folder.")
    pygame.quit()
    exit()

load_track(current_index)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                play_track()

            elif event.key == pygame.K_s:
                stop_track()

            elif event.key == pygame.K_n:
                next_track()

            elif event.key == pygame.K_b:
                previous_track()

            elif event.key == pygame.K_q:
                running = False

    # Auto next when track ends
    if is_playing and not pygame.mixer.music.get_busy():
        next_track()

    draw_ui()
    pygame.display.update()

pygame.quit()