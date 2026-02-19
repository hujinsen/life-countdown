import os
import sys
from datetime import datetime, timedelta

import customtkinter as ctk

from core.calculator import calculate_days_remaining, calculate_total_days
from core.settings import load_settings
from ui.settings_dialog import SettingsDialog


def get_resource_path(relative_path):
    """获取资源文件路径（支持开发和打包后的环境）"""
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller 打包后的临时目录
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), relative_path)


class LifeCountdownApp(ctk.CTk):
    """人生倒计时主应用"""

    def __init__(self):
        super().__init__()

        self.title("人生计时器")
        self.geometry("500x350")
        self.resizable(False, False)

        # 设置窗口图标
        try:
            icon_path = get_resource_path('assets/app.ico')
            if os.path.exists(icon_path):
                self.iconbitmap(icon_path)
        except Exception:
            pass  # 图标加载失败不影响程序运行

        self.settings = load_settings()

        # 顶部标题栏
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", padx=20, pady=(20, 10))

        # 设置按钮（先pack以保持右侧）
        self.settings_btn = ctk.CTkButton(
            self.header_frame,
            text="⚙",
            font=ctk.CTkFont(size=20),
            width=40,
            height=40,
            fg_color="transparent",
            hover_color="#E0E0E0",
            text_color="#333333",
            command=self.open_settings
        )
        self.settings_btn.pack(side="right")

        # 标题（expand填满剩余空间并居中）
        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="人生计时器",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.title_label.pack(side="left", fill="x", expand=True)

        # 中间倒计时显示
        self.countdown_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.countdown_frame.pack(expand=True)

        self.days_row_frame = ctk.CTkFrame(self.countdown_frame, fg_color="transparent")
        self.days_row_frame.pack()

        self.days_label = ctk.CTkLabel(
            self.days_row_frame,
            text="0",
            font=ctk.CTkFont(size=80, weight="bold")
        )
        self.days_label.pack(side="left")

        self.days_text_label = ctk.CTkLabel(
            self.days_row_frame,
            text="天",
            font=ctk.CTkFont(size=20)
        )
        self.days_text_label.pack(side="left", padx=(5, 0), pady=(30, 0))

        # 底部进度条
        self.progress_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.progress_frame.pack(fill="x", padx=40, pady=(10, 30))

        self.progress_bar = ctk.CTkProgressBar(
            self.progress_frame,
            height=20,
            corner_radius=10
        )
        self.progress_bar.pack(fill="x", pady=(0, 10))
        self.progress_bar.set(0)

        self.progress_text = ctk.CTkLabel(
            self.progress_frame,
            text="0%",
            font=ctk.CTkFont(size=14)
        )
        self.progress_text.pack()

        # 更新显示
        self.update_display()

        # 设置午夜更新定时器
        self.schedule_midnight_update()

    def schedule_midnight_update(self):
        """设置定时器在午夜更新天数"""
        now = datetime.now()
        # 计算下一个午夜的时间
        tomorrow = now + timedelta(days=1)
        midnight = datetime(tomorrow.year, tomorrow.month, tomorrow.day, 0, 0, 0)
        # 计算到下一个午夜的毫秒数
        ms_until_midnight = int((midnight - now).total_seconds() * 1000)
        # 设置定时器
        self.after(ms_until_midnight, self.on_midnight)

    def on_midnight(self):
        """午夜时更新显示并设置下一个定时器"""
        self.update_display()
        self.schedule_midnight_update()

    def update_display(self):
        """更新显示内容"""
        birthdate = self.settings.get("birthdate", "1988-07-19")
        lifespan_years = self.settings.get("lifespan_years", 75)

        total_days = calculate_total_days(lifespan_years)
        remaining_days = calculate_days_remaining(birthdate, lifespan_years)
        passed_days = total_days - remaining_days

        # 更新天数显示
        self.days_label.configure(text=str(remaining_days))

        # 更新进度条
        progress = passed_days / total_days if total_days > 0 else 0
        progress = max(0, min(1, progress))
        self.progress_bar.set(progress)

        # 更新进度百分比
        percentage = int(progress * 100)
        self.progress_text.configure(text=f"{percentage}%")

    def open_settings(self):
        """打开设置对话框"""
        dialog = SettingsDialog(self, self.settings, self.on_settings_saved)
        dialog.focus()

    def on_settings_saved(self, new_settings):
        """设置保存后的回调"""
        self.settings = new_settings
        self.update_display()
