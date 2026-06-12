import pygame
import sys

pygame.init()

# -------------------------
# CONFIGURACIÓN
# -------------------------
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Transformaciones 2D con Pygame")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

# -------------------------
# CARGAR IMAGEN
# -------------------------
image_original = pygame.image.load("imagen.jpg").convert()
image = image_original.copy()

# -------------------------
# VARIABLES
# -------------------------
angle = 0
scale = 1.0

x = WIDTH // 2
y = HEIGHT // 2

# -------------------------
# FUNCIONES
# -------------------------

def grayscale(surface):
    nueva = surface.copy()

    for i in range(nueva.get_width()):
        for j in range(nueva.get_height()):
            color = nueva.get_at((i, j))

            r = color.r
            g = color.g
            b = color.b

            gris = (r + g + b) // 3

            nueva.set_at((i, j), (gris, gris, gris))

    return nueva


def invert_colors(surface):
    nueva = surface.copy()

    for i in range(nueva.get_width()):
        for j in range(nueva.get_height()):
            color = nueva.get_at((i, j))

            r = 255 - color.r
            g = 255 - color.g
            b = 255 - color.b

            nueva.set_at((i, j), (r, g, b))

    return nueva


# -------------------------
# BUCLE PRINCIPAL
# -------------------------

running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # -------------------------
        # ZOOM CON RUEDA DEL MOUSE
        # -------------------------
        if event.type == pygame.MOUSEWHEEL:

            if event.y > 0:
                scale += 0.1

            if event.y < 0:
                scale = max(0.1, scale - 0.1)

        # -------------------------
        # TECLADO
        # -------------------------
        if event.type == pygame.KEYDOWN:

            # Rotar
            if event.key == pygame.K_q:
                angle += 10

            if event.key == pygame.K_e:
                angle -= 10

            # Zoom +
            if event.key in (
                pygame.K_PLUS,
                pygame.K_EQUALS,
                pygame.K_KP_PLUS
            ):
                scale += 0.1

            # Zoom -
            if event.key in (
                pygame.K_MINUS,
                pygame.K_KP_MINUS
            ):
                scale = max(0.1, scale - 0.1)

            # Escala de grises
            if event.key == pygame.K_g:
                image = grayscale(image)

            # Invertir colores
            if event.key == pygame.K_i:
                image = invert_colors(image)

            # Reflejo horizontal
            if event.key == pygame.K_h:
                image = pygame.transform.flip(
                    image,
                    True,
                    False
                )

            # Reflejo vertical
            if event.key == pygame.K_v:
                image = pygame.transform.flip(
                    image,
                    False,
                    True
                )

            # Restaurar
            if event.key == pygame.K_r:
                image = image_original.copy()
                angle = 0
                scale = 1.0
                x = WIDTH // 2
                y = HEIGHT // 2

    # -------------------------
    # MOVIMIENTO
    # -------------------------
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        x -= 5

    if keys[pygame.K_RIGHT]:
        x += 5

    if keys[pygame.K_UP]:
        y -= 5

    if keys[pygame.K_DOWN]:
        y += 5

    # -------------------------
    # DIBUJO
    # -------------------------
    screen.fill((25, 25, 25))

    transformed = pygame.transform.rotozoom(
        image,
        angle,
        scale
    )

    rect = transformed.get_rect(center=(x, y))

    screen.blit(transformed, rect)

    mx, my = pygame.mouse.get_pos()

    instrucciones = [
        "Q = Rotar Izquierda",
        "E = Rotar Derecha",
        "+ / - = Zoom",
        "Rueda Mouse = Zoom",
        "Flechas = Mover Imagen",
        "G = Escala de Grises",
        "I = Invertir Colores",
        "H = Reflejo Horizontal",
        "V = Reflejo Vertical",
        "R = Restaurar",
        f"Escala: {scale:.1f}",
        f"Angulo: {angle}",
        f"Mouse: ({mx}, {my})"
    ]

    for i, texto in enumerate(instrucciones):
        txt = font.render(texto, True, (255, 255, 255))
        screen.blit(txt, (20, 20 + i * 28))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()