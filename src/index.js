export default {
  async queue(batch, env) {
    try {
      for (const message of batch.messages) {
        try {
          // Validar mensagem antes de processar
          if (!message || !message.body) {
            console.error('Mensagem inválida:', message);
            continue;
          }

          await processWhatsappMessage(message.body, env);
          message.ack();
        } catch (error) {
          console.error('Erro no processamento da mensagem:', error);
          message.retry();
        }
      }
    } catch (batchError) {
      console.error('Erro no processamento do lote:', batchError);
    }
  },

  async fetch(request, env) {
    try {
      if (request.method !== 'POST') {
        return new Response('Método não permitido', { status: 405 });
      }

      const messageBody = await request.json();
      
      // Validação adicional dos dados
      if (!isValidMessage(messageBody)) {
        return new Response('Dados inválidos', { status: 400 });
      }

      await env.WHATSAPP_QUEUE.send(messageBody);
      return new Response('Mensagem enfileirada', { status: 200 });
    } catch (error) {
      console.error('Erro no processamento da requisição:', error);
      return new Response('Erro interno', { status: 500 });
    }
  }
};

function isValidMessage(message) {
  // Implementar validação específica para sua estrutura de mensagem
  return message && 
         typeof message === 'object' && 
         message.phone && 
         message.text;
}

async function processWhatsappMessage(message, env) {
  try {
    console.log('Processando mensagem:', message);
    // Lógica de processamento da mensagem
  } catch (error) {
    console.error('Erro no processamento da mensagem:', error);
    throw error;
  }
}
