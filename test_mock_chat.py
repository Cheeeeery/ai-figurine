import yaml
import os
import sys
import random

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'server'))

from llm_engine import LLMEngine

config_path = os.path.join(os.path.dirname(__file__), 'server', 'config.yaml')
with open(config_path, 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

llm = LLMEngine(config['llm'])

# Load system prompt to verify it's correct
prompt_path = os.path.join(os.path.dirname(__file__), 'prompt', 'system.txt')
with open(prompt_path, 'r', encoding='utf-8') as f:
    system_prompt = f.read()

print("=" * 50)
print("  AI Figurine - Mock Chat Test")
print("=" * 50)
print()
print("=== Loaded System Prompt (first 500 chars) ===")
print(system_prompt[:500])
print()
print("=" * 50)
print("  Simulating 10 rounds of conversation")
print("=" * 50)

test_messages = [
    "你好呀",
    "在干嘛呢",
    "今天好累啊",
    "我想你了",
    "你吃饭了吗",
    "晚安",
    "我心情不好",
    "你在干嘛怎么不回我",
    "我们聊聊天吧",
    "好啦不生气了"
]

for i, msg in enumerate(test_messages, 1):
    print(f"\n--- Round {i} ---")
    print(f"ry: {msg}")
    response = llm.generate_response(msg)
    print(f"人格: {response}")
