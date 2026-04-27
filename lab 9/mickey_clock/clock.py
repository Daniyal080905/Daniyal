import pygame
import datetime
import os


class MickeyClock:
    def __init__(self, screen):
        self.screen = screen

        self.WIDTH, self.HEIGHT = screen.get_size()
        self.CENTER = (self.WIDTH // 2, self.HEIGHT // 2)

        # Folder path
        BASE_DIR = os.path.dirname(__file__)
        IMAGES_DIR = os.path.join(BASE_DIR, "images")

        # Load images
        self.clock_face = pygame.image.load(
            os.path.join(IMAGES_DIR, "clock_face (3).png")
        ).convert_alpha()

        self.mickey = pygame.image.load(
            os.path.join(IMAGES_DIR, "mickey.png")
        ).convert_alpha()

        self.left_hand = pygame.image.load(
            os.path.join(IMAGES_DIR, "left_hand.png")
        ).convert_alpha()

        self.right_hand = pygame.image.load(
            os.path.join(IMAGES_DIR, "right_hand.png")
        ).convert_alpha()

        # Resize images
        self.clock_face = pygame.transform.smoothscale(self.clock_face, (650, 650))
        self.mickey = pygame.transform.smoothscale(self.mickey, (260, 260))

        # Left hand = second hand
        self.left_hand = pygame.transform.smoothscale(self.left_hand, (45, 150))

        # Right hand = minute hand
        self.right_hand = pygame.transform.smoothscale(self.right_hand, (70, 135))

        # Positions
        self.clock_center = (self.CENTER[0], self.CENTER[1] + 15)
        self.clock_pos = self.clock_face.get_rect(center=self.clock_center)
        self.mickey_pos = self.mickey.get_rect(center=(self.CENTER[0], self.CENTER[1] + 55))

    def rotate_hand_from_bottom(self, image, angle):
        """
        Rotate hand around its bottom center.
        The bottom of the hand stays in the clock center.
        """
        w, h = image.get_size()

        # pivot point inside image: bottom center
        pivot = pygame.Vector2(w / 2, h - 20)

        # offset from image center to pivot
        image_center = pygame.Vector2(w / 2, h / 2)
        offset = image_center - pivot

        # rotate image
        rotated_image = pygame.transform.rotate(image, -angle)

        # rotate offset
        rotated_offset = offset.rotate(angle)

        # place rotated image so pivot is in clock center
        rotated_rect = rotated_image.get_rect(
            center=pygame.Vector2(self.clock_center) + rotated_offset
        )

        return rotated_image, rotated_rect

    def get_time_angles(self):
        now = datetime.datetime.now()

        minutes = now.minute
        seconds = now.second

        if seconds > 59:
            seconds = 59

        # 1 minute/second = 6 degrees
        minute_angle = (minutes + seconds / 60) * 6
        second_angle = seconds * 6

        return minute_angle, second_angle, now

    def draw_time_text(self, now):
        font = pygame.font.SysFont("Arial", 30, bold=True)
        text = font.render(f"{now.minute:02d}:{now.second:02d}", True, (30, 30, 30))
        rect = text.get_rect(center=(self.WIDTH // 2, self.HEIGHT - 35))
        self.screen.blit(text, rect)

    def draw(self):
        minute_angle, second_angle, now = self.get_time_angles()

        # Background
        self.screen.fill((245, 245, 245))

        # Draw clock face
        self.screen.blit(self.clock_face, self.clock_pos)

        # Draw Mickey
        self.screen.blit(self.mickey, self.mickey_pos)

        # Rotate hands
        minute_img, minute_rect = self.rotate_hand_from_bottom(
            self.right_hand,
            minute_angle
        )

        second_img, second_rect = self.rotate_hand_from_bottom(
            self.left_hand,
            second_angle
        )

        # Draw hands
        self.screen.blit(minute_img, minute_rect)
        self.screen.blit(second_img, second_rect)

        # Center dot
        pygame.draw.circle(self.screen, (30, 30, 30), self.clock_center, 8)

        # Digital time
        self.draw_time_text(now)