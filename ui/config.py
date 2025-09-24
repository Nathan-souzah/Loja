import json

CONFIG_FILE = "config.json"

class Config:
    def __init__(self):
        self.load()

    def load(self):
        with open(CONFIG_FILE, "r") as f:
            cfg = json.load(f)
        self.bg_color = cfg.get("bg_color", "#f0f0f0")
        self.fg_color = cfg.get("fg_color", "#000000")
        self.font = cfg.get("font", "Arial 12")
        self.logo = cfg.get("logo", "logo.png")
        self.button_color = cfg.get("button_color", "#007acc")

    def save(self, bg_color=None, fg_color=None, font=None, logo=None, button_color=None):
        cfg = {
            "bg_color": bg_color or self.bg_color,
            "fg_color": fg_color or self.fg_color,
            "font": font or self.font,
            "logo": logo or self.logo,
            "button_color": button_color or self.button_color
        }
        with open(CONFIG_FILE, "w") as f:
            json.dump(cfg, f, indent=4)
        self.load()
