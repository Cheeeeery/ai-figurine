import yaml
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'server'))

from llm_engine import LLMEngine

config_path = os.path.join(os.path.dirname(__file__), 'server', 'config.yaml')
with open(config_path, 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

llm = LLMEngine(config['llm'])

print("=" * 50)
print("  AI Figurine - Chat Test")
print("  输入消息和人格对话，输入 quit 退出")
print("=" * 50)
print()

while True:
    try:
        user_input = input("你: ").strip()
        if not user_input:
            continue
        if user_input.lower() in ('quit', 'exit', 'q'):
            print("再见！")
            break
        
        response = llm.generate_response(user_input)
        print(f"人格: {response}")
        print()
    except KeyboardInterrupt:
        print("\n再见！")
        break
