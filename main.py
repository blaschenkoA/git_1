import pygame
from random import randrange

def draw(screen):
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 30)
    text = font.render("Нажмите для рисования круга", True, (100, 255, 100))
    text_x = width // 2 - text.get_width() // 2
    text_y = 25
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))
    pygame.draw.rect(screen, (0, 255, 0), (text_x - 10, text_y - 10,
                                           text_w + 20, text_h + 20), 1)

    return text_x - 10, text_y - 10, text_w + 20, text_h + 20

def clik(screen, d, r, g, b):
    pygame.draw.circle(screen, (r, g, b), (400, 300), d)


if __name__ == '__main__':
    pygame.init()
    size = width, height = 800, 600
    screen = pygame.display.set_mode(size)
    running = True
    circle = False
    r, g, b = 0, 0, 0
    d = 0

    while running:
        x, y, w, h = draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x1, y1 = event.pos
                if x <= x1 and x1 <= x + w and y <= y1 and y1 <= y + h:
                    r, g, b = randrange(0, 255), randrange(0, 255), randrange(0, 255)
                    d = randrange(10, 200)
                    circle = True
        if circle:
            clik(screen, d, r, g ,b)
        pygame.display.flip()