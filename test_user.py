import yaml, os, sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'server'))

from llm_engine import LLMEngine

# Load user persona
config_path = os.path.join(os.path.dirname(__file__), 'server', 'config.yaml')
with open(config_path, 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

llm = LLMEngine(config['llm'])

# Temporarily swap system prompt
original_prompt = llm.system_prompt
user_prompt_path = os.path.join(os.path.dirname(__file__), 'prompt', 'system.txt')
with open(user_prompt_path, 'r', encoding='utf-8') as f:
    llm.system_prompt = f.read()

print("=" * 50)
print("  Test: User Persona (渐渐被你吸引丶)")
print("  Type 'quit' to exit")
print("=" * 50)
print()

while True:
    try:
        user_input = input("ry: ").strip()
        if not user_input:
            continue
        if user_input.lower() in ('quit', 'exit', 'q'):
            print("再见！")
            break
        response = llm.generate_response(user_input)
        print(f"你: {response}")
        print()
    except KeyboardInterrupt:
        print("\n再见！")
        break

llm.system_prompt = original_prompt
