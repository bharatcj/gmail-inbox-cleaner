#!/usr/bin/env python3
import os.path, sys, time
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# ── fancy colors (falls back silently if colorama not installed) ────────────────
try:
    from colorama import init, Fore, Style

    init(autoreset=True)
    CLR = {
        "HDR": Fore.MAGENTA + Style.BRIGHT,
        "OK": Fore.GREEN + Style.BRIGHT,
        "INF": Fore.CYAN + Style.BRIGHT,
        "WRN": Fore.YELLOW + Style.BRIGHT,
        "ERR": Fore.RED + Style.BRIGHT,
        "RST": Style.RESET_ALL,
    }
except Exception:
    CLR = {k: "" for k in ["HDR", "OK", "INF", "WRN", "ERR", "RST"]}

SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]


def banner(txt):
    line = "═" * len(txt)
    print(f"{CLR['HDR']}{line}\n{txt}\n{line}{CLR['RST']}")


def make_service():
    print(f"{CLR['INF']}🔑  Checking credentials…{CLR['RST']}")
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        if not set(SCOPES).issubset(set(creds.scopes or [])):
            creds = None
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            print(
                f"{CLR['INF']}🌐  Opening browser for OAuth consent (modify scope)…{CLR['RST']}"
            )
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as t:
            t.write(creds.to_json())
    print(f"{CLR['OK']}✅  Authenticated!\n{CLR['RST']}")
    return build("gmail", "v1", credentials=creds, cache_discovery=False)


def unread_ids(service):
    page_token = None
    while True:
        resp = (
            service.users()
            .messages()
            .list(
                userId="me", labelIds=["UNREAD"], pageToken=page_token, maxResults=500
            )
            .execute()
        )
        for msg in resp.get("messages", []):
            yield msg["id"]
        page_token = resp.get("nextPageToken")
        if not page_token:
            break


def mark_read(service, ids):
    if ids:
        service.users().messages().batchModify(
            userId="me", body={"ids": ids, "removeLabelIds": ["UNREAD"]}
        ).execute()


def main():
    banner("📬  Gmail - Mark ALL Unread as Read")
    start = time.time()
    try:
        svc = make_service()

        print(f"{CLR['INF']}📥  Collecting unread message IDs…{CLR['RST']}")
        ids = list(unread_ids(svc))
        print(f"{CLR['OK']}🔍  Found {len(ids)} unread messages{CLR['RST']}\n")

        if not ids:
            print(f"{CLR['WRN']}🎉  Inbox already clean. Nothing to do!{CLR['RST']}")
            return

        print(f"{CLR['INF']}✏️   Removing UNREAD label in batches of 1 000…{CLR['RST']}")
        for n, i in enumerate(range(0, len(ids), 1000), 1):
            batch = ids[i : i + 1000]
            mark_read(svc, batch)
            print(f"{CLR['OK']}   • Batch {n:<3}  →  {len(batch)} done ✔{CLR['RST']}")

        elapsed = time.time() - start
        print(
            f"\n{CLR['OK']}🏁  All done! Marked {len(ids)} messages as read in "
            f"{elapsed:.1f}s.{CLR['RST']}"
        )

    except HttpError as e:
        print(f"{CLR['ERR']}🚨  API error: {e}{CLR['RST']}")
    except KeyboardInterrupt:
        print(f"\n{CLR['WRN']}⚠️   Interrupted by user.{CLR['RST']}")


if __name__ == "__main__":
    main()
