import json, re, sys
from collections import Counter

sys.stdout.reconfigure(encoding='utf-8')

with open(r'D:\VPN\LAST\ry\ry.html', 'r', encoding='utf-8') as f:
    content = f.read()

match = re.search(r'window\.CHAT_DATA\s*=\s*(\{.*?\});\s*<', content, re.DOTALL)
data = json.loads(match.group(1))
msgs = data['messages']

# Count all types
types = Counter()
for m in msgs:
    types[m.get('type','')] += 1
print('All message types:')
for t, c in types.most_common():
    print(f'  Type {t}: {c}')

# Show type 1 messages (text)
print('\n=== Type 1 (text) messages ===')
count = 0
for m in msgs:
    if m.get('type') == 1:
        count += 1
        if count <= 10:
            print(f'  Sender: {m.get("sender")}')
            print(f'  Content: {m.get("content","")[:150]}')
            print(f'  RawContent: {m.get("rawContent","")[:150]}')
            print('  ---')
print(f'  Total type 1: {count}')
