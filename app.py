import tkinter as tk
import math
import ctypes
import os
import json
from pynput import mouse, keyboard

# Bật nhận diện DPI để lấy tọa độ pixel gốc
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
except AttributeError:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except:
        pass

class DistanceOverlay:
    def __init__(self, monitor_w, monitor_h, game_w, game_h, scale_percent, sec_pos, sec_w, sec_h):
        self.root = tk.Tk()
        self.root.title("Spotline Info") 
        
        self.monitor_w = monitor_w
        self.STRETCH_X = monitor_w / game_w
        self.STRETCH_Y = monitor_h / game_h
        self.SCALE_RATIO = scale_percent / 100.0
        self.sec_pos = sec_pos

        self.ui_w = 800
        self.ui_h = 300

        # Ép kiểu int tuyệt đối (xóa số thập phân) 
        sec_w_int = int(float(sec_w))
        sec_h_int = int(float(sec_h))
        mon_w_int = int(float(self.monitor_w))

        # Phép chia // 2 đảm bảo luôn ra số nguyên int
        offset_x = (sec_w_int - self.ui_w) // 2
        offset_y = (sec_h_int - self.ui_h) // 2

        if self.sec_pos == "Left":
            self.ui_x = -sec_w_int + offset_x
        else: 
            self.ui_x = mon_w_int + offset_x

        self.ui_y = offset_y

        # Ép cứng dấu + để dùng Tọa độ tuyệt đối (Absolute Coordinates)
        # Nếu ui_x âm, python tự điền thành +-X (cú pháp chuẩn để ném sang màn Left của Tkinter)
        geo_string = f"{self.ui_w}x{self.ui_h}+{self.ui_x}+{self.ui_y}"
        self.root.geometry(geo_string) 
        self.root.attributes('-topmost', True)
        self.root.config(bg='black')

        self.canvas = tk.Canvas(self.root, bg='black', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.is_active = False
        self.ctrl_pressed = False
        self.ratio = None
        self.calib_points = []
        self.measure_points = []
        
        self.info_text = self.canvas.create_text(
            400, 150, 
            text="Spotline OFF", 
            fill="red", 
            font=("Consolas", 32, "bold"), 
            anchor="center",
            justify="center"
        )

        self.kb_listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.ms_listener = mouse.Listener(on_click=self.on_click)
        self.kb_listener.start()
        self.ms_listener.start()

    def calculate_accurate_distance(self, p1, p2):
        dx = ((p2[0] - p1[0]) / self.SCALE_RATIO) / self.STRETCH_X
        dy = ((p2[1] - p1[1]) / self.SCALE_RATIO) / self.STRETCH_Y
        return math.hypot(dx, dy)

    def update_ui(self, text, color):
        self.canvas.itemconfig(self.info_text, text=text, fill=color)

    def on_press(self, key):
        if hasattr(key, 'char') and key.char == ']':
            os._exit(0) 
            
        elif hasattr(key, 'char') and key.char == '[':
            self.is_active = not self.is_active
            status = "ON" if self.is_active else "OFF"
            color = "green" if self.is_active else "red"
            ratio_str = f"{self.ratio:.4f}" if self.ratio else "None"
            self.root.after(0, self.update_ui, f"Spotline {status}\nRatio: {ratio_str} m/px", color)
                
        elif key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
            self.ctrl_pressed = True

    def on_release(self, key):
        if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
            self.ctrl_pressed = False

    def on_click(self, x, y, button, pressed):
        if not self.is_active or button != mouse.Button.middle or not pressed:
            return

        if self.sec_pos == "Left" and x < 0:
            return
        if self.sec_pos == "Right" and x >= self.monitor_w:
            return

        if self.ctrl_pressed:
            self.calib_points.append((x, y))
            if len(self.calib_points) == 1:
                self.root.after(0, self.update_ui, "Calibrating...\nClick point 2", "yellow")
            elif len(self.calib_points) == 2:
                p1, p2 = self.calib_points
                dist_px = self.calculate_accurate_distance(p1, p2)
                if dist_px > 0:
                    self.ratio = 100 / dist_px
                    self.root.after(0, self.update_ui, f"100m Set!\nRatio: {self.ratio:.4f} m/px", "lime")
                self.calib_points.clear()
        else:
            if self.ratio is None:
                self.root.after(0, self.update_ui, "ERROR:\nCtrl + Mid Click 2 points\nto set 100m!", "red")
                return
            
            self.measure_points.append((x, y))
            if len(self.measure_points) == 1:
                self.root.after(0, self.update_ui, "Measuring...\nClick point 2", "cyan")
            elif len(self.measure_points) == 2:
                p1, p2 = self.measure_points
                dist_px = self.calculate_accurate_distance(p1, p2)
                real_dist = dist_px * self.ratio
                self.root.after(0, self.update_ui, f"RESULT:\n{real_dist:.1f} meters", "cyan")
                self.measure_points.clear()

    def run(self):
        self.root.mainloop()

def launch_setup():
    config_data = None
    CONFIG_FILE = "spotline_config.json"
    
    def_scale, def_mw, def_mh, def_gw, def_gh = "100", "1920", "1080", "1920", "1080"
    def_sec_w, def_sec_h = "1920", "1200"
    def_pos = "Left"
    has_config = False
    
    # Bước 1: Đọc Config TRƯỚC KHI tạo cửa sổ
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                saved = json.load(f)
                def_scale = str(saved.get("scale", 100))
                def_mw = str(saved.get("monitor_w", 1920))
                def_mh = str(saved.get("monitor_h", 1080))
                def_gw = str(saved.get("game_w", 1920))
                def_gh = str(saved.get("game_h", 1080))
                def_sec_w = str(saved.get("sec_w", 1920))
                def_sec_h = str(saved.get("sec_h", 1200))
                def_pos = str(saved.get("sec_pos", "Left"))
                has_config = True
        except:
            pass

    # Bước 2: Tạo cửa sổ Setup
    setup = tk.Tk()
    setup.title("Spotline Configuration")
    setup.attributes('-topmost', True)
    
    setup_w = 400
    setup_h = 480
    
    # Bước 3: Đẩy cửa sổ Setup sang màn phụ nếu đã có Config
    if has_config:
        sec_w_int = int(float(def_sec_w))
        sec_h_int = int(float(def_sec_h))
        mon_w_int = int(float(def_mw))

        offset_x = (sec_w_int - setup_w) // 2
        offset_y = (sec_h_int - setup_h) // 2
        
        if def_pos == "Left":
            setup_x = -sec_w_int + offset_x
        else:
            setup_x = mon_w_int + offset_x
            
        # Ép cứng + setup_x để sinh ra tọa độ tuyệt đối (vd: +-1160)
        setup.geometry(f"{setup_w}x{setup_h}+{setup_x}+{offset_y}")
    else:
        # Nếu chưa có Config (mở lần đầu), căn giữa ở màn hình chính
        setup.geometry(f"{setup_w}x{setup_h}")
        setup.eval('tk::PlaceWindow . center')
    
    # Giao diện Form điền dữ liệu
    tk.Label(setup, text="1. Windows Scale (%) :", font=("Arial", 10, "bold")).pack(pady=(10, 0))
    entry_scale = tk.Entry(setup, justify='center', font=("Arial", 12))
    entry_scale.insert(0, def_scale) 
    entry_scale.pack(pady=5)
    
    tk.Label(setup, text="2. Monitor (Resolution X,Y) :", font=("Arial", 10, "bold")).pack(pady=(10, 0))
    frame_mon = tk.Frame(setup)
    frame_mon.pack()
    entry_mon_w = tk.Entry(frame_mon, justify='center', font=("Arial", 12), width=10)
    entry_mon_w.insert(0, def_mw) 
    entry_mon_w.pack(side=tk.LEFT, padx=5)
    entry_mon_h = tk.Entry(frame_mon, justify='center', font=("Arial", 12), width=10)
    entry_mon_h.insert(0, def_mh) 
    entry_mon_h.pack(side=tk.LEFT, padx=5)

    tk.Label(setup, text="3.In Game (Resolution X,Y) :", font=("Arial", 10, "bold")).pack(pady=(10, 0))
    frame_game = tk.Frame(setup)
    frame_game.pack()
    entry_game_w = tk.Entry(frame_game, justify='center', font=("Arial", 12), width=10)
    entry_game_w.insert(0, def_gw) 
    entry_game_w.pack(side=tk.LEFT, padx=5)
    entry_game_h = tk.Entry(frame_game, justify='center', font=("Arial", 12), width=10)
    entry_game_h.insert(0, def_gh) 
    entry_game_h.pack(side=tk.LEFT, padx=5)

    tk.Label(setup, text="4.Second Monitor (Resolution X,Y) :", font=("Arial", 10, "bold")).pack(pady=(10, 0))
    frame_sec = tk.Frame(setup)
    frame_sec.pack()
    entry_sec_w = tk.Entry(frame_sec, justify='center', font=("Arial", 12), width=10)
    entry_sec_w.insert(0, def_sec_w) 
    entry_sec_w.pack(side=tk.LEFT, padx=5)
    entry_sec_h = tk.Entry(frame_sec, justify='center', font=("Arial", 12), width=10)
    entry_sec_h.insert(0, def_sec_h) 
    entry_sec_h.pack(side=tk.LEFT, padx=5)

    tk.Label(setup, text="5.Second Monitor Position :", font=("Arial", 10, "bold")).pack(pady=(10, 0))
    pos_var = tk.StringVar(value=def_pos)
    frame_pos = tk.Frame(setup)
    frame_pos.pack()
    tk.Radiobutton(frame_pos, text="Left", variable=pos_var, value="Left", font=("Arial", 10)).pack(side=tk.LEFT, padx=10)
    tk.Radiobutton(frame_pos, text="Right", variable=pos_var, value="Right", font=("Arial", 10)).pack(side=tk.LEFT, padx=10)
    
    def on_start(event=None):
        nonlocal config_data
        try:
            scale = float(entry_scale.get().strip() or 100.0)
            m_w = float(entry_mon_w.get().strip() or 1920.0)
            m_h = float(entry_mon_h.get().strip() or 1080.0)
            g_w = float(entry_game_w.get().strip() or 1920.0)
            g_h = float(entry_game_h.get().strip() or 1080.0)
            sec_w = float(entry_sec_w.get().strip() or 1920.0)
            sec_h = float(entry_sec_h.get().strip() or 1080.0)
            sec_pos = pos_var.get()
            
            if scale <= 0 or m_w <= 0 or m_h <= 0 or g_w <= 0 or g_h <= 0 or sec_w <= 0 or sec_h <= 0: 
                return
            
            new_config = {
                "scale": scale, "monitor_w": m_w, "monitor_h": m_h,
                "game_w": g_w, "game_h": g_h, "sec_w": sec_w, "sec_h": sec_h, "sec_pos": sec_pos
            }
            try:
                with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                    json.dump(new_config, f, ensure_ascii=False, indent=4)
            except: pass

            config_data = (m_w, m_h, g_w, g_h, scale, sec_pos, sec_w, sec_h)
            setup.destroy()
        except ValueError:
            pass 

    tk.Button(setup, text="Launch Spotline (Enter)", command=on_start, bg="#4CAF50", fg="white", font=("Arial", 11, "bold")).pack(pady=20)
    
    setup.bind('<Return>', on_start)
    entry_scale.focus_set()
    setup.mainloop()
    
    return config_data

if __name__ == "__main__":
    configs = launch_setup()
    if configs is not None:
        app = DistanceOverlay(*configs)
        app.run()
#& "C:/Program Files/Python312/python.exe" -m PyInstaller --noconsole --onefile app.py