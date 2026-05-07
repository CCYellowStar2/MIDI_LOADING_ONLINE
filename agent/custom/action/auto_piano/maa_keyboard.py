from __future__ import annotations

import time

from .key_mapping import NOTE_KEY_MAPPING


WIN32_VK = {
    "shift": 0x10,
    "ctrl": 0x11,
    "a": 0x41,
    "b": 0x42,
    "c": 0x43,
    "d": 0x44,
    "e": 0x45,
    "f": 0x46,
    "g": 0x47,
    "h": 0x48,
    "i": 0x49,
    "j": 0x4A,
    "k": 0x4B,
    "l": 0x4C,
    "m": 0x4D,
    "n": 0x4E,
    "o": 0x4F,
    "p": 0x50,
    "q": 0x51,
    "r": 0x52,
    "s": 0x53,
    "t": 0x54,
    "u": 0x55,
    "v": 0x56,
    "w": 0x57,
    "x": 0x58,
    "y": 0x59,
    "z": 0x5A,
}


class MaaKeyboardBridge:
    def __init__(self, controller, hold_seconds: float = 0.01, wait_jobs: bool = False):
        self.controller = controller
        self.hold_seconds = hold_seconds
        self.wait_jobs = wait_jobs
        self.mapping = NOTE_KEY_MAPPING

    def execute_chord(self, midi_notes):
        normal_keys = []
        shift_keys = []
        ctrl_keys = []

        for note in midi_notes:
            action = self.mapping.get(note)
            if not action:
                continue

            key = action.split("+")[-1]
            if "shift+" in action:
                shift_keys.append(key)
            elif "ctrl+" in action:
                ctrl_keys.append(key)
            else:
                normal_keys.append(key)

        self._press_group(normal_keys)
        self._press_group(shift_keys, modifier="shift")
        self._press_group(ctrl_keys, modifier="ctrl")

    def _press_group(self, keys, modifier: str | None = None):
        if not keys:
            return

        if modifier:
            self._post_key_down(WIN32_VK[modifier])

        vk_codes = [WIN32_VK[key] for key in keys if key in WIN32_VK]
        for vk_code in vk_codes:
            self._post_key_down(vk_code)

        time.sleep(self.hold_seconds)

        for vk_code in reversed(vk_codes):
            self._post_key_up(vk_code)

        if modifier:
            self._post_key_up(WIN32_VK[modifier])

    def _post_key_down(self, vk_code: int):
        job = self.controller.post_key_down(vk_code)
        if self.wait_jobs:
            self._wait(job)

    def _post_key_up(self, vk_code: int):
        job = self.controller.post_key_up(vk_code)
        if self.wait_jobs:
            self._wait(job)

    @staticmethod
    def _wait(job):
        wait = getattr(job, "wait", None)
        if wait is not None:
            wait()
