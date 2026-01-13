# AI + Online Earning Telegram Bot

A comprehensive Telegram bot built with Python that provides daily AI prompts, online earning guides, mini courses, and private channel access through subscription-based plans.

## Features

- **Subscription Plans**: Weekly (₹49), Monthly (₹149), Yearly (₹499)
- **Daily Content**: AI prompts, earning guides, tutorials
- **User Management**: SQLite database for user tracking, payments, referrals
- **Referral System**: Earn ₹10 per referral
- **Wallet System**: Track earnings and payments
- **AI Integration**: OpenAI and Google Gemini API support
- **QR Code Generation**: For payment verification
- **Admin Panel**: Statistics and user management

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd python-telegram-bot-20.7
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure the bot:
   - Edit `config.py` with your bot token, API keys, and settings
   - Replace placeholder values with your actual credentials

4. Run the bot:
   ```bash
   python bot.py
   ```

## Configuration

Create a `config.py` file with the following variables:

```python
TOKEN = "your-telegram-bot-token"
ADMIN_ID = your-admin-user-id
UPI_ID = "your-upi-id-for-payments"
PRIVATE_CHANNEL = "https://t.me/your-private-channel"
PLANS = {
    'weekly': {'price': 49, 'duration': 7},
    'monthly': {'price': 149, 'duration': 30},
    'yearly': {'price': 499, 'duration': 365}
}
OPENAI_API_KEY = "your-openai-api-key"
GEMINI_API_KEY = "your-google-gemini-api-key"
```

## Usage

1. Start the bot by sending `/start`
2. Choose a subscription plan
3. Make payment via UPI
4. Send payment screenshot for verification
5. Access premium content and private channel

## Commands

- `/start` - Initialize the bot and view plans
- Inline buttons for plan selection, content access, expiry check, wallet, referrals, and UPI setup

## Database

The bot uses SQLite (`database.db`) to store:
- User information (ID, payment status, expiry, referrals, wallet balance)
- Automatic database initialization on first run

## Dependencies

- python-telegram-bot==20.7
- qrcode[pil]
- openai
- google-genai

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support or questions, contact the admin or create an issue in the repository.
