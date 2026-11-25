import random
import string
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from supabase import create_client, Client

# --- الإعدادات (مضافة مباشرة) ---
TELEGRAM_TOKEN = "9102799416:AAEV-YHYDA9DDDByFitRHK1BbBsvzXeOqSA"
SUPABASE_URL = "https://ophcgggfhaehmsszeqrv.supabase.co"
SUPABASE_KEY = "sb_secret_YY4hMkITpcegoIwjMuik4w_vmcYHBf1"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def generate_code():
    characters = string.ascii_letters + string.digits + "$#!@%^&*"
    return ''.join(random.choice(characters) for i in range(15))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("🎁 احصل على كودك المجاني", callback_data='get_code')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "أهلاً بك في بوت Zain Academy!\n\n"
        "هذا البوت مخصص لتوليد كودات الباقة المجانية فقط.\n"
        "اضغط على الزر أدناه للحصول على كودك.",
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
            
            # هنا نرسل البيانات للجدول. لاحظ أن الباقة دائماً "free"
            data = {
                "code": new_code,
                "plan_type": "free", # مجاني فقط
                "telegram_id": user_id
            }
            
            # محاولة الحفظ في قاعدة البيانات
            supabase.table('codes').insert(data).execute()
            
            await query.edit_message_text(
                f"✅ تم توليد كودك بنجاح!\n\n"
                f"🔑 الكود الخاص بك:\n`{new_code}`\n\n"
                f"⚠️ انسخ الكود الآن واذهب للمنصة لتفعيل حسابك.\n"
                f"ملاحظة: الكود يستخدم لمرة واحدة فقط.",
                parse_mode='Markdown'
            )
        except Exception as e:
            await query.edit_message_text(text=f"❌ حدث خطأ: الكود تعارض أو السيرفر مشغول. اضغط مرة ثانية.")

def run_bot():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("البوت شغال...")
    app.run_polling()
