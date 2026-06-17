import os, struct, wave, sys

sys.stdout.reconfigure(encoding='utf-8')

voice_dir = r'C:\Users\Administrator\Desktop\ai-figurine-v2.1\voice_samples'
output_dir = r'C:\Users\Administrator\Desktop\ai-figurine-v2.1\voice_train'
os.makedirs(output_dir, exist_ok=True)

files = [f for f in os.listdir(voice_dir) if f.endswith('.wav')]
print(f"Total WAV files: {len(files)}")

# Analyze each file
good_samples = []
for fname in files:
    fpath = os.path.join(voice_dir, fname)
    try:
        with wave.open(fpath, 'rb') as wf:
            frames = wf.getnframes()
            rate = wf.getframerate()
            channels = wf.getnchannels()
            sampwidth = wf.getsampwidth()
            duration = frames / rate
            
            # Read audio data to check volume
            data = wf.readframes(frames)
            if sampwidth == 2:
                samples = struct.unpack(f'<{frames * channels}h', data)
                max_vol = max(abs(s) for s in samples)
                avg_vol = sum(abs(s) for s in samples) / len(samples)
            else:
                continue
            
            # Filter criteria:
            # 1. Duration: 2-15 seconds (good for training)
            # 2. Has actual audio (not silence)
            # 3. Reasonable volume
            if 2 <= duration <= 15 and max_vol > 1000 and avg_vol > 200:
                good_samples.append({
                    'file': fname,
                    'duration': duration,
                    'max_vol': max_vol,
                    'avg_vol': avg_vol,
                    'rate': rate,
                    'channels': channels
                })
    except Exception as e:
        continue

print(f"Good samples (2-15s, with audio): {len(good_samples)}")

# Sort by duration and pick top 50-100 for training
good_samples.sort(key=lambda x: x['duration'], reverse=True)

# Select diverse samples (mix of short and long)
selected = []
target_duration = 300  # 5 minutes total
current_duration = 0

for s in good_samples:
    if current_duration >= target_duration:
        break
    selected.append(s)
    current_duration += s['duration']

print(f"Selected {len(selected)} samples for training")
print(f"Total duration: {current_duration:.1f}s ({current_duration/60:.1f}min)")

# Copy selected files
import shutil
for s in selected:
    src = os.path.join(voice_dir, s['file'])
    dst = os.path.join(output_dir, s['file'])
    shutil.copy2(src, dst)

print(f"\nCopied to {output_dir}")

# Print selection summary
print(f"\n=== Selected Samples ===")
for i, s in enumerate(selected[:20]):
    print(f"  {i+1}. {s['file']} ({s['duration']:.1f}s, vol={s['avg_vol']:.0f})")
if len(selected) > 20:
    print(f"  ... and {len(selected)-20} more")
