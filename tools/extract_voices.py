import json, re, sys, os, base64, urllib.request

sys.stdout.reconfigure(encoding='utf-8')

with open(r'D:\VPN\LAST\ry\ry.html', 'r', encoding='utf-8') as f:
    content = f.read()

match = re.search(r'window\.CHAT_DATA\s*=\s*(\{.*?\});\s*<', content, re.DOTALL)
data = json.loads(match.group(1))
msgs = data['messages']
members = {m['id']: m['name'] for m in data['members']}

user_id = 'wxid_t7px489jmjag22'

# Find voice messages
voice_msgs = []
for m in msgs:
    if m.get('sender') == user_id and m.get('type') == 43:
        voice_msgs.append(m)

print(f"Found {len(voice_msgs)} voice messages from ry")

# Show first 10 with content
for i, m in enumerate(voice_msgs[:10]):
    print(f"  Voice {i+1}: sender={m.get('sender')}, content={m.get('content','')[:100]}")
    print(f"    rawContent={m.get('rawContent','')[:150]}")
    print()
