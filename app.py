import tkinter as tk
from datetime import datetime
from PIL import Image, ImageTk, ImageDraw
import barcode
from barcode.writer import ImageWriter
import os

# -------------------------
# CONFIGURACIÓN Y CONSTANTES
# -------------------------
W, H = 420, 780
BG_YELLOW = "#FFB703"
PURPLE = "#7B2CBF"
GREEN_BG = "#D4EDDA"
GREEN_TEXT = "#28A745"
BLACK = "#000000"
WHITE = "#FFFFFF"

# -------------------------
# GENERAR CÓDIGO DE BARRAS
# -------------------------
def generar_barcode(texto="987654321"):
    fname = "barcode_temp"
    code128 = barcode.get('code128', texto, writer=ImageWriter())
    fullname = code128.save(fname, options={"module_height": 10, "font_size": 0})
    return fullname

# -------------------------
# ACTUALIZAR RELOJ
# -------------------------
def actualizar_reloj():
    ahora = datetime.now().strftime("%H:%M:%S")
    canvas.itemconfig(id_hora, text=ahora)
    hoy = datetime.now().strftime("%d %B %Y")
    canvas.itemconfig(id_fecha, text=hoy)
    root.after(1000, actualizar_reloj)

# -------------------------
# CREAR VENTANA
# -------------------------
root = tk.Tk()
root.title("ID CARD")
root.geometry(f"{W}x{H}")
root.resizable(False, False)

canvas = tk.Canvas(root, width=W, height=H, bg=BG_YELLOW, highlightthickness=0)
canvas.pack()

# -------------------------
# DIMENSIONES DE LA TARJETA
# -------------------------
cx = W // 2
card_margin = 30
card_left = card_margin
card_right = W - card_margin
card_top = 180
card_bottom = H - 100
card_radius = 20

# Radio del círculo del avatar
avatar_r = 85
avatar_cy = card_top - 40  # El círculo se superpone a la tarjeta

# -------------------------
# DIBUJAR TARJETA BLANCA CON ESQUINAS REDONDEADAS
# -------------------------
def crear_rectangulo_redondeado(x1, y1, x2, y2, r, **kwargs):
    points = [
        x1+r, y1,
        x1+r, y1,
        x2-r, y1,
        x2-r, y1,
        x2, y1,
        x2, y1+r,
        x2, y1+r,
        x2, y2-r,
        x2, y2-r,
        x2, y2,
        x2-r, y2,
        x2-r, y2,
        x1+r, y2,
        x1+r, y2,
        x1, y2,
        x1, y2-r,
        x1, y2-r,
        x1, y1+r,
        x1, y1+r,
        x1, y1
    ]
    return canvas.create_polygon(points, smooth=True, **kwargs)

# Dibujar tarjeta blanca
crear_rectangulo_redondeado(card_left, card_top, card_right, card_bottom, card_radius, fill=WHITE, outline=WHITE)

# Crear semicírculo en la parte superior de la tarjeta para el avatar
canvas.create_arc(cx - avatar_r - 5, avatar_cy - avatar_r - 5,
                  cx + avatar_r + 5, avatar_cy + avatar_r + 5,
                  start=180, extent=180, style='pieslice', fill=WHITE, outline=WHITE)

# -------------------------
# CÍRCULO DEL AVATAR
# -------------------------
# Borde amarillo (anillo exterior)
canvas.create_oval(cx - avatar_r, avatar_cy - avatar_r,
                   cx + avatar_r, avatar_cy + avatar_r,
                   fill=BG_YELLOW, outline=BG_YELLOW, width=4)

# Círculo blanco interior
inner_r = avatar_r - 8
canvas.create_oval(cx - inner_r, avatar_cy - inner_r,
                   cx + inner_r, avatar_cy + inner_r,
                   fill=WHITE, outline=WHITE)

# Cargar y mostrar la foto del usuario
try:
foto_path = "user_photo.jpg"  # o simplemente comenta esta línea
img_foto = Image.open(foto_path)
    
    # Redimensionar y recortar la imagen en círculo
    foto_size = int(inner_r * 2)
    img_foto = img_foto.resize((foto_size, foto_size), Image.LANCZOS)
    
    # Crear máscara circular
    mask = Image.new('L', (foto_size, foto_size), 0)
    from PIL import ImageDraw
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, foto_size, foto_size), fill=255)
    
    # Aplicar máscara
    img_foto.putalpha(mask)
    
    photo_usuario = ImageTk.PhotoImage(img_foto)
    canvas.photo_usuario = photo_usuario
    canvas.create_image(cx, avatar_cy, image=photo_usuario)
    
except Exception as e:
    # Si falla cargar la foto, mostrar silueta por defecto
    head_r = 25
    canvas.create_oval(cx - head_r, avatar_cy - 15 - head_r,
                       cx + head_r, avatar_cy - 15 + head_r,
                       fill=BLACK, outline=BLACK)
    canvas.create_rectangle(cx - 30, avatar_cy + 10, cx + 30, avatar_cy + 45,
                            fill=BLACK, outline=BLACK)
    canvas.create_arc(cx - 45, avatar_cy + 20, cx + 45, avatar_cy + 95,
                      start=0, extent=180, style='pieslice', fill=BLACK, outline=BLACK)
    print(f"Error cargando foto: {e}")

# -------------------------
# BADGE "ACTIVO"
# -------------------------
badge_y = avatar_cy + avatar_r + 35
badge_w, badge_h = 140, 40

# Crear rectángulo con esquinas redondeadas para el badge
badge_r = 8
canvas.create_rectangle(cx - badge_w//2 + badge_r, badge_y,
                        cx + badge_w//2 - badge_r, badge_y + badge_h,
                        fill=GREEN_BG, outline=GREEN_BG)
canvas.create_oval(cx - badge_w//2, badge_y,
                   cx - badge_w//2 + 2*badge_r, badge_y + badge_h,
                   fill=GREEN_BG, outline=GREEN_BG)
canvas.create_oval(cx + badge_w//2 - 2*badge_r, badge_y,
                   cx + badge_w//2, badge_y + badge_h,
                   fill=GREEN_BG, outline=GREEN_BG)

canvas.create_text(cx, badge_y + badge_h//2, text="✓ ACTIVO",
                   font=("Arial", 13, "bold"), fill=GREEN_TEXT)

# -------------------------
# NOMBRE
# -------------------------
nombre_y = badge_y + 80
canvas.create_text(cx, nombre_y, text="Marck Nolte Salinas",
                   font=("Arial Black", 22, "bold"), fill=PURPLE, justify="center")

# -------------------------
# CARRERA Y NIVEL
# -------------------------
carrera_y = nombre_y + 80
canvas.create_text(cx, carrera_y, text="Ing. Ambiental",
                   font=("Arial", 16, "bold"), fill=BLACK)
canvas.create_text(cx, carrera_y + 35, text="🎓 Pregrado",
                   font=("Arial", 14), fill=BLACK)

# -------------------------
# LÍNEA PUNTEADA
# -------------------------
linea_y = carrera_y + 70
for i in range(card_left + 10, card_right - 10, 10):
    canvas.create_line(i, linea_y, i + 5, linea_y, fill="#CCCCCC", width=2)

# -------------------------
# HORA DINÁMICA
# -------------------------
hora_y = linea_y + 60
id_hora = canvas.create_text(cx, hora_y, text=datetime.now().strftime("%H:%M:%S"),
                             font=("Arial Black", 38, "bold"), fill=PURPLE)

# -------------------------
# CÓDIGO DE BARRAS
# -------------------------
try:
    barcode_path = generar_barcode("987654321")
    img_bar = Image.open(barcode_path)
    img_bar = img_bar.resize((340, 75), Image.LANCZOS)
    photo_bar = ImageTk.PhotoImage(img_bar)
    canvas.photo_bar = photo_bar
    canvas.create_image(cx, hora_y + 90, image=photo_bar)
    try:
        os.remove(barcode_path)
    except:
        pass
except Exception as e:
    canvas.create_rectangle(cx-170, hora_y + 55, cx+170, hora_y + 125,
                            fill=WHITE, outline=BLACK, width=2)
    canvas.create_text(cx, hora_y + 90, text="|||  ||||||  |||  ||||||  |||",
                       font=("Courier", 16, "bold"), fill=BLACK)

# -------------------------
# FECHA
# -------------------------
id_fecha = canvas.create_text(cx, hora_y + 160, text=datetime.now().strftime("%d %B %Y"),
                             font=("Arial", 13), fill=BLACK)

# -------------------------
# INICIAR RELOJ
# -------------------------
root.after(0, actualizar_reloj)
root.mainloop()

