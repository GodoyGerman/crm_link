# utils/pdf_generator.py

from xhtml2pdf import pisa

def generar_pdf(html: str, ruta_salida: str) -> bool:
    try:
        with open(ruta_salida, "w+b") as archivo:
            pisa_status = pisa.CreatePDF(html, dest=archivo)
        return not pisa_status.err
    except Exception as e:
        print("Error al generar PDF:", e)
        return False
