import json, re, sys, os
from collections import Counter, defaultdict

sys.stdout.reconfigure(encoding='utf-8')

with open(r'D:\VPN\LAST\ry\ry.html', 'r', encoding='utf-8') as f:
    content = f.read()

match = re.search(r'window\.CHAT_DATA\s*=\s*(\{.*?\});\s*<', content, re.DOTALL)
data = json.loads(match.group(1))
msgs = data['messages']
members = {m['id']: m['name'] for m in data['members']}

print(f"=== Chat Info ===")
print(f"Total messages: {len(msgs)}")
print(f"Members: {members}")

sender_count = Counter()
for m in msgs:
    sid = m.get('sender','')
    sender_count[sid] += 1

user_id = None
partner_id = None
for sid, cnt in sender_count.most_common():
    name = members.get(sid, sid)
    print(f"  {name}: {cnt} messages")
    if user_id is None:
        user_id = sid
    elif partner_id is None:
        partner_id = sid

print(f"\n=== User: {members.get(user_id, user_id)}")
print(f"=== Partner: {members.get(partner_id, partner_id)}")

# Extract text messages only
user_texts = []
partner_texts = []

for m in msgs:
    if m.get('type') != 'text':
        continue
    content_text = m.get('content', '').strip()
    if not content_text or len(content_text) < 2:
        continue
    sid = m.get('sender', '')
    ts = m.get('timestamp', 0)
    if sid == user_id:
        user_texts.append((ts, content_text))
    elif sid == partner_id:
        partner_texts.append((ts, content_text))

print(f"\nUser text msgs: {len(user_texts)}")
print(f"Partner text msgs: {len(partner_texts)}")

# Show recent 30 messages from each person
print(f"\n=== Recent User messages (last 30) ===")
for ts, txt in user_texts[-30:]:
    from datetime import datetime
    dt = datetime.fromtimestamp(ts/1000) if ts > 1e12 else datetime.fromtimestamp(ts)
    print(f"  [{dt.strftime('%Y-%m-%d %H:%M')}] {txt[:100]}")

print(f"\n=== Recent Partner messages (last 30) ===")
for ts, txt in partner_texts[-30:]:
    from datetime import datetime
    dt = datetime.fromtimestamp(ts/1000) if ts > 1e12 else datetime.fromtimestamp(ts)
    print(f"  [{dt.strftime('%Y-%m-%d %H:%M')}] {txt[:100]}")

# Analyze speaking patterns
def analyze_pattern(texts, label):
    print(f"\n=== {label} Speaking Pattern ===")
    
    # Average length
    lengths = [len(t) for _, t in texts]
    avg_len = sum(lengths) / len(lengths) if lengths else 0
    print(f"  Avg message length: {avg_len:.1f} chars")
    
    # Common phrases
    all_text = ' '.join(t for _, t in texts)
    
    # Emoji usage
    import re
    emojis = re.findall(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F900-\U0001F9FF\U00002600-\U000027BF\U0000FE00-\U0000FE0F\U0001F000-\U0001FFFF]', all_text)
    print(f"  Total emojis: {len(emojis)}")
    
    # Common words (simple Chinese tokenization)
    from collections import Counter
    words = []
    for _, t in texts:
        # Extract common patterns
        for pattern in re.findall(r'[\u4e00-\u9fff]{2,4}', t):
            words.append(pattern)
    
    word_count = Counter(words)
    print(f"  Top 30 frequent words/phrases:")
    for word, cnt in word_count.most_common(30):
        print(f"    {word}: {cnt}")
    
    # Common sentence endings
    endings = Counter()
    for _, t in texts:
        if len(t) >= 2:
            endings[t[-2:]] += 1
    print(f"  Top 10 sentence endings:")
    for ending, cnt in endings.most_common(10):
        print(f"    ...{ending}: {cnt}")
    
    # Questions
    questions = [t for _, t in texts if '?' in t or '?' in t or t.endswith('?') or t.endswith('?')]
    print(f"  Questions: {len(questions)} ({100*len(questions)/len(texts):.1f}%)")
    
    # Short msgs vs long msgs
    short = sum(1 for _, t in texts if len(t) <= 5)
    medium = sum(1 for _, t in texts if 5 < len(t) <= 20)
    long = sum(1 for _, t in texts if len(t) > 20)
    print(f"  Short(<=5): {short}, Medium(6-20): {medium}, Long(>20): {long}")
    
    # Time distribution
    from datetime import datetime
    hours = Counter()
    for ts, _ in texts:
        dt = datetime.fromtimestamp(ts/1000) if ts > 1e12 else datetime.fromtimestamp(ts)
        hours[dt.hour] += 1
    peak_hours = sorted(hours.items(), key=lambda x: -x[1])[:5]
    print(f"  Peak hours: {peak_hours}")

analyze_pattern(user_texts, members.get(user_id, 'User'))
analyze_pattern(partner_texts, members.get(partner_id, 'Partner'))

# Timeline analysis - check conversation frequency over months
from datetime import datetime
monthly_user = Counter()
monthly_partner = Counter()
for ts, _ in user_texts:
    dt = datetime.fromtimestamp(ts/1000) if ts > 1e12 else datetime.fromtimestamp(ts)
    monthly_user[dt.strftime('%Y-%m')] += 1
for ts, _ in partner_texts:
    dt = datetime.fromtimestamp(ts/1000) if ts > 1e12 else datetime.fromtimestamp(ts)
    monthly_partner[dt.strftime('%Y-%m')] += 1

all_months = sorted(set(list(monthly_user.keys()) + list(monthly_partner.keys())))
print(f"\n=== Monthly Activity ===")
for month in all_months:
    u = monthly_user.get(month, 0)
    p = monthly_partner.get(month, 0)
    total = u + p
    bar = '#' * min(total // 50, 60)
    print(f"  {month}: User={u:4d} Partner={p:4d} Total={total:5d} {bar}")

# Recent sentiment check - last 200 messages
print(f"\n=== Recent 200 messages (sentiment check) ===")
recent = msgs[-200:]
for m in recent:
    if m.get('type') != 'text':
        continue
    sid = m.get('sender', '')
    txt = m.get('content', '')[:120]
    ts = m.get('timestamp', 0)
    dt = datetime.fromtimestamp(ts/1000) if ts > 1e12 else datetime.fromtimestamp(ts)
    name = members.get(sid, sid)
    marker = '>>> ' if sid == user_id else '    '
    print(f"  {marker}[{dt.strftime('%m-%d %H:%M')}] {name}: {txt}")

# Relationship timeline - key moments
print(f"\n=== Key relationship indicators ===")
# Count daily messages for last 60 days
from datetime import timedelta
now = datetime.now()
daily = Counter()
for ts, _ in user_texts + partner_texts:
    dt = datetime.fromtimestamp(ts/1000) if ts > 1e12 else datetime.fromtimestamp(ts)
    day_str = dt.strftime('%Y-%m-%d')
    daily[day_str] += 1

print(f"  Last 30 days daily message count:")
for i in range(30):
    day = (now - timedelta(days=29-i)).strftime('%Y-%m-%d')
    cnt = daily.get(day, 0)
    bar = '#' * min(cnt // 3, 40)
    print(f"  {day}: {cnt:4d} {bar}")
