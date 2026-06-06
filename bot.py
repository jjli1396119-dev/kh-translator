import telebot
import os
import threading
from flask import Flask
from openai import OpenAI

# 初始化
BOT_TOKEN = os.environ.get('BOT_TOKEN')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
bot = telebot.TeleBot(BOT_TOKEN)
client = OpenAI(api_key=OPENAI_API_KEY)
app = Flask(__name__)

# 虚拟网页服务：让 Render 以为这是个网页，就不会强制关掉你了
@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    # Render 会通过环境变量 PORT 告诉程序监听哪个端口
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# 翻译逻辑
SYSTEM_PROMPT = """你是一位精通中柬翻译的专业助手，专注建筑、贸易、人力劳务领域。"""

@bot.message_handler(func=lambda message: True)
def translate(message):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"将以下内容翻译成柬埔寨语: {message.text}"}
            ]
        )
        bot.reply_to(message, response.choices[0].message.content)
    except Exception as e:
        bot.reply_to(message, "服务处理中...")

# 同时启动 Flask 网页和机器人
if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    bot.infinity_polling(none_stop=True, skip_pending=True)
