import tkinter as tk
from tkinter import Toplevel, ttk, messagebox, colorchooser
import json
import os
import time
import colorsys
import base64
from pathlib import Path

class ShadyCalc:
    def __init__(self, root):
        self.root = root
        self.version = "5.5.0"
        self.font_fam = "Consolas"
        self.last_slot_time = 0
        self.last_slot_idx = -1
        self.res_bypass = "---"
        self.res_rods = "---"
        self.trim = 0
        self.is_topmost = True
        self.scale_factor = 1.0
        self.is_locked = False
        
        self.DATABASE_SPLIT = {
            487: 3350, 492: 3360, 497: 3370, 502: 3380, 507: 3390, 512: 3400, 517: 3410,
            522: 3425, 527: 3435, 532: 3445, 537: 3455, 542: 3465, 547: 3480, 552: 3495,
            557: 3510, 562: 3525, 567: 3540, 572: 3555, 577: 3565, 582: 3575, 587: 3600,
            592: 3620, 597: 3630, 602: 3630, 607: 3640, 612: 3655, 617: 3665, 622: 3680,
            627: 3690, 632: 3705, 637: 3720, 642: 3730, 647: 3740, 652: 3750, 657: 3760,
            662: 3770, 667: 3780, 672: 3790, 677: 3800, 682: 3810, 687: 3820, 692: 3835,
            697: 3850, 702: 3860, 707: 3870, 712: 3880, 717: 3890, 722: 3900, 727: 3910,
            732: 3920, 737: 3930, 742: 3940, 747: 3950, 750: 3955, 752: 3955, 757: 3955,
            762: 3955
        }
        self.DATABASE_LOW = {
            487: 3545, 492: 3555, 497: 3565, 502: 3575, 507: 3585, 512: 3595, 517: 3605,
            522: 3620, 527: 3630, 532: 3640, 537: 3650, 542: 3660, 547: 3675, 552: 3690,
            557: 3705, 562: 3720, 567: 3735, 572: 3750, 577: 3760, 582: 3770, 587: 3795,
            592: 3815, 597: 3825, 602: 3825, 607: 3835, 612: 3850, 617: 3860, 622: 3875,
            627: 3885, 632: 3900, 637: 3915, 642: 3925, 647: 3935, 652: 3945, 657: 3955,
            662: 3965, 667: 3975, 672: 3985, 677: 3995, 682: 4005, 687: 4015, 692: 4030,
            697: 4045, 702: 4055, 707: 4065, 712: 4075, 717: 4085, 722: 4095, 727: 4105,
            732: 4115, 737: 4125, 742: 4135, 747: 4145, 750: 4150, 752: 4150, 757: 4150,
            762: 4150
        }
        self.LANGS = {
            "RU": {
                "head": "ONPS CALCULATOR", "mode": "РЕЖИМ", "sets": "Настройки", "save": "СОХРАНИТЬ",
                "cancel": "ОТМЕНА", "edit": "[ КОНСТРУКТОР ТЕМ ]", "acc": "ЦВЕТ ТЕМЫ", "txt": "ЦВЕТ RODS",
                "slot": "ЯЧЕЙКИ ПАМЯТИ", "bg_op": "ЯРКОСТЬ УЗОРА", "win_op": "ПРОЗРАЧНОСТЬ", "rgb_sp": "СКОРОСТЬ RGB",
                "anim_sp": "СКОРОСТЬ АНИМ.", "pt": "УЗОРЫ", "presets": "ПРЕСЕТЫ", "c_by": "ЦВЕТ BYPASS",
                "c_btn": "ЦВЕТ КНОПОК", "c_bg": "ЦВЕТ ФОНА", "c_pt": "ЦВЕТ УЗОРА", "m1": "Split Dea",
                "m2": "Low Water Dea", "l_title": "ЯЗЫК", "exe": "ВЫПОЛНИТЬ", "c_title": "Конструктор",
                "res": "СБРОС", "ok": "OK", "trim": "ТРИМ", "topmost": "ПОВЕРХ ОКХОН", "scale": "МАСШТАБ", "lock": "ЗАМОК"
            },
            "EN": {
                "head": "ONPS CALCULATOR", "mode": "MODE", "sets": "Settings", "save": "SAVE",
                "cancel": "CANCEL", "edit": "[ THEME DESIGNER ]", "acc": "THEME COLOR", "txt": "RODS COLOR",
                "slot": "MEMORY SLOTS", "bg_op": "PATTERN BRIGHT.", "win_op": "OPACITY", "rgb_sp": "RGB SPEED",
                "anim_sp": "ANIM SPEED", "pt": "PATTERNS", "presets": "PRESETS", "c_by": "BYPASS COLOR",
                "c_btn": "BTNS COLOR", "c_bg": "WINDOW BG", "c_pt": "PATTERN COLOR", "m1": "Split Dea",
                "m2": "Low Water Dea", "l_title": "LANGUAGE", "exe": "EXECUTE", "c_title": "Designer",
                "res": "RESET", "ok": "OK", "trim": "TRIM", "topmost": "ALWAYS ON TOP", "scale": "UI SCALE", "lock": "LOCK UI"
            }
        }
        self.LANGS.update({
            "UA": {
                "head": "ONPS КАЛЬКУЛЯТОР", "mode": "РЕЖИМ", "sets": "Налаштування", "save": "ЗБЕРЕГТИ",
                "cancel": "ВІДМІНА", "edit": "[ КОНСТРУКТОР ТЕМ ]", "acc": "КОЛІР ТЕМИ", "txt": "КОЛІР RODS",
                "slot": "ОСЕРЕДКИ ПАМ'ЯТІ", "bg_op": "ЯСКРАВІСТЬ УЗОРА", "win_op": "ПРОЗОРІСТЬ", "rgb_sp": "ШВИДКІСТЬ RGB",
                "anim_sp": "ШВИДКІСТЬ АНІМ.", "pt": "ВІЗЕРУНКИ", "presets": "ПРЕСЕТИ", "c_by": "КОЛІР BYPASS",
                "c_btn": "КОЛІР КНОПОК", "c_bg": "КОЛІР ФОНУ", "c_pt": "КОЛІР ВІЗЕРУНКУ", "m1": "Split Dea",
                "m2": "Low Water Dea", "l_title": "МОВА", "exe": "ВИКОНАТИ", "c_title": "Конструктор",
                "res": "СКИДАННЯ", "ok": "OK", "trim": "ТРИМ", "topmost": "ПОВЕРХ ВІКОН", "scale": "МАСШТАБ", "lock": "ЗАМОК"
            },
            "DE": {
                "head": "ONPS RECHNER", "mode": "MODUS", "sets": "Setup", "save": "SPEICHERN",
                "cancel": "ABBRECHEN", "edit": "[ DESIGN-DESIGNER ]", "acc": "THEMENFARBE", "txt": "RODS FARBE",
                "slot": "SPEICHER", "bg_op": "MUSTER-HELL.", "win_op": "OPAZITÄT", "rgb_sp": "RGB SPEED",
                "anim_sp": "ANIM SPEED", "pt": "MUSTER", "presets": "PRESETS", "c_by": "BYPASS FARBE",
                "c_btn": "TASTENFARBE", "c_bg": "WINDOW BG", "c_pt": "MUSTERFARBE", "m1": "Split Dea",
                "m2": "Low Water Dea", "l_title": "SPRACHE", "exe": "AUSFÜHREN", "c_title": "Designer",
                "res": "RESET", "ok": "OK", "trim": "TRIM", "topmost": "IMMER OBEN", "scale": "UI SKALIERUNG", "lock": "LOCK"
            },
            "PL": {
                "head": "ONPS KALKULATOR", "mode": "TRYB", "sets": "Opcje", "save": "ZAPISZ",
                "cancel": "ANULUJ", "edit": "[ KREATOR TEMATÓW ]", "acc": "KOLOR TEMATU", "txt": "KOLOR RODS",
                "slot": "PAMIĘĆ", "bg_op": "JASNOŚĆ WZORУ", "win_op": "PRZEZROCZYSTOŚĆ", "rgb_sp": "PRĘDKOŚĆ RGB",
                "anim_sp": "PRĘDKOŚĆ ANIM.", "pt": "WZORY", "presets": "PRESETY", "c_by": "KOLOR BYPASS",
                "c_btn": "KOLOR GUZIKÓW", "c_bg": "TŁO OKNA", "c_pt": "KOLOR WZORU", "m1": "Split Dea",
                "m2": "Low Water Dea", "l_title": "JĘZYK", "exe": "WYKONAJ", "c_title": "Kreator",
                "res": "RESET", "ok": "OK", "trim": "TRIM", "topmost": "NA WIERZCHU", "scale": "SKALA UI", "lock": "BLOKADA"
            }
        })
        self.THEME_MASTER = {"SHADY": "#9B30FF", "NUCLEAR": "#FFD700", "MATRIX": "#00FF00", "ICE": "#00FFFF", "CYBER": "#FF00FF", "GOLD": "#DAAB19", "TOXIC": "#ADFF2F"}
        self.cur_lang = "RU"; self.current_theme = "SHADY"; self.acc_col = "#9B30FF"
        self.text_col = "#00FF00"; self.bypass_col = "#3498db"; self.btn_bg_col = "#151515"
        self.win_bg_col = "#050505"; self.pt_custom_col = "#9B30FF"; self.opacity = 0.1
        self.win_opacity = 1.0; self.rgb_speed = 0.05; self.current_pattern = "GRID"
        self.rgb_mode = 0; self.anim_offset = 0; self.anim_speed = 2.0; self.active_mode = 1
        self.slots = [None]*10; self.reset_mode = False
        self.load_settings_from_docs()
        self.setup_main_window()
        self.apply_style()
        self.main_loop_fx()

    def setup_main_window(self):
        w_base = int(240 * self.scale_factor)
        h_base = int(465 * self.scale_factor)
        self.root.title("ONPS"); self.root.geometry(f"{w_base}x{h_base}")
        self.root.configure(bg=self.win_bg_col)
        self.root.attributes("-topmost", self.is_topmost)
        self.root.resizable(False, False)
        for child in self.root.winfo_children():
            child.destroy()
        self.canvas = tk.Canvas(self.root, width=w_base, height=h_base, bg=self.win_bg_col, highlightthickness=0)
        self.canvas.place(x=0, y=0)
        f_size_set = max(6, int(12 * self.scale_factor))
        self.btn_set = tk.Button(self.root, text="≡", font=("Arial", f_size_set, "bold"), bg=self.win_bg_col, fg="#444", relief="flat", bd=0, activebackground=self.win_bg_col, command=self.open_settings)
        self.btn_set.place(x=int(210 * self.scale_factor), y=int(5 * self.scale_factor))
        f_size_head = max(6, int(11 * self.scale_factor))
        self.lbl_head = tk.Label(self.root, text="ONPS CALCULATOR", bg=self.win_bg_col, font=(self.font_fam, f_size_head, "bold"))
        self.lbl_head.pack(pady=(int(15 * self.scale_factor), 0))
        h_frame = int(45 * self.scale_factor)
        self.entry_frame = tk.Frame(self.root, bg=self.win_bg_col, height=h_frame)
        self.entry_frame.pack_propagate(False)
        self.entry_frame.pack(pady=int(10 * self.scale_factor), padx=int(12 * self.scale_factor), fill="x")
        f_size_disp = max(6, int(18 * self.scale_factor))
        self.display = tk.Entry(self.entry_frame, font=(self.font_fam, f_size_disp, "bold"), justify="center", bg="#0a0a0a", borderwidth=0, highlightthickness=2)
        if self.is_locked:
            self.display.insert(0, "LOCKED")
            self.display.config(state="disabled")
        else:
            self.display.insert(0, "Demand")
            self.display.config(fg="#1a1a1a", font=(self.font_fam, max(6, int(13 * self.scale_factor)), "bold"))
        self.display.bind("<FocusIn>", self.on_focus_in)
        self.display.bind("<FocusOut>", self.on_focus_out)
        self.display.pack(expand=True, fill="both")
        self.f_btn = tk.Frame(self.root, bg=self.win_bg_col)
        self.f_btn.pack(pady=0)
        self.btns_list = []
        w_btn = max(1, int(5 * self.scale_factor))
        f_size_num = max(6, int(14 * self.scale_factor))
        for i, b in enumerate(['1','2','3','4','5','6','7','8','9','C','0','⌫']):
            btn = tk.Button(self.f_btn, text=b, width=w_btn, height=1, font=(self.font_fam, f_size_num, "bold"), relief="flat", bd=0, command=lambda x=b: self.click_num(x))
            btn.grid(row=i//3, column=i%3, padx=int(2 * self.scale_factor), pady=int(2 * self.scale_factor))
            if self.is_locked:
                btn.config(state="disabled")
            self.btns_list.append(btn)
        self.f_trim = tk.Frame(self.root, bg=self.win_bg_col)
        self.f_trim.pack(pady=int(5 * self.scale_factor))
        f_size_trim = max(6, int(10 * self.scale_factor))
        self.btn_trim_minus = tk.Button(self.f_trim, text="-", width=max(1, int(3 * self.scale_factor)), font=(self.font_fam, f_size_trim, "bold"), relief="flat", bd=0, command=lambda: self.change_trim(-5))
        self.btn_trim_minus.pack(side="left", padx=int(5 * self.scale_factor))
        self.lbl_trim = tk.Label(self.f_trim, text="TRIM: 0", font=(self.font_fam, f_size_trim, "bold"), bg=self.win_bg_col)
        self.lbl_trim.pack(side="left", padx=int(10 * self.scale_factor))
        self.btn_trim_plus = tk.Button(self.f_trim, text="+", width=max(1, int(3 * self.scale_factor)), font=(self.font_fam, f_size_trim, "bold"), relief="flat", bd=0, command=lambda: self.change_trim(5))
        self.btn_trim_plus.pack(side="left", padx=int(5 * self.scale_factor))
        if self.is_locked:
            self.btn_trim_minus.config(state="disabled")
            self.btn_trim_plus.config(state="disabled")
        self.exe_btn = tk.Button(self.root, text="EXECUTE", relief="flat", bd=0, command=self.calculate)
        self.exe_btn.pack(pady=(int(4 * self.scale_factor), int(2 * self.scale_factor)), padx=int(18 * self.scale_factor), fill="x", ipady=int(8 * self.scale_factor))
        if self.is_locked:
            self.exe_btn.config(state="disabled")
        self.lbl_auto = tk.Label(self.root, text="", bg=self.win_bg_col, font=(self.font_fam, f_size_trim, "bold"))
        self.lbl_auto.pack()
        self.lbl_rods = tk.Label(self.root, text="", bg=self.win_bg_col, font=(self.font_fam, f_size_trim, "bold"))
        self.lbl_rods.pack()
        f_size_mode = max(6, int(8 * self.scale_factor))
        self.lbl_m = tk.Label(self.root, text="MODE", font=(self.font_fam, f_size_mode, "bold"), bg=self.win_bg_col, fg="white")
        self.lbl_m.pack(pady=(int(2 * self.scale_factor), 0))
        self.m_f = tk.Frame(self.root, bg=self.win_bg_col); self.m_f.pack(pady=int(2 * self.scale_factor), padx=int(12 * self.scale_factor), fill="x")
        self.m_f.grid_columnconfigure(0, weight=1); self.m_f.grid_columnconfigure(1, weight=1)
        f_size_m_btn = max(6, int(7 * self.scale_factor))
        self.btn_m1 = tk.Button(self.m_f, text="Split Dea", font=(self.font_fam, f_size_m_btn, "bold"), relief="flat", command=lambda: self.set_mode(1))
        self.btn_m1.grid(row=0, column=0, sticky="nsew", padx=int(2 * self.scale_factor), ipady=int(6 * self.scale_factor))
        self.btn_m2 = tk.Button(self.m_f, text="Low Water Dea", font=(self.font_fam, f_size_m_btn, "bold"), relief="flat", command=lambda: self.set_mode(2))
        self.btn_m2.grid(row=0, column=1, sticky="nsew", padx=int(2 * self.scale_factor), ipady=int(6 * self.scale_factor))
        if self.is_locked:
            self.btn_m1.config(state="disabled")
            self.btn_m2.config(state="disabled")
        f_size_made = max(5, int(6 * self.scale_factor))
        tk.Label(self.root, text="Made by: Shady", font=("Arial", f_size_made, "bold"), bg=self.win_bg_col, fg="#222").place(x=int(5 * self.scale_factor), y=int(450 * self.scale_factor))

    def change_trim(self, val):
        if self.is_locked:
            return
        self.trim += val
        tr = self.LANGS.get(self.cur_lang, self.LANGS["RU"])
        self.lbl_trim.config(text=f"{tr['trim']}: {self.trim}")

    def on_focus_in(self, e):
        if self.is_locked:
            return
        if self.display.get() == "Demand":
            self.display.delete(0, 'end')
        f_size_disp = max(6, int(18 * self.scale_factor))
        self.display.config(fg="white", font=(self.font_fam, f_size_disp, "bold"))

    def on_focus_out(self, e):
        if self.is_locked:
            return
        if not self.display.get():
            self.display.insert(0, "Demand")
            self.display.config(fg="#1a1a1a", font=(self.font_fam, max(6, int(13 * self.scale_factor)), "bold"))

    def apply_style(self):
        tr = self.LANGS.get(self.cur_lang, self.LANGS["RU"])
        self.root.configure(bg=self.win_bg_col); self.canvas.configure(bg=self.win_bg_col)
        self.root.attributes("-alpha", self.win_opacity)
        self.lbl_head.config(text=tr["head"], fg=self.acc_col)
        self.display.config(highlightbackground=self.acc_col, highlightcolor=self.acc_col)
        self.exe_btn.config(bg=self.acc_col, fg="white", text=tr["exe"])
        self.btn_trim_minus.config(bg=self.btn_bg_col, fg=self.acc_col)
        self.btn_trim_plus.config(bg=self.btn_bg_col, fg=self.acc_col)
        self.lbl_trim.config(text=f"{tr['trim']}: {self.trim}", fg=self.acc_col)
        self.lbl_auto.config(fg=self.bypass_col, text=f"AutoBypass: {self.res_bypass} rpm")
        self.lbl_rods.config(fg=self.text_col, text=f"ControlRods: {self.res_rods} Mw")
        self.lbl_m.config(text=tr["mode"])
        for b in self.btns_list:
            b.config(bg=self.btn_bg_col, fg="#ccc")
        c1, c2 = (self.acc_col, "#151515") if self.active_mode == 1 else ("#151515", self.acc_col)
        f1, f2 = ("white", self.acc_col) if self.active_mode == 1 else (self.acc_col, "white")
        self.btn_m1.config(bg=c1, fg=f1, text=tr["m1"]); self.btn_m2.config(bg=c2, fg=f2, text=tr["m2"])
        self.canvas.delete("pt")
        if self.current_pattern == "NONE":
            return
        pt_base = self.pt_custom_col if self.pt_custom_col else self.acc_col
        r_h = pt_base.lstrip('#'); r,g,b = tuple(int(r_h[i:i+2], 16) for i in (0, 2, 4))
        p_col = f"#{int(r*self.opacity):02x}{int(g*self.opacity):02x}{int(b*self.opacity):02x}"
        w = int(240 * self.scale_factor)
        h = int(465 * self.scale_factor)
        off = self.anim_offset % 20
        if self.current_pattern == "GRID":
            for i in range(0, w+21, 20):
                self.canvas.create_line(i, 0, i, h, fill=p_col, tags="pt")
            for i in range(-20, h+21, 20):
                self.canvas.create_line(0, i+off, w, i+off, fill=p_col, tags="pt")
        elif self.current_pattern == "DOTS":
            for x in range(0, w+21, 20):
                for y in range(-20, h+21, 20):
                    self.canvas.create_oval(x, y+off, x+2, y+2+off, fill=p_col, outline=p_col, tags="pt")
        elif self.current_pattern == "LINES":
            for i in range(-20, h+21, 15):
                self.canvas.create_line(0, i+off, w, i+off, fill=p_col, tags="pt")
        elif self.current_pattern == "CROSS":
            for x in range(0, w+21, 30):
                for y in range(-30, h+31, 30):
                    yo=y+off
                    self.canvas.create_line(x-4,yo,x+4,yo,fill=p_col,tags="pt")
                    self.canvas.create_line(x,yo-4,x,yo+4,fill=p_col,tags="pt")
    def open_settings(self):
        tr = self.LANGS.get(self.cur_lang, self.LANGS["RU"])
        win = Toplevel(self.root)
        win.title(tr["sets"])
        win.geometry("265x640")
        win.configure(bg="#050505")
        self.root.attributes("-topmost", False)
        win.attributes("-topmost", True)
        canv = tk.Canvas(win, bg="#050505", highlightthickness=0)
        canv.pack(side="left", fill="both", expand=True)
        scroll = ttk.Scrollbar(win, orient="vertical", command=canv.yview)
        scroll.pack(side="right", fill="y")
        canv.configure(yscrollcommand=scroll.set)
        scr = tk.Frame(canv, bg="#050505")
        canv.create_window((125, 0), window=scr, anchor="n")
        scr.bind("<Configure>", lambda e: canv.configure(scrollregion=canv.bbox("all")))
        win.bind("<MouseWheel>", lambda e: canv.yview_scroll(int(-1*(e.delta/120)), "units"))
        sl, sb, ss = {"bg": "#050505", "fg": "#555", "font": (self.font_fam, 8, "bold")}, {"bg": "#151515", "fg": "#aaa", "relief": "flat", "bd": 0}, {"bg": "#050505", "fg": "white", "highlightthickness": 0, "troughcolor": "#151515", "orient": "horizontal", "length": 180}
        bck = {"l":self.cur_lang, "t":self.current_theme, "p":self.current_pattern, "o":self.opacity, "wo":self.win_opacity, "rs":self.rgb_speed, "as":self.anim_speed, "ac":self.acc_col, "tm":self.is_topmost, "sf":self.scale_factor, "lk":self.is_locked}
        tk.Label(scr, text=tr["l_title"], **sl).pack(pady=5)
        lf = tk.Frame(scr, bg="#050505")
        lf.pack()
        for l in ["RU", "EN", "UA", "DE", "PL"]:
            tk.Button(lf, text=l, width=3, **sb, command=lambda x=l: [setattr(self, 'cur_lang', x), self.setup_main_window(), self.apply_style(), win.destroy(), self.open_settings()]).pack(side="left", padx=1)
        tk.Label(scr, text=tr["presets"], **sl).pack(pady=10)
        for t in self.THEME_MASTER.keys():
            tk.Button(scr, text=t, width=25, **sb, command=lambda n=t: [setattr(self, 'current_theme', n), setattr(self, 'acc_col', self.THEME_MASTER[n]), setattr(self, 'rgb_mode', 0), self.apply_style(), self.save_settings_to_docs()]).pack(pady=1)
        tk.Label(scr, text=tr["pt"], **sl).pack(pady=10)
        for p in ["GRID", "DOTS", "LINES", "CROSS", "NONE"]:
            tk.Button(scr, text=p, width=25, **sb, command=lambda n=p: [setattr(self, 'current_pattern', n), self.apply_style(), self.save_settings_to_docs()]).pack(pady=1)
        tk.Label(scr, text=tr["bg_op"], **sl).pack(pady=(15,0))
        s1 = tk.Scale(scr, from_=0.0, to=0.5, resolution=0.01, **ss, command=lambda v: [setattr(self, 'opacity', float(v)), self.apply_style()])
        s1.set(self.opacity); s1.pack()
        tk.Label(scr, text=tr["win_op"], **sl).pack()
        s2 = tk.Scale(scr, from_=0.3, to=1.0, resolution=0.05, **ss, command=lambda v: [setattr(self, 'win_opacity', float(v)), self.apply_style()])
        s2.set(self.win_opacity); s2.pack()
        tk.Label(scr, text=tr["rgb_sp"], **sl).pack()
        s3 = tk.Scale(scr, from_=0.0, to=0.2, resolution=0.01, **ss, command=lambda v: setattr(self, 'rgb_speed', float(v)))
        s3.set(self.rgb_speed); s3.pack()
        tk.Label(scr, text=tr["anim_sp"], **sl).pack()
        s4 = tk.Scale(scr, from_=0.0, to=10.0, resolution=0.5, **ss, command=lambda v: setattr(self, 'anim_speed', float(v)))
        s4.set(self.anim_speed); s4.pack()
        tk.Label(scr, text=tr["scale"], **sl).pack(pady=(5,0))
        s_scale = tk.Scale(scr, from_=0.7, to=2.0, resolution=0.1, **ss, command=lambda v: setattr(self, 'scale_factor', float(v)))
        s_scale.set(self.scale_factor)
        s_scale.pack()
        f_chk = tk.Frame(scr, bg="#050505")
        f_chk.pack(pady=10)
        cb_top = tk.Checkbutton(f_chk, text=tr["topmost"], bg="#050505", fg="#aaa", selectcolor="#111", font=(self.font_fam, 8), command=lambda: setattr(self, 'is_topmost', not self.is_topmost))
        if self.is_topmost:
            cb_top.select()
        cb_top.pack(anchor="w")
        cb_lock = tk.Checkbutton(f_chk, text=tr["lock"], bg="#050505", fg="#aaa", selectcolor="#111", font=(self.font_fam, 8), command=lambda: setattr(self, 'is_locked', not self.is_locked))
        if self.is_locked:
            cb_lock.select()
        cb_lock.pack(anchor="w")
        rgb_btn = tk.Button(scr, text=f"RGB: {'ON' if self.rgb_mode else 'OFF'}", width=25, bg="#111", fg="#2ecc71" if self.rgb_mode else "#e74c3c", relief="flat", command=lambda: self.toggle_rgb(rgb_btn))
        rgb_btn.pack(pady=10)
        tk.Button(scr, text=tr["edit"], width=25, bg="#222", fg="cyan", font=(self.font_fam, 8, "bold"), relief="flat", command=self.open_designer).pack(pady=5)
        bf = tk.Frame(scr, bg="#050505")
        bf.pack(pady=15)

        def save_action():
            self.setup_main_window()
            self.apply_style()
            self.root.attributes("-topmost", self.is_topmost)
            self.save_settings_to_docs()
            win.destroy()

        tk.Button(bf, text=tr["save"], width=12, bg="#1a1a1a", fg="#2ecc71", relief="flat", command=save_action).pack(side="left", padx=3)

        def cancel_action():
            self.cur_lang, self.current_theme, self.current_pattern = bck["l"], bck["t"], bck["p"]
            self.opacity, self.win_opacity, self.rgb_speed, self.anim_speed, self.acc_col = bck["o"], bck["wo"], bck["rs"], bck["as"], bck["ac"]
            self.is_topmost, self.scale_factor, self.is_locked = bck["tm"], bck["sf"], bck["lk"]
            self.setup_main_window()
            self.apply_style()
            self.root.attributes("-topmost", self.is_topmost)
            win.destroy()

        tk.Button(bf, text=tr["cancel"], width=12, bg="#1a1a1a", fg="#e74c3c", relief="flat", command=cancel_action).pack(side="left", padx=3)
        tk.Label(win, text=f"v{self.version}", font=("Arial", 6, "bold"), bg="#050505", fg="#222").place(x=5, y=620)
    def open_designer(self):
        tr = self.LANGS.get(self.cur_lang, self.LANGS["RU"])
        te = Toplevel(self.root)
        te.title(tr["c_title"]); te.geometry("280x580"); te.configure(bg="#050505"); te.attributes("-topmost", True)

        def pick(t):
            c = colorchooser.askcolor()[1]
            if c:
                if t=="acc": self.acc_col = c
                elif t=="mw": self.text_col = c
                elif t=="by": self.bypass_col = c
                elif t=="btn": self.btn_bg_col = c
                elif t=="win": self.win_bg_col = c
                elif t=="pt": self.pt_custom_col = c
                self.apply_style()
                self.save_settings_to_docs()

        tk.Label(te, text="DESIGNER", bg="#050505", fg="cyan", font=(self.font_fam, 10, "bold")).pack(pady=10)
        btns = [("acc", tr["acc"]), ("mw", tr["txt"]), ("by", tr["c_by"]), ("btn", tr["c_btn"]), ("win", tr["c_bg"]), ("pt", tr["c_pt"])]
        for k, v in btns:
            tk.Button(te, text=v, width=28, bg="#151515", fg="white", relief="flat", command=lambda x=k: pick(x)).pack(pady=3)
        tk.Label(te, text=tr["slot"], bg="#050505", fg="#555", font=(self.font_fam, 8, "bold")).pack(pady=5)
        self.res_btn = tk.Button(te, text=f"{tr['res']} SLOT: OFF", bg="#111", fg="#aaa", relief="flat", command=self.toggle_reset_mode); self.res_btn.pack(pady=5)
        gs = tk.Frame(te, bg="#050505"); gs.pack()
        self.slot_btns = []
        for i in range(10):
            clr = self.acc_col if self.slots[i] else "#333"
            btn = tk.Button(gs, text=f"S{i+1}", width=4, bg="#111", fg=clr, relief="flat")
            btn.bind("<Button-1>", lambda e, x=i: self.handle_slot_logic(x))
            btn.grid(row=i//5, column=i%5, padx=2, pady=2); self.slot_btns.append(btn)
        tk.Button(te, text=tr["ok"], width=20, bg="#1a1a1a", fg="#2ecc71", relief="flat", command=lambda: [self.save_settings_to_docs(), te.destroy()]).pack(pady=15)
        tk.Label(te, text=f"v{self.version}", font=("Arial", 6, "bold"), bg="#050505", fg="#222").place(x=5, y=560)

    def toggle_reset_mode(self):
        self.reset_mode = not self.reset_mode
        self.res_btn.config(text=f"RESET SLOT: {'ON' if self.reset_mode else 'OFF'}", fg="red" if self.reset_mode else "#aaa")

    def handle_slot_logic(self, i):
        now = time.time()
        if self.reset_mode:
            self.slots[i] = None; self.slot_btns[i].config(fg="#333")
            self.save_settings_to_docs()
        elif i == self.last_slot_idx and (now - self.last_slot_time) < 0.5:
            self.slots[i] = [self.acc_col, self.text_col, self.bypass_col, self.btn_bg_col, self.win_bg_col, self.pt_custom_col]
            self.slot_btns[i].config(fg=self.acc_col)
            self.save_settings_to_docs()
        else:
            if self.slots[i]:
                self.acc_col, self.text_col, self.bypass_col, self.btn_bg_col, self.win_bg_col, self.pt_custom_col = self.slots[i]
                self.apply_style()
            self.last_slot_time, self.last_slot_idx = now, i

    def calculate(self):
        if self.is_locked:
            return
        v_str = self.display.get()
        if v_str == "Demand":
            return
        try:
            val = float(v_str); n = int((val/2)+12)
            if n > 750:
                n = 750
            db = self.DATABASE_SPLIT if self.active_mode == 1 else self.DATABASE_LOW
            if n in db:
                self.res_bypass = n
                self.res_rods = db[n] + self.trim
                self.lbl_auto.config(text=f"AutoBypass: {self.res_bypass} rpm")
                self.lbl_rods.config(text=f"ControlRods: {self.res_rods} Mw")
            else:
                self.shake()
        except:
            self.shake()

    def save_settings_to_docs(self):
        try:
            doc_path = Path.home() / "Documents"
            if not doc_path.exists():
                doc_path.mkdir(parents=True, exist_ok=True)
            file_path = doc_path / "shady_calc_settings.json"
            data = {
                "cur_lang": self.cur_lang, "current_theme": self.current_theme, "acc_col": self.acc_col,
                "text_col": self.text_col, "bypass_col": self.bypass_col, "btn_bg_col": self.btn_bg_col,
                "win_bg_col": self.win_bg_col, "pt_custom_col": self.pt_custom_col, "opacity": self.opacity,
                "win_opacity": self.win_opacity, "rgb_speed": self.rgb_speed, "current_pattern": self.current_pattern,
                "anim_speed": self.anim_speed, "active_mode": self.active_mode, "trim": self.trim,
                "is_topmost": self.is_topmost, "scale_factor": self.scale_factor, "is_locked": self.is_locked, "slots": self.slots
            }
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception:
            pass

    def load_settings_from_docs(self):
        try:
            file_path = Path.home() / "Documents" / "shady_calc_settings.json"
            if file_path.exists():
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.cur_lang = data.get("cur_lang", self.cur_lang)
                self.current_theme = data.get("current_theme", self.current_theme)
                self.acc_col = data.get("acc_col", self.acc_col)
                self.text_col = data.get("text_col", self.text_col)
                self.bypass_col = data.get("bypass_col", self.bypass_col)
                self.btn_bg_col = data.get("btn_bg_col", self.btn_bg_col)
                self.win_bg_col = data.get("win_bg_col", self.win_bg_col)
                self.pt_custom_col = data.get("pt_custom_col", self.pt_custom_col)
                self.opacity = data.get("opacity", self.opacity)
                self.win_opacity = data.get("win_opacity", self.win_opacity)
                self.rgb_speed = data.get("rgb_speed", self.rgb_speed)
                self.current_pattern = data.get("current_pattern", self.current_pattern)
                self.anim_speed = data.get("anim_speed", self.anim_speed)
                self.active_mode = data.get("active_mode", self.active_mode)
                self.trim = data.get("trim", self.trim)
                self.is_topmost = data.get("is_topmost", self.is_topmost)
                self.scale_factor = data.get("scale_factor", self.scale_factor)
                self.is_locked = data.get("is_locked", self.is_locked)
                self.slots = data.get("slots", self.slots)
        except Exception:
            pass

    def main_loop_fx(self):
        if self.rgb_mode:
            h = (time.time() * self.rgb_speed) % 1.0; r,g,b = [int(x*255) for x in colorsys.hsv_to_rgb(h,1,1)]
            self.acc_col = f'#{r:02x}{g:02x}{b:02x}'; self.apply_style()
        if self.anim_speed > 0:
            self.anim_offset += self.anim_speed; self.apply_style()
        self.root.after(50, self.main_loop_fx)

    def click_num(self, v):
        if self.is_locked:
            return
        cur = self.display.get()
        if v == 'C':
            self.display.delete(0, 'end'); self.on_focus_out(None)
        elif v == '⌫':
            if cur != "Demand":
                self.display.delete(len(cur)-1)
                if not self.display.get():
                    self.on_focus_out(None)
        else:
            if cur == "Demand":
                self.display.delete(0, 'end')
            f_size_disp = max(6, int(18 * self.scale_factor))
            self.display.config(fg="white", font=(self.font_fam, f_size_disp, "bold"))
            self.display.insert('end', v)

    def toggle_rgb(self, btn):
        if self.is_locked:
            return
        if self.rgb_mode == 0:
            self.pre_acc, self.rgb_mode = self.acc_col, 1; btn.config(text="RGB: ON", fg="#2ecc71")
        else:
            self.rgb_mode = 0; self.acc_col = self.pre_acc; btn.config(text="RGB: OFF", fg="#e74c3c"); self.apply_style()

    def shake(self):
        if self.is_locked:
            return
        o = self.root.winfo_x()
        for i in range(4):
            self.root.geometry(f"+{o+4}+{self.root.winfo_y()}"), self.root.update(), time.sleep(0.01)
            self.root.geometry(f"+{o-4}+{self.root.winfo_y()}"), self.root.update(), time.sleep(0.01)

    def set_mode(self, m):
        if self.is_locked:
            return
        self.active_mode = m; self.apply_style(); self.save_settings_to_docs()

if __name__ == "__main__":
    root = tk.Tk()
    app = ShadyCalc(root)
    root.mainloop()
