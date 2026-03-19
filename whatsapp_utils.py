import os
import httpx
import logging

logger = logging.getLogger(__name__)


async def enviar_mensagem_whatsapp(telefone_destino: str, texto_resposta: str):
    token = os.getenv("WHATSAPP_TOKEN")

    phone_number_id = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
    url = f"https://graph.facebook.com/v18.0/{phone_number_id}/messages"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": telefone_destino,
        "type": "text",
        "text": {"body": texto_resposta}
    }

    async with httpx.AsyncClient() as client:
        try:
            resposta = await client.post(url, headers=headers, json=payload)
            resposta.raise_for_status()
            logger.info(f"Mensagem enviada com sucesso para {telefone_destino}")
        except httpx.HTTPStatusError as e:
            logger.error(f"Erro ao enviar WhatsApp: {e.response.text}")