import pygame
import moderngl

pygame.init()

pygame.display.set_mode(
    (800, 600),
    pygame.OPENGL | pygame.DOUBLEBUF
)

ctx = moderngl.create_context()

print(ctx.info)
print(ctx.viewport)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    ctx.screen.use()
    ctx.clear(1.0, 0.0, 0.0, 1.0)

    pygame.display.flip()

pygame.quit()