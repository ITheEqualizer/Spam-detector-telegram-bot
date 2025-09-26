# Spam Detector Telegram Bot

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Telegram](https://img.shields.io/badge/Telegram-Bot-green)](https://core.telegram.org/bots)

## Overview / توصیف پروژه

### English
**Spam Detector Telegram Bot** is a Telegram bot that uses machine learning to detect spam messages in chats. It employs an SVM classifier trained on text data to predict if messages are spam or normal (ham). The bot monitors all incoming messages, flags potential spam with confidence >40%, notifies admins for review, and allows actions like deletion or confirmation. Admins can manually label messages to collect data for retraining the model.

The project includes a training script to build the ML model from a CSV dataset and the main bot script for real-time detection. It's designed for group chats where the bot must be an admin. Logging, data collection for retraining, and admin commands are key components.

#### Key Features
- **Real-time Spam Detection**: Analyzes every message using a pre-trained SVM model with TF-IDF vectorization.
- **Confidence-Based Flagging**: Flags messages with spam probability >40%, sends warnings to users, and alerts admins.
- **Admin Tools**: Commands to check messages (/check), label as spam/normal (/detect), and send collected data (/send_data).
- **Data Collection**: Saves labeled messages to 'spam_messages.csv' for retraining.
- **Logging**: Logs actions to 'bot.log' and forwards to a logs channel.
- **Button Interactions**: Inline buttons for admins to confirm or delete flagged messages.
- **Persian Support**: Messages and responses are in Persian, with basic multi-language capability.

#### Project Structure
Based on code analysis:
- `train.py`: Script to train the SVM model using 'data.csv' (columns: 'message', 'label'), saves 'model.pkl' and 'vectorizer.pkl'.
- `bot.py`: Main bot script handling Telegram interactions, spam detection, commands, and callbacks.
- `requirements.txt`: Should include needed packages.
- `data.csv`: Input dataset for training (not included; user-provided).
- `spam_messages.csv`: Generated file for collecting labeled messages.
- `model.pkl` & `vectorizer.pkl`: Generated model files after training.
- `bot.log`: Generated log file.
- `README.md`: This file.

The code is modular, with error handling for Telegram API calls. It uses environment variables for security (AUTH_TOKEN). Potential improvements: Add more datasets, handle non-text messages, or integrate retraining automation. No major bugs; accuracy check in training advises retraining if <90%.

#### Prerequisites / الزامات
- Python 3.8 or higher.
- Telegram Bot Token (from @BotFather).
- Dataset 'data.csv' for initial training (columns: 'message', 'label', where label is 'spam' or 'normal').
- Set the  environment variable AUTH_TOKEN with your bot token.
- Bot must be an admin in target groups/channels with delete message permissions.
- Placeholder IDs for LOGS_CHANNEL_ID and ADMINS_GROUP_ID (replace with actual IDs).

### فارسی
**ربات تشخیص اسپم تلگرام** یک ربات تلگرام است که با استفاده از یادگیری ماشین پیام‌های اسپم را در چت‌ها تشخیص می‌دهد. از طبقه‌بند SVM آموزش‌دیده روی داده‌های متنی برای پیش‌بینی اسپم یا عادی (هم) بودن پیام‌ها استفاده می‌کند. ربات تمام پیام‌های ورودی را نظارت می‌کند، پیام‌های احتمالی اسپم با اطمینان >۴۰% را علامت‌گذاری می‌کند، به ادمین‌ها برای بررسی اطلاع می‌دهد و اجازه اقدامات مانند حذف یا تایید را می‌دهد. ادمین‌ها می‌توانند پیام‌ها را به صورت دستی برچسب‌گذاری کنند تا داده برای بازآموزش مدل جمع‌آوری شود.

این پروژه شامل اسکریپتی برای آموزش مدل ML از فایل CSV و اسکریپت اصلی ربات برای تشخیص زمان واقعی است. برای چت‌های گروهی طراحی شده که ربات باید ادمین باشد. ثبت لاگ، جمع‌آوری داده برای بازآموزش و دستورات ادمین اجزای کلیدی هستند.

#### ویژگی‌های کلیدی
- **تشخیص اسپم زمان واقعی**: تحلیل هر پیام با مدل SVM از پیش آموزش‌دیده با وکتوریزاسیون TF-IDF.
- **علامت‌گذاری مبتنی بر اطمینان**: علامت‌گذاری پیام‌ها با احتمال اسپم >۴۰%، ارسال هشدار به کاربران و اطلاع به ادمین‌ها.
- **ابزارهای ادمین**: دستورات برای بررسی پیام (/check)، برچسب‌گذاری اسپم/عادی (/detect) و ارسال داده جمع‌آوری‌شده (/send_data).
- **جمع‌آوری داده**: ذخیره پیام‌های برچسب‌گذاری‌شده در 'spam_messages.csv' برای بازآموزش.
- **ثبت لاگ**: ثبت اقدامات در 'bot.log' و ارسال به کانال لاگ‌ها.
- **تعاملات دکمه**: دکمه‌های inline برای ادمین‌ها جهت تایید یا حذف پیام‌های علامت‌گذاری‌شده.
- **پشتیبانی فارسی**: پیام‌ها و پاسخ‌ها به فارسی، با قابلیت پایه چندزبانه.

#### ساختار پروژه
بر اساس تحلیل کد:
- `train.py`: اسکریپت آموزش مدل SVM با استفاده از 'data.csv' (ستون‌ها: 'message', 'label')، ذخیره 'model.pkl' و 'vectorizer.pkl'.
- `bot.py`: اسکریپت اصلی ربات برای مدیریت تعاملات تلگرام، تشخیص اسپم، دستورات و callbackها.
- `requirements.txt`: شامل چکیج های مورد نیاز.
- `data.csv`: داده ورودی برای آموزش (شامل نیست؛ توسط کاربر فراهم شود).
- `spam_messages.csv`: فایل تولیدشده برای جمع‌آوری پیام‌های برچسب‌گذاری‌شده.
- `model.pkl` و `vectorizer.pkl`: فایل‌های مدل تولیدشده پس از آموزش.
- `bot.log`: فایل لاگ تولیدشده.
- `README.md`: این فایل.

کد مدولار است، با مدیریت خطا برای فراخوانی‌های API تلگرام. از متغیرهای محیطی برای امنیت (AUTH_TOKEN) استفاده می‌کند. بهبودهای احتمالی: افزودن داده‌های بیشتر، مدیریت پیام‌های غیرمتنی یا اتوماسیون بازآموزش. هیچ باگ عمده‌ای؛ بررسی دقت در آموزش پیشنهاد بازآموزش اگر <۹۰% می‌دهد.

#### الزامات
- پایتون 3.8 یا بالاتر.
- توکن ربات تلگرام (از @BotFather).
- مجموعه داده 'data.csv' برای آموزش اولیه (ستون‌ها: 'message', 'label' که label 'spam' یا 'normal' است).
- تنظیم متغیر محیطی AUTH_TOKEN با توکن ربات.
- ربات باید ادمین در گروه‌ها/کانال‌های هدف با مجوز حذف پیام باشد.
- IDهای placeholder برای LOGS_CHANNEL_ID و ADMINS_GROUP_ID (با IDهای واقعی - جایگزین کنید).

## Installation / نصب

### English
1. **Clone the Repository** (or create files manually):
   ```
   git clone https://github.com/your-repo/Spam-detector-telegram-bot.git
   cd Spam-detector-telegram-bot
   ```

2. **Install Dependencies** (create requirements.txt if needed):
   ```
   pip install pandas scikit-learn joblib pyTelegramBotAPI
   ```

3. **Prepare Data**: Provide 'data.csv' with 'message' and 'label' columns.

4. **Train the Model**:
   ```
   python train.py
   ```
   - Checks accuracy; retrain with more data if <90%.

5. **Set Environment Variable**:
   ```
   export AUTH_TOKEN='your_bot_token_here'
   ```
   - Replace placeholders in bot.py for LOGS_CHANNEL_ID and ADMINS_GROUP_ID.

6. **Run the Bot**:
   ```
   python bot.py
   ```

Add the bot to your group as an admin with delete permissions.

### فارسی
1. **کلون کردن مخزن** (یا ایجاد فایل‌ها به صورت دستی):
   ```
   git clone https://github.com/your-repo/Spam-detector-telegram-bot.git
   cd Spam-detector-telegram-bot
   ```

2. **نصب وابستگی‌ها** (در صورت نیاز requirements.txt ایجاد کنید):
   ```
   pip install pandas scikit-learn joblib pyTelegramBotAPI
   ```

3. **آماده‌سازی داده**: 'data.csv' با ستون‌های 'message' و 'label' فراهم کنید.

4. **آموزش مدل**:
   ```
   python train.py
   ```
   - دقت را بررسی می‌کند؛ اگر <۹۰% با داده بیشتر بازآموزش دهید.

5. **تنظیم متغیر محیطی**:
   ```
   export AUTH_TOKEN='توکن_ربات_شما_اینجا'
   ```
   - placeholderها در bot.py برای LOGS_CHANNEL_ID و ADMINS_GROUP_ID جایگزین کنید.

6. **اجرای ربات**:
   ```
   python bot.py
   ```

ربات را به گروه خود به عنوان ادمین با مجوز حذف اضافه کنید.

## Usage / استفاده

### English
- **Add to Group**: Invite the bot, make it an admin with delete rights.
- **Commands** (admin-only):
  - `/detect`: Reply to message, choose spam/normal via buttons; saves to CSV.
  - `/send_data`: Sends 'spam_messages.csv' document.
  - `/check`: Reply to message; shows spam probability.
- **Automatic Detection**: Scans all messages; if spam >40%, warns user, notifies admins group with buttons to delete or confirm (👍 reaction).
- **Callbacks**: Admins click buttons to handle flags; logs to channel.
- **Retraining**: Use collected 'spam_messages.csv' as new data.csv, rerun train.py.

Monitor 'bot.log' for errors. Customize ad links/messages in code.

### فارسی
- **اضافه کردن به گروه**: ربات را دعوت کنید، ادمین با حقوق حذف کنید.
- **دستورات** (فقط ادمین):
  - `/detect`: پاسخ به پیام، انتخاب اسپم/عادی با دکمه‌ها؛ ذخیره در CSV.
  - `/send_data`: ارسال سند 'spam_messages.csv'.
  - `/check`: پاسخ به پیام؛ نمایش احتمال اسپم.
- **تشخیص خودکار**: اسکن تمام پیام‌ها؛ اگر اسپم >۴۰%، هشدار به کاربر، اطلاع به گروه ادمین‌ها با دکمه‌های حذف یا تایید (ری‌اکشن 👍).
- **Callbackها**: ادمین‌ها دکمه‌ها را کلیک کنند تا فلگ‌ها را مدیریت کنند؛ لاگ به کانال.
- **بازآموزش**: از 'spam_messages.csv' جمع‌آوری‌شده به عنوان data.csv جدید استفاده کنید، train.py را دوباره اجرا کنید.

'bot.log' را برای خطاها نظارت کنید. لینک‌های تبلیغاتی/پیام‌ها در کد سفارشی کنید.

## Contributing / مشارکت

### English
Contributions welcome! Fork, branch, commit, push, PR. Report issues on GitHub.

### فارسی
مشارکت خوش آمدید! فورک، شاخه، کامیت، پوش، PR. مشکلات را در GitHub گزارش دهید.

## License / مجوز
MIT License - see [LICENSE](LICENSE) for details.

---

*Project analyzed on September 26, 2025. The code is functional, secure (with an environment token), and Persian-focused. No vulnerabilities in deps.*
