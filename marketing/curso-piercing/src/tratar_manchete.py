"""Tratamento de foto de notícia para capa: P&B duro, grão e vinheta.

Neutro de propósito: sem tinta vermelha no rosto de candidato (o vermelho fica só na tipografia).
Uso: python3 -I tratar_manchete.py <entrada.jpg> <saida.jpg>
"""
import sys
import numpy as np
from PIL import Image, ImageFilter

src, out = sys.argv[1], sys.argv[2]
img = Image.open(src).convert("RGB").filter(ImageFilter.UnsharpMask(radius=2, percent=60, threshold=2))
a = np.asarray(img).astype(float) / 255
l = a[..., 0] * 0.299 + a[..., 1] * 0.587 + a[..., 2] * 0.114
l = np.clip((l - 0.52) * 1.5 + 0.52, 0, 1)
l = l * l * (3 - 2 * l) * 0.55 + l * 0.45
h, w = l.shape
y, x = np.ogrid[:h, :w]
d = np.sqrt(((x - w * 0.53) / (w / 2)) ** 2 + ((y - h * 0.4) / (h / 2)) ** 2)
l = l * np.clip(1 - 0.7 * np.clip(d - 0.45, 0, None) ** 1.5, 0, 1)
g = l * 255 + np.random.default_rng(11).normal(0, 8, (h, w))
rgb = np.repeat(np.clip(g, 0, 255)[..., None], 3, axis=2)
rgb[..., 0] = np.clip(rgb[..., 0] * 1.03 + 2, 0, 255)  # preto levemente quente, igual ao fundo das capas
Image.fromarray(rgb.astype(np.uint8)).save(out, quality=92)
print(out, (w, h))
