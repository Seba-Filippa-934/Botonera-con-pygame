"""
Botonera de Sonidos — 100% Pygame
=================================

Requisitos:
    pip install pygame   (versión 2.x)

Ejecución:
    python botonera.py

Controles:
    * Clic en un botón   -> reproduce su sonido.
    * Clic en 🔁         -> activa/desactiva el loop del sonido.
    * Teclas 1 a 9       -> primeros nueve sonidos.
    * Teclas Q a O       -> siguientes nueve sonidos.
    * Botón DETENER TODOS-> detiene inmediatamente todos los sonidos.
    * F11                -> alterna pantalla completa / ventana.
    * ESC                -> salir.

Personalización:
    Para cambiar los sonidos y los nombres mostrados solo hay que editar
    las listas ARCHIVOS_SONIDOS y NOMBRES_BOTONES. Los archivos se buscan
    en la misma carpeta donde esté este script. Si un archivo no existe,
    su botón se muestra en gris y no hace nada al presionarlo.
"""

import math
import os
import sys

import pygame

# ===========================================================================
# CONSTANTES DE CONFIGURACIÓN
# ===========================================================================

# --- Ventana ---------------------------------------------------------------
ANCHO_VENTANA = 1200
ALTO_VENTANA = 700
FPS_OBJETIVO = 60

# --- Grilla de botones (6 columnas x 3 filas = 18 botones) -----------------
COLUMNAS = 6
FILAS = 3
NUM_BOTONES = COLUMNAS * FILAS
MARGEN_LATERAL = 42  # Ajustado para centrar perfectamente 6 columnas
SEPARACION_BOTONES = 24
Y_GRILLA = 104
ANCHO_BOTON = (ANCHO_VENTANA - 2 * MARGEN_LATERAL
               - (COLUMNAS - 1) * SEPARACION_BOTONES) // COLUMNAS
ALTO_BOTON = 150
RADIO_BORDE = 16

# --- Botón "DETENER TODOS" ---------------------------------------------------
ANCHO_BOTON_DETENER = 380
ALTO_BOTON_DETENER = 64
Y_BOTON_DETENER = ALTO_VENTANA - ALTO_BOTON_DETENER - 18

# --- Título y textos ---------------------------------------------------------
Y_TITULO = 44
TAMANO_TITULO = 60
TAMANO_TEXTO_BOTON = 34
TAMANO_TEXTO_DETENER = 40
TAMANO_TEXTO_ATAJO = 22
TAMANO_TEXTO_MINI = 20
TAMANO_TEXTO_INFO = 22

# --- Animaciones --------------------------------------------------------------
DURACION_PULSACION_MS = 150

# --- Audio ---------------------------------------------------------------------
FRECUENCIA_AUDIO = 44100
TAMANO_BUFFER_AUDIO = 512
NUMERO_CANALES = 32  # permite reproducir muchos sonidos a la vez

# --- Carpeta base (donde está el script) ---------------------------------------
if getattr(sys, "frozen", False):
    CARPETA_BASE = os.path.dirname(os.path.abspath(sys.executable))
else:
    CARPETA_BASE = os.path.dirname(os.path.abspath(__file__))

# --- Lista de archivos de sonido (EDITAR AQUÍ) ---------------------------------
ARCHIVOS_SONIDOS = [
    "1A.mp3",
    "1B-Inglaterra.mp3",
    "1C.mp3",
    "1D-Uruguay.mp3",
    "2A-Francia.mp3",
    "2B.mp3",
    "2C.mp3",
    "3A.mp3",
    "3B-Colombia.mp3",
    "3C-EEUU.mp3",
    "4A.mp3",
    "4B.mp3",
    "cargar.mp3",
    "5B.mp3",
    "cargar.mp3",
    "cargar.mp3",
    "cargar.mp3",
    "7B-Noruega.mp3"
]

# --- Nombres mostrados en los botones (EDITAR AQUÍ) -----------------------------
NOMBRES_BOTONES = [
    "1A",
    "1B-Inglaterra",
    "1C",
    "1D-Uruguay",
    "2A-Francia",
    "2B",
    "2C",
    "3A",
    "3B-Colombia",
    "3C-EEUU",
    "4A",
    "4B",
    "5A",
    "5B",
    "6",
    "6",
    "7A",
    "7B-Noruega"
]

# ===========================================================================
# COLORES
# ===========================================================================
COLOR_FONDO_SUPERIOR = (17, 20, 32)
COLOR_FONDO_INFERIOR = (8, 9, 16)
COLOR_HALO_1 = (86, 126, 255, 16)
COLOR_HALO_2 = (168, 92, 255, 14)
COLOR_HALO_3 = (72, 210, 190, 12)

COLOR_TITULO = (238, 243, 255)
COLOR_ACENTO = (96, 140, 255)
COLOR_TEXTO_INFO = (150, 160, 185)

COLOR_SOMBRA = (0, 0, 0, 150)
COLOR_BRILLO = (255, 255, 255, 20)

COLOR_BOTON = (40, 46, 70)
COLOR_BOTON_HOVER = (62, 74, 112)
COLOR_BOTON_BORDE = (92, 108, 158)
COLOR_BOTON_BORDE_HOVER = (150, 175, 235)
COLOR_TEXTO_BOTON = (232, 238, 252)

COLOR_BOTON_DESHABILITADO = (46, 48, 55)
COLOR_BOTON_DESHABILITADO_BORDE = (66, 68, 76)
COLOR_TEXTO_DESHABILITADO = (122, 126, 138)

# --- Colores para el botón de loop ------------------------------------------
COLOR_LOOP_ACTIVO = (96, 245, 155)      # Verde brillante cuando está activo
COLOR_LOOP_INACTIVO = (62, 74, 112)     # Gris azulado cuando está inactivo
COLOR_LOOP_BORDE = (150, 175, 235)      # Borde del botón de loop
COLOR_TEXTO_LOOP = (232, 238, 252)      # Color del símbolo
# ----------------------------------------------------------------------------

COLOR_DETENER = (186, 42, 52)
COLOR_DETENER_HOVER = (224, 62, 70)
COLOR_DETENER_BORDE = (255, 110, 115)
COLOR_DETENER_BORDE_HOVER = (255, 160, 160)

COLOR_BADGE = (24, 28, 44)
COLOR_BADGE_DESHABILITADO = (36, 38, 44)
COLOR_TEXTO_ATAJO = (170, 185, 220)

COLOR_LED = (96, 245, 155)
COLOR_LED_HALO = (38, 105, 70)
COLOR_BARRA_FONDO = (20, 24, 38)
COLOR_BARRA = (96, 245, 155)

# Esquemas de color de los botones
ESQUEMA_NORMAL = {
    "base": COLOR_BOTON,
    "hover": COLOR_BOTON_HOVER,
    "borde": COLOR_BOTON_BORDE,
    "borde_hover": COLOR_BOTON_BORDE_HOVER,
    "texto": COLOR_TEXTO_BOTON,
}
ESQUEMA_DETENER = {
    "base": COLOR_DETENER,
    "hover": COLOR_DETENER_HOVER,
    "borde": COLOR_DETENER_BORDE,
    "borde_hover": COLOR_DETENER_BORDE_HOVER,
    "texto": COLOR_TEXTO_BOTON,
}
ESQUEMA_DESHABILITADO = {
    "base": COLOR_BOTON_DESHABILITADO,
    "hover": COLOR_BOTON_DESHABILITADO,
    "borde": COLOR_BOTON_DESHABILITADO_BORDE,
    "borde_hover": COLOR_BOTON_DESHABILITADO_BORDE,
    "texto": COLOR_TEXTO_DESHABILITADO,
}


# ===========================================================================
# FUNCIONES AUXILIARES
# ===========================================================================
def mezclar_colores(color_a, color_b, proporcion):
    """Interpola linealmente entre dos colores RGB."""
    return tuple(
        int(can_a + (can_b - can_a) * proporcion)
        for can_a, can_b in zip(color_a, color_b)
    )


def crear_fondo():
    """Crea el fondo (degradado vertical + halos decorativos) una sola vez."""
    fondo = pygame.Surface((ANCHO_VENTANA, ALTO_VENTANA))

    # Degradado vertical
    for y in range(ALTO_VENTANA):
        proporcion = y / max(ALTO_VENTANA - 1, 1)
        color = mezclar_colores(COLOR_FONDO_SUPERIOR, COLOR_FONDO_INFERIOR, proporcion)
        pygame.draw.line(fondo, color, (0, y), (ANCHO_VENTANA, y))

    # Halos decorativos semitransparentes
    decoracion = pygame.Surface((ANCHO_VENTANA, ALTO_VENTANA), pygame.SRCALPHA)
    pygame.draw.circle(decoracion, COLOR_HALO_1, (140, 110), 240)
    pygame.draw.circle(decoracion, COLOR_HALO_2, (1080, 620), 280)
    pygame.draw.circle(decoracion, COLOR_HALO_3, (1120, 90), 170)
    fondo.blit(decoracion, (0, 0))

    return fondo


# ===========================================================================
# CLASE BOTON
# ===========================================================================
class Boton:
    """Botón con bordes redondeados, sombra, hover, animación e indicadores."""

    def __init__(self, rect, texto, fuente_texto, fuente_atajo, fuente_mini,
                 sonido=None, atajo=None, esquema="normal"):
        self.rect = pygame.Rect(rect)
        self.texto = texto
        self.sonido = sonido
        self.atajo = atajo
        self.esquema_nombre = esquema

        # Selección del esquema de colores y del estado del botón
        if esquema == "detener":
            self.colores = ESQUEMA_DETENER
            self.activo = True
        elif sonido is None:
            self.colores = ESQUEMA_DESHABILITADO
            self.activo = False
        else:
            self.colores = ESQUEMA_NORMAL
            self.activo = True

        # Estado de animación y de reproducción
        self.presionado_hasta = -1
        self.inicio_reproduccion = -1
        self.duracion_ms = 0.0

        # Estado de loop
        self.en_loop = False
        self.fuente_loop = fuente_mini

        # ---- Superficies pre-renderizadas (elementos estáticos) ----
        self.sombra = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        pygame.draw.rect(self.sombra, COLOR_SOMBRA, self.sombra.get_rect(),
                         border_radius=RADIO_BORDE)

        self.brillo = pygame.Surface((max(self.rect.width - 12, 4), 4), pygame.SRCALPHA)
        pygame.draw.rect(self.brillo, COLOR_BRILLO, self.brillo.get_rect(),
                         border_radius=2)

        self.superficie_texto = fuente_texto.render(texto, True, self.colores["texto"])

        self.superficie_atajo = None
        if atajo is not None:
            color_atajo = COLOR_TEXTO_ATAJO if self.activo else COLOR_TEXTO_DESHABILITADO
            self.superficie_atajo = fuente_atajo.render(atajo, True, color_atajo)

        self.superficie_sin_audio = None
        if esquema == "normal" and sonido is None:
            self.superficie_sin_audio = fuente_mini.render(
                "SIN AUDIO", True, COLOR_TEXTO_DESHABILITADO)

    # ------------------------------------------------------------------
    def esta_sonando(self):
        """Devuelve True si el sonido del botón está sonando ahora mismo."""
        return self.sonido is not None and self.sonido.get_num_channels() > 0

    def presionar_visual(self):
        """Activa la animación de pulsado sin reproducir nada."""
        self.presionado_hasta = pygame.time.get_ticks() + DURACION_PULSACION_MS

    def reproducir(self):
        """Reproduce el sonido asociado. Devuelve True si tuvo éxito."""
        if not self.activo or self.sonido is None:
            return False
        ahora = pygame.time.get_ticks()
        self.presionado_hasta = ahora + DURACION_PULSACION_MS
        try:
            if self.en_loop:
                self.sonido.play(loops=-1)
            else:
                self.sonido.play()
        except pygame.error as exc:
            print(f"[ERROR] No se pudo reproducir '{self.texto}': {exc}")
            return False
        self.inicio_reproduccion = ahora
        self.duracion_ms = max(self.sonido.get_length() * 1000.0, 1.0)
        return True

    def toggle_loop(self):
        """Activa o desactiva el modo loop para este botón."""
        if not self.activo or self.sonido is None:
            return
        
        self.en_loop = not self.en_loop
        
        if self.en_loop:
            if self.esta_sonando():
                self.sonido.stop()
                self.sonido.play(loops=-1)
                self.inicio_reproduccion = pygame.time.get_ticks()
        else:
            if self.esta_sonando():
                self.sonido.stop()
    
    def clic_en_loop(self, posicion):
        """Detecta si el clic fue en el botón circular de loop."""
        if not self.activo or self.sonido is None:
            return False
        
        radio_loop = 14
        x_loop = self.rect.right - radio_loop - 8 
        y_loop = self.rect.top + radio_loop + 40
        
        distancia = math.sqrt((posicion[0] - x_loop)**2 + (posicion[1] - y_loop)**2)
        return distancia <= radio_loop

    # ------------------------------------------------------------------
    def dibujar(self, superficie, posicion_mouse):
        """Dibuja el botón completo: sombra, fondo, textos e indicadores."""
        ahora = pygame.time.get_ticks()
        presionado = ahora < self.presionado_hasta
        hover = self.activo and self.rect.collidepoint(posicion_mouse)

        desplazamiento = 3 if presionado else 0
        rect = self.rect.move(0, desplazamiento)

        # Sombra
        distancia_sombra = 2 if presionado else 6
        superficie.blit(self.sombra, (self.rect.x, self.rect.y + distancia_sombra))

        # Fondo y borde
        color_fondo = self.colores["hover"] if hover else self.colores["base"]
        pygame.draw.rect(superficie, color_fondo, rect, border_radius=RADIO_BORDE)
        color_borde = self.colores["borde_hover"] if hover else self.colores["borde"]
        pygame.draw.rect(superficie, color_borde, rect, width=2,
                         border_radius=RADIO_BORDE)

        # Brillo superior sutil
        superficie.blit(self.brillo, (rect.x + 6, rect.y + 5))

        # Texto principal
        if self.esquema_nombre == "normal":
            centro_texto = (rect.centerx, rect.centery - 8)
        else:
            centro_texto = rect.center
        superficie.blit(self.superficie_texto,
                        self.superficie_texto.get_rect(center=centro_texto))

        # Aviso para botones sin sonido
        if self.superficie_sin_audio is not None:
            superficie.blit(self.superficie_sin_audio,
                            self.superficie_sin_audio.get_rect(
                                center=(rect.centerx, rect.centery + 26)))

        # Insignia con la tecla de atajo
        if self.superficie_atajo is not None:
            rect_badge = self.superficie_atajo.get_rect()
            rect_badge.width += 14
            rect_badge.height += 8
            rect_badge.topleft = (rect.x + 10, rect.y + 10)
            color_badge = COLOR_BADGE if self.activo else COLOR_BADGE_DESHABILITADO
            pygame.draw.rect(superficie, color_badge, rect_badge, border_radius=6)
            superficie.blit(self.superficie_atajo,
                            self.superficie_atajo.get_rect(center=rect_badge.center))

        # Indicador de reproducción: LED pulsante + barra de progreso
        if self.esta_sonando():
            pulso = 0.5 + 0.5 * math.sin(ahora / 150.0)
            radio_led = 5 + round(pulso * 2)
            posicion_led = (rect.right - 20, rect.top + 20)
            pygame.draw.circle(superficie, COLOR_LED_HALO, posicion_led, radio_led + 6)
            pygame.draw.circle(superficie, COLOR_LED, posicion_led, radio_led)

            if self.inicio_reproduccion >= 0:
                transcurrido = ahora - self.inicio_reproduccion
                progreso = min(transcurrido / self.duracion_ms, 1.0)
                if progreso < 1.0:
                    margen = 14
                    ancho_total = rect.width - margen * 2
                    pista = pygame.Rect(rect.x + margen, rect.bottom - 16,
                                        ancho_total, 5)
                    pygame.draw.rect(superficie, COLOR_BARRA_FONDO, pista,
                                     border_radius=3)
                    ancho_relleno = int(ancho_total * progreso)
                    if ancho_relleno > 0:
                        relleno = pygame.Rect(rect.x + margen, rect.bottom - 16,
                                              ancho_relleno, 5)
                        pygame.draw.rect(superficie, COLOR_BARRA, relleno,
                                         border_radius=3)

        # Botón de loop circular (esquina superior derecha)
        if self.activo and self.sonido is not None:
            radio_loop = 14
            x_loop = rect.right - radio_loop - 8
            y_loop = rect.top + radio_loop + 40
            
            distancia_mouse = math.sqrt((posicion_mouse[0] - x_loop)**2 + 
                                       (posicion_mouse[1] - y_loop)**2)
            hover_loop = distancia_mouse <= radio_loop
            
            if self.en_loop:
                color_fondo_loop = COLOR_LOOP_ACTIVO
                color_borde_loop = (120, 255, 180)
            else:
                color_fondo_loop = COLOR_LOOP_INACTIVO if not hover_loop else COLOR_BOTON_HOVER
                color_borde_loop = COLOR_LOOP_BORDE
            
            pygame.draw.circle(superficie, color_fondo_loop, 
                             (x_loop, y_loop), radio_loop)
            pygame.draw.circle(superficie, color_borde_loop,
                             (x_loop, y_loop), radio_loop, width=2)
            
            try:
                simbolo = "rep"
                superficie_simbolo = self.fuente_loop.render(
                    simbolo, True, COLOR_TEXTO_LOOP)
                superficie.blit(superficie_simbolo, 
                              superficie_simbolo.get_rect(center=(x_loop, y_loop)))
            except:
                self._dibujar_simbolo_loop(superficie, x_loop, y_loop, COLOR_TEXTO_LOOP)

    def _dibujar_simbolo_loop(self, superficie, x, y, color):
        """Dibuja un símbolo de loop manual si el emoji no funciona."""
        pygame.draw.arc(superficie, color, (x-8, y-8, 16, 16), 0.5, 2.5, 2)
        pygame.draw.polygon(superficie, color, [(x+6, y-4), (x+10, y), (x+6, y+4)])
        pygame.draw.arc(superficie, color, (x-8, y-8, 16, 16), 3.6, 5.6, 2)
        pygame.draw.polygon(superficie, color, [(x-6, y+4), (x-10, y), (x-6, y-4)])


# ===========================================================================
# CLASE PRINCIPAL DE LA APLICACIÓN
# ===========================================================================
class BotoneraSonidos:
    """Aplicación principal: ventana, eventos, sonidos y dibujado."""

    def __init__(self):
        pygame.mixer.pre_init(FRECUENCIA_AUDIO, -16, 2, TAMANO_BUFFER_AUDIO)
        pygame.init()

        self.pantalla_completa = False
        self.pantalla = self._crear_ventana()
        pygame.display.set_caption("Botonera de Sonidos")
        self.reloj = pygame.time.Clock()

        try:
            pygame.mixer.set_num_channels(NUMERO_CANALES)
        except pygame.error:
            pass

        # ------------------------------- Fuentes ------------------------------
        self.fuente_titulo = pygame.font.Font(None, TAMANO_TITULO)
        self.fuente_titulo.set_bold(True)
        self.fuente_boton = pygame.font.Font(None, TAMANO_TEXTO_BOTON)
        self.fuente_detener = pygame.font.Font(None, TAMANO_TEXTO_DETENER)
        self.fuente_detener.set_bold(True)
        self.fuente_atajo = pygame.font.Font(None, TAMANO_TEXTO_ATAJO)
        self.fuente_mini = pygame.font.Font(None, TAMANO_TEXTO_MINI)
        self.fuente_info = pygame.font.Font(None, TAMANO_TEXTO_INFO)

        # -------------------------- Superficies estáticas ---------------------
        self.fondo = crear_fondo()
        self.superficie_titulo = self.fuente_titulo.render(
            "BOTONERA DE SONIDOS", True, COLOR_TITULO)
        self.superficie_ayuda = self.fuente_info.render(
            "1-9 / Q-O: sonidos   ·   F11: pantalla completa   ·   ESC: salir",
            True, COLOR_TEXTO_INFO)

        # ------------------------------- Botones ------------------------------
        self.botones = self._crear_botones()
        self.boton_detener = Boton(
            pygame.Rect((ANCHO_VENTANA - ANCHO_BOTON_DETENER) // 2,
                        Y_BOTON_DETENER,
                        ANCHO_BOTON_DETENER, ALTO_BOTON_DETENER),
            "DETENER TODOS",
            fuente_texto=self.fuente_detener,
            fuente_atajo=self.fuente_atajo,
            fuente_mini=self.fuente_mini,
            esquema="detener",
        )

        # ------------------------- Mapa de atajos de teclado ------------------
        self.mapa_teclas = {}
        for indice, (_etiqueta, tecla) in enumerate(self._teclas_y_etiquetas()):
            self.mapa_teclas[tecla] = indice
        for numero in range(1, 10):  # también el teclado numérico
            self.mapa_teclas[getattr(pygame, f"K_KP{numero}")] = numero - 1
        self.teclas_presionadas = set()

        self.corriendo = True

        cargados = sum(1 for boton in self.botones if boton.sonido is not None)
        print(f"[INFO] Sonidos cargados: {cargados}/{NUM_BOTONES}")

    # ------------------------------------------------------------------
    def _crear_ventana(self):
        """Crea la ventana aplicando el modo pantalla completa actual."""
        banderas = getattr(pygame, "SCALED", 0)
        if self.pantalla_completa:
            banderas |= pygame.FULLSCREEN
        try:
            return pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA), banderas)
        except pygame.error:
            banderas = pygame.FULLSCREEN if self.pantalla_completa else 0
            return pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA), banderas)

    @staticmethod
    def _teclas_y_etiquetas():
        """Devuelve pares (etiqueta visible, tecla pygame) para los 18 botones."""
        pares = []
        # Primera fila: 1 a 9
        for numero in range(1, 10):
            pares.append((str(numero), getattr(pygame, f"K_{numero}")))
        # Segunda fila: Q a O (9 teclas: Q, W, E, R, T, Y, U, I, O)
        for letra in ("q", "w", "e", "r", "t", "y", "u", "i", "o"):
            pares.append((letra.upper(), getattr(pygame, f"K_{letra}")))
        return pares

    def _cargar_sonidos(self):
        """Carga todos los sonidos de la lista ARCHIVOS_SONIDOS."""
        mixer_listo = pygame.mixer.get_init() is not None
        if not mixer_listo:
            print("[AVISO] No se pudo inicializar el audio; "
                  "los botones quedarán sin sonido.")

        sonidos = []
        for indice in range(NUM_BOTONES):
            if indice >= len(ARCHIVOS_SONIDOS):
                print(f"[AVISO] Falta el archivo del botón {indice + 1} "
                      f"en ARCHIVOS_SONIDOS.")
                sonidos.append(None)
                continue

            archivo = ARCHIVOS_SONIDOS[indice]
            if not mixer_listo:
                sonidos.append(None)
                continue

            ruta = os.path.join(CARPETA_BASE, archivo)
            if not os.path.isfile(ruta):
                print(f"[AVISO] No existe '{archivo}'. "
                      f"El botón {indice + 1} quedará deshabilitado.")
                sonidos.append(None)
                continue

            try:
                sonidos.append(pygame.mixer.Sound(ruta))
            except Exception as exc:
                print(f"[ERROR] No se pudo cargar '{archivo}': {exc}")
                sonidos.append(None)
        return sonidos

    def _crear_botones(self):
        """Crea la grilla de botones y les asigna su sonido y su atajo."""
        sonidos = self._cargar_sonidos()
        teclas = self._teclas_y_etiquetas()
        botones = []

        for indice in range(NUM_BOTONES):
            fila = indice // COLUMNAS
            columna = indice % COLUMNAS
            x = MARGEN_LATERAL + columna * (ANCHO_BOTON + SEPARACION_BOTONES)
            y = Y_GRILLA + fila * (ALTO_BOTON + SEPARACION_BOTONES)

            if indice < len(NOMBRES_BOTONES):
                nombre = NOMBRES_BOTONES[indice]
            else:
                nombre = f"SONIDO {indice + 1}"

            etiqueta_tecla, _tecla = teclas[indice]
            botones.append(
                Boton(
                    pygame.Rect(x, y, ANCHO_BOTON, ALTO_BOTON),
                    nombre,
                    fuente_texto=self.fuente_boton,
                    fuente_atajo=self.fuente_atajo,
                    fuente_mini=self.fuente_mini,
                    sonido=sonidos[indice],
                    atajo=etiqueta_tecla,
                )
            )
        return botones

    # ------------------------------------------------------------------
    def reproducir_indice(self, indice):
        """Reproduce el sonido del botón indicado (usado por los atajos)."""
        if 0 <= indice < len(self.botones):
            self.botones[indice].reproducir()

    def detener_todo(self):
        """Detiene inmediatamente todos los sonidos en reproducción."""
        try:
            pygame.mixer.stop()
        except pygame.error:
            pass

    def alternar_pantalla_completa(self):
        """Alterna entre modo ventana y pantalla completa."""
        self.pantalla_completa = not self.pantalla_completa
        self.pantalla = self._crear_ventana()

    def _manejar_clic(self, posicion):
        """Gestiona los clics sobre el botón detener, botones de loop y la grilla."""
        if self.boton_detener.rect.collidepoint(posicion):
            self.boton_detener.presionar_visual()
            self.detener_todo()
            return
        
        for boton in self.botones:
            if boton.clic_en_loop(posicion):
                boton.toggle_loop()
                return
            if boton.rect.collidepoint(posicion):
                boton.reproducir()
                return

    # ------------------------------------------------------------------
    def manejar_eventos(self):
        """Procesa todos los eventos de la cola de Pygame."""
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.corriendo = False

            elif evento.type == pygame.KEYDOWN:
                if evento.key in self.teclas_presionadas:
                    continue
                self.teclas_presionadas.add(evento.key)

                if evento.key == pygame.K_F11:
                    self.alternar_pantalla_completa()
                elif evento.key == pygame.K_ESCAPE:
                    self.corriendo = False
                elif evento.key in self.mapa_teclas:
                    self.reproducir_indice(self.mapa_teclas[evento.key])

            elif evento.type == pygame.KEYUP:
                self.teclas_presionadas.discard(evento.key)

            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                self._manejar_clic(evento.pos)

    # ------------------------------------------------------------------
    def dibujar(self):
        """Dibuja un fotograma completo de la aplicación."""
        self.pantalla.blit(self.fondo, (0, 0))
        posicion_mouse = pygame.mouse.get_pos()

        # Título y línea decorativa
        self.pantalla.blit(
            self.superficie_titulo,
            self.superficie_titulo.get_rect(center=(ANCHO_VENTANA // 2, Y_TITULO)))
        ancho_linea = 320
        pygame.draw.rect(self.pantalla, COLOR_ACENTO,
                         ((ANCHO_VENTANA - ancho_linea) // 2, 78, ancho_linea, 3),
                         border_radius=2)

        # Botones de sonido y botón de detener
        for boton in self.botones:
            boton.dibujar(self.pantalla, posicion_mouse)
        self.boton_detener.dibujar(self.pantalla, posicion_mouse)

        # Indicador de FPS (esquina superior izquierda)
        fps = self.reloj.get_fps()
        superficie_fps = self.fuente_info.render(f"FPS: {fps:5.1f}", True,
                                                 COLOR_TEXTO_INFO)
        self.pantalla.blit(superficie_fps, (12, 10))

        # Texto de ayuda (esquina superior derecha)
        self.pantalla.blit(
            self.superficie_ayuda,
            (ANCHO_VENTANA - self.superficie_ayuda.get_width() - 12, 12))

        pygame.display.flip()

    # ------------------------------------------------------------------
    def ejecutar(self):
        """Bucle principal de la aplicación."""
        while self.corriendo:
            self.manejar_eventos()
            self.dibujar()
            self.reloj.tick(FPS_OBJETIVO)
        pygame.quit()


# ===========================================================================
# PUNTO DE ENTRADA
# ===========================================================================
def main():
    app = BotoneraSonidos()
    app.ejecutar()


if __name__ == "__main__":
    main()