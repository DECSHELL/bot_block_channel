from telegram.ext import Updater
from bot import *
from settings import *

# Setup bot handlers
updater = Updater(TELEGRAM_TOKEN)

dp = updater.dispatcher
dp = setup_dispatcher(dp)
# Run bot
if HEROKU_APP_NAME is None:  # pooling mode
    print("بدأ البوت يعمل بنجاح✅")
    updater.start_polling(allowed_updates=Update.ALL_TYPES)
    updater.idle()

else:  # webhook mode
    print(f"تشغيل الروبوت في وضع الرد التلقائي على الويب.  تأكد من أن عنوان url هذا صحيح: https://{HEROKU_APP_NAME}.herokuapp.com/")
    updater.start_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TELEGRAM_TOKEN,
        webhook_url=f"https://{HEROKU_APP_NAME}.herokuapp.com/{TELEGRAM_TOKEN}"
    )

    updater.start_polling(allowed_updates=Update.ALL_TYPES)
