import json, re, sys, os, shutil, wave, struct

sys.stdout.reconfigure(encoding='utf-8')

with open(r'D:\VPN\LAST\ry\ry.html', 'r', encoding='utf-8') as f:
    content = f.read()

match = re.search(r'window\.CHAT_DATA\s*=\s*(\{.*?\});\s*<', content, re.DOTALL)
data = json.loads(match.group(1))
msgs = data['messages']
members = {m['id']: m['name'] for m in data['members']}

# The male user is "渐渐被你吸引丶"
male_id = 'wxid_qam4dw12vzik22'
male_name = members[male_id]
print(f"Extracting voice from: {male_name} ({male_id})")

# Find voice messages from male user (type 34)
voice_files = []
for m in msgs:
    if m.get('sender') == male_id and m.get('type') == 34:
        content_text = m.get('content', '')
        wav_match = re.search(r'voices/[\d/]+_?\d*\.wav', content_text)
        if wav_match:
            voice_files.append(wav_match.group())

print(f"Found {len(voice_files)} voice WAV files")

# Check which exist
base_dir = r'D:\VPN\LAST\ry'
existing = []
for vf in voice_files:
    full_path = os.path.join(base_dir, vf)
    if os.path.exists(full_path):
        existing.append(full_path)

print(f"Existing files: {len(existing)}")

# Analyze and filter for clean samples
good_samples = []
for fpath in existing:
    try:
        with wave.open(fpath, 'rb') as wf:
            frames = wf.getnframes()
            rate = wf.getframerate()
            channels = wf.getnchannels()
            sampwidth = wf.getsampwidth()
            duration = frames / rate
            
            if sampwidth != 2:
                continue
                
            data = wf.readframes(frames)
            samples = struct.unpack(f'<{frames * channels}h', data)
            max_vol = max(abs(s) for s in samples)
            avg_vol = sum(abs(s) for s in samples) / len(samples)
            
            # Filter: 2-15 seconds, has actual audio
            if 2 <= duration <= 15 and max_vol > 1000 and avg_vol > 200:
                good_samples.append({
                    'file': fpath,
                    'duration': duration,
                    'max_vol': max_vol,
                    'avg_vol': avg_vol
                })
    except:
        continue

print(f"Good samples: {len(good_samples)}")

# Sort and select ~5 minutes
good_samples.sort(key=lambda x: x['duration'], reverse=True)
selected = []
target = 300  # 5 min
current = 0
for s in good_samples:
    if current >= target:
        break
    selected.append(s)
    current += s['duration']

print(f"Selected {len(selected)} samples ({current:.1f}s = {current/60:.1f}min)")

# Copy to ljs_voice
output_dir = r'C:\Users\Administrator\Desktop\ai-figurine-v2.1\ljs_voice'
os.makedirs(output_dir, exist_ok=True)

for s in selected:
    dst = os.path.join(output_dir, os.path.basename(s['file']))
    shutil.copy2(s['file'], dst)

print(f"Copied to {output_dir}")
print(f"Total files: {len(os.listdir(output_dir))}")

# Print first 10
for i, s in enumerate(selected[:10]):
    print(f"  {i+1}. {os.path.basename(s['file'])} ({s['duration']:.1f}s)")
