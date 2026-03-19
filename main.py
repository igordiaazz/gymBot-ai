import os
from fastapi import FastAPI, Depends, Request, HTTPException, Query, Response
from sqlalchemy.orm import Session
import logging

import models
from database import engine, get_db
from ai_agent import gerar_resposta_ia
from whatsapp_utils import enviar_mensagem_whatsapp


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/webhook")
async def verifica_webhook(
        hub_mode: str = Query(None, alias="hub.mode"),
        hub_challenge: str = Query(None, alias="hub.challenge"),
        hub_verify_token: str = Query(None, alias="hub.verify_token")
):
    MEU_TOKEN_SECRETO = os.getenv("WEBHOOK_VERIFY_TOKEN")

    if hub_mode == "subscribe" and hub_verify_token == MEU_TOKEN_SECRETO:
        logger.info("Webhook verificado com sucesso pela Meta!")
        return Response(content=hub_challenge, media_type="text/plain")

    raise HTTPException(status_code=403, detail="Token de verificação inválido")


def extrair_mensagem_meta(dados: dict) -> tuple[str, str] | None:

    try:
        changes = dados["entry"][0]["changes"][0]["value"]


        if "messages" not in changes:
            return None

        mensagem_obj = changes["messages"][0]


        if mensagem_obj.get("type") != "text":
            logger.info(f"Tipo de mensagem não suportado: {mensagem_obj.get('type')}")
            return None

        telefone = mensagem_obj["from"]
        mensagem = mensagem_obj["text"]["body"]

        return telefone, mensagem

    except (KeyError, IndexError) as e:
        logger.error(f"Erro ao parsear payload da Meta: {e}")
        return None


@app.post("/webhook")
async def recebe_whatsapp(request: Request, db: Session = Depends(get_db)):
    try:
        dados = await request.json()

        resultado = extrair_mensagem_meta(dados)

        if resultado is None:

            return {"status": "ignorado"}

        telefone_cliente, mensagem_cliente = resultado

        aluno = db.query(models.Aluno).filter(models.Aluno.telefone == telefone_cliente).first()

        if not aluno:
            logger.warning(f"Número não cadastrado: {telefone_cliente}")
            return {"status": "ignorado", "motivo": "aluno_nao_encontrado"}

        aluno_dict = {
            "nome": aluno.nome,
            "objetivo": aluno.objetivo,
            "nivel_experiencia": aluno.nivel_experiencia.value,
            "mensalidade_ativa": aluno.mensalidade_ativa
        }

        try:
            resposta_gerada = gerar_resposta_ia(aluno_dict, mensagem_cliente)
        except Exception as e:
            logger.error(f"Erro no Gemini: {e}")
            resposta_gerada = "Desculpe, nosso sistema está passando por uma instabilidade. Logo retornaremos!"

        await enviar_mensagem_whatsapp(telefone_cliente, resposta_gerada)

        return {"status": "sucesso"}

    except Exception as e:
        logger.error(f"Erro interno no servidor: {e}")
        return {"status": "erro_processado"}