"""Destellos de lente de Idchel: núcleo blanco y rayos cobre/oro rosado, visibles sobre crema y sobre oscuro."""
import pathlib
import numpy as np
from PIL import Image

A = pathlib.Path(__file__).resolve().parent.parent / 'assets'
BLANCO = np.array([1, 1, 1.])
COBRE = np.array([.86, .46, .18])
ORO_ROSA = np.array([.90, .52, .54])
CHAMP = np.array([1, .86, .62])


def rejilla(n):
    c = (n - 1) / 2
    y, x = np.mgrid[0:n, 0:n]
    return (x - c) * 512 / n, (y - c) * 512 / n


def rayo(u, v, ancho, largo):
    return np.exp(-(v / ancho) ** 2) * np.exp(-np.abs(u) / largo)


def guarda(rgb, nombre, n):
    rgb = 1 - np.exp(-rgb * 1.5)
    borde = np.clip((256 - np.hypot(*rejilla(n))) / 44, 0, 1)
    rgb *= (borde * borde * (3 - 2 * borde))[..., None]
    al = rgb.max(2)
    col = rgb / np.maximum(al[..., None], .004)
    im = np.dstack([col, al])
    Image.fromarray((im.clip(0, 1) * 255 + .5).astype('uint8'), 'RGBA').save(A / (nombre + '.webp'), lossless=False, quality=88, alpha_quality=95, method=6)


n = 420
x, y = rejilla(n)
r = np.hypot(x, y)
u, v = (x + y) / np.sqrt(2), (x - y) / np.sqrt(2)
rgb = (np.exp(-(r / 6.5) ** 2) * 3.2)[..., None] * BLANCO
rgb += (np.exp(-r / 15) * .75)[..., None] * CHAMP
rgb += (np.exp(-r / 48) * .2)[..., None] * ORO_ROSA
rgb += (rayo(x, y, 1.35, 96) * 1.3)[..., None] * COBRE
rgb += (rayo(x, y, 5.5, 62) * .12)[..., None] * ORO_ROSA
rgb += (rayo(y, x, 1.1, 40) * 1.05)[..., None] * COBRE
rgb += (rayo(u, v, .85, 16) * .42)[..., None] * CHAMP
rgb += (rayo(v, u, .85, 16) * .42)[..., None] * CHAMP
rgb += (np.exp(-((r - 74) / 3.2) ** 2) * .03)[..., None] * ORO_ROSA
guarda(rgb, 'flare', n)

n = 150
x, y = rejilla(n)
r = np.hypot(x, y)
u, v = (x + y) / np.sqrt(2), (x - y) / np.sqrt(2)
rgb = (np.exp(-(r / 17) ** 2) * 3)[..., None] * BLANCO
rgb += (np.exp(-r / 42) * .45)[..., None] * CHAMP
rgb += (rayo(x, y, 3.4, 62) * 1.3)[..., None] * COBRE
rgb += (rayo(y, x, 3.4, 62) * 1.3)[..., None] * COBRE
rgb += (rayo(u, v, 2.2, 24) * .4)[..., None] * CHAMP
rgb += (rayo(v, u, 2.2, 24) * .4)[..., None] * CHAMP
guarda(rgb, 'flare-mini', n)

# Aguja: rama real de línea dorada, recoloreada a oro rosado con la base arriba
r_ = Image.open('C:/Users/aleja/boda-francisco-y-fernanda/public/ornaments/branch-gold.png').convert('RGBA')
a = np.asarray(r_).astype(float) / 255
al = np.clip((a[..., 3] - .32) / .5, 0, 1)
lum = a[..., :3].mean(2)
lum = np.clip((lum - lum[al > .5].min()) / max(np.ptp(lum[al > .5]), .01), 0, 1)[..., None]
col = np.array([.48, .24, .17]) * (1 - lum) + np.array([.96, .76, .62]) * lum
sal = Image.fromarray((np.dstack([col, al]) * 255 + .5).astype('uint8'), 'RGBA').rotate(180)
sal = sal.crop(sal.getbbox())
sal.thumbnail((132, 220), Image.LANCZOS)
sal.save(A / 'rama-aguja.webp', quality=90, alpha_quality=95, method=6)
print(sal.size)
