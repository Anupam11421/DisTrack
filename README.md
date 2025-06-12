# 🔥 DisTrack - Your AI-Powered Productivity Partner

> **Block distractions. Stay focused. Get AI Suggestions.**

DisTrack is a badass productivity tool built in Python that blocks distracting websites and gives you AI-generated suggestions to stay focused. Ideal for students, coders, freelancers — basically anyone who's serious about their goals. 💻🚀

---

## 🧠 Features

- 🔒 **Block Unlimited Sites** – No mercy for distractions like Instagram, YouTube, etc.
- 🧠 **AI Suggestions** – Suggests productive alternatives like “Pomodoro session” or “Try learning Git for 10 min”
- 🖱️ **Easy to Use** – Just edit a JSON and run the app
- 🔧 **Executable Ready** – Build into `.exe` file for Windows
- 📊 **Logs Your Distraction Attempts** – Know how many times you failed 😂

---

## 📂 Folder Structure

```
DisTrack/
│
├── app.py → Main app file
├── app.spec → For building .exe using PyInstaller
├── icon.ico → App icon
├── sites.json → Blocked sites list
├── logs.txt → Logs of blocked attempts
├── .gitignore → Ignored files/folders
├── README.md → This file (description & setup)
├── /build → Build files (ignored)
├── /dist → EXE generated here

```
---

## ⚙️ How to Run

1. Clone this repo
   ```bash
   git clone https://github.com/Anupam11421/DisTrack.git
   cd DisTrack

2. (Optional) Create virtual env

   bash
   Copy
   Edit
   python -m venv venv
   venv\Scripts\activate  # for Windows

3. Install dependencies (if any, like PyInstaller)
   pip install -r requirements.txt

4. Run the app
   python app.py


🧪 How to Create EXE File

1. Install PyInstaller if not already:
   pip install pyinstaller

2. Run this to generate .exe:
   pyinstaller --onefile --windowed --icon=icon.ico app.py

3. EXE will be in dist/ folder.

  🔍 How It Works
Edits the system hosts file → redirects blocked websites to 127.0.0.1

AI module gives alternate suggestions in terminal when you try opening a blocked site

Logs are saved in logs.txt with timestamps


📌 Add Your Sites to Block
Go to sites.json and add sites like:
[
    "facebook.com",
    "youtube.com",
    "instagram.com"
]

Save and run the app again.

---

## 🤝 Made by

> [Anupam Tiwari](https://www.linkedin.com/in/anupam-tiwari-08607b281/)

---

## 🔗 GitHub Repository

Feel free to ⭐ star this repo or fork it for your own custom productivity tool!

👉 [DisTrack on GitHub](https://github.com/Anupam11421/DisTrack)

---

## 🪪 License

MIT License — use, modify, destroy distractions!  
Feel free to use it your way — just don’t waste time. 😄

---

## 💬 Suggestions & Collabs Welcome!

Got a cool idea? Want to take this tool to the next level?

👨‍💻 Let’s build:
- AI chatbot for productivity 🤖  
- App blocker (not just websites) 🔒  
- Mobile version 📱  
- Cloud sync for focus stats ☁️

DM me on:
- [LinkedIn](https://www.linkedin.com/in/anupam-tiwari-08607b281/)
- [GitHub](https://github.com/Anupam11421)

Let’s cook something epic 👨‍🍳🔥





