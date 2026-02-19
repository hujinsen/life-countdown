import customtkinter as ctk

from ui.main_window import LifeCountdownApp

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")


if __name__ == "__main__":
    app = LifeCountdownApp()
    app.mainloop()
