BG = "#121212"
SURFACE = "#1e1e1e"
ENTRY_BG = "#0d0d0d"
BUTTON_BG = "#2a2a2a"
BUTTON_ACTIVE = "#3a3a3a"
DISABLED_FG = "#6f6f6f"
FOREGROUND = "#f2f2f2"
ACCENT = "#ffd23f"
ACCENT_DIM = "#4a4417"
DANGER = "#ff6b6b"

TCL_THEME = "clam"


def apply_theme(root):
    root.tk.call("ttk::style", "theme", "use", TCL_THEME)
    root.configure(bg=BG)


def button_kwargs():
    return {
        "bg": BUTTON_BG,
        "fg": FOREGROUND,
        "activebackground": BUTTON_ACTIVE,
        "activeforeground": FOREGROUND,
        "disabledforeground": DISABLED_FG,
        "relief": "flat",
        "highlightthickness": 0,
        "bd": 0,
    }
