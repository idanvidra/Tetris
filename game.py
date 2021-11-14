import pygame
from Tetris import Tetris
from constatnts import BOARD_COLORS, COLORS


def main():
    pygame.init()

    size = (400, 500)
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Tetris")

    # loop until the user click the close button
    done = False
    clock = pygame.time.Clock()
    fps = 25
    game = Tetris(20, 10)
    counter = 0

    pressing_down = False

    # main game loop
    while not done:
        if game.figure is None:
            game.new_figure()

        counter += 1
        if counter > 100000:
            counter = 0

        if counter % (fps // game.level // 2) == 0 or pressing_down:
            if game.state == "start":
                game.go_down()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    game.rotate()
                # if event.key == pygame.K_LEFT:
                #     game.go_side(-1)
                # if event.key == pygame.K_RIGHT:
                #     game.go_side(1)
                if event.key == pygame.K_SPACE:
                    game.go_space()
                if event.key == pygame.K_ESCAPE:
                    game.__init__(20, 10)
                    main()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and keys[pygame.K_UP]:
            game.rotate()
            game.go_side(1)
        if keys[pygame.K_LEFT] and keys[pygame.K_UP]:
            game.rotate()
            game.go_side(-1)
        if keys[pygame.K_LEFT]:
            game.go_side(-1)
        if keys[pygame.K_RIGHT]:
            game.go_side(1)
        # if keys[pygame.K_UP]:
        #     game.rotate()
        # if keys[pygame.K_SPACE]:
        #     game.go_space()
        # if keys[pygame.K_ESCAPE]:
        #     game.__init__(20, 10)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                pressing_down = False

        screen.fill(BOARD_COLORS["WHITE"])

        for i in range(game.height):
            for j in range(game.width):
                pygame.draw.rect(screen, BOARD_COLORS["GRAY"], 
                [game.x + game.zoom * j,
                game.y + game.zoom * i, 
                game.zoom, game.zoom], 
                1)
                if game.field[i][j] > 0:
                    pygame.draw.rect(screen, COLORS[game.field[i][j]], 
                    [game.x + game.zoom * j + 1, 
                    game.y + game.zoom * i + 1, 
                    game.zoom - 2, 
                    game.zoom - 1])

        if game.figure is not None:
            for i in range(4):
                for j in range(4):
                    p = i * 4 + j
                    if p in game.figure.image():
                        pygame.draw.rect(screen, COLORS[game.figure.color],
                                         [game.x + game.zoom * (j + game.figure.x) + 1,
                                         game.y + game.zoom *(i + game.figure.y) + 1,
                                         game.zoom - 2, 
                                         game.zoom - 2])

        font = pygame.font.SysFont('Calibri', 25, True, False)
        font1 = pygame.font.SysFont('Calibri', 65, True, False)
        text = font.render("Score: " + str(game.score),
                           True, BOARD_COLORS["BLACK"])
        text_game_over = font1.render(
            "Game Over", True, BOARD_COLORS["ORANGE"])
        text_game_over1 = font1.render(
            "Press ESC", True, BOARD_COLORS["YELLOW"])

        screen.blit(text, [0, 0])
        if game.state == "gameover":
            screen.blit(text_game_over, [20, 200])
            screen.blit(text_game_over1, [25, 265])

        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()


if __name__ == "__main__":
    main()
