from music21 import converter, note, chord
import os

class MidiProcessor:
    def parse(self, file_path):
        midi = converter.parse(file_path)
        notes = []
        for element in midi.flat.notes:
            if isinstance(element, note.Note):
                notes.append({'t': float(element.offset), 'p': element.pitch.midi})
            elif isinstance(element, chord.Chord):
                for n in element.notes:
                    notes.append({'t': float(element.offset), 'p': n.pitch.midi})
        
        notes.sort(key=lambda x: x['t'])
        
        return {
            'title': os.path.basename(file_path),
            'author': 'Unknown',
            'bpm': self._get_bpm(midi),
            'duration': float(midi.duration.quarterLength),
            'key': str(midi.analyze('key')),
            'notes': notes
        }

    def _get_bpm(self, midi):
        # 預設 120，若有標記則提取
        temp = midi.metronomeMarkBoundaries()
        return temp[0][2].number if temp else 120
    


#                      江城子 . 程序员之歌
#
#                  十年生死两茫茫，写程序，到天亮。
#                      千行代码，Bug何处藏。
#                  纵使上线又怎样，朝令改，夕断肠。
#
#                  领导每天新想法，天天改，日日忙。
#                      相顾无言，惟有泪千行。
#                  每晚灯火阑珊处，夜难寐，加班狂。



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