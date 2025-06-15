# Penguin Discord Bot

Penguin is a powerful Discord bot with a web UI that allows you to control your Linux or Windows laptop/server remotely via Discord channels. It is designed for home server management, remote access, download management, and more—all from the comfort of your Discord server.

---

## 🚀 Features

- **Remote Control:** Execute commands and scripts on your laptop/server from Discord.
- **Download Manager:** Manage downloads on your home server via Discord or the web UI.
- **Web UI:** Modern web interface for advanced management and monitoring.
- **Cross-Platform:** Works on both Linux and Windows.
- **Secure:** Uses Discord authentication and configurable permissions.
- **Network Resilience:** Automatically reconnects if the network goes down.

---

## 📁 Project Structure

```
Penguin/
├── main.py
├── config/
│   └── settings.py
│   └── config.yaml
├── core/
│   └── app_logic.py
├── models/
│   └── user.py
├── services/
│   └── user_service.py
├── utils/
│   └── validators.py
├── api/
│   └── routes.py
├── data/
│   └── data_loader.py
├── tests/
│   └── test_user.py
├── requirements.txt
├── README.md
└── copilot-dev-notes.txt
```

---

## ⚙️ Setup & Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/penguin.git
   cd penguin
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure your bot token:**

   - Preferred: Edit `config/config.yaml` and add your Discord bot token:
     ```yaml
     DISCORD_BOT_TOKEN: "your-bot-token-here"
     ```
   - Or, create a `.env` file in the project root:
     ```
     DISCORD_BOT_TOKEN=your-bot-token-here
     ```

4. **Run the bot:**
   ```bash
   python main.py
   ```

---

## 🖥️ Web UI

The web UI provides a dashboard for managing your server and downloads. (See `api/routes.py` for API endpoints and web server setup.)

---

## 🛡️ Security

- Only authorized Discord users can control the bot.
- All sensitive operations are permission-checked.

---

## 🧪 Testing

Run unit tests with:

```bash
pytest
```

---

## 📝 Contributing

Contributions are welcome! Please open issues or submit pull requests.

---

## 📄 License

MIT License

---

## ✨ Credits

Built with [nextcord](https://github.com/nextcord/nextcord), [rich](https://github.com/Textualize/rich), and ❤️ by the Penguin team.
