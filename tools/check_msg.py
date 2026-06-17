import json, re, sys
from collections import Counter

sys.stdout.reconfigure(encoding='utf-8')

with open(r'D:\VPN\LAST\ry\ry.html', 'r', encoding='utf-8') as f:
    content = f.read()

match = re.search(r'window\.CHAT_DATA\s*=\s*(\{.*?\});\s*<', content, re.DOTALL)
data = json.loads(match.group(1))
msgs = data['messages']

# Check message structure
types = Counter()
for m in msgs[:2000]:
    types[m.get('type','')] += 1
print('Message types:', types)

# Show first 5 messages
for m in msgs[:5]:
    print('Keys:', list(m.keys()))
    print('Type:', m.get('type'))
    print('Sender:', m.get('sender'))
    c = m.get('content','')
    print('Content:', repr(c[:200]) if c else 'NONE')
    print('Timestamp:', m.get('timestamp'))
    print('---')
