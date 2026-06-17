import asyncio
import struct
import math
import random

class TTSEngine:
    def __init__(self, config):
        self.config = config
        self.engine = config.get('engine', 'edge-tts')
        self.voice = config.get('voice', 'zh-CN-YunxiNeural')
        self.rate = config.get('rate', '+0%')
        self.pitch = config.get('pitch', '+0Hz')
    
    async def _edge_tts_generate(self, text):
        import edge_tts
        
        communicate = edge_tts.Communicate(
            text,
            self.voice,
            rate=self.rate,
            pitch=self.pitch
        )
        
        audio_data = b''
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_data += chunk["data"]
        
        return audio_data
    
    def generate(self, text):
        if not text:
            return b''
        
        if self.engine == 'edge-tts':
            return self._edge_tts_generate_sync(text)
        else:
            return self._mock_generate(text)
    
    def _edge_tts_generate_sync(self, text):
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as pool:
                    future = pool.submit(asyncio.run, self._edge_tts_generate(text))
                    return future.result(timeout=30)
            else:
                return loop.run_until_complete(self._edge_tts_generate(text))
        except Exception as e:
            print(f"[TTS] Edge TTS error: {e}")
            return self._mock_generate(text)
    
    def _mock_generate(self, text):
        sample_rate = self.config.get('sample_rate', 16000)
        duration = min(len(text) * 0.15, 5.0)
        num_samples = int(sample_rate * duration)
        
        freq = 220 + random.random() * 100
        samples = []
        for i in range(num_samples):
            t = i / sample_rate
            val = 0.3 * math.sin(2 * math.pi * freq * t)
            val += 0.1 * math.sin(2 * math.pi * freq * 2 * t)
            
            if i < sample_rate * 0.05:
                val *= i / (sample_rate * 0.05)
            elif i > num_samples - sample_rate * 0.1:
                val *= (num_samples - i) / (sample_rate * 0.1)
            
            samples.append(int(val * 32767))
        
        return struct.pack(f'<{len(samples)}h', *samples)
    
    def generate_to_file(self, text, output_path):
        audio_data = self.generate(text)
        if audio_data:
            with open(output_path, 'wb') as f:
                f.write(audio_data)
            return True
        return False
