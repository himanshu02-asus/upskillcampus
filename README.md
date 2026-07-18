# Upskill Campus Python Projects

A collection of small Python projects I built while learning and interning as a Python developer. Each project focuses on a different practical concept — file handling, encryption, web apps, and working with JSON data.

## Projects

### 1. File Organizer (`file_organizer.py`)
A script that scans a folder and automatically sorts files into category folders (Images, Documents, Videos, Audio, Archives, Code, Others) based on their file extension.

**Concepts used:** `os`, `shutil`, file handling, dictionaries

**How to run:**
```bash
python file_organizer.py
```
You'll be prompted to enter the path of the folder you want to organize.

---

### 2. Password Manager (`password_manager.py`)
A command-line password manager that stores account credentials securely. Passwords are encrypted using Fernet (symmetric encryption), with the encryption key derived from a master password via PBKDF2.

**Concepts used:** `sqlite3`, `cryptography` (Fernet, PBKDF2HMAC), password hashing/salting

**How to run:**
```bash
pip install cryptography
python password_manager.py
```

**Note:** Running this script generates `passwords.db` and `salt.bin` locally. These files are **not included** in this repo since they'd contain real encrypted data and salt values — including them would defeat the purpose of the encryption.

---

### 3. Quiz Game (`quiz_game.py`)
A multiple-choice quiz game that loads questions from a JSON file, shuffles both the question order and the answer options, tracks your score, and shows a result summary at the end.

**Concepts used:** `json`, `random`, file I/O

**How to run:**
```bash
python quiz_game.py
```
Make sure `questions.json` is in the same folder. If it's missing, the script will auto-generate a sample set of questions.

---

### 4. URL Shortener (`url_shortener.py`)
A simple web app (built with Flask) that converts long URLs into short, unique codes and redirects visitors to the original URL.

**Concepts used:** `flask`, `sqlite3`, routing, HTML templating

**How to run:**
```bash
pip install flask
python url_shortener.py
```
Then open `http://127.0.0.1:5000` in your browser.

**Note:** Running this generates `urls.db` locally, which is not included in this repo.

---

## Why some files aren't included

The `.db` and `.bin` files (`passwords.db`, `salt.bin`, `urls.db`) are excluded on purpose. They're generated automatically the first time you run the respective script, and including them in the repo would mean uploading real data/encryption material rather than just the source code.

## About

I'm a B.Tech student in AI and Data Science, currently doing a Python development internship. These projects are part of my ongoing practice in Python fundamentals, file handling, encryption basics, and building small end-to-end applications.
