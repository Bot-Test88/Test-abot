import os
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# বট কনফিগারেশন
TOKEN = os.getenv('TELEGRAM_TOKEN')
API_URL = "https://api16-normal-c-useast1a.tiktokv.com/aweme/v1/feed/"

# স্টার্ট কমান্ড হ্যান্ডলার
def start(update: Update, context: CallbackContext):
    update.message.reply_text("🎬 TikTok Downloader Bot!\n\nযেকোনো TikTok ভিডিওর লিংক পাঠান, আমি ডাউনলোড করে দেব!")

# লিংক হ্যান্ডলার
def handle_link(update: Update, context: CallbackContext):
    try:
        url = update.message.text
        if 'tiktok.com' not in url:
            update.message.reply_text("⚠️ দয়া করে একটি বৈধ TikTok লিংক পাঠান")
            return

        video_id = url.split('/video/')[1].split('?')[0]
        response = requests.get(f"{API_URL}?aweme_id={video_id}").json()
        
        if 'aweme_list' not in response:
            update.message.reply_text("❌ ভিডিও ডাউনলোড করতে সমস্যা হয়েছে")
            return

        video_data = response['aweme_list'][0]
        video_url = video_data['video']['play_addr']['url_list'][0]
        caption = f"📹 {video_data['desc']}\n\n⚡ @YourBotName"
        
        update.message.reply_video(
            video=video_url,
            caption=caption,
            supports_streaming=True
        )
    except Exception as e:
        update.message.reply_text(f"🚫 Error: {str(e)}")

# মেইন ফাংশন
def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_link))
    
    # Render/Heroku কম্প্যাটিবল
    PORT = int(os.environ.get('PORT', 5000))
    updater.start_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TOKEN,
        webhook_url=f"https://your-app-name.onrender.com/{TOKEN}"
    )
    updater.idle()

if __name__ == '__main__':
    main()
