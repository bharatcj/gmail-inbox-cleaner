<div align="center">

# 📬 **Gmail Inbox Cleaner**

> *Turn every unread email into “read” — in one colourful, blazing-fast sweep*  
> _Because life’s too short to be haunted by notification bubbles._

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![Gmail API](https://img.shields.io/badge/Gmail%20API-v1-EA4335?logo=gmail&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

</div>

---

## 🤔 Why?
That **“9 k+ unread”** badge staring at you?  
Run **`gmail_reader.py`** once and watch the counter smash to **0** while a vibrant live log shows *exactly* what’s happening.  

_Pro-tip: scream “KOBE!” while you hit **Enter** for maximum catharsis._

---

## ✨ Features

| ⚡ | Description |
|---|-------------|
| **One-shot cleanup** | Removes the **UNREAD** label from every message in Gmail-safe batches of `1 000`. |
| **Ultra-light** | Touches only message IDs — *no bodies, no attachments*. |
| **Colourised live log** | Follow progress batch-by-batch in bright ANSI colours (falls back gracefully if colours aren’t supported). |
| **Smart OAuth** | Detects stale or scope-mismatched tokens and refreshes / recreates them automatically. |

---

## 🌐 Google Cloud setup (≈ 10 min, once)

| Steps |
|------|
| **1. Create project:** Open [Google Cloud Console](https://console.cloud.google.com/) → **☰ Menu → IAM & Admin → Manage resources → CREATE PROJECT** → name it `Gmail Reader` → **CREATE** |
| **2. Enable Gmail API:** **☰ Menu → APIs & Services → Enabled APIs & services → + ENABLE APIS AND SERVICES** → search **“Gmail API”** → **Gmail API → ENABLE** |
| **3. Make OAuth client:** Still under **APIs & Services** → **Credentials → + CREATE CREDENTIALS → OAuth client ID** |
| **4. Configure client:** Choose **Application type = Desktop app**, any name → **CREATE** → **DOWNLOAD JSON** → rename to **`credentials.json`**, place next to the script |
| **5. Consent screen & test user:** Go to **OAuth consent screen** → click **Audience** tab → under **Test users**, click **+ ADD USERS** → add your Gmail address → click **Save and Continue** → you're done! ✅ |

✅ You now have `credentials.json`; the Gmail API trusts your desktop script.  
_Pat yourself on the back — you’ve just wrestled Google Cloud into submission._

---

## 🐍 Installing Python (for complete beginners)

1. **Windows / macOS** – Download Python 3.11.x from [python.org](https://www.python.org/downloads/) and run the installer.  
   **⚠️ Tick “Add Python to PATH”!**  
2. **Linux** – Most distros already include Python 3.8+. Otherwise:  
   ```bash
   sudo apt-get install python3 python3-venv python3-pip     # Debian / Ubuntu

Verify:

```bash
python --version     # or:  python3 --version
```

Should show **3.8** or newer.
*If it prints 2.7, quietly close your laptop and rethink some life choices.*

---

## 💻 Project setup

```bash
git clone https://github.com/<your-user>/gmail-inbox-cleaner.git
cd gmail-inbox-cleaner

# create & activate a virtual environment (recommended)
python -m venv .venv
# Windows ➜ .venv\Scripts\activate
source .venv/bin/activate

# install dependencies
pip install -r requirements.txt
```

*(Leave the virtual env any time with `deactivate` — it won’t get offended.)*

---

## ▶️ Usage

```bash
python gmail_reader.py
```

1. A browser window appears once. **Log in with the Gmail account you added under *Test users*.**
2. Grant the permissions.
3. Enjoy the show:

```
══════════════════════════════════
📬  Gmail - Mark ALL Unread as Read
══════════════════════════════════
🔑  Checking credentials…
✅  Authenticated!

📥  Collecting unread message IDs…
🔍  Found 8 432 unread messages

✏️   Removing UNREAD label in batches of 1 000…
   • Batch 1   →  1 000 done ✔
   • Batch 2   →  1 000 done ✔
⋯
🏁  All done! Marked 8 432 messages as read in 22.7 s.
```

*Toast a marshmallow while you wait — it’ll be done before it melts.*

---

## 🛠 What’s happening inside the script?

1. **List IDs** – calls `users().messages().list(labelIds=["UNREAD"], maxResults=500)` repeatedly to collect every unread **ID** (no message payload).
2. **Chunk** – splits the ID list into blocks of **1 000** (Gmail’s `batchModify` hard limit).
3. **Batch modify** – each chunk is sent to `users().messages().batchModify({"removeLabelIds": ["UNREAD"]})`.
4. **Display progress** – colourful prints after every batch keep you updated.

*No deletes • No moves • Just a pristine **read** inbox.*

---

## 🩹 Troubleshooting

| Symptom                                   | Fix                                                                                     |
| ----------------------------------------- | --------------------------------------------------------------------------------------- |
| `HttpError 403 … insufficientPermissions` | Delete **`token.json`** (created with the wrong scope) and run again.                   |
| Browser can’t launch (headless server)    | Replace `flow.run_local_server()` with `flow.run_console()` in `make_service()`.        |
| Want to switch Gmail account              | Remove **`token.json`** so OAuth prompts again, or run with `--noauth_local_webserver`. |

---

## 🤝 Contributing

PRs for new features, docs tweaks, or ASCII fireworks are welcome—open an issue first so we don’t double-work.
*Bonus points if your PR includes a fresh pun about inbox zero.*

---

## 📜 License

MIT — enjoy, but please don’t abuse anyone’s mailbox.
*Yoda wisdom: “With great scripts, great responsibility comes.”*
