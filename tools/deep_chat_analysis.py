import json, re, sys, os
from collections import Counter, defaultdict
from datetime import datetime, timedelta

sys.stdout.reconfigure(encoding='utf-8')

with open(r'D:\VPN\LAST\ry\ry.html', 'r', encoding='utf-8') as f:
    content = f.read()

match = re.search(r'window\.CHAT_DATA\s*=\s*(\{.*?\});\s*<', content, re.DOTALL)
data = json.loads(match.group(1))
msgs = data['messages']
members = {m['id']: m['name'] for m in data['members']}

male_id = 'wxid_qam4dw12vzik22'
female_id = 'wxid_t7px489jmjag22'
male_name = members[male_id]
female_name = members[female_id]

print(f"Male: {male_name} ({male_id})")
print(f"Female: {female_name} ({female_id})")

# Extract text messages
male_texts = []
female_texts = []

for m in msgs:
    if m.get('type') != 1:
        continue
    txt = m.get('content', '').strip()
    if not txt:
        continue
    ts = m.get('timestamp', 0)
    sid = m.get('sender', '')
    if sid == male_id:
        male_texts.append((ts, txt))
    elif sid == female_id:
        female_texts.append((ts, txt))

print(f"Male texts: {len(male_texts)}")
print(f"Female texts: {len(female_texts)}")

# Analyze both people
def analyze(name, texts, label):
    if not texts:
        return {}
    
    all_text = ' '.join(t for _, t in texts)
    
    # Word frequency
    words = Counter()
    for _, t in texts:
        for w in re.findall(r'[\u4e00-\u9fff]{2,6}', t):
            words[w] += 1
    
    # WeChat bracket emojis
    bracket_emojis = re.findall(r'\[([\u4e00-\u9fff]+)\]', all_text)
    emoji_counter = Counter(bracket_emojis)
    
    # Particles
    particles = re.findall(r'[哈嗯哦噢嘿唉呜啊呀吧嘛呢吗么]+', all_text)
    particle_freq = Counter(particles)
    
    # Sentence patterns
    starts = Counter()
    ends = Counter()
    for _, t in texts:
        if len(t) >= 2:
            starts[t[:2]] += 1
            ends[t[-2:]] += 1
    
    # Length distribution
    lengths = [len(t) for _, t in texts]
    avg_len = sum(lengths) / len(lengths)
    
    # Questions
    q_count = sum(1 for _, t in texts if '?' in t or '?' in t or t.endswith('吗') or t.endswith('呢') or t.endswith('嘛'))
    
    # Time distribution
    hours = Counter()
    for ts, _ in texts:
        dt = datetime.fromtimestamp(ts) if ts < 1e12 else datetime.fromtimestamp(ts/1000)
        hours[dt.hour] += 1
    
    # Monthly activity
    monthly = Counter()
    for ts, _ in texts:
        dt = datetime.fromtimestamp(ts) if ts < 1e12 else datetime.fromtimestamp(ts/1000)
        monthly[dt.strftime('%Y-%m')] += 1
    
    # Last 50 messages
    last50 = [(ts, t) for ts, t in texts[-50:]]
    
    return {
        'name': name,
        'label': label,
        'total': len(texts),
        'avg_len': avg_len,
        'top_words': words.most_common(40),
        'top_emojis': emoji_counter.most_common(15),
        'top_particles': particle_freq.most_common(15),
        'top_starts': starts.most_common(15),
        'top_ends': ends.most_common(15),
        'question_rate': q_count / len(texts) * 100,
        'peak_hours': sorted(hours.items(), key=lambda x: -x[1])[:5],
        'monthly': sorted(monthly.items()),
        'last50': last50,
    }

male_analysis = analyze(male_name, male_texts, "male")
female_analysis = analyze(female_name, female_texts, "female")

# Save analysis as JSON for reference
analysis = {
    'male': {k: v for k, v in male_analysis.items() if k != 'last50'},
    'female': {k: v for k, v in female_analysis.items() if k != 'last50'},
    'male_last50': [(datetime.fromtimestamp(ts).strftime('%m-%d %H:%M'), t) for ts, t in male_analysis['last50']],
    'female_last50': [(datetime.fromtimestamp(ts).strftime('%m-%d %H:%M'), t) for ts, t in female_analysis['last50']],
}

with open(r'C:\Users\Administrator\Desktop\ai-figurine-v2.1\tools\chat_analysis.json', 'w', encoding='utf-8') as f:
    json.dump(analysis, f, ensure_ascii=False, indent=2)

print("\n=== Male Analysis ===")
print(f"Avg length: {male_analysis['avg_len']:.1f}")
print(f"Top 10 words: {male_analysis['top_words'][:10]}")
print(f"Top 5 emojis: {male_analysis['top_emojis'][:5]}")
print(f"Top 5 starts: {male_analysis['top_starts'][:5]}")
print(f"Top 5 ends: {male_analysis['top_ends'][:5]}")

print("\n=== Female Analysis ===")
print(f"Avg length: {female_analysis['avg_len']:.1f}")
print(f"Top 10 words: {female_analysis['top_words'][:10]}")
print(f"Top 5 emojis: {female_analysis['top_emojis'][:5]}")
print(f"Top 5 starts: {female_analysis['top_starts'][:5]}")
print(f"Top 5 ends: {female_analysis['top_ends'][:5]}")

print("\n=== Last 50 Messages ===")
all_last50 = []
for ts, t in male_analysis['last50']:
    all_last50.append((ts, male_name, t))
for ts, t in female_analysis['last50']:
    all_last50.append((ts, female_name, t))
all_last50.sort(key=lambda x: x[0])

for ts, name, txt in all_last50[-30:]:
    dt = datetime.fromtimestamp(ts) if ts < 1e12 else datetime.fromtimestamp(ts/1000)
    print(f"  [{dt.strftime('%m-%d %H:%M')}] {name}: {txt[:80]}")
