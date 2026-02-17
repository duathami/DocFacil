from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.responses import StreamingResponse, HTMLResponse, FileResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.core.processor import process_and_convert_to_pdf
import io
import os

app = FastAPI(title="DocFácil - O Scanner do MEI")

# Configurações de Pastas Estáticas e Templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Renderiza a página inicial do conversor."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/privacidade", response_class=HTMLResponse)
async def privacidade(request: Request):
    """Renderiza a página de Políticas de Privacidade."""
    return templates.TemplateResponse("privacidade.html", {"request": request})


@app.get("/termos", response_class=HTMLResponse)
async def termos(request: Request):
    return templates.TemplateResponse("termos.html", {"request": request})


@app.get("/ajuda", response_class=HTMLResponse)
async def ajuda(request: Request):
    return templates.TemplateResponse("ajuda.html", {"request": request})


@app.get("/ads.txt")
async def get_ads_txt():
    # Tenta encontrar o arquivo na raiz ou na pasta app
    paths_to_check = ["ads.txt", "app/ads.txt", "../ads.txt"]
    
    for path in paths_to_check:
        if os.path.exists(path):
            return FileResponse(path)
    
    # Se não encontrar o arquivo físico, ele retorna o texto direto (Truque de mestre)
    content = "google.com, pub-4988918194052295, DIRECT, f08c47fec0942fa0"
    return PlainTextResponse(content=content)


@app.post("/convert")
async def convert_images(files: list[UploadFile] = File(...)):
    """
    Recebe as fotos, processa em memória e devolve o PDF para download imediato.
    """
    image_bytes_list = []

    for file in files:
        # Lendo o conteúdo do arquivo enviado para a memória
        content = await file.read()
        image_bytes_list.append(content)

    # Chamando o nosso "Cérebro" de processamento
    pdf_result = process_and_convert_to_pdf(image_bytes_list)

    # Criando um stream para download (sem salvar no HD do servidor)
    return StreamingResponse(
        io.BytesIO(pdf_result),
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=documento_docfacil.pdf"}
    )