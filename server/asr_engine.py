import struct
import random

class ASREngine:
    def __init__(self, config):
        self.config = config
        self.model = None
        self._init_model()
    
    def _init_model(self):
        try:
            from funasr import AutoModel
            self.model = AutoModel(
                model=self.config.get('model', 'paraformer-zh'),
                disable_update=True
            )
            print("[ASR] FunASR model loaded successfully")
        except (ImportError, Exception):
            print("[ASR] FunASR not available, using mock ASR")
            self.model = None
    
    def recognize(self, audio_data):
        if self.model is None:
            return self._mock_recognize(audio_data)
        
        try:
            result = self.model.generate(input=audio_data)
            if result and len(result) > 0:
                return result[0].get('text', '')
            return ''
        except Exception as e:
            print(f"[ASR] Recognition error: {e}")
            return self._mock_recognize(audio_data)
    
    def _mock_recognize(self, audio_data):
        duration = len(audio_data) / (self.config.get('sample_rate', 16000) * 2)
        
        mock_responses = [
            "你好呀",
            "今天过得怎么样",
            "我想你了",
            "晚上吃什么",
            "你在干嘛呢",
            "晚安",
            "早上好",
            "今天天气真好"
        ]
        
        if duration > 0.5:
            return random.choice(mock_responses)
        return ''
