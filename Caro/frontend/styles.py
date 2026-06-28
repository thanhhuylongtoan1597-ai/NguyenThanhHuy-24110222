import tkinter as tk
from tkinter import ttk

BG_MAIN = '#ffffff'
BG_PANEL = '#f8f9fa'
BG_BTN = '#ffffff'
BG_BTN_HOVER = '#f1f3f5'
FG_DARK = '#212529'
FG_GRAY = '#495057'
COLOR_X = '#228be6'
COLOR_O = '#fa5252'
COLOR_WIN = '#40c057'
COLOR_TEXT_WIN = '#ffffff'
COLOR_ACCENT = '#15aabf'

def setup_styles(root):
    style = ttk.Style()
    style.theme_use('clam')

    style.configure(
        'TCombobox',
        fieldbackground='#ffffff',
        background='#e9ecef',
        foreground=FG_DARK,
        arrowcolor=FG_DARK,
        bordercolor='#dee2e6',
        darkcolor='#dee2e6',
        lightcolor='#dee2e6'
    )
    root.option_add('*TCombobox*Listbox.background', '#ffffff')
    root.option_add('*TCombobox*Listbox.foreground', FG_DARK)
    root.option_add('*TCombobox*Listbox.selectBackground', COLOR_X)
    root.option_add('*TCombobox*Listbox.selectForeground', '#ffffff')

    style.configure(
        'Horizontal.TScale',
        background=BG_PANEL,
        troughcolor='#dee2e6',
        sliderlength=15
    )
    return style
