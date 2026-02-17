import io
from PIL import Image, ImageEnhance, ImageOps
import img2pdf

def process_and_convert_to_pdf(image_list):
    """
    Recebe uma lista de arquivos (bytes), limpa as imagens 
    e retorna um único PDF em memória.
    """
    processed_images = []

    for img_bytes in image_list:
        # 1. Carregar a imagem da memória
        img = Image.open(io.BytesIO(img_bytes))
        
        # 2. Converter para Grayscale (Preto e Branco) - Opcional, mas economiza espaço
        # Se preferir colorido, comente a linha abaixo
        img = ImageOps.grayscale(img)

        # 3. Efeito "Scanner": Aumentar o Contraste
        # O fator 1.5 a 2.0 costuma "estourar" o fundo branco e destacar as letras
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(2.0)

        # 4. Ajuste de Brilho (para remover sombras leves)
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(1.2)

        # 5. Salvar a imagem processada em um buffer temporário (formato JPEG otimizado)
        img_buffer = io.BytesIO()
        # Convertemos para RGB se estiver em Grayscale para garantir compatibilidade
        if img.mode != 'RGB':
            img = img.convert('RGB')
            
        img.save(img_buffer, format="JPEG", quality=85) # Quality 85 é o "sweet spot" de SEO/Performance
        processed_images.append(img_buffer.getvalue())

    # 6. Converter todas as imagens em um único PDF usando img2pdf (extremamente rápido)
    pdf_bytes = img2pdf.convert(processed_images)
    
    return pdf_bytes