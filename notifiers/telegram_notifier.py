from telegram import Bot

class TelegramNotifier:
    def __init__(self, bot_token, chat_id):
        """
        Inicializa el objeto TelegramNotifier.
        
        :param bot_token: Token del bot proporcionado por BotFather.
        :param chat_id: ID del chat al que se enviarán los mensajes.
        """
        self.bot = Bot(token=bot_token)
        self.chat_id = chat_id

    async def send_message(self, message):
        """
        Envía un mensaje al chat de Telegram.

        :param message: Texto del mensaje a enviar.
        """
        try:
            await self.bot.send_message(chat_id=self.chat_id, text=message)
            print("Mensaje enviado correctamente.")
        except Exception as e:
            print(f"Error al enviar el mensaje: {e}")
