import os
import mido

class MidiProcessor:
    def parse(self, file_path):
        ext = os.path.splitext(file_path)[1].lower()
        
        # 根據副檔名選擇解析引擎
        if ext in ['.mid', '.midi']:
            return self._parse_midi_with_mido(file_path)
        else:
            raise ValueError(f"不支援的檔案格式: {ext}，僅支援 .mid / .midi")

    def _parse_midi_with_mido(self, file_path):
        """使用 mido 解析 MIDI 檔案 (節奏最精準，支援變速，並過濾鼓組)"""
        mid = mido.MidiFile(file_path)
        notes = []
        current_time_sec = 0.0 
        
        for msg in mid:
            current_time_sec += msg.time
            
            # 捕捉按下音符的瞬間 (有些 MIDI 用 velocity=0 代表鬆開)
            if msg.type == 'note_on' and msg.velocity > 0:
                
                # 【新增的過濾邏輯】：如果是第 10 通道 (索引為 9) 的鼓組，就跳過不處理
                if msg.channel == 9:
                    continue
                    
                notes.append({
                    't': current_time_sec, # 絕對秒數
                    'p': msg.note
                })
        
        notes.sort(key=lambda x: x['t'])
        
        return {
            'title': os.path.basename(file_path),
            'author': 'Unknown',
            'bpm': 120, # 僅供顯示
            'duration': mid.length, # 總時長(秒)
            'key': 'Unknown',
            'notes': notes
        }
