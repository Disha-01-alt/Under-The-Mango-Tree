import re
import os
import json
import logging

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, "..", "..")) 
DATA_DIR = os.path.join(PROJECT_ROOT, "data")

def create_slug(name: str) -> str:
    if not isinstance(name, str): return ''
    slug = name.lower()
    slug = re.sub(r'[^a-z0-9\s-]', '', slug).strip()
    slug = re.sub(r'\s+', '-', slug)
    return slug

def extract_youtube_id(url: str) -> str:
    if not url: return None
    match = re.search(r'(?:v=|/embed/|youtu.be/|/v/|list=|/watch\?.*&v=)([a-zA-Z0-9_-]{11})', url)
    return match.group(1) if match else None

def load_json_data(filename: str):
    filepath = os.path.join(DATA_DIR, filename)
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Error loading {filename} from {filepath}: {e}")
        return {}

def find_video_details(video_id_str: str, data_source: dict):
    if not video_id_str or not data_source: return None, None, None, None
    all_videos = [v for topic in data_source.get('topics', []) for v in topic.get('videos', [])]
    try:
        idx = next(i for i, v in enumerate(all_videos) if str(v.get('id')) == video_id_str)
    except (StopIteration, KeyError):
        return None, None, None, None

    current = all_videos[idx]
    current['youtube_id'] = extract_youtube_id(current.get('youtube_url'))
    topic_name = next((t.get('name') for t in data_source.get('topics', []) 
                      if any(str(v.get('id')) == video_id_str for v in t.get('videos', []))), None)
    prev_v = all_videos[idx - 1] if idx > 0 else None
    next_v = all_videos[idx + 1] if idx < len(all_videos) - 1 else None
    return current, topic_name, prev_v, next_v

def preprocess_ai_tools(raw_data):
    if not raw_data or not isinstance(raw_data, list): return []
    categorized = {}
    for tool in raw_data:
        cat = tool.get('Category', 'Uncategorized').strip()
        tool_meta = tool.copy()
        tool_meta['slug'] = create_slug(tool.get('Tool Name', ''))
        tool_meta['youtube_id'] = extract_youtube_id(tool.get('YouTube Tutorial'))
        if cat not in categorized: categorized[cat] = []
        categorized[cat].append(tool_meta)
    processed = [{'name': k, 'tools': sorted(v, key=lambda x: x.get('Tool Name', ''))} for k, v in categorized.items()]
    return sorted(processed, key=lambda x: x['name'])
