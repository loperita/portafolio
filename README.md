# Portafolio — Pablo Moreno

Sitio web personal de **Pablo Moreno**, desarrollador freelance **Fullstack & Mobile**.

🔗 **En vivo:** https://loperita.github.io/portafolio/ · versión en inglés: https://loperita.github.io/portafolio/en/

Página única (HTML/CSS/JS embebidos; imágenes en `img/` y fuente Syne en `fonts/`, sin dependencias externas): retrato con recorte de fondo, tema claro/oscuro, animaciones al hacer scroll y modales de caso con galería.

## Stack
React · Angular · JavaScript · Node.js · Express · Spring Boot · Python · SQL · Flutter · Firebase

## Contacto
- Email: pablomoreno44@gmail.com
- LinkedIn: https://www.linkedin.com/in/pablo-moreno-develop/
- GitHub: https://github.com/loperita

## Configuración rápida
Al inicio de `index.html` está el bloque `SITE_CONFIG`:
- `whatsapp`: número con indicativo, solo dígitos (ej. `573001234567`). Activa el botón flotante y el de contacto.
- `booking`: enlace de Cal.com o Calendly. Activa el botón "Agendar llamada gratis".
- `posthogKey`: clave pública de PostHog (`phc_...`). Activa la analítica y el registro de clics en botones clave.

Si un valor está vacío, su botón o función queda oculto.

La versión en inglés (`en/index.html`) tiene su propio bloque `SITE_CONFIG` y el mismo diseño: si cambias un valor o un estilo, cámbialo en los dos archivos.

## Precios en USD (versión en inglés)
Los precios base están en COP (atributo `data-cop`). Todos los días a las 00:00 hora Colombia, la tarea `.github/workflows/actualizar-precios.yml` consulta la TRM oficial (datos.gov.co), recalcula los USD en `en/index.html` y en `pdf/one-pager-en.html`, y si cambian regenera `Pablo-Moreno-Portfolio-EN.pdf`. Se puede correr a mano desde la pestaña **Actions** → *Actualizar precios (TRM)* → *Run workflow*.

Como esa tarea hace commits en `main`, haz `git pull` antes de editar.

## PDF del perfil
- Español: `Pablo-Moreno-Portafolio.pdf`, generado desde `pdf/one-pager-es.html`.
- Inglés: `Pablo-Moreno-Portfolio-EN.pdf`, generado desde `pdf/one-pager-en.html` (los precios los actualiza la tarea diaria).

Para regenerarlos: abrir el HTML en Chrome → Imprimir → Guardar como PDF, A4, sin márgenes ni encabezados.
