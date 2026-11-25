import os
import random
import string
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from supabase import create_client, Client

# جلب المفاتيح من إعدادات الاستضافة (آمن)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def generate_code():
    characters = string.ascii_letters + string.digits + "$#!@%^&*"
    return ''.join(random.choice(characters) for i in range(15))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("🎁 احصل على كودك المجاني", callback_data='get_code')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "أهلاً بك في بوت Zain Academy!\n\nاضغط على الزر أدناه للحصول على كود تفعيل الباقة المجانية.",
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'get_code':
        user_id = query.from_user.id
        await query.edit_message_text(text="⏳ جاري توليد الكود الخاص بك...")
        try:
            new_code = generate_code()
            data = {"code": new_code, "plan_type": "free", "telegram_id": user_id}
            supabase.table('codes').insert(data).execute()
            await query.edit_message_text(
                f"✅ تم توليد كودك بنجاح!\n\n🔑 الكود الخاص بك:\n`{new_code}`\n\n⚠️ انسخ الكود الآن واذهب للمنصة لتفعيل حسابك.",
                parse_mode='Markdown'
            )
        except Exception as e:
            await query.edit_message_text(text=f"❌ حدث خطأ: {str(e)}")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("البوت شغال...")
    app.run_polling()

if __name__ == '__main__':
    main()
