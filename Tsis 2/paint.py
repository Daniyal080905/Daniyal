import pygame
from tools import *

pygame.init()

WIDTH, HEIGHT = 1000, 700
TOOLBAR_HEIGHT = 90

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS2 Paint")

canvas = pygame.Surface((WIDTH, HEIGHT - TOOLBAR_HEIGHT))
canvas.fill((255, 255, 255))

font = pygame.font.SysFont("Arial", 22)
text_font = pygame.font.SysFont("Arial", 32)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

current_color = BLACK
brush_size = 5
tool = "pencil"

drawing = False
start_pos = None
last_pos = None

text_mode = False
text_pos = None
typed_text = ""

colors = [
    (0, 0, 0),
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (255, 165, 0),
    (128, 0, 128),
    (255, 255, 255)
]

tools = [
    "pencil",
    "line",
    "rect",
    "square",
    "circle",
    "right_tri",
    "eq_tri",
    "rhombus",
    "fill",
    "text",
    "eraser"
]


def draw_toolbar():
    pygame.draw.rect(screen, (220, 220, 220), (0, 0, WIDTH, TOOLBAR_HEIGHT))

    x = 10

    for t in tools:
        rect = pygame.Rect(x, 10, 85, 30)

        if tool == t:
            pygame.draw.rect(screen, (180, 180, 180), rect)
        else:
            pygame.draw.rect(screen, (240, 240, 240), rect)

        pygame.draw.rect(screen, BLACK, rect, 2)

        label = font.render(t, True, BLACK)
        screen.blit(label, (x + 5, 15))

        x += 90

    x = 10
    y = 50

    for color in colors:
        rect = pygame.Rect(x, y, 35, 30)
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)
        x += 45

    size_text = font.render(f"Brush: {brush_size} | keys: 1=2px 2=5px 3=10px | Ctrl+S Save", True, BLACK)
    screen.blit(size_text, (420, 55))


def get_canvas_pos(pos):
    x, y = pos
    return x, y - TOOLBAR_HEIGHT


def draw_shape(surface, selected_tool, color, start, end, width):
    if selected_tool == "line":
        pygame.draw.line(surface, color, start, end, width)

    elif selected_tool == "rect":
        draw_rectangle(surface, color, start, end, width)

    elif selected_tool == "square":
        draw_square(surface, color, start, end, width)

    elif selected_tool == "circle":
        draw_circle(surface, color, start, end, width)

    elif selected_tool == "right_tri":
        draw_right_triangle(surface, color, start, end, width)

    elif selected_tool == "eq_tri":
        draw_equilateral_triangle(surface, color, start, end, width)

    elif selected_tool == "rhombus":
        draw_rhombus(surface, color, start, end, width)


running = True

while running:
    screen.fill(WHITE)

    screen.blit(canvas, (0, TOOLBAR_HEIGHT))

    preview = canvas.copy()

    if drawing and start_pos and tool in [
        "line",
        "rect",
        "square",
        "circle",
        "right_tri",
        "eq_tri",
        "rhombus"
    ]:
        mouse_pos = pygame.mouse.get_pos()
        canvas_mouse_pos = get_canvas_pos(mouse_pos)

        draw_shape(
            preview,
            tool,
            current_color,
            start_pos,
            canvas_mouse_pos,
            brush_size
        )

        screen.blit(preview, (0, TOOLBAR_HEIGHT))

    if text_mode and text_pos:
        text_surface = text_font.render(typed_text, True, current_color)
        screen.blit(text_surface, (text_pos[0], text_pos[1] + TOOLBAR_HEIGHT))

    draw_toolbar()

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                brush_size = 2

            elif event.key == pygame.K_2:
                brush_size = 5

            elif event.key == pygame.K_3:
                brush_size = 10

            elif event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                save_canvas(canvas)

            elif text_mode:
                if event.key == pygame.K_RETURN:
                    text_surface = text_font.render(typed_text, True, current_color)
                    canvas.blit(text_surface, text_pos)

                    text_mode = False
                    typed_text = ""
                    text_pos = None

                elif event.key == pygame.K_ESCAPE:
                    text_mode = False
                    typed_text = ""
                    text_pos = None

                elif event.key == pygame.K_BACKSPACE:
                    typed_text = typed_text[:-1]

                else:
                    typed_text += event.unicode

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos

            if mouse_y < TOOLBAR_HEIGHT:
                x = 10

                for t in tools:
                    rect = pygame.Rect(x, 10, 85, 30)

                    if rect.collidepoint(event.pos):
                        tool = t

                    x += 90

                x = 10
                y = 50

                for color in colors:
                    rect = pygame.Rect(x, y, 35, 30)

                    if rect.collidepoint(event.pos):
                        current_color = color

                    x += 45

            else:
                canvas_pos = get_canvas_pos(event.pos)

                if tool == "fill":
                    flood_fill(canvas, canvas_pos, current_color)

                elif tool == "text":
                    text_mode = True
                    text_pos = canvas_pos
                    typed_text = ""

                else:
                    drawing = True
                    start_pos = canvas_pos
                    last_pos = canvas_pos

        elif event.type == pygame.MOUSEMOTION:
            if drawing:
                canvas_pos = get_canvas_pos(event.pos)

                if tool == "pencil":
                    pygame.draw.line(
                        canvas,
                        current_color,
                        last_pos,
                        canvas_pos,
                        brush_size
                    )
                    last_pos = canvas_pos

                elif tool == "eraser":
                    pygame.draw.line(
                        canvas,
                        WHITE,
                        last_pos,
                        canvas_pos,
                        brush_size
                    )
                    last_pos = canvas_pos

        elif event.type == pygame.MOUSEBUTTONUP:
            if drawing:
                end_pos = get_canvas_pos(event.pos)

                if tool in [
                    "line",
                    "rect",
                    "square",
                    "circle",
                    "right_tri",
                    "eq_tri",
                    "rhombus"
                ]:
                    draw_shape(
                        canvas,
                        tool,
                        current_color,
                        start_pos,
                        end_pos,
                        brush_size
                    )

                drawing = False
                start_pos = None
                last_pos = None

pygame.quit()