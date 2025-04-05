# 🧠 Anki Card Generator from Word List

A Python script that takes a list of words from a `words.txt` file and automatically creates vocabulary flashcards in Anki using definitions scraped from online sources.
Note: the words must be lower case and separated by a new line.

Built with:
- 🐍 Python
- 🌐 BeautifulSoup & Requests for web scraping
- 🔗 AnkiConnect for pushing cards to Anki

---

## 📌 Features

- Reads a list of words from `words.txt`
- Scrapes definitions using web scraping (via BeautifulSoup)
- Automatically adds cards to Anki using [AnkiConnect](https://ankiweb.net/shared/info/2055492159)
- Supports basic card creation with example + definition
- Customizable deck and model

---

## 🧰 Requirements

- Anki Desktop with AnkiConnect installed and running

### 📦 Python Dependencies

```bash
pip install beautifulsoup4 requests
