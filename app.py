from flask import Flask, request, jsonify

app = Flask(__name__)

# Rota para o webhook do WhatsApp
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        # Verificação inicial do webhook no Meta for Developers
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        if token == "SEU_TOKEN_VERIFICACAO":
            return challenge
        return "Token inválido", 403

    elif request.method == 'POST':
        data = request.json
        print("Mensagem recebida:", data)
        return jsonify({"status": "mensagem recebida"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
