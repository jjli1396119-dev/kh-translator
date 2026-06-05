```python
import telebot
import os

# 从环境变量读取 Token，更加安全
BOT_TOKEN = os.environ.get('BOT_TOKEN', '8979204824:AAF2i0-BnBalcqbpgWoVRX_AVQ9LD9B-eRE')
bot = telebot.TeleBot(BOT_TOKEN)

# 简单的权限检查（Whitelist）
def is_authorized(user_id):
    # 这里定义允许使用机器人的ID，例如你可以填入你自己的ID
    allowed_ids = [5615210204] 
    return user_id in allowed_ids

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "老井中柬通已就绪，请输入中文进行翻译。")

@bot.message_handler(func=lambda message: True)
def translate(message):
    if not is_authorized(message.from_user.id):
        bot.reply_to(message, "您尚未开通权限，请联系老井。")
        return
    
    # 你的核心翻译逻辑可以在这里扩展
    bot.reply_to(message, f"收到你的指令: {message.text}")

bot.infinity_polling()
