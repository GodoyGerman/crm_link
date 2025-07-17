import aiosmtplib
from email.message import EmailMessage

async def enviar_cotizacion_por_correo(
    destinatario: str,
    contenido_pdf: bytes,
    nombre_pdf: str,
    asunto: str = "Cotización Link Soluciones",
    cuerpo: str = (
    "Gracias por confiar en nosotros. Te enviamos adjunta la cotización con el detalle de los servicios solicitados."
    "Si tienes alguna pregunta o necesitas ajustar algo, no dudes en responder a este correo."
    "Saludos cordiales,\n"
    "Link Soluciones Colombia S.A.S  "
    "Tu solución a un solo click"
)
):
    # Configura el email
    mensaje = EmailMessage()
    mensaje["From"] = "linksolucionco@gmail.com"  # Cambia por tu email real o el del remitente
    mensaje["To"] = destinatario
    mensaje["Subject"] = asunto
    mensaje.set_content(cuerpo)

    # Adjuntar PDF
    mensaje.add_attachment(
        contenido_pdf,
        maintype="application",
        subtype="pdf",
        filename=nombre_pdf,
    )

    # Configuración SMTP (Ejemplo con Gmail SMTP)
    smtp_host = "smtp.gmail.com"
    smtp_port = 587
    usuario = "linksolucionco@gmail.com"       # Cambia aquí
    contrasena = "cxoq finn gqfi wzvz"       # Usa contraseña de aplicación o token OAuth

    await aiosmtplib.send(
        mensaje,
        hostname=smtp_host,
        port=smtp_port,
        start_tls=True,
        username=usuario,
        password=contrasena,
    )
