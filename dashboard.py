import tkinter as tk
import math
import os
import random

from PIL import (
    Image,
    ImageTk,
    ImageEnhance,
    ImageFilter
)


class Dashboard:

    # =========================================================
    # COLORS
    # =========================================================

    BG = "#020611"
    PANEL = "#06112A"
    PANEL_2 = "#071735"

    CYAN = "#00E5FF"
    BLUE = "#1769FF"
    PURPLE = "#9B5CFF"
    PINK = "#D65CFF"

    TEXT = "#E7FAFF"
    MUTED = "#6B91A8"

    # =========================================================
    # INIT
    # =========================================================

    def __init__(self):

        self.root = tk.Tk()

        self.root.title(
            "AVNI // AI DESKTOP ASSISTANT"
        )

        self.root.geometry(
            "1200x760"
        )

        self.root.minsize(
            1000,
            650
        )

        self.root.configure(
            bg=self.BG
        )

        # -----------------------------------------------------
        # CANVAS
        # -----------------------------------------------------

        self.canvas = tk.Canvas(
            self.root,
            bg=self.BG,
            highlightthickness=0
        )

        self.canvas.pack(
            fill="both",
            expand=True
        )

        # -----------------------------------------------------
        # STATE
        # -----------------------------------------------------

        self.state = "IDLE"

        self.animation = 0

        self.wave_animation = 0

        # Random particles
        self.particles = []

        for _ in range(80):

            self.particles.append({
                "x": random.random(),
                "y": random.random(),
                "speed": random.uniform(
                    0.0002,
                    0.001
                ),
                "size": random.choice(
                    [1, 1, 1, 2]
                )
            })

        # -----------------------------------------------------
        # CHARACTER
        # -----------------------------------------------------

        self.character = None
        self.character_glow = None

        self.character_tk = None
        self.character_glow_tk = None

        self.load_character()

        # -----------------------------------------------------
        # CLOSE
        # -----------------------------------------------------

        self.root.bind(
            "<Escape>",
            lambda event: self.root.destroy()
        )

        # -----------------------------------------------------
        # START
        # -----------------------------------------------------

        self.animate()

    # =========================================================
    # CHARACTER
    # =========================================================

    def load_character(self):

        image_path = os.path.join(
            os.path.dirname(__file__),
            "cuteCharacter.webp"
        )

        if not os.path.exists(image_path):

            print(
                "Character not found:",
                image_path
            )

            return

        try:

            image = Image.open(
                image_path
            ).convert("RGBA")

            # -------------------------------------------------
            # RESIZE
            # -------------------------------------------------

            image.thumbnail(
                (500, 500),
                Image.Resampling.LANCZOS
            )

            # -------------------------------------------------
            # REMOVE GREY BACKGROUND
            # -------------------------------------------------

            pixels = image.load()

            w, h = image.size

            for y in range(h):

                for x in range(w):

                    r, g, b, a = pixels[x, y]

                    # Detect grey / near-white background
                    if (
                        r > 180
                        and g > 180
                        and b > 180
                        and max(r, g, b)
                        - min(r, g, b) < 18
                    ):

                        pixels[x, y] = (
                            r,
                            g,
                            b,
                            0
                        )

            # -------------------------------------------------
            # SOFT CHARACTER
            # -------------------------------------------------

            self.character = image

            # -------------------------------------------------
            # CREATE BLUE/PURPLE GLOW
            # -------------------------------------------------

            alpha = image.getchannel("A")

            glow = Image.new(
                "RGBA",
                image.size,
                (
                    0,
                    180,
                    255,
                    0
                )
            )

            glow.putalpha(
                alpha.point(
                    lambda p: int(p * 0.55)
                )
            )

            glow = glow.filter(
                ImageFilter.GaussianBlur(18)
            )

            self.character_glow = glow

            # -------------------------------------------------
            # TK IMAGES
            # -------------------------------------------------

            self.character_tk = ImageTk.PhotoImage(
                self.character
            )

            self.character_glow_tk = ImageTk.PhotoImage(
                self.character_glow
            )

        except Exception as e:

            print(
                "Character loading error:",
                e
            )

    # =========================================================
    # STATE
    # =========================================================

    def set_state(self, state):

        self.state = state.upper()

    # =========================================================
    # ROUNDED RECTANGLE
    # =========================================================

    def rounded_panel(
        self,
        x1,
        y1,
        x2,
        y2,
        radius=18,
        outline=None,
        fill=None,
        width=1
    ):

        if fill is None:
            fill = self.PANEL

        if outline is None:
            outline = "#124C82"

        points = [
            x1 + radius,
            y1,

            x2 - radius,
            y1,

            x2,
            y1 + radius,

            x2,
            y2 - radius,

            x2 - radius,
            y2,

            x1 + radius,
            y2,

            x1,
            y2 - radius,

            x1,
            y1 + radius
        ]

        self.canvas.create_polygon(
            points,
            smooth=True,
            fill=fill,
            outline=outline,
            width=width
        )

    # =========================================================
    # BACKGROUND
    # =========================================================

    def draw_background(
        self,
        width,
        height
    ):

        # Dark horizontal bands

        for i in range(
            0,
            height,
            30
        ):

            shade = (
                "#020714"
                if i % 60 == 0
                else "#020611"
            )

            self.canvas.create_rectangle(
                0,
                i,
                width,
                i + 30,
                fill=shade,
                outline=""
            )

        # Grid

        for x in range(
            0,
            width,
            45
        ):

            self.canvas.create_line(
                x,
                65,
                x,
                height,
                fill="#071326"
            )

        for y in range(
            70,
            height,
            45
        ):

            self.canvas.create_line(
                0,
                y,
                width,
                y,
                fill="#071326"
            )

        # -----------------------------------------------------
        # PARTICLES
        # -----------------------------------------------------

        for p in self.particles:

            p["y"] -= p["speed"]

            if p["y"] < 0:

                p["y"] = 1

            x = p["x"] * width
            y = p["y"] * height

            self.canvas.create_oval(
                x,
                y,
                x + p["size"],
                y + p["size"],
                fill="#164B78",
                outline=""
            )

    # =========================================================
    # HEADER
    # =========================================================

    def draw_header(
        self,
        width
    ):

        # Top line

        self.canvas.create_line(
            0,
            65,
            width,
            65,
            fill="#0D4C78",
            width=1
        )

        # Logo circle

        self.canvas.create_oval(
            24,
            15,
            58,
            49,
            outline=self.CYAN,
            width=2
        )

        self.canvas.create_oval(
            32,
            23,
            50,
            41,
            outline=self.BLUE,
            width=2
        )

        # AVNI

        self.canvas.create_text(
            72,
            32,
            anchor="w",
            text="AVNI",
            fill=self.CYAN,
            font=(
                "Segoe UI",
                27,
                "bold"
            )
        )

        self.canvas.create_text(
            175,
            33,
            anchor="w",
            text="// AI DESKTOP ASSISTANT",
            fill="#5FA9D1",
            font=(
                "Consolas",
                13
            )
        )

        # Status

        status_symbol = {
            "IDLE": "●",
            "LISTENING": "◉",
            "THINKING": "◆",
            "SPEAKING": "◖"
        }

        self.canvas.create_text(
            width - 40,
            32,
            anchor="e",
            text=(
                f"{status_symbol.get(self.state, '●')} "
                f"[ {self.state} ]"
            ),
            fill=self.CYAN,
            font=(
                "Consolas",
                12,
                "bold"
            )
        )

    # =========================================================
    # LEFT PANEL
    # =========================================================

    def draw_left_panel(self):

        x1 = 25
        y1 = 105
        x2 = 330
        y2 = 285

        self.rounded_panel(
            x1,
            y1,
            x2,
            y2,
            outline="#087EC0",
            fill="#06142E",
            width=2
        )

        # Corner accents

        self.canvas.create_line(
            x1 + 18,
            y1,
            x1 + 70,
            y1,
            fill=self.CYAN,
            width=2
        )

        # Microphone circle

        self.canvas.create_oval(
            50,
            135,
            120,
            205,
            outline=self.BLUE,
            width=3
        )

        self.canvas.create_oval(
            60,
            145,
            110,
            195,
            outline=self.PURPLE,
            width=2
        )

        # Mic icon

        self.canvas.create_text(
            85,
            170,
            text="♩",
            fill=self.CYAN,
            font=(
                "Segoe UI",
                30,
                "bold"
            )
        )

        # Greeting

        self.canvas.create_text(
            145,
            145,
            anchor="w",
            text="Hey Avni",
            fill=self.CYAN,
            font=(
                "Segoe UI",
                18,
                "bold"
            )
        )

        self.canvas.create_text(
            145,
            178,
            anchor="w",
            text="I'm here.",
            fill=self.TEXT,
            font=(
                "Segoe UI",
                12
            )
        )

        self.canvas.create_text(
            145,
            200,
            anchor="w",
            text="How can I help",
            fill=self.TEXT,
            font=(
                "Segoe UI",
                12
            )
        )

        self.canvas.create_text(
            145,
            222,
            anchor="w",
            text="you today?",
            fill=self.TEXT,
            font=(
                "Segoe UI",
                12
            )
        )

        # =====================================================
        # STATE PANEL
        # =====================================================

        y1 = 310
        y2 = 650

        self.rounded_panel(
            25,
            y1,
            330,
            y2,
            outline="#075A91",
            fill="#05132C",
            width=2
        )

        states = [
            (
                "IDLE",
                "Waiting for your voice..."
            ),
            (
                "LISTENING",
                "Processing your speech..."
            ),
            (
                "THINKING",
                "Getting the best response..."
            ),
            (
                "SPEAKING",
                "Talking to you..."
            )
        ]

        start_y = 355

        for index, (
            state,
            description
        ) in enumerate(states):

            y = start_y + index * 76

            active = (
                self.state == state
            )

            # Active box

            if active:

                self.rounded_panel(
                    40,
                    y - 30,
                    315,
                    y + 40,
                    radius=12,
                    outline=self.BLUE,
                    fill="#081D45",
                    width=2
                )

            # Icon circle

            self.canvas.create_oval(
                53,
                y - 18,
                88,
                y + 17,
                outline=(
                    self.CYAN
                    if active
                    else "#3D5C91"
                ),
                width=2
            )

            icons = {
                "IDLE": "●",
                "LISTENING": "◉",
                "THINKING": "◆",
                "SPEAKING": "◖"
            }

            self.canvas.create_text(
                70,
                y,
                text=icons[state],
                fill=(
                    self.CYAN
                    if active
                    else "#6D80A5"
                ),
                font=(
                    "Segoe UI",
                    13,
                    "bold"
                )
            )

            self.canvas.create_text(
                105,
                y - 8,
                anchor="w",
                text=state,
                fill=(
                    self.CYAN
                    if active
                    else "#9CC7E2"
                ),
                font=(
                    "Segoe UI",
                    11,
                    "bold"
                )
            )

            self.canvas.create_text(
                105,
                y + 14,
                anchor="w",
                text=description,
                fill="#6B91A8",
                font=(
                    "Segoe UI",
                    9
                )
            )

            if index < 3:

                self.canvas.create_line(
                    50,
                    y + 52,
                    305,
                    y + 52,
                    fill="#10304E"
                )

    # =========================================================
    # RIGHT PANEL
    # =========================================================

    def draw_right_panel(
        self,
        width
    ):

        x1 = width - 335
        x2 = width - 25

        # -----------------------------------------------------
        # TIME
        # -----------------------------------------------------

        self.rounded_panel(
            x1,
            105,
            x2,
            195,
            outline="#087EC0",
            fill="#06142E",
            width=2
        )

        self.canvas.create_text(
            x1 + 30,
            135,
            anchor="w",
            text="◷",
            fill=self.CYAN,
            font=(
                "Segoe UI",
                30
            )
        )

        self.canvas.create_text(
            x1 + 85,
            132,
            anchor="w",
            text="AVNI ONLINE",
            fill=self.CYAN,
            font=(
                "Consolas",
                10,
                "bold"
            )
        )

        self.canvas.create_text(
            x1 + 85,
            158,
            anchor="w",
            text="VOICE SYSTEM",
            fill=self.TEXT,
            font=(
                "Segoe UI",
                12
            )
        )

        # -----------------------------------------------------
        # QUICK ACTIONS
        # -----------------------------------------------------

        self.rounded_panel(
            x1,
            215,
            x2,
            535,
            outline="#087EC0",
            fill="#06142E",
            width=2
        )

        self.canvas.create_text(
            x1 + 25,
            245,
            anchor="w",
            text="Quick Actions",
            fill=self.CYAN,
            font=(
                "Segoe UI",
                17,
                "bold"
            )
        )

        actions = [
            ("◎", "Open Browser"),
            ("♫", "Play Music"),
            ("☁", "Check Weather"),
            ("▤", "Open Notepad"),
            ("▦", "More")
        ]

        start_y = 285

        for index, (
            icon,
            text
        ) in enumerate(actions):

            y = start_y + index * 48

            self.rounded_panel(
                x1 + 18,
                y,
                x2 - 18,
                y + 40,
                radius=12,
                outline="#153F83",
                fill="#081B43",
                width=1
            )

            self.canvas.create_text(
                x1 + 42,
                y + 20,
                text=icon,
                fill=self.PURPLE,
                font=(
                    "Segoe UI",
                    17,
                    "bold"
                )
            )

            self.canvas.create_text(
                x1 + 72,
                y + 20,
                anchor="w",
                text=text,
                fill=self.TEXT,
                font=(
                    "Segoe UI",
                    10
                )
            )

            self.canvas.create_text(
                x2 - 38,
                y + 20,
                text="›",
                fill=self.CYAN,
                font=(
                    "Segoe UI",
                    18
                )
            )

        # -----------------------------------------------------
        # TAGLINE
        # -----------------------------------------------------

        self.rounded_panel(
            x1,
            555,
            x2,
            650,
            outline="#087EC0",
            fill="#06142E",
            width=2
        )

        self.canvas.create_text(
            x1 + 25,
            580,
            anchor="w",
            text="Always here",
            fill=self.TEXT,
            font=(
                "Segoe UI",
                15,
                "italic"
            )
        )

        self.canvas.create_text(
            x1 + 25,
            610,
            anchor="w",
            text="for you ♡",
            fill=self.PURPLE,
            font=(
                "Segoe UI",
                15,
                "italic"
            )
        )

        self.draw_waveform(
            x2 - 100,
            605,
            75,
            30
        )

    # =========================================================
    # CHARACTER
    # =========================================================

    def draw_character(
        self,
        width,
        height
    ):

        if self.character_tk is None:

            return

        center_x = width / 2

        # Center area

        center_y = (
            height / 2
            + 30
        )

        # Floating motion

        floating = math.sin(
            self.animation * 1.5
        ) * 4

        y = center_y + floating

        # -----------------------------------------------------
        # LARGE GLOW
        # -----------------------------------------------------

        glow_size = (
            330
            + math.sin(
                self.animation * 2
            ) * 10
        )

        self.canvas.create_oval(
            center_x - glow_size,
            y - glow_size,
            center_x + glow_size,
            y + glow_size,
            outline="#071F42",
            width=2
        )

        # -----------------------------------------------------
        # HOLOGRAM CIRCLES
        # -----------------------------------------------------

        active = (
            self.state != "IDLE"
        )

        for i, radius in enumerate(
            [185, 205, 225]
        ):

            pulse = math.sin(
                self.animation * 2
                + i
            ) * 7

            r = radius + pulse

            self.canvas.create_oval(
                center_x - r,
                y - r,
                center_x + r,
                y + r,
                outline=(
                    "#15518B"
                    if not active
                    else "#087EC0"
                ),
                width=2
            )

        # -----------------------------------------------------
        # GLOW IMAGE
        # -----------------------------------------------------

        if self.character_glow_tk:

            self.canvas.create_image(
                center_x,
                y,
                image=self.character_glow_tk,
                anchor="center"
            )

        # -----------------------------------------------------
        # CHARACTER
        # -----------------------------------------------------

        self.canvas.create_image(
            center_x,
            y,
            image=self.character_tk,
            anchor="center"
        )

        # -----------------------------------------------------
        # SCAN EFFECT
        # ONLY AT EDGES, NOT OVER FACE
        # -----------------------------------------------------

        if active:

            for i in range(5):

                scan_y = (
                    y - 190
                    + (
                        (
                            self.animation * 45
                            + i * 50
                        ) % 380
                    )
                )

                self.canvas.create_line(
                    center_x - 210,
                    scan_y,
                    center_x - 175,
                    scan_y,
                    fill="#00E5FF",
                    width=1
                )

                self.canvas.create_line(
                    center_x + 175,
                    scan_y,
                    center_x + 210,
                    scan_y,
                    fill="#00E5FF",
                    width=1
                )

    # =========================================================
    # PLATFORM
    # =========================================================

    def draw_platform(
        self,
        width,
        height
    ):

        center_x = width / 2

        y = height - 90

        # Outer glow

        for i in range(4):

            offset = i * 7

            self.canvas.create_oval(
                center_x - 245 - offset,
                y - 22 - offset / 4,
                center_x + 245 + offset,
                y + 22 + offset / 4,
                outline=(
                    "#153C77"
                    if i > 1
                    else "#155DB4"
                ),
                width=2
            )

        # Main platform

        self.canvas.create_oval(
            center_x - 225,
            y - 17,
            center_x + 225,
            y + 17,
            outline=self.CYAN,
            width=3
        )

        # Inner platform

        self.canvas.create_oval(
            center_x - 180,
            y - 9,
            center_x + 180,
            y + 9,
            outline=self.PURPLE,
            width=2
        )

        # Prompt

        prompt = {
            "IDLE": 'Say "Hey Avni"',
            "LISTENING": "Listening...",
            "THINKING": "Thinking...",
            "SPEAKING": "Speaking..."
        }

        self.canvas.create_text(
            center_x,
            y + 48,
            text=prompt.get(
                self.state,
                self.state
            ),
            fill=self.CYAN,
            font=(
                "Segoe UI",
                17,
                "bold"
            )
        )

    # =========================================================
    # WAVEFORM
    # =========================================================

    def draw_waveform(
        self,
        center_x,
        center_y,
        width,
        height
    ):

        points = []

        for i in range(40):

            x = (
                center_x
                - width / 2
                + (
                    width / 39
                ) * i
            )

            wave = math.sin(
                self.wave_animation
                + i * 0.55
            )

            wave2 = math.sin(
                self.wave_animation * 1.7
                + i * 0.21
            )

            amp = (
                abs(wave)
                * height
                * 0.5
                * (
                    0.5
                    + abs(wave2) * 0.5
                )
            )

            points.append(
                (x, center_y - amp)
            )

        for i in range(
            len(points) - 1
        ):

            self.canvas.create_line(
                points[i][0],
                points[i][1],
                points[i + 1][0],
                points[i + 1][1],
                fill=self.CYAN,
                width=2
            )

    # =========================================================
    # MAIN ANIMATION
    # =========================================================

    def animate(self):

        self.canvas.delete(
            "all"
        )

        width = self.canvas.winfo_width()

        height = self.canvas.winfo_height()

        if width < 100:

            width = 1200

        if height < 100:

            height = 760

        self.animation += 0.045

        self.wave_animation += 0.18

        # -----------------------------------------------------
        # BACKGROUND
        # -----------------------------------------------------

        self.draw_background(
            width,
            height
        )

        # -----------------------------------------------------
        # HEADER
        # -----------------------------------------------------

        self.draw_header(
            width
        )

        # -----------------------------------------------------
        # LEFT
        # -----------------------------------------------------

        self.draw_left_panel()

        # -----------------------------------------------------
        # RIGHT
        # -----------------------------------------------------

        self.draw_right_panel(
            width
        )

        # -----------------------------------------------------
        # CHARACTER
        # -----------------------------------------------------

        self.draw_character(
            width,
            height
        )

        # -----------------------------------------------------
        # PLATFORM
        # -----------------------------------------------------

        self.draw_platform(
            width,
            height
        )

        # -----------------------------------------------------
        # NEXT FRAME
        # -----------------------------------------------------

        self.root.after(
            40,
            self.animate
        )

    # =========================================================
    # RUN
    # =========================================================

    def run(self):

        self.root.mainloop()