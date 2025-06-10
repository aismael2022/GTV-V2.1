import os
import time
import pyfiglet
import pandas as pd
from datetime import datetime
from typing import Optional

# Imports from your modules
from Scraper import stage_one_extract_and_save, stage_two_enrich_search_results
from video_factory_V2 import build_prompt, generate_content, save_to_file, extract_visual_keywords
from images_factory import search_and_save_images

def run_stage_one() -> Optional[str]:
    """Stage 1: Run Scraper and enrich search results."""
    print("\n" + "="*50)
    print("Running Stage [1]: Scraping TV Trends")
    print("="*50 + "\n")
    
    file = stage_one_extract_and_save()
    if not file or not os.path.exists(file):
        print("❌ Failed to extract data.")
        return None
    
    print(f"✅ Stage 1A Complete: Extracted file: {file}")
    
    print("\n[→] Enriching file with Search Results...\n")
    stage_two_enrich_search_results(file)
    
    if not os.path.exists(file):
        print("❌ Enriched file not found.")
        return None

    print("✅ Stage 1B Complete: Enrichment done.")
    return file

def filter_valid_rows(input_file: str) -> pd.DataFrame:
    df = pd.read_excel(input_file)
    
    # Convert "Search Results" to numeric
    df["Search Results"] = pd.to_numeric(df["Search Results"], errors="coerce")
    
    # Apply filtering criteria
    df = df[
        (df["Is Person"] == True) &
        (df["Search Results"].between(1_000_000, 20_000_000))
    ]
    
    return df

def run_stage_two(input_file: str) -> None:
    """Stage 2: Generate video scripts."""
    print("\n" + "="*50)
    print("Running Stage [2]: Generating Video Scripts")
    print("="*50 + "\n")
    
    df = filter_valid_rows(input_file)

    for _, row in df.iterrows():
        topic = row['Name']
        print(f"\n📝 Generating script for: {topic}")
        
        prompt = build_prompt(topic=topic, video_type="Who is", video_duration="1 to 2 minutes")
        content = generate_content(prompt)
        
        if content:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{topic.replace(' ', '_')}_script_{timestamp}.txt"
            save_to_file(content, filename)
            
            # Optional: extract visual keywords
            keywords = extract_visual_keywords(content)
            print(f"🔑 Visual keywords for {topic}: {keywords}")

def run_stage_three(input_file: str) -> None:
    """Stage 3: Generate images for valid names."""
    print("\n" + "="*50)
    print("Running Stage [3]: Generating Images")
    print("="*50 + "\n")
    
    df = filter_valid_rows(input_file)

    for _, row in df.iterrows():
        name = row['Name']
        print(f"\n🖼️ Fetching images for: {name}")
        search_and_save_images(name, count=20)

def main():
    ascii_art = pyfiglet.figlet_format("NOVA ClIP", font="standard")
    print(ascii_art)
    
    try:
        # Stage 1: Scraper + Enrichment
        stage1_output = run_stage_one()
        if not stage1_output:
            print("❌ Stage 1 failed. Exiting.")
            return
        
        time.sleep(2)  # buffer

        # Stage 2: Video scripts
        run_stage_two(stage1_output)

        time.sleep(2)  # buffer

        # Stage 3: Images
        run_stage_three(stage1_output)

        print("\n" + "="*50)
        print("🎉 Workflow Completed Successfully!")
        print("="*50 + "\n")

    except Exception as e:
        print(f"\n❌ Workflow failed: {str(e)}")

if __name__ == "__main__":
    main()
