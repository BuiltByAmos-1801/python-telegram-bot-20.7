from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters
import qrcode
import os
import openai
from openai import OpenAI
import google.genai as genai
from database import add_user, get_user, verify_user, unverify_user, get_paid_users, get_stats, check_expiry_reminders, update_referral_count, add_to_wallet, deduct_from_wallet, set_upi_id
from content import get_daily_content, PRIVATE_CHANNEL
from config import TOKEN, ADMIN_ID, UPI_ID, PLANS, OPENAI_API_KEY, GEMINI_API_KEY
from datetime import datetime, time

async def send_long_message(update_or_query, text):
    """Send message, splitting if too long"""
    max_length = 4096
    if len(text) <= max_length:
        await update_or_query.message.reply_text(text)
    else:
        parts = [text[i:i+max_length] for i in range(0, len(text), max_length)]
        for part in parts:
            await update_or_query.message.reply_text(part)

# Bot setup
app = ApplicationBuilder().token(TOKEN).build()
openai_client = OpenAI(api_key=OPENAI_API_KEY)
client = genai.Client(api_key=GEMINI_API_KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Welcome message and instructions"""
    user_id = update.effective_user.id
    referred_by = None
    if context.args:
        try:
            referred_by = int(context.args[0])
        except:
            pass
    add_user(user_id, referred_by)
    if referred_by:
        update_referral_count(referred_by)
        add_to_wallet(referred_by, 10)
    keyboard = [
        [InlineKeyboardButton("📋 View Plan", callback_data="plan")],
        [InlineKeyboardButton(" Content Access", callback_data="content")],
        [InlineKeyboardButton("⏰ Expiry Check", callback_data="expiry")],
        [InlineKeyboardButton("💰 Wallet", callback_data="wallet"), InlineKeyboardButton("🔗 Refer", callback_data="referral")],
        [InlineKeyboardButton("💳 Set UPI ID", callback_data="set_upi")]
    ]
    if os.path.exists('welcome.jpg'):
        await update.message.reply_photo(
            open('images/welcome.jpg', 'rb'),
            caption="🤖 Welcome to AI + Online Earning Bot!\n\n"
            "Here you will find:\n"
            "- Daily AI Prompts\n"
            "- Online Earning Guides\n"
            "- Mini Courses & Tutorials\n"
            "- Private Channel Access\n\n"
            "Choose your plan:\n"
            "📅 Weekly: ₹49 (7 days)\n"
            "📅 Monthly: ₹149 (30 days)\n"
            "📅 Yearly: ₹499 (365 days)",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        await update.message.reply_text(
            "🤖 Welcome to AI + Online Earning Bot!\n\n"
            "Here you will find:\n"
            "- Daily AI Prompts\n"
            "- Online Earning Guides\n"
            "- Mini Courses & Tutorials\n"
            "- Private Channel Access\n\n"
            "Choose your plan:\n"
            "📅 Weekly: ₹49 (7 days)\n"
            "📅 Monthly: ₹149 (30 days)\n"
            "📅 Yearly: ₹599 (365 days)",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle inline buttons"""
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    data = query.data

    if data == "plan":
        keyboard = [
            [InlineKeyboardButton("📅 Weekly - ₹49", callback_data="plan_weekly")],
            [InlineKeyboardButton("📅 Monthly - ₹149", callback_data="plan_monthly")],
            [InlineKeyboardButton("📅 Yearly - ₹499", callback_data="plan_yearly")]
        ]
        await query.message.reply_text("Choose your subscription plan:", reply_markup=InlineKeyboardMarkup(keyboard))
    elif data == "plan_weekly":
        await query.message.reply_text(
            f"📅 Weekly Plan:\n\n"
            f"💰 Price: ₹{PLANS['weekly']['price']}\n"
            f"⏳ Duration: {PLANS['weekly']['duration']} Days\n\n"
            f"Benefits:\n"
            f"✅ Daily AI Prompts\n"
            f"✅ Online Earning Guides\n"
            f"✅ Mini Courses & Tutorials\n"
            f"✅ Private Telegram Channel Access\n\n"
            f"Pay via PhonePe/UPI and send screenshot to admin.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("💳 Pay ₹49", callback_data="pay_weekly")]])
        )
    elif data == "plan_monthly":
        await query.message.reply_text(
            f"📅 Monthly Plan:\n\n"
            f"💰 Price: ₹{PLANS['monthly']['price']}\n"
            f"⏳ Duration: {PLANS['monthly']['duration']} Days\n\n"
            f"Benefits:\n"
            f"✅ Daily AI Prompts\n"
            f"✅ Online Earning Guides\n"
            f"✅ Mini Courses & Tutorials\n"
            f"✅ Private Telegram Channel Access\n\n"
            f"Pay via PhonePe/UPI and send screenshot to admin.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("💳 Pay ₹149", callback_data="pay_monthly")]])
        )
    elif data == "plan_yearly":
        await query.message.reply_text(
            f"📅 Yearly Plan:\n\n"
            f"💰 Price: ₹{PLANS['yearly']['price']}\n"
            f"⏳ Duration: {PLANS['yearly']['duration']} Days\n\n"
            f"Benefits:\n"
            f"✅ Daily AI Prompts\n"
            f"✅ Online Earning Guides\n"
            f"✅ Mini Courses & Tutorials\n"
            f"✅ Private Telegram Channel Access\n\n"
            f"Pay via PhonePe/UPI and send screenshot to admin.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("💳 Pay ₹499", callback_data="pay_yearly")]])
        )
    elif data == "pay_weekly":
        amount = PLANS['weekly']['price']
        upi_url = f"upi://pay?pa={UPI_ID}&pn=AI+Earning+Bot&am={amount}&cu=INR"
        qr = qrcode.make(upi_url)
        qr.save('payment_qr.png')
        await query.message.reply_photo(
            open('payment_qr.png', 'rb'),
            caption=f"💳 Pay ₹{amount} via PhonePe/UPI\n\n"
                    f"UPI ID: {UPI_ID}\n\n"
                    f"After payment, send screenshot to admin."
        )
    elif data == "pay_monthly":
        amount = PLANS['monthly']['price']
        upi_url = f"upi://pay?pa={UPI_ID}&pn=AI+Earning+Bot&am={amount}&cu=INR"
        qr = qrcode.make(upi_url)
        qr.save('payment_qr.png')
        await query.message.reply_photo(
            open('payment_qr.png', 'rb'),
            caption=f"💳 Pay ₹{amount} via PhonePe/UPI\n\n"
                    f"UPI ID: {UPI_ID}\n\n"
                    f"After payment, send screenshot to admin."
        )
    elif data == "pay_yearly":
        amount = PLANS['yearly']['price']
        upi_url = f"upi://pay?pa={UPI_ID}&pn=AI+Earning+Bot&am={amount}&cu=INR"
        qr = qrcode.make(upi_url)
        qr.save('payment_qr.png')
        await query.message.reply_photo(
            open('payment_qr.png', 'rb'),
            caption=f"💳 Pay ₹{amount} via PhonePe/UPI\n\n"
                    f"UPI ID: {UPI_ID}\n\n"
                    f"After payment, send screenshot to admin."
        )
    elif data == "content":
        user = get_user(user_id)
        if user and user[1] == 1:  # is_paid
            keyboard = [
                [InlineKeyboardButton("🤖 Premium AI Prompts & Tools", callback_data="ai_prompts")],
                [InlineKeyboardButton("💰 Online Earning Guides", callback_data="earning_guides")],
                [InlineKeyboardButton("🎓 Big Premium Tutorials & Mini Courses", callback_data="tutorials")],
                [InlineKeyboardButton("📦 Ready-to-Use Resources", callback_data="resources")],
                [InlineKeyboardButton("🔔 Daily AI & Earning Tips", callback_data="daily_tips")],
                [InlineKeyboardButton("🔐 Paid Access System", callback_data="access_system")],
                [InlineKeyboardButton("📢 Exclusive Updates", callback_data="updates")],
                [InlineKeyboardButton("📺 Join Private Channel", callback_data="join_channel")],
                [InlineKeyboardButton("🎨 Generate AI Image", callback_data="gen_image")],
                [InlineKeyboardButton("🎥 Generate AI Video (Coming Soon)", callback_data="gen_video")],
                [InlineKeyboardButton("🤖 Chat with Gemini AI", callback_data="gemini_chat")]
            ]
            await query.message.reply_text("Choose what you want to access:", reply_markup=InlineKeyboardMarkup(keyboard))
        else:
            await query.message.reply_text("❌ No access. First make payment and get verified.")
    elif data == "gen_image":
        context.user_data['waiting_for_image_prompt'] = True
        await query.message.reply_text("🎨 Enter your image generation prompt:")
    elif data == "gen_video":
        await query.message.reply_text("🎥 AI Video generation is coming soon! Stay tuned.")
    elif data == "gemini_chat":
        context.user_data['waiting_for_gemini_prompt'] = True
        await query.message.reply_text("🤖 Ask Gemini AI anything:")
    elif data == "expiry":
        user = get_user(user_id)
        if user and user[1] == 1 and user[2]:
            await query.message.reply_text(f"⏰ Your subscription expires on: {user[2]}")
        else:
            await query.message.reply_text("❌ No active subscription.")
    elif data == "wallet":
        user = get_user(user_id)
        balance = user[6] if user and len(user) > 6 else 0
        upi = user[7] if user and len(user) > 7 else None
        upi_text = f"💳 Your UPI ID: {upi}\n\n" if upi else "💳 Set your UPI ID using the button below.\n\n"
        await query.message.reply_text(f"💰 Your Wallet Balance: ₹{balance}\n\n{upi_text}Minimum withdrawal: ₹100\n\nUse /withdraw <upi_id> to request payout.")
    elif data == "referral":
        referral_link = f"https://t.me/{query._bot.username}?start={user_id}"
        await query.message.reply_text(
            f"🔗 Your Referral Link: {referral_link}\n\n"
            f"🎁 Reward: ₹10 per successful referral!\n\n"
            f"Share this link with friends and earn money in your wallet."
        )
    elif data == "set_upi":
        context.user_data['waiting_for_upi'] = True
        await query.message.reply_text("💳 Type your UPI ID and send it.")
    elif data == "ai_prompts":
        try:
            response = client.models.generate_content(model='models/gemini-1.5-flash', contents="Generate 5 premium AI prompts for content creation, social media, and marketing.")
            content = response.candidates[0].content.parts[0].text
            await send_long_message(query, f"🤖 Premium AI Prompts & Tools:\n\n{content}")
        except Exception as e:
            await query.message.reply_text(f"❌ Error generating AI prompts: {str(e)}")
    elif data == "earning_guides":
        try:
            response = client.models.generate_content(model='models/gemini-1.5-flash', contents="Generate a comprehensive guide on online earning methods including freelancing, affiliate marketing, dropshipping, and passive income.")
            content = response.candidates[0].content.parts[0].text
            await send_long_message(query, f"💰 Online Earning Guides:\n\n{content}")
        except Exception as e:
            await query.message.reply_text(f"❌ Error generating earning guides: {str(e)}")
    elif data == "tutorials":
        try:
            response = client.models.generate_content(model='models/gemini-1.5-flash', contents="Generate a mini course outline on using AI for online business and earning, including modules on basics, tools, and strategies.")
            content = response.candidates[0].content.parts[0].text
            await send_long_message(query, f"🎓 Big Premium Tutorials & Mini Courses:\n\n{content}")
        except Exception as e:
            await query.message.reply_text(f"❌ Error generating tutorials: {str(e)}")
    elif data == "resources":
        try:
            response = client.models.generate_content(model='models/gemini-1.5-flash', contents="Generate a list of ready-to-use resources for online business: scripts, templates, checklists, tools, and software recommendations.")
            content = response.candidates[0].content.parts[0].text
            await send_long_message(query, f"📦 Ready-to-Use Resources:\n\n{content}")
        except Exception as e:
            await query.message.reply_text(f"❌ Error generating resources: {str(e)}")
    elif data == "daily_tips":
        try:
            response = client.models.generate_content(model='models/gemini-1.5-flash', contents="Generate 5 daily tips on using AI for productivity and online earning strategies.")
            content = response.candidates[0].content.parts[0].text
            await send_long_message(query, f"🔔 Daily AI & Earning Tips:\n\n{content}")
        except Exception as e:
            await query.message.reply_text(f"❌ Error generating tips: {str(e)}")
    elif data == "access_system":
        user = get_user(user_id)
        if user and user[2]:
            await query.message.reply_text(f"🔐 Paid Access System: Your subscription expires on {user[2]}. Renew to continue.")
        else:
            await query.message.reply_text("🔐 Paid Access System: No active subscription.")
    elif data == "updates":
        await query.message.reply_text("📢 Exclusive Updates: New AI tools & earning methods coming soon!")
    elif data == "join_channel":
        await query.message.reply_text(f"📺 Join our Private Channel: {PRIVATE_CHANNEL}")

async def verify(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin command to verify user"""
    if update.effective_user.id != ADMIN_ID:
        return
    if len(context.args) >= 2:
        user_id = int(context.args[0])
        amount = int(context.args[1])
        days = 30
        if amount == 49:
            days = 7
        elif amount == 149:
            days = 30
        elif amount == 499:
            days = 365
        try:
            user_chat = await context.bot.get_chat(user_id)
            user_name = user_chat.first_name + (f" {user_chat.last_name}" if user_chat.last_name else "")
        except:
            user_name = "Unknown"
        verify_user(user_id, amount)
        await update.message.reply_text(f"✅ User {user_id} ({user_name}) verified. Access granted for {days} days. Payment: ₹{amount}")
    else:
        await update.message.reply_text("Usage: /verify user_id amount")

async def unverify(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin command to unverify user"""
    if update.effective_user.id != ADMIN_ID:
        return
    if context.args:
        user_id = int(context.args[0])
        unverify_user(user_id)
        await update.message.reply_text(f"❌ User {user_id} access removed.")
    else:
        await update.message.reply_text("Usage: /unverify user_id")

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin command to broadcast message to paid users"""
    if update.effective_user.id != ADMIN_ID:
        return
    if context.args:
        message = ' '.join(context.args)
        paid_users = get_paid_users()
        for uid in paid_users:
            try:
                await context.bot.send_message(chat_id=uid, text=f"📢 Broadcast: {message}")
            except:
                pass
        await update.message.reply_text(f"📢 Message sent to {len(paid_users)} users.")
    else:
        await update.message.reply_text("Usage: /broadcast message")

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Admin command to show stats"""
    if update.effective_user.id != ADMIN_ID:
        return
    total, paid = get_stats()
    await update.message.reply_text(f"📊 Stats:\nTotal Users: {total}\nPaid Users: {paid}")

async def plan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show plan details"""
    await update.message.reply_text(
        f"📋 Subscription Plan:\n\n"
        f"💰 Price: ₹{PLAN_PRICE}\n"
        f"⏳ Duration: 30 Days\n\n"
        f"Benefits:\n"
        f"✅ Daily AI Prompts\n"
        f"✅ Online Earning Guides\n"
        f"✅ Mini Courses & Tutorials\n"
        f"✅ Private Telegram Channel Access"
    )

async def pay(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show payment instructions"""
    amount = PLAN_PRICE
    upi_url = f"upi://pay?pa={UPI_ID}&pn=AI+Earning+Bot&am={amount}&cu=INR"
    qr = qrcode.make(upi_url)
    qr.save('payment_qr.png')
    await update.message.reply_photo(
        open('payment_qr.png', 'rb'),
        caption=f"💳 Pay ₹{amount} via PhonePe/UPI\n\n"
                f"UPI ID: {UPI_ID}\n\n"
                f"After payment, send screenshot to admin."
    )

async def content(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Access content if paid"""
    user_id = update.effective_user.id
    user = get_user(user_id)
    if user and user[1] == 1:
        day = datetime.now().day
        content = get_daily_content(day)
        await update.message.reply_text(f"🤖 AI Prompt:\n\n{content['ai_prompt']}")
        await update.message.reply_text(f"💼 Earning Guide:\n\n{content['earning_guide']}")
        await update.message.reply_text(f"📖 Tutorial:\n\n{content['tutorial']}")
        await update.message.reply_text(f"🔗 Private Channel: {PRIVATE_CHANNEL}")
    else:
        await update.message.reply_text("❌ No access. First make payment and get verified.")

async def expiry(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show expiry date"""
    user_id = update.effective_user.id
    user = get_user(user_id)
    if user and user[1] == 1 and user[2]:
        await update.message.reply_text(f"⏰ Your subscription expires on: {user[2]}")
    else:
        await update.message.reply_text("❌ No active subscription.")

async def referral(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show referral link"""
    user_id = update.effective_user.id
    referral_link = f"https://t.me/{context.bot.username}?start={user_id}"
    await update.message.reply_text(
        f"🔗 Your Referral Link: {referral_link}\n\n"
        f"🎁 Reward: ₹10 per successful referral!\n\n"
        f"Share this link with friends and earn money in your wallet."
    )

async def wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show wallet balance"""
    user_id = update.effective_user.id
    user = get_user(user_id)
    balance = user[6] if user and len(user) > 6 else 0  # wallet_balance is index 6
    upi = user[7] if user and len(user) > 7 and user[7] else "Not set"
    await update.message.reply_text(f"💰 Your Wallet Balance: ₹{balance}\n\nUPI ID: {upi}\n\nMinimum withdrawal: ₹100")

async def withdraw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Request withdrawal"""
    user_id = update.effective_user.id
    user = get_user(user_id)
    balance = user[6] if user and len(user) > 6 else 0
    if balance < 100:
        await update.message.reply_text("❌ Minimum withdrawal is ₹100.")
        return
    upi = user[7] if user and len(user) > 7 and user[7] else (context.args[0] if context.args else None)
    if not upi:
        await update.message.reply_text("❌ UPI ID not set. Use /setupi <your_upi_id> or provide in command: /withdraw <your_upi_id>")
        return
    # Send to admin
    try:
        await context.bot.send_message(chat_id=ADMIN_ID, text=f"💸 Withdrawal Request:\nUser: {user_id}\nUPI: {upi}\nAmount: ₹{balance}")
        deduct_from_wallet(user_id, balance)
        await update.message.reply_text("✅ Withdrawal request sent. You will receive payment soon.")
    except:
        await update.message.reply_text("❌ Error processing request.")

async def set_upi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Set UPI ID for user"""
    user_id = update.effective_user.id
    if context.args:
        upi = context.args[0]
        set_upi_id(user_id, upi)
        await update.message.reply_text("✅ Your UPI ID has been set.")
    else:
        await update.message.reply_text("Usage: /setupi <your_upi_id>")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle user messages for UPI ID setting and image prompts"""
    user_id = update.effective_user.id
    if context.user_data.get('waiting_for_upi'):
        upi = update.message.text
        set_upi_id(user_id, upi)
        del context.user_data['waiting_for_upi']
        user = get_user(user_id)
        balance = user[6] if user and len(user) > 6 else 0
        upi_text = f"💳 Your UPI ID: {upi}\n\n" if upi else "💳 Set your UPI ID using the button below.\n\n"
        await update.message.reply_text(f"✅ Your UPI ID has been set.\n\n💰 Your Wallet Balance: ₹{balance}\n\n{upi_text}Minimum withdrawal: ₹100\n\nUse /withdraw <upi_id> to request payout.")
    elif context.user_data.get('waiting_for_image_prompt'):
        prompt = update.message.text
        del context.user_data['waiting_for_image_prompt']
        user = get_user(user_id)
        if not user or not user[1]:  # not paid
            await update.message.reply_text("❌ Access denied. Subscribe first.")
            return
        try:
            await update.message.reply_text("🎨 Generating image... Please wait.")
            response = openai_client.images.generate(prompt=prompt, model="dall-e-3", size="1024x1024")
            image_url = response.data[0].url
            await update.message.reply_photo(image_url, caption=f"🎨 Generated image for: {prompt}")
        except Exception as e:
            await update.message.reply_text(f"❌ Error generating image: {str(e)}")
    elif context.user_data.get('waiting_for_gemini_prompt'):
        prompt = update.message.text
        del context.user_data['waiting_for_gemini_prompt']
        user = get_user(user_id)
        if not user or not user[1]:  # not paid
            await update.message.reply_text("❌ Access denied. Subscribe first.")
            return
        try:
            await update.message.reply_text("🤖 Thinking...")
            response = client.models.generate_content(model='models/gemini-1.5-flash', contents=prompt)
            reply = response.candidates[0].content.parts[0].text
            await update.message.reply_text(f"🤖 Gemini: {reply}")
        except Exception as e:
            await update.message.reply_text(f"❌ Error with Gemini: {str(e)}")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle payment screenshots"""
    if update.message.photo:
        user = update.effective_user
        name = user.first_name + (f" {user.last_name}" if user.last_name else "")
        username = f"@{user.username}" if user.username else "No username"
        user_id = user.id
        date_time = update.message.date.strftime('%Y-%m-%d %H:%M:%S')
        # Forward the photo to admin
        await context.bot.send_photo(
            chat_id=ADMIN_ID,
            photo=update.message.photo[-1].file_id,  # highest resolution
            caption=f"💳 Payment Screenshot Received\n\n"
                    f"👤 Name: {name}\n"
                    f"🆔 User ID: {user_id}\n"
                    f"👨 Username: {username}\n"
                    f"📅 Date & Time: {date_time}"
        )
        await update.message.reply_text("✅ Payment screenshot sent to admin. Please wait for verification.")

# Handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(CommandHandler("verify", verify))
app.add_handler(CommandHandler("unverify", unverify))
app.add_handler(CommandHandler("broadcast", broadcast))
app.add_handler(CommandHandler("stats", stats))
app.add_handler(CommandHandler("plan", plan))
app.add_handler(CommandHandler("pay", pay))
app.add_handler(CommandHandler("content", content))
app.add_handler(CommandHandler("expiry", expiry))
app.add_handler(CommandHandler("referral", referral))
app.add_handler(CommandHandler("wallet", wallet))
app.add_handler(CommandHandler("withdraw", withdraw))
app.add_handler(CommandHandler("setupi", set_upi))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

async def send_expiry_reminders(context: ContextTypes.DEFAULT_TYPE):
    """Send expiry reminders to users expiring in 2 days"""
    users = check_expiry_reminders()
    for uid in users:
        try:
            await context.bot.send_message(chat_id=uid, text="⏰ Reminder: Your subscription expires in 2 days. Renew now!")
        except:
            pass

# Schedule daily reminders at 9 AM
app.job_queue.run_daily(send_expiry_reminders, time=time(hour=9, minute=0))

print("🤖 Bot Running...")
app.run_polling()

