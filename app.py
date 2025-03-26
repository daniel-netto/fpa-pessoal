import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

VERIFY_TOKEN = os.environ.get("SEU_TOKEN_VERIFICACAO")
WHATSAPP_TOKEN = os.environ.get(WHATSAPP_ACCESS_TOKEN)

WHATSAPP_API_URL = "https://graph.facebook.com/v22.0/me/messages"

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        if token == VERIFY_TOKEN:
            return challenge, 200
        return "Token inválido", 403

    elif request.method == 'POST':
        data = request.json
        print("Mensagem recebida:", data)

        # Processar mensagens do WhatsApp
        if "messages" in data["entry"][0]["changes"][0]["value"]:
            for message in data["entry"][0]["changes"][0]["value"]["messages"]:
                sender_id = message["from"]
                text = message["text"]["body"]

                # Responder automaticamente
                send_whatsapp_message(sender_id, f"Você disse: {text}")

        return jsonify({"status": "mensagem recebida"}), 200

def send_whatsapp_message(to, text):
    """ Envia mensagem via WhatsApp Cloud API """
    headers = {
        "Authorization": f"Bearer {WHATSAPP_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": to,
        "type": "text",
        "text": {"body": text}
    }
    response = requests.post(WHATSAPP_API_URL, headers=headers, json=data)
    print("Resposta do WhatsApp:", response.json())

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)


def webhook_handler(request):
    # URL do Worker Cloudflare (será gerada após deploy)
    CLOUDFLARE_WORKER_URL = os.getenv('CLOUDFLARE_WORKER_URL')
    
    message_data = request.json()
    
    # Enviar mensagem para fila do Cloudflare
    response = requests.post(
        CLOUDFLARE_WORKER_URL, 
        json=message_data,
        headers={'Content-Type': 'application/json'}
    )
    
    return {'status': 'success'}
