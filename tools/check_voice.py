import json, re, sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r'D:\VPN\LAST\ry\ry.html', 'r', encoding='utf-8') as f:
    content = f.read()

match = re.search(r'window\.CHAT_DATA\s*=\s*(\{.*?\});\s*<', content, re.DOTALL)
data = json.loads(match.group(1))
msgs = data['messages']

user_id = 'wxid_t7px489jmjag22'

# Check different message types
for msg_type in [34, 43, 47, 50]:
    voice_msgs = [m for m in msgs if m.get('sender') == user_id and m.get('type') == msg_type]
    if voice_msgs:
        print(f"\n=== Type {msg_type}: {len(voice_msgs)} messages ===")
        m = voice_msgs[0]
        print(f"  content: {m.get('content','')[:200]}")
        raw = m.get('rawContent','')
        print(f"  rawContent (first 300): {raw[:300]}")
        print()

# Also look for silk/amr/audio file references
print("\n=== Searching for audio file references ===")
for m in msgs:
    raw = m.get('rawContent', '')
    if any(ext in raw.lower() for ext in ['.silk', '.amr', '.mp3', '.wav', 'voicemsg', 'audio']):
        if m.get('sender') == user_id:
            print(f"  Type={m.get('type')}, content={m.get('content','')[:50]}")
            print(f"  raw: {raw[:300]}")
            print()
            break
