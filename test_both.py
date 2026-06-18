import yaml, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'server'))

from llm_engine import LLMEngine

config_path = os.path.join(os.path.dirname(__file__), 'server', 'config.yaml')
with open(config_path, 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

# Test user persona
print("=== User Persona (渐渐被你吸引丶) ===")
llm = LLMEngine(config['llm'])
with open(os.path.join(os.path.dirname(__file__), 'prompt', 'system.txt'), 'r', encoding='utf-8') as f:
    llm.system_prompt = f.read()

tests = ['在干嘛', '我好累', '想你了', '晚安', '你爱不爱我']
for msg in tests:
    r = llm.generate_response(msg)
    print(f"ry: {msg}")
    print(f"你: {r}")
    print()

# Test ry persona
print("=== ry Persona (女朋友) ===")
llm2 = LLMEngine(config['llm'])
with open(os.path.join(os.path.dirname(__file__), 'prompt', 'personality_ry_disabled.txt'), 'r', encoding='utf-8') as f:
    llm2.system_prompt = f.read()

tests2 = ['在干嘛', '我好累', '想你了', '晚安', '你爱不爱我']
for msg in tests2:
    r = llm2.generate_response(msg)
    print(f"你: {msg}")
    print(f"ry: {r}")
    print()
