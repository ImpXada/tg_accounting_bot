# Telegram Accounting Bot

[English](README.md) | [中文](README_zh.md)

An AI-powered accounting bot for Telegram that automatically categorizes expenses and income using natural language processing.

## Features

- 🤖 **AI-Powered Parsing**: Automatically extracts amount, category, date, and other details from natural language input
- 📊 **Smart Categorization**: Pre-defined categories covering income, fixed expenses, dining, transportation, healthcare, and more
- 💾 **SQLite Database**: Lightweight local database for storing transaction records
- 📱 **Telegram Interface**: Easy-to-use Telegram bot for quick expense logging
- 🌐 **Multi-Currency Support**: Default CNY with support for other currencies

## Quick Start

### Prerequisites

- Python 3.8+
- Telegram Bot Token
- OpenAI API Key (or Azure OpenAI)

### Installation

1. Clone the repository:
```bash
git clone git@github.com:ImpXada/tg_accounting_bot.git
cd tg_accounting_bot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

4. Run the bot:
```bash
cd src
python main.py
```

## Configuration

Create a `.env` file with the following variables:

```env
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=your_telegram_bot_token

# OpenAI Configuration (choose one)
OPENAI_API_KEY=your_openai_api_key

# OR Azure OpenAI Configuration
AZURE_OPENAI_API_KEY=your_azure_openai_key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_OPENAI_DEPLOYMENT_NAME=your-deployment-name
```

## Usage

Send messages to your Telegram bot with natural language descriptions:

- `"Bought coffee for $5 today"`
- `"Paid rent $1200 yesterday"`
- `"Salary received $5000 this month"`

The bot will automatically:
1. Parse the amount and currency
2. Categorize the expense/income
3. Extract date and time information
4. Store the record in the database

## Categories

The system supports 10 main categories:

1. **Income**: Salary, bonus, reimbursement, dividends, gifts
2. **Fixed Expenses**: Rent, utilities, insurance, subscriptions
3. **Dining**: Takeout, groceries, snacks, restaurants, fruits
4. **Transportation & Accommodation**: Public transport, taxi, flights, hotels
5. **Home & Daily**: Daily necessities, repairs, furniture, appliances
6. **Medical & Health**: Clinic visits, medicine, medical supplies, fitness
7. **Fashion & Personal Care**: Clothing, accessories, cosmetics, beauty
8. **Entertainment & Social**: Games, movies, dining out, gifts
9. **Learning & Tools**: Books, courses, stationery, software
10. **Visa & Other Necessary Fees**: Documents, visa fees

## API Response Format

The AI service returns structured JSON:

```json
{
  "return_code": 0,
  "return_msg": "success",
  "account": "wallet",
  "currency": "CNY", 
  "record_type": "expense",
  "main_category": "Medical & Health",
  "sub_category": "Medicine",
  "amount": -77.8,
  "name": "Medicine",
  "merchant": "",
  "date": "2025/08/25",
  "time": "19:34",
  "project": "",
  "description": "Symbicort inhaler"
}
```

## Project Structure

```
tg_accounting_bot/
├── src/                      # Source code
│   ├── main.py              # Main entry point
│   ├── telegram_bot.py      # Telegram bot handler
│   ├── ai_service.py        # AI parsing service
│   ├── accounting_service.py # Business logic
│   ├── models.py           # Data models
│   └── config.py           # Configuration management
├── accounting.db           # SQLite database
├── requirements.txt        # Dependencies
└── .env.example           # Environment template
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
- AI powered by OpenAI GPT models
- Database management with SQLAlchemy