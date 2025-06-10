import os
import re
import json
import requests
import pandas as pd
from glob import glob
from googleapiclient.discovery import build

# ——— CONFIGS ———
API_KEY = "AIzaSyCXVNZjrHkmf65kFsMUThLe9_vGAe6ih7k"
CSE_ID  = "a71b1ebb654dc4e4b"
BASE_IMAGE_DIR = os.path.join(os.path.dirname(__file__), "images")
CREDITS_FILE = "image_credits.json"

os.makedirs(BASE_IMAGE_DIR, exist_ok=True)

def get_latest_scraper_output():
    """Get the most recent trends Excel file"""
    files = glob(os.path.join(os.path.dirname(__file__), "google_trends_tv_results_*.xlsx"))
    return max(files, key=os.path.getctime) if files else None

def get_valid_names(file_path):
    df = pd.read_excel(file_path)
    df = df[df["Is Person"] == True]
    df = df[df["Search Results"].between(1_000_000, 20_000_000)]
    return df["Name"].dropna().tolist()

def search_and_save_images(query, count=10):
    service = build("customsearch", "v1", developerKey=API_KEY)
    headers = {"User-Agent": "Mozilla/5.0"}
    saved_credits = []

    safe_name = re.sub(r"[^\w\s]", "", query).strip().lower().replace(" ", "_")
    image_dir = os.path.join(BASE_IMAGE_DIR, f"{safe_name}_images")
    os.makedirs(image_dir, exist_ok=True)

    for i in range(count):
        res = service.cse().list(
            q=query,
            cx=CSE_ID,
            searchType="image",
            imgType="stock",
            num=1,
            start=i + 1,
            imgSize="LARGE"
        ).execute()

        items = res.get("items")
        if not items:
            print(f"[!] No image found for: {query} (index {i+1})")
            continue

        item = items[0]
        img_url = item["link"]
        source_url = item.get("image", {}).get("contextLink", "N/A")

        try:
            resp = requests.get(img_url, headers=headers, timeout=10)
            resp.raise_for_status()
        except Exception as e:
            print(f"[!] Failed to download {img_url}: {e}")
            continue

        ext = os.path.splitext(img_url)[1].split("?")[0]
        if not ext or len(ext) > 5:
            ext = ".jpg"
        filename = f"{safe_name}_{i+1}{ext}"
        path = os.path.join(image_dir, filename)

        with open(path, "wb") as f:
            f.write(resp.content)

        print(f"[OK] Saved: {path}")

        saved_credits.append({
            "filename": filename,
            "query": query,
            "image_url": img_url,
            "source": source_url
        })

    if saved_credits:
        with open(CREDITS_FILE, "a", encoding="utf-8") as f:
            json.dump(saved_credits, f, indent=4, ensure_ascii=False)

def main():
    latest_file = get_latest_scraper_output()
    if not latest_file:
        print("❌ No Scraper output file found.")
        return

    names = get_valid_names(latest_file)
    print(f"✅ Found {len(names)} valid names.")

    for name in names:
        print(f"\n🔍 Fetching images for: {name}")
        search_and_save_images(name, count=10)

if __name__ == "__main__":
    main()