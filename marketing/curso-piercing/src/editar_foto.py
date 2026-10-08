"""Tratamento da foto do profissional: paleta vermelho sangue + preto.

Uso: python3 -I editar_foto.py <foto_original.jpg> <pasta_saida>
Gera recortes 4:5 (1080x1350) em dois tratamentos: 'sangue' (duotone) e 'noir' (P&B com luz vermelha).
"""
import sys, os
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance

SRC, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)
base = Image.open(SRC).convert("RGB")

# recortes 4:5 na foto original (1200x1600): (x0, y0, largura)
CROPS = {
    "cena":       (0,   100, 1200),   # sala inteira: descarbox, EPI, maca
    "atendimento": (170, 420, 900),   # piercer + cliente
    "piercer":    (300, 470, 500),    # rosto e mãos do profissional
}

def lum(a):
    return a[..., 0] * 0.299 + a[..., 1] * 0.587 + a[..., 2] * 0.114

def curve(x, contrast=1.35, pivot=0.5):
    x = np.clip((x - pivot) * contrast + pivot, 0, 1)
    return x * x * (3 - 2 * x) * 0.6 + x * 0.4  # leve curva em S

def gradient_map(l, stops):
    pos = np.array([s[0] for s in stops]); cols = np.array([s[1] for s in stops], dtype=float)
    out = np.zeros(l.shape + (3,))
    for c in range(3):
        out[..., c] = np.interp(l, pos, cols[:, c])
    return out

def vignette(h, w, strength=0.75):
    y, x = np.ogrid[:h, :w]
    d = np.sqrt(((x - w / 2) / (w / 2)) ** 2 + ((y - h * 0.42) / (h / 2)) ** 2)
    return np.clip(1 - strength * np.clip(d - 0.35, 0, None) ** 1.6, 0, 1)

def grain(h, w, amount=9, seed=7):
    rng = np.random.default_rng(seed)
    g = rng.normal(0, amount, (h, w))
    return np.repeat(g[..., None], 3, axis=2)

SANGUE = [(0.00, (5, 2, 2)), (0.30, (38, 3, 4)), (0.58, (122, 6, 12)),
          (0.80, (190, 24, 30)), (1.00, (248, 228, 222))]

def tratar(img, modo):
    img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=70, threshold=2))
    a = np.asarray(img).astype(float) / 255
    l = curve(lum(a), contrast=1.45 if modo == "sangue" else 1.6, pivot=0.55)
    h, w = l.shape
    if modo == "sangue":
        rgb = gradient_map(l, SANGUE)
    else:  # noir: P&B duro com luz vermelha vindo da direita
        g = l[..., None] * 255
        rgb = np.concatenate([g, g, g], axis=2)
        x = np.linspace(0, 1, w)[None, :]
        luz = np.clip((x - 0.35) / 0.65, 0, 1) ** 1.4 * (1 - l) * 0.85
        rgb = rgb * (1 - luz[..., None]) + np.array([150, 8, 14]) * luz[..., None]
    rgb = rgb * vignette(h, w)[..., None]
    rgb = rgb + grain(h, w)
    return Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8))

for nome, (x0, y0, cw) in CROPS.items():
    ch = int(cw * 5 / 4)
    crop = base.crop((x0, y0, x0 + cw, y0 + ch)).resize((1080, 1350), Image.LANCZOS)
    for modo in ("sangue", "noir"):
        out = tratar(crop, modo)
        p = os.path.join(OUT, f"{nome}-{modo}.jpg")
        out.save(p, quality=92)
        print(p, out.size)
