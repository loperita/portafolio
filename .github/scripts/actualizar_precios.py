"""Actualiza los precios en USD de la versión en inglés con la TRM oficial del día.

Fuente: Superintendencia Financiera, publicada en datos.gov.co (dataset 32sa-8pi3).
Los precios base están en COP en el atributo data-cop; aquí solo se recalcula el valor en USD
(redondeado a múltiplos de 5) y la nota con la tasa usada.

Uso (desde la raíz del repo):  python3 .github/scripts/actualizar_precios.py
Si la consulta falla, no toca ningún archivo y termina con error (GitHub avisa por correo).
"""
import datetime as dt
import json
import math
import os
import re
import sys
import urllib.parse
import urllib.request

ARCHIVOS = ["en/index.html", "pdf/one-pager-en.html"]
MESES = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

# Fecha de hoy en Colombia (UTC-5, sin horario de verano)
hoy = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=5)).date()

query = urllib.parse.urlencode({
    "$where": f"vigenciadesde <= '{hoy.isoformat()}T00:00:00'",
    "$order": "vigenciadesde DESC",
    "$limit": "1",
})
url = "https://www.datos.gov.co/resource/32sa-8pi3.json?" + query
req = urllib.request.Request(url, headers={"User-Agent": "portfolio-price-updater"})
try:
    with urllib.request.urlopen(req, timeout=30) as r:
        fila = json.load(r)[0]
    trm = float(fila["valor"])
    vigente = dt.date.fromisoformat(fila["vigenciadesde"][:10])
except Exception as e:  # noqa: BLE001
    sys.exit(f"No se pudo consultar la TRM: {e}")

if not 1000 < trm < 10000:
    sys.exit(f"TRM fuera de rango, no se actualiza: {trm}")


def usd(cop):
    return int(math.floor(cop / trm / 5 + 0.5) * 5)


nota = f"COP {trm:,.2f} per USD on {MESES[vigente.month - 1]} {vigente.day}, {vigente.year}"
precios_cambiaron = False

for ruta in ARCHIVOS:
    with open(ruta, encoding="utf-8", newline="") as f:
        html = f.read()

    def poner_precio(m):
        return f'{m.group(1)}USD&nbsp;{usd(int(m.group(2))):,}<'

    nuevo, n = re.subn(r'(data-cop="(\d+)"[^>]*>)USD&nbsp;[\d,]+<', poner_precio, html)
    if n == 0:
        sys.exit(f"{ruta}: no encontré precios con data-cop")
    if nuevo != html:
        precios_cambiaron = True
    nuevo = re.sub(r"(<span data-trm>)[^<]*(</span>)", rf"\g<1>{nota}\g<2>", nuevo)

    if nuevo != html:
        with open(ruta, "w", encoding="utf-8", newline="") as f:
            f.write(nuevo)

print(f"TRM {trm} (vigente {vigente}); precios cambiaron: {precios_cambiaron}")
salida = os.environ.get("GITHUB_OUTPUT")
if salida:
    with open(salida, "a", encoding="utf-8") as f:
        f.write(f"prices_changed={'true' if precios_cambiaron else 'false'}\n")
        f.write(f"fecha={vigente.isoformat()}\n")
