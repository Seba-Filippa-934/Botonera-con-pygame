import pygame
import os

# ==========================
# INICIALIZAR PYGAME
# ==========================

pygame.init()
pygame.mixer.init()

# ==========================
# VENTANA
# ==========================

ANCHO = 900
ALTO = 500

VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Botonera de Sonidos")

# ==========================
# COLORES
# ==========================

BLANCO = (255, 255, 255)
GRIS = (200, 200, 200)
GRIS_OSCURO = (160, 160, 160)
NEGRO = (0, 0, 0)
ROJO = (180, 50, 50)
ROJO_CLARO = (220, 80, 80)

# ==========================
# FUENTE
# ==========================

fuente = pygame.font.SysFont("Arial", 24)

# ==========================
# CARGAR SONIDOS
# ==========================

def cargar_sonido(ruta):
    if os.path.exists(ruta):
        return pygame.mixer.Sound(ruta)
    else:
        print(f"No se encontró el archivo: {ruta}")
        return None

# Cambiá estos nombres por los de tus archivos
sonido1 = cargar_sonido("rayo.mp3")
sonido2 = cargar_sonido("disparo.mp3")
sonido3 = cargar_sonido("palas.mp3")
sonido4 = cargar_sonido("corta.mp3")
sonido5 = cargar_sonido("sonido5.wav")
sonido6 = cargar_sonido("sonido6.wav")

sonidos = [
    sonido1,
    sonido2,
    sonido3,
    sonido4,
    sonido5,
    sonido6
]

nombres = [
    "Rayo",
    "Disparo",
    "Palas",
    "Cortadora",
    "Sonido 5",
    "Sonido 6"
]

# ==========================
# CREAR BOTONES
# ==========================

botones = []

ANCHO_BOTON = 220
ALTO_BOTON = 80
ESPACIO = 30

inicio_x = (ANCHO - (3 * ANCHO_BOTON + 2 * ESPACIO)) // 2

fila_superior = 70
fila_inferior = 180

# Tres botones arriba
for i in range(3):
    botones.append(
        pygame.Rect(
            inicio_x + i * (ANCHO_BOTON + ESPACIO),
            fila_superior,
            ANCHO_BOTON,
            ALTO_BOTON
        )
    )

# Tres botones abajo
for i in range(3):
    botones.append(
        pygame.Rect(
            inicio_x + i * (ANCHO_BOTON + ESPACIO),
            fila_inferior,
            ANCHO_BOTON,
            ALTO_BOTON
        )
    )

# Botón para detener sonidos
boton_stop = pygame.Rect(
    (ANCHO - 250) // 2,
    330,
    250,
    70
)

# ==========================
# BUCLE PRINCIPAL
# ==========================

corriendo = True

while corriendo:

    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            corriendo = False

        if evento.type == pygame.MOUSEBUTTONDOWN:

            if evento.button == 1:

                # Botones de sonidos
                for i, boton in enumerate(botones):

                    if boton.collidepoint(evento.pos):

                        if sonidos[i] is not None:
                            sonidos[i].play()
                        else:
                            print(f"El sonido {i+1} no está cargado.")

                # Botón detener
                if boton_stop.collidepoint(evento.pos):
                    pygame.mixer.stop()

    # ==========================
    # DIBUJAR PANTALLA
    # ==========================

    VENTANA.fill(BLANCO)

    mouse = pygame.mouse.get_pos()

    # Dibujar botones de sonidos
    for i, boton in enumerate(botones):

        if boton.collidepoint(mouse):
            color = GRIS_OSCURO
        else:
            color = GRIS

        pygame.draw.rect(
            VENTANA,
            color,
            boton,
            border_radius=10
        )

        texto = fuente.render(
            nombres[i],
            True,
            NEGRO
        )

        texto_rect = texto.get_rect(center=boton.center)

        VENTANA.blit(texto, texto_rect)

    # Dibujar botón detener
    if boton_stop.collidepoint(mouse):
        color_stop = ROJO_CLARO
    else:
        color_stop = ROJO

    pygame.draw.rect(
        VENTANA,
        color_stop,
        boton_stop,
        border_radius=10
    )

    texto_stop = fuente.render(
        "DETENER SONIDOS",
        True,
        BLANCO
    )

    texto_stop_rect = texto_stop.get_rect(center=boton_stop.center)

    VENTANA.blit(texto_stop, texto_stop_rect)

    pygame.display.flip()

pygame.quit()