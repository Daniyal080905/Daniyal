import pygame

from persistence import load_settings, save_settings
from ui import main_menu, leaderboard_screen, settings_screen, input_name_screen, game_over_screen
from racer import RacerGame, WIDTH, HEIGHT


def main():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Racer goo")

    clock = pygame.time.Clock()
    settings = load_settings()

    while True:
        action = main_menu(screen, clock)

        if action == "quit":
            break

        elif action == "leaderboard":
            result = leaderboard_screen(screen, clock)

            if result == "quit":
                break

        elif action == "settings":
            result = settings_screen(screen, clock, settings)
            save_settings(settings)

            if result == "quit":
                break

        elif action == "play":
            player_name = input_name_screen(screen, clock)

            if player_name is None:
                break

            while True:
                game = RacerGame(screen, clock, player_name, settings)
                result = game.run()

                if result == "quit":
                    pygame.quit()
                    return

                next_action = game_over_screen(
                    screen,
                    clock,
                    result["score"],
                    result["distance"],
                    result["coins"]
                )

                if next_action == "retry":
                    continue

                elif next_action == "menu":
                    break

                elif next_action == "quit":
                    pygame.quit()
                    return

    save_settings(settings)
    pygame.quit()


if __name__ == "__main__":
    main()