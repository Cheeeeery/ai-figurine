import json, re, sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta

sys.stdout.reconfigure(encoding='utf-8')

with open(r'D:\VPN\LAST\ry\ry.html', 'r', encoding='utf-8') as f:
    content = f.read()

match = re.search(r'window\.CHAT_DATA\s*=\s*(\{.*?\});\s*<', content, re.DOTALL)
data = json.loads(match.group(1))
msgs = data['messages']
members = {m['id']: m['name'] for m in data['members']}

user_id = 'wxid_t7px489jmjag22'
partner_id = 'wxid_qam4dw12vzik22'
user_name = members[user_id]
partner_name = members[partner_id]

# Extract text messages
user_texts = []
partner_texts = []

for m in msgs:
    if m.get('type') != 1:
        continue
    txt = m.get('content', '').strip()
    if not txt or len(txt) < 1:
        continue
    sid = m.get('sender', '')
    ts = m.get('timestamp', 0)
    is_send = m.get('isSend', False)
    if sid == user_id:
        user_texts.append((ts, txt, is_send))
    elif sid == partner_id:
        partner_texts.append((ts, txt, is_send))

print(f"User ({user_name}) text msgs: {len(user_texts)}")
print(f"Partner ({partner_name}) text msgs: {len(partner_texts)}")

# ==================== Pattern Analysis ====================
def analyze_pattern(texts, label):
    if not texts:
        print(f"\n=== {label}: No texts ===")
        return
    
    print(f"\n{'='*50}")
    print(f"=== {label} Speaking Pattern ===")
    print(f"{'='*50}")
    
    lengths = [len(t) for _, t, _ in texts]
    avg_len = sum(lengths) / len(lengths)
    print(f"  Total messages: {len(texts)}")
    print(f"  Avg length: {avg_len:.1f} chars")
    print(f"  Max length: {max(lengths)}")
    
    # Length distribution
    very_short = sum(1 for l in lengths if l <= 3)
    short = sum(1 for l in lengths if 4 <= l <= 10)
    medium = sum(1 for l in lengths if 11 <= l <= 30)
    long_ = sum(1 for l in lengths if l > 30)
    print(f"  Very short (1-3): {very_short} ({100*very_short/len(texts):.1f}%)")
    print(f"  Short (4-10): {short} ({100*short/len(texts):.1f}%)")
    print(f"  Medium (11-30): {medium} ({100*medium/len(texts):.1f}%)")
    print(f"  Long (>30): {long_} ({100*long_/len(texts):.1f}%)")
    
    # Common words
    all_text = ''.join(t for _, t, _ in texts)
    words = Counter()
    for _, t, _ in texts:
        for w in re.findall(r'[\u4e00-\u9fff]{2,6}', t):
            words[w] += 1
    
    print(f"\n  Top 40 frequent words:")
    for w, c in words.most_common(40):
        if c >= 5:
            print(f"    {w}: {c}")
    
    # Common sentence patterns
    sentence_starts = Counter()
    sentence_ends = Counter()
    for _, t, _ in texts:
        if len(t) >= 2:
            sentence_starts[t[:2]] += 1
            sentence_ends[t[-2:]] += 1
    
    print(f"\n  Top 15 sentence starts:")
    for s, c in sentence_starts.most_common(15):
        print(f"    {s}...: {c}")
    
    print(f"\n  Top 15 sentence endings:")
    for e, c in sentence_ends.most_common(15):
        print(f"    ...{e}: {c}")
    
    # Emoji/bracket usage
    bracket_emojis = re.findall(r'\[([\u4e00-\u9fff]+)\]', all_text)
    emoji_counter = Counter(bracket_emojis)
    print(f"\n  Top 15 WeChat emojis:")
    for e, c in emoji_counter.most_common(15):
        print(f"    [{e}]: {c}")
    
    # Questions
    q_count = sum(1 for _, t, _ in texts if '?' in t or '?' in t or t.endswith('吗') or t.endswith('呢') or t.endswith('嘛') or t.endswith('啊') or t.endswith('不'))
    print(f"\n  Questions: {q_count} ({100*q_count/len(texts):.1f}%)")
    
    # Initiating conversations (time gap analysis)
    times = sorted([ts for ts, _, _ in texts])
    if len(times) > 1:
        gaps = [(times[i+1] - times[i]) for i in range(len(times)-1)]
        avg_gap = sum(gaps) / len(gaps) if gaps else 0
        print(f"  Avg time between own messages: {avg_gap/3600:.1f} hours")
    
    # Time distribution
    hours = Counter()
    for ts, _, _ in texts:
        dt = datetime.fromtimestamp(ts) if ts < 1e12 else datetime.fromtimestamp(ts/1000)
        hours[dt.hour] += 1
    
    print(f"\n  Time distribution:")
    for h in range(24):
        cnt = hours.get(h, 0)
        bar = '#' * min(cnt // 100, 50)
        print(f"    {h:02d}:00 {cnt:5d} {bar}")

analyze_pattern(user_texts, f"{user_name} (ry/你)")
analyze_pattern(partner_texts, f"{partner_name} (渐渐被你吸引丶/对象)")

# ==================== Interaction Analysis ====================
print(f"\n{'='*50}")
print(f"=== Interaction Analysis ===")
print(f"{'='*50}")

# Response time analysis
user_times = sorted([ts for ts, _, _ in user_texts])
partner_times = sorted([ts for ts, _, _ in partner_texts])

# Find conversation pairs (user sends -> partner replies within 10 min)
response_times_to_partner = []
response_times_to_user = []

all_msgs_sorted = sorted(msgs, key=lambda x: x.get('timestamp', 0))

for i in range(len(all_msgs_sorted) - 1):
    curr = all_msgs_sorted[i]
    nxt = all_msgs_sorted[i+1]
    if curr.get('type') != 1 or nxt.get('type') != 1:
        continue
    
    curr_ts = curr.get('timestamp', 0)
    nxt_ts = nxt.get('timestamp', 0)
    gap = nxt_ts - curr_ts
    
    if gap < 0 or gap > 600:  # > 10 min skip
        continue
    
    if curr.get('sender') == user_id and nxt.get('sender') == partner_id:
        response_times_to_partner.append(gap)
    elif curr.get('sender') == partner_id and nxt.get('sender') == user_id:
        response_times_to_user.append(gap)

if response_times_to_partner:
    avg_resp_partner = sum(response_times_to_partner) / len(response_times_to_partner)
    print(f"  Your avg response time to partner: {avg_resp_partner:.0f}s ({avg_resp_partner/60:.1f}min)")
if response_times_to_user:
    avg_resp_user = sum(response_times_to_user) / len(response_times_to_user)
    print(f"  Partner avg response time to you: {avg_resp_user:.0f}s ({avg_resp_user/60:.1f}min)")

# Initiating conversations
user_first_hour = Counter()
partner_first_hour = Counter()
for m in msgs:
    if m.get('type') != 1:
        continue
    ts = m.get('timestamp', 0)
    sid = m.get('sender', '')
    dt = datetime.fromtimestamp(ts) if ts < 1e12 else datetime.fromtimestamp(ts/1000)
    
    # Check if this is first message after 3+ hour gap
    if sid == user_id:
        user_first_hour[dt.hour] += 1
    elif sid == partner_id:
        partner_first_hour[dt.hour] += 1

# ==================== Relationship Timeline ====================
print(f"\n{'='*50}")
print(f"=== Relationship Timeline (Monthly) ===")
print(f"{'='*50}")

monthly_user = Counter()
monthly_partner = Counter()
monthly_total = Counter()

for m in msgs:
    if m.get('type') != 1:
        continue
    ts = m.get('timestamp', 0)
    sid = m.get('sender', '')
    dt = datetime.fromtimestamp(ts) if ts < 1e12 else datetime.fromtimestamp(ts/1000)
    month = dt.strftime('%Y-%m')
    monthly_total[month] += 1
    if sid == user_id:
        monthly_user[month] += 1
    elif sid == partner_id:
        monthly_partner[month] += 1

all_months = sorted(monthly_total.keys())
for month in all_months:
    u = monthly_user.get(month, 0)
    p = monthly_partner.get(month, 0)
    total = u + p
    ratio = f"{100*u/total:.0f}:{100*p/total:.0f}" if total > 0 else "0:0"
    bar_u = '#' * min(u // 50, 30)
    bar_p = '=' * min(p // 50, 30)
    print(f"  {month}: {total:5d} ({ratio}) |{bar_u}{bar_p}")

# ==================== Last 50 messages ====================
print(f"\n{'='*50}")
print(f"=== Last 50 Text Messages ===")
print(f"{'='*50}")

text_msgs = [m for m in msgs if m.get('type') == 1]
for m in text_msgs[-50:]:
    ts = m.get('timestamp', 0)
    sid = m.get('sender', '')
    txt = m.get('content', '')
    dt = datetime.fromtimestamp(ts) if ts < 1e12 else datetime.fromtimestamp(ts/1000)
    name = user_name if sid == user_id else partner_name
    marker = '>>>' if sid == user_id else '   '
    print(f"  {marker} [{dt.strftime('%m-%d %H:%M')}] {name}: {txt}")

# ==================== Emotional Keywords ====================
print(f"\n{'='*50}")
print(f"=== Emotional Keywords ===")
print(f"{'='*50}")

positive_words = ['爱', '喜欢', '想你', '想你了', '开心', '高兴', '幸福', '抱抱', '亲亲', '宝贝', '亲爱的', '么么', '嘻嘻', '哈哈', '好呀', '可以呀', '没问题', '好的呀']
negative_words = ['生气', '烦', '烦死', '讨厌', '不爱', '分手', '滚', '别找我', '不想', '算了', '随便', '无语', '心累', '累', '不想说', '算了', '呵', '哦', '随便你', '无所谓']
neutral_words = ['嗯', '哦', '好吧', '随便', '都行', '无所谓']

user_pos = sum(1 for _, t, _ in user_texts if any(w in t for w in positive_words))
user_neg = sum(1 for _, t, _ in user_texts if any(w in t for w in negative_words))
partner_pos = sum(1 for _, t, _ in partner_texts if any(w in t for w in positive_words))
partner_neg = sum(1 for _, t, _ in partner_texts if any(w in t for w in negative_words))

print(f"  {user_name}: positive={user_pos} ({100*user_pos/len(user_texts):.1f}%), negative={user_neg} ({100*user_neg/len(user_texts):.1f}%)")
print(f"  {partner_name}: positive={partner_pos} ({100*partner_pos/len(partner_texts):.1f}%), negative={partner_neg} ({100*partner_neg/len(partner_texts):.1f}%)")

# Recent emotional shift
recent_user = user_texts[-500:]
recent_partner = partner_texts[-500:]
if recent_user:
    recent_u_pos = sum(1 for _, t, _ in recent_user if any(w in t for w in positive_words))
    recent_u_neg = sum(1 for _, t, _ in recent_user if any(w in t for w in negative_words))
    print(f"\n  Recent 500 msgs - {user_name}: pos={recent_u_pos} neg={recent_u_neg}")
if recent_partner:
    recent_p_pos = sum(1 for _, t, _ in recent_partner if any(w in t for w in positive_words))
    recent_p_neg = sum(1 for _, t, _ in recent_partner if any(w in t for w in negative_words))
    print(f"  Recent 500 msgs - {partner_name}: pos={recent_p_pos} neg={recent_p_neg}")
