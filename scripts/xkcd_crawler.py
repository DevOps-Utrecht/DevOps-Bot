#!/usr/bin/env python
"""
Retrieve all xkcd meta data
Expected runtime 3.5 minutes

Requirement: requests
Optional: tqdm
"""
import json
import devbot.database as db

try:
    import requests
except ImportError:
    raise Exception("Run pip install requests")


# optional status bar
try:
    from tqdm import tqdm
except ImportError:
    tqdm = list


def get_xkcd(num: int = None) -> dict or None:
    """Retrieve a xkcd comic by its number"""
    if num:
        url = f"https://xkcd.com/{num}/info.0.json"
    else:
        url = "https://xkcd.com/info.0.json"
    r = requests.get(url)
    try:
        data = json.loads(r.text)
        return data
    except json.decoder.JSONDecodeError:
        return


def main():
    """Crawl all comic data and add it to the database"""
    warning = []
    min_id: int = 1  # adjust here if necessary
    max_id: int = get_xkcd()["num"]
    print(f"Retrieving xkcd {min_id} through {max_id}...")

    session = db.Session()
    for n in tqdm(range(min_id, max_id)):
        try:
            xkcd = get_xkcd(n)
            session.merge(db.XKCD(**xkcd))
        except TypeError:
            warning.append(n)

    if warning:
        print(f"[WARNING] Unable to retrieve these comics: {', '.join(warning)}")

    print("Updating the database...")
    session.commit()

    print("Done!")


if __name__ == "__main__":
    main()
