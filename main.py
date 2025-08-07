import os
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# imghdr ফিক্স (Python 3.13+ এর জন্য)
try:
    import imghdr
except ImportError:
    from PIL import Image
    def imghdr_what(file):
        try:
            Image.open(file)
            return 'image'
        except:
            return None
    import sys
    sys.modules['imghdr'] = type(sys)('imghdr')
    sys.modules['imghdr'].what = imghdr_what

# কনফিগারেশন
TOKEN = os.getenv('TELEGRAM_TOKEN')
API_URL = "https://api16-normal-c-useast1a.tiktokv.com/aweme/v1/feed/"

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "🎬 TikTok Downloader Bot\n\n"
        "যেকোনো TikTok ভিডিওর লিংক পাঠান, আমি ডাউনলোড করে দেব!\n\n"
        "উদাহরণ:\n"
        "https://www.tiktok.com/@username/video/123456789"
    )

def handle_link(update: Update, context: CallbackContext):
    try:
        url = update.message.text
        
        if 'tiktok.com' not in url:
            update.message.reply_text("⚠️ দয়া করে একটি বৈধ TikTok লিংক পাঠান")
            return

        # ভিডিও আইডি এক্সট্রাক্ট
        if '/video/' in url:
            video_id = url.split('/video/')[1].split('?')[0]
        else:
            update.message.reply_text("❌ লিংক ফরম্যাট সঠিক নয়")
            return

        # API থেকে ডেটা ফেচ করা
        response = requests.get(f"{API_URL}?aweme_id={video_id}", timeout=10).json()
        
        if not response.get('aweme_list'):
            update.message.reply_text("❌ ভিডিও ডাউনলোড করতে সমস্যা হয়েছে")
            return

        video_data = response['aweme_list'][0]
        video_url = video_data['video']['play_addr']['url_list'][0]
        caption = f"📹 {video_data.get('desc', '')}\n\n⚡ @{update.message.from_user.username}"

        # ভিডিও সেন্ড করা
        update.message.reply_video(
            video=video_url,
            caption=caption[:1000],  # টেলিগ্রাম ক্যাপশন লিমিট
            supports_streaming=True,
            timeout=100
        )

    except requests.Timeout:
        update.message.reply_text("⌛ রিকোয়েস্ট টাইমআউট হয়েছে, আবার চেষ্টা করুন")
    except Exception as e:
        update.message.reply_text(f"🚫 ত্রুটি: {str(e)}")

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
    print("🤖 বট সফলভাবে চালু হয়েছে!")
    updater.idle()

if __name__ == '__main__':
    main()        )
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
