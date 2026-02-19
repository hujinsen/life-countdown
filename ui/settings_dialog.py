from datetime import datetime

import customtkinter as ctk

from core.settings import save_settings


class SettingsDialog(ctk.CTkToplevel):
    """设置对话框"""

    def __init__(self, parent, settings, on_save):
        super().__init__(parent)
        self.settings = settings
        self.on_save = on_save

        self.title("设置")
        self.geometry("350x280")
        self.resizable(False, False)

        # 居中显示
        self.transient(parent)
        self.grab_set()

        # 计算居中位置
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - 350) // 2
        y = parent.winfo_y() + (parent.winfo_height() - 280) // 2
        self.geometry(f"+{x}+{y}")

        # 出生日期
        self.label_birth = ctk.CTkLabel(self, text="出生日期 (YYYY-MM-DD):")
        self.label_birth.pack(pady=(20, 5))

        self.entry_birth = ctk.CTkEntry(self, width=200)
        self.entry_birth.insert(0, settings.get("birthdate", ""))
        self.entry_birth.pack()

        # 预期寿命
        self.label_lifespan = ctk.CTkLabel(self, text="预期寿命 (年):")
        self.label_lifespan.pack(pady=(15, 5))

        self.entry_lifespan = ctk.CTkEntry(self, width=200)
        self.entry_lifespan.insert(0, str(settings.get("lifespan_years", 75)))
        self.entry_lifespan.pack()

        # 保存按钮
        self.btn_save = ctk.CTkButton(self, text="保存", command=self.save)
        self.btn_save.pack(pady=20)

    def save(self):
        """保存设置"""
        try:
            birthdate = self.entry_birth.get().strip()
            lifespan = int(self.entry_lifespan.get().strip())

            # 验证日期格式
            datetime.strptime(birthdate, "%Y-%m-%d")

            new_settings = {"birthdate": birthdate, "lifespan_years": lifespan}
            save_settings(new_settings)
            self.on_save(new_settings)
            self.destroy()
        except ValueError as e:
            self.label_birth.configure(text=f"错误: 请检查输入格式!", text_color="red")
