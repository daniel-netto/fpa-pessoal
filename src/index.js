export default {
  async queue(batch, env) {
    for (let message of batch.messages) {
      try {
        // Processar mensagem da fila
        await processWhatsappMessage(message.body, env);
        message.ack();
      } catch (error) {
        message.retry(error);
      }
    }
  },

  async fetch(request, env) {
    if (request.method === 'POST') {
      const messageBody = await request.json();
      await env.WHATSAPP_QUEUE.send(messageBody);
      return new Response('Mensagem enfileirada', { status: 200 });
    }
    return new Response('Método não permitido', { status: 405 });
  }
};

async function processWhatsappMessage(message, env) {
  // Lógica de processamento
  console.log('Processando mensagem:', message);
}
