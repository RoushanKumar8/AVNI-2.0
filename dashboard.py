import tkinter as tk
import math


class Dashboard:

    BG = "#050814"
    CYAN = "#00E5FF"
    BLUE = "#1769FF"
    TEXT = "#D9F9FF"
    MUTED = "#52758A"

    def __init__(self):

        self.root = tk.Tk()

        self.root.title(
            "AVNI // AI DESKTOP ASSISTANT"
        )

        self.root.geometry(
            "1000x650"
        )

        self.root.configure(
            bg=self.BG
        )

        self.canvas = tk.Canvas(
            self.root,
            bg=self.BG,
            highlightthickness=0
        )

        self.canvas.pack(
            fill="both",
            expand=True
        )

        self.state = "IDLE"

        self.animation = 0

        self.root.bind(
            "<Escape>",
            lambda event: self.root.destroy()
        )

        self.animate()

    def set_state(self, state):

        self.state = state.upper()

    def animate(self):

        self.canvas.delete("all")

        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        if width < 100:
            width = 1000

        if height < 100:
            height = 650

        center_x = width / 2
        center_y = height / 2

        # Grid

        for x in range(0, width, 40):

            self.canvas.create_line(
                x,
                0,
                x,
                height,
                fill="#091526"
            )

        for y in range(0, height, 40):

            self.canvas.create_line(
                0,
                y,
                width,
                y,
                fill="#091526"
            )

        # Header

        self.canvas.create_text(
            40,
            35,
            anchor="w",
            text="AVNI",
            fill=self.CYAN,
            font=("Segoe UI", 25, "bold")
        )

        self.canvas.create_text(
            40,
            65,
            anchor="w",
            text="AI DESKTOP ASSISTANT // ENGLISH MODE",
            fill=self.MUTED,
            font=("Consolas", 9)
        )

        # Status

        self.canvas.create_text(
            width - 40,
            45,
            anchor="e",
            text=f"[ {self.state} ]",
            fill=self.CYAN,
            font=("Consolas", 12, "bold")
        )

        # Animation

        active = self.state != "IDLE"

        self.animation += (
            0.08 if active else 0.025
        )

        # Holographic rings

        for index, radius in enumerate(
            [80, 105, 130, 160]
        ):

            wobble = math.sin(
                self.animation + index
            ) * (5 if active else 2)

            r = radius + wobble

            self.canvas.create_oval(
                center_x - r,
                center_y - r,
                center_x + r,
                center_y + r,
                outline="#0C3852",
                width=2
            )

        # Core

        core = 55

        if active:

            core += math.sin(
                self.animation * 2
            ) * 8

        self.canvas.create_oval(
            center_x - core,
            center_y - core,
            center_x + core,
            center_y + core,
            outline=self.CYAN,
            width=3
        )

        self.canvas.create_text(
            center_x,
            center_y,
            text="AVNI",
            fill=self.TEXT,
            font=("Segoe UI", 18, "bold")
        )

        # Hint

        messages = {

            "IDLE": 'Say "Hey Avni"',

            "LISTENING": "Listening...",

            "THINKING": "Thinking...",

            "SPEAKING": "Speaking..."

        }

        self.canvas.create_text(
            center_x,
            center_y + 210,
            text=messages.get(
                self.state,
                self.state
            ),
            fill=self.MUTED,
            font=("Segoe UI", 13)
        )

        self.root.after(
            40,
            self.animate
        )

    def run(self):

        self.root.mainloop()