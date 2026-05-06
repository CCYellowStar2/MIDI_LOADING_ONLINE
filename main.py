import tkinter as tk
from tkinter import ttk, filedialog
import threading
import time
import psutil
from processor import MidiProcessor
from bridge import KeyboardBridge
from logger import AppLogger

class AIPianoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Piano Aoto Player v0.4.0")
        self.root.geometry("850x720")
        
        self.processor = MidiProcessor()
        self.bridge = KeyboardBridge()
        self.logger = AppLogger()
        
        self.current_song = None
        self.is_playing = False
        self.is_paused = False
        self.keys_rects = {}
        
        # UI 變量
        self.speed = tk.DoubleVar(value=1.0)
        self.transpose = tk.IntVar(value=0)
        self.visual_on = tk.BooleanVar(value=True)
        self.ui_mode_pro = tk.BooleanVar(value=True)
        self.countdown_text = tk.StringVar(value="")
        
        self.setup_ui()
        self.update_cpu_monitor()

    def setup_ui(self):
        # 1. 頂部控制欄
        ctrl_frame = ttk.Frame(self.root)
        ctrl_frame.pack(pady=10, fill="x", padx=20)
        
        ttk.Button(ctrl_frame, text="導入檔案 (MIDI/XML)", command=self.load_midi).pack(side="left", padx=5)
        ttk.Button(ctrl_frame, text="播放/繼續", command=self.start_playback).pack(side="left", padx=5)
        ttk.Button(ctrl_frame, text="暫停", command=self.pause_playback).pack(side="left", padx=5)
        ttk.Button(ctrl_frame, text="停止", command=self.stop_playback).pack(side="left", padx=5)
        
        self.cpu_lbl = ttk.Label(ctrl_frame, text="CPU: 0%", foreground="green")
        self.cpu_lbl.pack(side="right", padx=10)

        # 2. 狀態顯示與紅字倒數
        self.info_lbl = ttk.Label(self.root, text="[等待中] 請導入歌曲", font=("Microsoft JhengHei", 12), justify="center")
        self.info_lbl.pack(pady=5)
        
        self.countdown_lbl = tk.Label(self.root, textvariable=self.countdown_text, font=("Arial", 32, "bold"), fg="red")
        self.countdown_lbl.pack(pady=5)

        # 3. 演奏參數設置區
        set_frame = ttk.LabelFrame(self.root, text="演奏與視覺設定")
        set_frame.pack(pady=5, fill="x", padx=20)
        
        # 播放速度 0.1~5.0
        ttk.Label(set_frame, text="播放速度:").grid(row=0, column=0, padx=5)
        self.speed_scale = ttk.Scale(set_frame, from_=0.1, to=5.0, variable=self.speed, orient="horizontal", length=200, command=self.update_speed_display)
        self.speed_scale.grid(row=0, column=1)
        self.speed_val_lbl = ttk.Label(set_frame, text="1.0x")
        self.speed_val_lbl.grid(row=0, column=2, padx=5)
        
        # 轉調
        ttk.Label(set_frame, text="轉調:").grid(row=0, column=3, padx=5)
        self.tp_spin = ttk.Spinbox(set_frame, from_=-12, to=12, textvariable=self.transpose, width=5)
        self.tp_spin.grid(row=0, column=4)
        
        ttk.Checkbutton(set_frame, text="開啟視覺化", variable=self.visual_on).grid(row=0, column=5, padx=10)

        # 4. 88鍵畫布
        self.setup_visual_canvas()

    def setup_visual_canvas(self):
        v_frame = ttk.LabelFrame(self.root, text="視覺化鋼琴 (88鍵)")
        v_frame.pack(fill="x", padx=10, pady=5)
        self.v_canvas = tk.Canvas(v_frame, width=820, height=120, bg="white")
        self.v_canvas.pack(pady=5)
        
        w = 11.0 # 每個白鍵的基本寬度
        white_idx = 0
        # 繪製白鍵 (MIDI 21-108)
        for midi in range(21, 109):
            if midi % 12 not in [1, 3, 6, 8, 10]:
                x0 = white_idx * w
                rect = self.v_canvas.create_rectangle(x0, 0, x0 + w, 120, fill="white", outline="gray")
                self.keys_rects[midi] = rect
                white_idx += 1
        # 重疊繪製黑鍵
        white_idx = 0
        for midi in range(21, 109):
            if midi % 12 in [1, 3, 6, 8, 10]:
                x0 = (white_idx * w) - (w * 0.3)
                rect = self.v_canvas.create_rectangle(x0, 0, x0 + (w * 0.6), 75, fill="black")
                self.keys_rects[midi] = rect
            else:
                white_idx += 1

    def update_speed_display(self, *args):
        val = round(self.speed.get(), 1)
        self.speed.set(val)
        self.speed_val_lbl.config(text=f"{val}x")
        self.update_info_display()

    def update_info_display(self):
        if not self.current_song: return
        s_factor = self.speed.get()
        # 動態計算當前速度下的總長度
        real_total_duration = (self.current_song['duration'] * (60 / self.current_song['bpm'])) / s_factor
        tm, ts = divmod(int(real_total_duration), 60)
        
        status = "[播放中]" if self.is_playing else "[已停止]"
        if self.is_paused: status = "[暫停中]"
        
        info = f"{status} {self.current_song['title']}\n總時長: {tm:02d}:{ts:02d} (於 {s_factor}x 速度)"
        self.info_lbl.config(text=info)

    def load_midi(self):
        path = filedialog.askopenfilename(filetypes=[
            ("所有支援格式", "*.mid;*.midi;*.xml;*.mxl"),
            ("MIDI files", "*.mid;*.midi"),
            ("MusicXML files", "*.xml;*.mxl")
        ])
        if path:
            try:
                self.current_song = self.processor.parse(path)
                self.update_info_display()
                self.logger.info(f"成功載入: {path}")
            except Exception as e:
                self.logger.error(f"載入失敗: {e}")

    def trigger_key_visual(self, midi_note):
        if not self.visual_on.get() or midi_note not in self.keys_rects: return
        rect = self.keys_rects[midi_note]
        orig_color = "black" if midi_note % 12 in [1, 3, 6, 8, 10] else "white"
        self.v_canvas.itemconfig(rect, fill="cyan")
        self.root.after(150, lambda: self.v_canvas.itemconfig(rect, fill=orig_color))

    def start_playback(self):
        if not self.current_song: return
        if self.is_paused:
            self.is_paused = False
            return
        if not self.is_playing:
            self.is_playing = True
            threading.Thread(target=self.play_engine, daemon=True).start()

    def play_engine(self):
        # 倒數計時邏輯
        for i in range(3, 0, -1):
            if not self.is_playing: 
                self.countdown_text.set("")
                return
            self.countdown_text.set(f"倒數: {i}")
            time.sleep(1)
        
        self.countdown_text.set("GO!")
        self.root.after(1000, lambda: self.countdown_text.set(""))

        start_t = time.time()
        elapsed = 0
        notes = self.current_song['notes']
        bpm_factor = 60 / self.current_song['bpm']
        i = 0
        
        while i < len(notes) and self.is_playing:
            if self.is_paused:
                time.sleep(0.1)
                start_t = time.time() - elapsed
                continue

            current_speed = self.speed.get()
            n = notes[i]
            target_time = (n['t'] * bpm_factor) / current_speed
            
            # 和弦優化：抓取同一時間點的所有音符
            chord_midi = [n['p'] + self.transpose.get()]
            j = i + 1
            while j < len(notes) and abs(notes[j]['t'] - n['t']) < 0.005:
                chord_midi.append(notes[j]['p'] + self.transpose.get())
                j += 1

            # 精確等待
            while elapsed < target_time:
                if not self.is_playing: return
                elapsed = time.time() - start_t
                time.sleep(0.0005)

            # 執行演奏
            self.bridge.execute_chord(chord_midi)
            
            # 視覺化與進度更新
            for m_note in chord_midi:
                self.root.after(0, self.trigger_key_visual, m_note)
            
            # 每隔一小段時間更新一次進度顯示，避免 UI 過載
            if i % 2 == 0:
                self.root.after(0, self.update_playback_timer, elapsed)
            
            i = j 
        
        self.is_playing = False
        self.update_info_display()

    def update_playback_timer(self, elapsed):
        m, s = divmod(int(elapsed), 60)
        # 這裡僅更新時間數值，不重繪整個 info 標籤以節省資源
        current_text = self.info_lbl.cget("text").split("\n")[0]
        self.info_lbl.config(text=f"{current_text}\n當前進度: {m:02d}:{s:02d}")

    def stop_playback(self):
        self.is_playing = False
        self.is_paused = False
        self.countdown_text.set("")

    def pause_playback(self):
        if self.is_playing: self.is_paused = True

    def update_cpu_monitor(self):
        usage = psutil.cpu_percent()
        color = "red" if usage > 80 else "orange" if usage > 50 else "green"
        self.cpu_lbl.config(text=f"CPU: {usage}%", foreground=color)
        self.root.after(1500, self.update_cpu_monitor)

if __name__ == "__main__":
    root = tk.Tk()
    app = AIPianoApp(root)
    root.mainloop()



#                            _ooOoo_  
#                           o8888888o  
#                           88" . "88  
#                           (| -_- |)  
#                            O\ = /O  
#                        ____/`---'\____  
#                      .   ' \\| |# `.  
#                       / \\||| : |||# \  
#                     / _||||| -:- |||||- \  
#                       | | \\\ - #/ | |  
#                     | \_| ''\---/'' | |  
#                      \ .-\__ `-` ___/-. /  
#                   ___`. .' /--.--\ `. . __  
#                ."" '< `.___\_<|>_/___.' >'"".  
#               | | : `- \`.;`\ _ /`;.`/ - ` : | |  
#                 \ \ `-. \_ __\ /__ _/ .-` / /  
#         ======`-.____`-.___\_____/___.-`____.-'======  
#                            `=---='  
#  
#         .............................................  
#                  佛祖保佑             永无BUG 
#          佛曰:  
#                  写字楼里写字间，写字间里程序员；  
#                  程序人员写程序，又拿程序换酒钱。  
#                  酒醒只在网上坐，酒醉还来网下眠；  
#                  酒醉酒醒日复日，网上网下年复年。  
#                  但愿老死电脑间，不愿鞠躬老板前；  
#                  奔驰宝马贵者趣，公交自行程序员。  
#                  别人笑我忒疯癫，我笑自己命太贱；  
#                  不见满街漂亮妹，哪个归得程序员？





#                   .::::.
#                 .::::::::.
#                :::::::::::
#             ..:::::::::::'
#          '::::::::::::'
#            .::::::::::
#       '::::::::::::::..
#            ..::::::::::::.
#          ``::::::::::::::::
#           ::::``:::::::::'        .:::.
#          ::::'   ':::::'       .::::::::.
#        .::::'      ::::     .:::::::'::::.
#       .:::'       :::::  .:::::::::' ':::::.
#      .::'        :::::.:::::::::'      ':::::.
#     .::'         ::::::::::::::'         ``::::.
# ...:::           ::::::::::::'              ``::.
#```` ':.          ':::::::::'                  ::::..
#                   '.:::::'                    ':'````..