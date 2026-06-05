import telebot
import os
from openai import OpenAI

# 从环境变量读取配置
BOT_TOKEN = os.environ.get('BOT_TOKEN')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

bot = telebot.TeleBot(BOT_TOKEN)
client = OpenAI(api_key=OPENAI_API_KEY)

# --- 你的专业术语库/人设规则 ---
SYSTEM_PROMPT = """你是一位专业的中柬翻译官，精通建筑、人力劳务和贸易领域。
请遵循以下规则：
1. 保持用词专业、地道，符合柬埔寨本地商务习惯。
2. 遇到“打款”、“人力”、“建筑材料”等词汇，请使用精准的行业用语。
3. 如果用户输入的中文包含歧义，请根据贸易上下文进行逻辑修正后再翻译。"""

# 简单的权限检查
def is_authorized(user_id):
    allowed_ids = [5615210204]
    return user_id in allowed_ids

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "老井翻译官已就绪，请输入中文，我将为你进行专业中柬互译。")

@bot.message_handler(func=lambda message: True)
def translate(message):
    if not is_authorized(message.from_user.id):
        bot.reply_to(message, "您尚未开通权限，请联系老井。")
        return
    
    try:
        # 调用 OpenAI 进行智能翻译
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"请将以下内容翻译成柬埔寨语: {message.text}"}
            ]
        )
        # 将 AI 翻译的结果发回给 Telegram
        bot.reply_to(message, response.choices[0].message.content)
    except Exception as e:
        bot.reply_to(message, "翻译服务处理中，请稍后。")

bot.infinity_polling()
