import os
import openai
import json
from typing import List, Optional

# OpenAI Key
openai.api_key = "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"

def build_prompt(topic: str, video_type: str, video_duration: str) -> str:
    return f"""
You are a content creator specializing in sports history and storytelling for YouTube.

Create a highly engaging script and video description for a {video_duration} YouTube video titled: "{video_type} {topic}".

### Script Content Requirements:
- Structure the script in 3 parts: The Origins, The Achievements, and The Impact
- Write it for narration, suitable for a YouTube video with energetic pacing and a documentary-style tone
- The total length should be about 1 to 2 minutes, which means roughly 150 to 300 words
- Include timestamps for each section in the format (mm:ss - mm:ss), dividing the script evenly
- Each section should have a title heading in square brackets, e.g. [THE ORIGINS]

### Description Requirements:
After the script, write a YouTube video description using this structure:
- Hook (1-2 lines): Catchy intro or question
- Summary (2-3 lines): Recap the topic and what viewers will learn
- Call to Action (1-2 lines): Ask users to like, comment, or subscribe
- Relevant Hashtags

Output the script first, then the YouTube description.
"""

def generate_content(prompt: str, model: str = "gpt-4", temperature: float = 0.8) -> Optional[str]:
    try:
        response = openai.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature
        )
        return response.choices[0].message.content if response.choices else None
    except Exception as e:
        print(f"❌ Error calling OpenAI API: {e}")
        return None

def save_to_file(content: str, filename: str) -> None:
    output_path = os.path.join(os.path.dirname(__file__), filename)
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ Content saved to {output_path}")
    except Exception as e:
        print(f"❌ Error saving file: {e}")

def extract_visual_keywords(script_text: str, model: str = "gpt-4", temperature: float = 0.5) -> List[str]:
    keyword_prompt = f"""
You're an assistant helping video editors find visual assets for YouTube videos.

Given the following narration script, extract a list of 5–8 **visual search terms** a user can input into Google Images or a stock image tool. Focus on:
- Famous locations or cities
- Notable people mentioned
- Specific events or awards
- Visual symbols related to the story
- Car or race-related terms if relevant

Return as a clean Python list of strings. Here's the script:

\"\"\"{script_text}\"\"\"
"""
    try:
        keyword_response = openai.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": keyword_prompt}],
            temperature=temperature
        )
        keyword_content = keyword_response.choices[0].message.content if keyword_response.choices else None

        if keyword_content:
            try:
                parsed = json.loads(keyword_content.strip())
                return parsed if isinstance(parsed, list) else []
            except json.JSONDecodeError as e:
                print(f"❌ JSON parsing error: {e}")
                print(f"🧾 Raw keyword content: {keyword_content}")
                return []
        else:
            print("⚠️ No keyword content returned from OpenAI.")
            return []
    except Exception as e:
        print(f"❌ Error extracting keywords: {e}")
        return []

def generate_video_assets(name: str):
    video_type = "Who is"
    video_duration = "1 to 2 minutes"
    safe_filename = name.strip().lower().replace(" ", "_")
    filename = f"{safe_filename}_script_and_description.txt"

    print(f"\n🎬 Generating script for: {name}")
    prompt = build_prompt(name, video_type, video_duration)
    content = generate_content(prompt)

    if content:
        save_to_file(content, filename)
        keywords = extract_visual_keywords(content)
        print(f"🔑 Visual Keywords for {name}: {keywords}")
    else:
        print(f"⚠️ Failed to generate content for {name}")