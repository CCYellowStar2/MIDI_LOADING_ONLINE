import time
from pynput.keyboard import Controller, Key

class KeyboardBridge:
    def __init__(self):
        self.keyboard = Controller()
        # 根據圖片分析的完整映射
        self.mapping = {
            # 低音 Z-M
            60: "z", 61: "shift+z", 62: "x", 63: "ctrl+c", 64: "c", 65: "v", 66: "shift+v",
            67: "b", 68: "shift+b", 69: "n", 70: "ctrl+m", 71: "m",
            # 中音 A-J
            72: "a", 73: "shift+a", 74: "s", 75: "ctrl+d", 76: "d", 77: "f", 78: "shift+f",
            79: "g", 80: "shift+g", 81: "h", 82: "ctrl+j", 83: "j",
            # 高音 Q-U
            84: "q", 85: "shift+q", 86: "w", 87: "ctrl+e", 88: "e", 89: "r", 90: "shift+r",
            91: "t", 92: "shift+t", 93: "y", 94: "ctrl+u", 95: "u"
        }

    def execute_chord(self, midi_notes):
        """和弦並行處理：先按住功能鍵，再敲擊字母鍵"""
        active_keys = []
        needs_shift = False
        needs_ctrl = False

        for note in midi_notes:
            if note in self.mapping:
                action = self.mapping[note]
                if 'shift+' in action: needs_shift = True
                if 'ctrl+' in action: needs_ctrl = True
                active_keys.append(action.split('+')[-1])

        try:
            if needs_shift: self.keyboard.press(Key.shift)
            if needs_ctrl: self.keyboard.press(Key.ctrl)
            
            for k in active_keys: self.keyboard.press(k)
            time.sleep(0.02) # 確保遊戲捕捉到按鍵
            for k in active_keys: self.keyboard.release(k)
            
            if needs_shift: self.keyboard.release(Key.shift)
            if needs_ctrl: self.keyboard.release(Key.ctrl)
        except Exception:
            pass





#                        ____________
#                       |            |
#                       |            |
#                       |            |
#                       |            |
#                       |            |
#                       |            |
#                       |            |
#  _____________________|            |_____________________
# |                                                        |
# |                                                        |
# |                                                        |
# |_____________________              _____________________|
#                       |            |
#                       |            |
#                       |            |
#                       |            |
#                       |            |
#                       |            |
#                       |            |
#                       |            |
#                       |            |
#                       |            |
#                       |            |
#                       |            |
#                       |            |
#                       |            |
#                       |            |
#                       |____________|


# 耶和華是我的牧者，我必不致缺乏。
# 他使我躺臥在青草地上，領我在可安歇的水邊。
# 他使我的靈魂甦醒，為自己的名引導我走義路。
# 我雖然行過死蔭的幽谷，也不怕遭害，因為你與我同在；你的杖，你的竿，都安慰我。
# 在我敵人面前，你為我擺設筵席；你用油膏了我的頭，使我的福杯滿溢。
# 我一生一世必有恩惠慈愛隨著我；我且要住在耶和華的殿中，直到永遠。
# - 詩篇 23篇



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