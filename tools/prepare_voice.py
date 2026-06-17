import json, re, sys, os, shutil

sys.stdout.reconfigure(encoding='utf-8')

with open(r'D:\VPN\LAST\ry\ry.html', 'r', encoding='utf-8') as f:
    content = f.read()

match = re.search(r'window\.CHAT_DATA\s*=\s*(\{.*?\});\s*<', content, re.DOTALL)
data = json.loads(match.group(1))
msgs = data['messages']

user_id = 'wxid_t7px489jmjag22'

# Extract voice file paths
voice_files = []
for m in msgs:
    if m.get('sender') == user_id and m.get('type') == 34:
        content_text = m.get('content', '')
        # Extract WAV path
        wav_match = re.search(r'voices/[\d/]+_?\d*\.wav', content_text)
        if wav_match:
            voice_files.append(wav_match.group())

print(f"Found {len(voice_files)} voice WAV files")

# Check which ones exist
existing = []
base_dir = r'D:\VPN\LAST\ry'
for vf in voice_files:
    full_path = os.path.join(base_dir, vf)
    if os.path.exists(full_path):
        existing.append(full_path)

print(f"Existing files: {len(existing)}")

# Show first 5
for f in existing[:5]:
    size = os.path.getsize(f)
    print(f"  {f} ({size} bytes)")

# Copy to training folder
train_dir = r'C:\Users\Administrator\Desktop\ai-figurine-v2.1\voice_samples'
os.makedirs(train_dir, exist_ok=True)

copied = 0
for f in existing:
    fname = os.path.basename(f)
    dst = os.path.join(train_dir, fname)
    if not os.path.exists(dst):
        shutil.copy2(f, dst)
        copied += 1

print(f"\nCopied {copied} files to {train_dir}")
print(f"Total training files: {len(os.listdir(train_dir))}")

# Calculate total duration
total_size = sum(os.path.getsize(os.path.join(train_dir, f)) for f in os.listdir(train_dir))
# WAV 16bit 24kHz mono = 48000 bytes/sec
duration_sec = total_size / 48000
print(f"Estimated total duration: {duration_sec:.1f} seconds ({duration_sec/60:.1f} minutes)")
