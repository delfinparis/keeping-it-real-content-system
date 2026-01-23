#!/usr/bin/env python3
"""
Transcribe podcast episodes using OpenAI Whisper.
Outputs JSON with timestamps and plain text versions.
"""

import whisper
import json
import re
import os
import sys
from pathlib import Path
from datetime import datetime
from tqdm import tqdm

DATA_DIR = Path(__file__).parent.parent / "data"
INDEX_DIR = DATA_DIR / "index"
MP3_DIR = DATA_DIR / "raw" / "mp3"
TRANSCRIPT_DIR = DATA_DIR / "transcripts"

# Real estate terms that Whisper might mis-transcribe
REAL_ESTATE_CORRECTIONS = {
    # Common mis-transcriptions -> correct terms
    r'\bfor sale by owner\b': 'FSBO',
    r'\bf s b o\b': 'FSBO',
    r'\bfsbo\b': 'FSBO',
    r'\bmls\b': 'MLS',
    r'\bm l s\b': 'MLS',
    r'\bnar\b': 'NAR',
    r'\bn a r\b': 'NAR',
    r'\brealtor\b': 'REALTOR',
    r'\brealtors\b': 'REALTORS',
    r'\bescro\b': 'escrow',
    r'\bcma\b': 'CMA',
    r'\bc m a\b': 'CMA',
    r'\bhoa\b': 'HOA',
    r'\bh o a\b': 'HOA',
    r'\broi\b': 'ROI',
    r'\br o i\b': 'ROI',
    r'\bcrm\b': 'CRM',
    r'\bc r m\b': 'CRM',
    r'\bkvcore\b': 'kvCORE',
    r'\bkv core\b': 'kvCORE',
    r'\bzillow\b': 'Zillow',
    r'\brealtor.com\b': 'Realtor.com',
    r'\bredfin\b': 'Redfin',
    r'\bcompass\b': 'Compass',
    r'\bkeller williams\b': 'Keller Williams',
    r'\bkw\b': 'KW',
    r'\bre/max\b': 'RE/MAX',
    r'\bremax\b': 'RE/MAX',
    r'\bcoldwell banker\b': 'Coldwell Banker',
    r'\bcentury 21\b': 'Century 21',
    r'\bberkshire hathaway\b': 'Berkshire Hathaway',
    r'\bexp realty\b': 'eXp Realty',
    r'\bexp\b': 'eXp',
}

def load_progress():
    """Load transcription progress."""
    progress_path = INDEX_DIR / "progress.json"
    with open(progress_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_progress(progress):
    """Save transcription progress."""
    progress_path = INDEX_DIR / "progress.json"
    progress['last_updated'] = datetime.now().isoformat()
    with open(progress_path, 'w', encoding='utf-8') as f:
        json.dump(progress, f, indent=2)

def apply_corrections(text):
    """Apply real estate terminology corrections."""
    for pattern, replacement in REAL_ESTATE_CORRECTIONS.items():
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    return text

def format_timestamp(seconds):
    """Format seconds as HH:MM:SS."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"

def transcribe_episode(mp3_path, model, output_dir):
    """
    Transcribe a single episode.

    Returns:
        dict with 'json_path', 'txt_path', 'success', 'error'
    """
    mp3_path = Path(mp3_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    base_name = mp3_path.stem
    json_path = output_dir / f"{base_name}.json"
    txt_path = output_dir / f"{base_name}.txt"

    try:
        # Transcribe with word-level timestamps
        result = model.transcribe(
            str(mp3_path),
            word_timestamps=True,
            verbose=False
        )

        # Process segments
        segments = []
        full_text_parts = []

        for segment in result['segments']:
            # Apply corrections to segment text
            corrected_text = apply_corrections(segment['text'].strip())

            # Process words if available
            words = []
            if 'words' in segment:
                for word in segment['words']:
                    words.append({
                        'word': apply_corrections(word['word']),
                        'start': round(word['start'], 2),
                        'end': round(word['end'], 2)
                    })

            segment_data = {
                'id': segment['id'],
                'start': round(segment['start'], 2),
                'end': round(segment['end'], 2),
                'start_formatted': format_timestamp(segment['start']),
                'end_formatted': format_timestamp(segment['end']),
                'text': corrected_text,
                'words': words
            }
            segments.append(segment_data)
            full_text_parts.append(corrected_text)

        # Full corrected text
        full_text = apply_corrections(result['text'])

        # Build JSON output
        json_output = {
            'source_file': mp3_path.name,
            'language': result.get('language', 'en'),
            'duration_seconds': segments[-1]['end'] if segments else 0,
            'duration_formatted': format_timestamp(segments[-1]['end']) if segments else '00:00:00',
            'transcribed_at': datetime.now().isoformat(),
            'model_used': model.name if hasattr(model, 'name') else 'whisper',
            'segments': segments,
            'full_text': full_text
        }

        # Save JSON
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(json_output, f, indent=2, ensure_ascii=False)

        # Save plain text with timestamps
        txt_lines = []
        txt_lines.append(f"Transcript: {mp3_path.name}")
        txt_lines.append(f"Duration: {json_output['duration_formatted']}")
        txt_lines.append("=" * 60)
        txt_lines.append("")

        for seg in segments:
            txt_lines.append(f"[{seg['start_formatted']}] {seg['text']}")

        txt_lines.append("")
        txt_lines.append("=" * 60)
        txt_lines.append("FULL TEXT (no timestamps):")
        txt_lines.append("=" * 60)
        txt_lines.append(full_text)

        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(txt_lines))

        return {
            'json_path': str(json_path),
            'txt_path': str(txt_path),
            'success': True,
            'duration': json_output['duration_formatted'],
            'segments': len(segments),
            'error': None
        }

    except Exception as e:
        return {
            'json_path': None,
            'txt_path': None,
            'success': False,
            'error': str(e)
        }

def cleanup_mp3(filename):
    """Delete MP3 file after successful transcription."""
    mp3_path = MP3_DIR / filename
    if mp3_path.exists():
        size_mb = mp3_path.stat().st_size / (1024 * 1024)
        mp3_path.unlink()
        return True, size_mb
    return False, 0

def transcribe_episodes(model_name='base', limit=None, force=False, cleanup=False):
    """
    Transcribe downloaded episodes.

    Args:
        model_name: Whisper model to use (tiny, base, small, medium, large)
        limit: Maximum number of episodes to transcribe
        force: Re-transcribe even if already done
        cleanup: Delete MP3 files after successful transcription
    """
    print(f"Loading Whisper model '{model_name}'...")
    model = whisper.load_model(model_name)
    print(f"Model loaded.\n")

    progress = load_progress()
    TRANSCRIPT_DIR.mkdir(parents=True, exist_ok=True)

    # Get list of downloaded episodes
    downloaded = progress.get('downloaded', [])
    transcribed = set(progress.get('transcribed', []))

    # Filter to episodes that need transcription
    to_transcribe = []
    for filename in downloaded:
        if not force and filename in transcribed:
            continue
        mp3_path = MP3_DIR / filename
        if mp3_path.exists():
            to_transcribe.append(filename)
        if limit and len(to_transcribe) >= limit:
            break

    if not to_transcribe:
        print("No episodes to transcribe.")
        return

    print(f"Transcribing {len(to_transcribe)} episodes...")
    print(f"Output directory: {TRANSCRIPT_DIR}")
    if cleanup:
        print("MP3 cleanup enabled - files will be deleted after transcription\n")
    else:
        print("")

    success_count = 0
    fail_count = 0
    space_freed_mb = 0

    for filename in tqdm(to_transcribe, desc="Transcribing"):
        mp3_path = MP3_DIR / filename

        result = transcribe_episode(mp3_path, model, TRANSCRIPT_DIR)

        if result['success']:
            # Update progress
            if filename not in progress['transcribed']:
                progress['transcribed'].append(filename)
            save_progress(progress)
            success_count += 1

            # Cleanup MP3 if requested
            cleanup_msg = ""
            if cleanup:
                deleted, size_mb = cleanup_mp3(filename)
                if deleted:
                    space_freed_mb += size_mb
                    cleanup_msg = f" [deleted {size_mb:.1f}MB]"

            tqdm.write(f"  ✓ {filename} ({result['duration']}, {result['segments']} segments){cleanup_msg}")
        else:
            fail_count += 1
            tqdm.write(f"  ✗ {filename}: {result['error']}")

    print(f"\n{'='*60}")
    print("Transcription complete!")
    print(f"  Successful: {success_count}")
    print(f"  Failed: {fail_count}")
    print(f"  Total transcribed: {len(progress['transcribed'])}")
    if cleanup and space_freed_mb > 0:
        print(f"  Space freed: {space_freed_mb:.1f} MB")
    print(f"{'='*60}")

def show_status():
    """Show transcription status."""
    progress = load_progress()

    downloaded = len(progress.get('downloaded', []))
    transcribed = len(progress.get('transcribed', []))
    remaining = downloaded - transcribed

    print(f"\n{'='*60}")
    print("TRANSCRIPTION STATUS")
    print(f"{'='*60}")
    print(f"Episodes downloaded: {downloaded}")
    print(f"Episodes transcribed: {transcribed}")
    print(f"Remaining: {remaining}")
    print(f"Last updated: {progress.get('last_updated', 'Never')}")
    print(f"{'='*60}\n")

    # List transcribed files
    if transcribed > 0:
        print("Transcribed episodes:")
        for f in progress['transcribed'][:10]:
            print(f"  - {f}")
        if transcribed > 10:
            print(f"  ... and {transcribed - 10} more")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Transcribe podcast episodes with Whisper")
    parser.add_argument('--model', '-m', default='base',
                       choices=['tiny', 'base', 'small', 'medium', 'large'],
                       help='Whisper model to use (default: base)')
    parser.add_argument('--limit', '-l', type=int, default=None,
                       help='Limit number of episodes to transcribe')
    parser.add_argument('--force', '-f', action='store_true',
                       help='Re-transcribe even if already done')
    parser.add_argument('--cleanup', '-c', action='store_true',
                       help='Delete MP3 files after successful transcription to save space')
    parser.add_argument('--status', action='store_true',
                       help='Show transcription status only')

    args = parser.parse_args()

    if args.status:
        show_status()
    else:
        transcribe_episodes(
            model_name=args.model,
            limit=args.limit,
            force=args.force,
            cleanup=args.cleanup
        )
