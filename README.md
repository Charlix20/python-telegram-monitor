# Web Monitor & Telegram Automation Bot

Automated Python script that monitors web content using web scraping and pushes real-time notifications to a Telegram Bot.

## Features
- **Web Scraping:** Parses HTML elements with `BeautifulSoup` and `requests`.
- **Duplicate Prevention:** Tracks state with a local text buffer to send unique alerts only.
- **Telegram Integration:** Leverages Telegram REST API with custom HTML formatting.
- **Continuous Monitoring:** Implements continuous loops and exception handling.

## Tech Stack
- Python 3
- BeautifulSoup4
- Requests
- Telegram Bot API

## Setup & Installation
1. Clone the repository:
   ```bash
   git clone [https://github.com/Charlix20/python-telegram-monitor.git](https://github.com/Charlix20/python-telegram-monitor.git)