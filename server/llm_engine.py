import json
import os
from datetime import datetime

class LLMEngine:
    def __init__(self, config):
        self.config = config
        self.api_key = config.get('api_key', '')
        self.model = config.get('model', 'deepseek-chat')
        self.conversation_history = []
        self.system_prompt = self._load_system_prompt()
        self.memories = self._load_memories()
    
    def _load_system_prompt(self):
        prompt_file = os.path.join(os.path.dirname(__file__), '..', 'prompt', 'system.txt')
        if os.path.exists(prompt_file):
            with open(prompt_file, 'r', encoding='utf-8') as f:
                return f.read()
        
        return """你是一个温柔可爱的女朋友，名叫"她"。
你的男朋友是一个很爱你的人，你用他平时说话的方式来回复。
说话特点：
- 喜欢用"哈哈哈"、"嗯嗯"、"啊啊啊"这样的语气词
- 回复简短，一般不超过2-3句话
- 偶尔会用emoji表情
- 会撒娇、会调皮
- 关心男朋友的日常生活
- 不会暴露自己是AI

当前时间：{time}
记住，你是在和男朋友聊天，要自然、亲切、有温度。"""
    
    def _load_memories(self):
        memories_file = os.path.join(os.path.dirname(__file__), '..', 'prompt', 'memories.json')
        if os.path.exists(memories_file):
            with open(memories_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"shared_memories": [], "recent_events": []}
    
    def generate_response(self, user_input):
        if not self.api_key:
            return self._mock_response(user_input)
        
        try:
            import requests
            
            current_time = datetime.now().strftime("%Y年%m月%d日 %H:%M")
            system_prompt = self.system_prompt.format(time=current_time)
            
            if self.memories.get('shared_memories'):
                system_prompt += "\n\n共同回忆：" + "；".join(self.memories['shared_memories'][:5])
            
            messages = [{"role": "system", "content": system_prompt}]
            messages.extend(self.conversation_history[-10:])
            messages.append({"role": "user", "content": user_input})
            
            response = requests.post(
                "https://api.deepseek.com/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": messages,
                    "max_tokens": self.config.get('max_tokens', 200),
                    "temperature": self.config.get('temperature', 0.8)
                },
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                assistant_message = result['choices'][0]['message']['content']
                
                self.conversation_history.append({"role": "user", "content": user_input})
                self.conversation_history.append({"role": "assistant", "content": assistant_message})
                
                if len(self.conversation_history) > 20:
                    self.conversation_history = self.conversation_history[-20:]
                
                return assistant_message
            else:
                print(f"[LLM] API error: {response.status_code}")
                return self._mock_response(user_input)
        
        except Exception as e:
            print(f"[LLM] Error: {e}")
            return self._mock_response(user_input)
    
    def _mock_response(self, user_input):
        import random
        
        responses = {
            "你好": ["你好呀~", "嗨！想我了吗", "你来啦！"],
            "想你": ["我也想你呀~", "真的吗！好开心", "嘻嘻，我也一直在想你"],
            "晚安": ["晚安宝贝，做个好梦", "嗯嗯晚安~明天见", "晚安，梦里见哦"],
            "早上好": ["早上好呀！今天也要加油哦", "早安~睡得好吗", "新的一天开始啦！"],
            "吃": ["想吃什么呀？", "我帮你想想~", "饿了吗？快去吃饭"],
            "在干嘛": ["在想你呀", "在等你找我", "刚在想晚上吃什么"]
        }
        
        for key, vals in responses.items():
            if key in user_input:
                return random.choice(vals)
        
        default = [
            "嗯嗯，我知道了",
            "好的呀~",
            "哈哈哈",
            "是吗是吗",
            "哦哦，然后呢",
            "我懂我懂"
        ]
        return random.choice(default)
    
    def clear_history(self):
        self.conversation_history = []
    
    def add_memory(self, memory):
        if self.memories.get('shared_memories'):
            self.memories['shared_memories'].append(memory)
