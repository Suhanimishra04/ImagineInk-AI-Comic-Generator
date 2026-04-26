from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtGui import QPainter, QPixmap
import requests
import database

def show_error(parent, message):
    dialog = QDialog(parent)
    dialog.setWindowTitle("Error")
    dialog.setFixedSize(360, 160)
    dialog.setModal(True)

    dialog.setWindowFlags(
    Qt.WindowType.Dialog |
    Qt.WindowType.WindowTitleHint |  
    Qt.WindowType.WindowCloseButtonHint
    )

    dialog.setStyleSheet("""
        QDialog {
            background-color: #edeaff;;
            border-radius: 12px;
        }
    """)

    layout = QVBoxLayout(dialog)
    layout.setContentsMargins(20, 20, 20, 20)
    layout.setSpacing(14)

    label = QLabel(message)
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    label.setWordWrap(True)
    label.setTextInteractionFlags(Qt.TextInteractionFlag.NoTextInteraction)
    label.setStyleSheet("""
     background-color: transparent;   
    font-size: 15px;
    font-weight: 600;
    color: #1f1f4a;   
    """)

    ok_btn = QPushButton("OK")
    ok_btn.setFixedHeight(36)
    ok_btn.setStyleSheet("""
        QPushButton {
            background-color: #6c5ce7;
            color: white;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 600;
            padding: 0 22px;
        }
        QPushButton:hover {
            background-color: #6b5cff;
        }
    """)
    ok_btn.clicked.connect(dialog.accept)

    layout.addStretch()
    layout.addWidget(label)
    layout.addStretch()
    layout.addWidget(ok_btn, alignment=Qt.AlignmentFlag.AlignCenter)

    dialog.exec()
    
    
def show_success(parent, message):
    dialog = QDialog(parent)
    dialog.setWindowTitle("Success")
    dialog.setFixedSize(360, 170)
    dialog.setModal(True)

    dialog.setWindowFlags(
        Qt.WindowType.Dialog |
        Qt.WindowType.WindowTitleHint |
        Qt.WindowType.WindowCloseButtonHint
    )

    dialog.setStyleSheet("""
        QDialog {
            background-color: #edeaff;
            border-radius: 14px;
        }
    """)

    layout = QVBoxLayout(dialog)
    layout.setContentsMargins(20, 20, 20, 20)
    layout.setSpacing(14)

    label = QLabel(message)
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    label.setWordWrap(True)
    label.setStyleSheet("""
        background-color: transparent;
        font-size: 15px;
        font-weight: 600;
        color: #1f1f4a;
    """)

    ok_btn = QPushButton("OK")
    ok_btn.setFixedSize(110, 38)
    ok_btn.setStyleSheet("""
        QPushButton {
            background-color: #6b5cff;
            color: white;
            border-radius: 10px;
            font-size: 14px;
            font-weight: 600;
        }
        QPushButton:hover {
            background-color: #5a4de0;
        }
    """)
    ok_btn.clicked.connect(dialog.accept)

    layout.addStretch()
    layout.addWidget(label)
    layout.addStretch()
    layout.addWidget(ok_btn, alignment=Qt.AlignmentFlag.AlignCenter)

    dialog.exec()


# ================= HELP / HOW TO USE DIALOG =================
class HelpDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Help – How to Use ImagineInk")
        self.setFixedSize(520, 420)
        self.setModal(True)

        self.setStyleSheet("""
            QDialog {
                background-color: #edeaff;
                border-radius: 18px;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(14)

        title = QLabel("❓ How to Use ImagineInk")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            font-size: 20px;
            font-weight: 700;
            color: #1f1f4a;
        """)

        help_text = QLabel(
            "1️⃣ How do I start creating a story?\n"
            "      Click on 'Start Creating' and log in or sign up.\n\n"
            "2️⃣ How do I generate a story?\n"
            "      Write a prompt, select a genre, and click 'Create My Story'.\n\n"
            "3️⃣ Can I convert my story into a comic?\n"
            "      Yes! Click 'Convert Story to Comic' after generating a story.\n\n"
            "4️⃣ Is my data saved?\n"
            "      Yes, your stories and account data are saved safely.\n\n"
            "5️⃣ Can I edit my prompt?\n"
            "      Yes, you can rewrite your prompt anytime before generating.\n\n"
            "6️⃣ Can I log out safely?\n"
            "      Yes, you can log out anytime without losing data.\n\n"
            "7️⃣ Is ImagineInk free to use?\n"
            "      Yes, this version is free and made for learning & creativity ✨"
        )

        help_text.setWordWrap(True)
        help_text.setStyleSheet("""
            font-size: 14px;
            font-weight: 500;
            color: #333;
        """)

        close_btn = QPushButton("Close")
        close_btn.setFixedSize(140, 44)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #6b5cff;
                color: white;
                border-radius: 10px;
                font-size: 14px;
                font-weight: 600;
                padding: 8px 24px; 
            }
            QPushButton:hover {
                background-color: #5a4de0;
            }
        """)
        close_btn.clicked.connect(self.close)

        layout.addWidget(title)
        layout.addWidget(help_text)
        layout.addStretch()
        layout.addWidget(close_btn, alignment=Qt.AlignmentFlag.AlignCenter)


class ComicWindow(QMainWindow):

    def __init__(self, panel_paths):
        super().__init__()
        self.setWindowTitle("📖 Comic Reader")
        self.resize(1100, 800)
        self.panel_paths = panel_paths
        self.current_page = 0
        self.zoom = 1.0

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)

        top_bar = QHBoxLayout()
        self.prev_btn = QPushButton("◀ Previous")
        self.next_btn = QPushButton("Next ▶")
        self.page_label = QLabel()
        self.page_label.setStyleSheet("color:white; font-size:14px; font-weight:bold;")
        self.prev_btn.clicked.connect(self.prev_page)
        self.next_btn.clicked.connect(self.next_page)

        for b in [self.prev_btn, self.next_btn]:
            b.setFixedHeight(36)
            b.setStyleSheet("""
                QPushButton { background:#4338ca; color:white; border-radius:8px; padding:6px 14px; }
                QPushButton:hover { background:#3730a3; }
            """)

        top_bar.addWidget(self.prev_btn)
        top_bar.addStretch()
        top_bar.addWidget(self.page_label)
        top_bar.addStretch()
        top_bar.addWidget(self.next_btn)
        main_layout.addLayout(top_bar)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("QScrollArea { background:#0f172a; border:none; }")

        container = QWidget()
        self.image_layout = QVBoxLayout(container)
        self.image_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_layout.addWidget(self.image_label)
        self.scroll.setWidget(container)
        main_layout.addWidget(self.scroll)

        bottom = QHBoxLayout()
        zoom_in = QPushButton("＋")
        zoom_out = QPushButton("－")
        zoom_in.clicked.connect(self.zoom_in)
        zoom_out.clicked.connect(self.zoom_out)

        for b in [zoom_in, zoom_out]:
            b.setFixedSize(40, 40)
            b.setStyleSheet("""
                QPushButton { background:#1e293b; color:white; font-size:18px; border-radius:8px; }
                QPushButton:hover { background:#334155; }
            """)

        bottom.addStretch()
        bottom.addWidget(zoom_out)
        bottom.addWidget(zoom_in)
        main_layout.addLayout(bottom)
        self.load_page()

    def load_page(self):
        path = self.panel_paths[self.current_page]
        pixmap = QPixmap(path)
        w = int(850 * self.zoom)
        h = int(650 * self.zoom)
        pixmap = pixmap.scaled(w, h, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.image_label.setPixmap(pixmap)
        self.page_label.setText(f"Page {self.current_page+1} / {len(self.panel_paths)}")

    def next_page(self):
        if self.current_page < len(self.panel_paths) - 1:
            self.current_page += 1
            self.load_page()

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.load_page()

    def zoom_in(self):
        self.zoom += 0.1
        self.load_page()

    def zoom_out(self):
        if self.zoom > 0.5:
            self.zoom -= 0.1
            self.load_page()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Right:
            self.next_page()
        elif event.key() == Qt.Key.Key_Left:
            self.prev_page()
        elif event.key() == Qt.Key.Key_Plus:
            self.zoom_in()
        elif event.key() == Qt.Key.Key_Minus:
            self.zoom_out()

    def wheelEvent(self, event):
        if event.angleDelta().y() < 0:
            self.next_page()
        else:
            self.prev_page()


# ================= LOGOUT CONFIRMATION PAGE =================
class LogoutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Log Out")
        self.setFixedSize(380, 200)
        self.setModal(True)

        self.setStyleSheet("QDialog { background-color: #edeaff; border-radius: 16px; }")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(14)

        title = QLabel("🔐 Log Out")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: 700; color: #1f1f4a;")

        message = QLabel(
            "Are you sure you want to log out?\n\n"
            "✨ Your stories and data are saved safely.\n"
            "You can log in again anytime."
        )
        message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        message.setWordWrap(True)
        message.setStyleSheet("font-size: 14px; font-weight: 600; color: #333;")

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setFixedHeight(36)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: white; color: #6b5cff;
                border-radius: 10px; font-size: 14px; font-weight: 600;
                border: 1.5px solid #6b5cff;
            }
            QPushButton:hover { background-color: #f4f3ff; }
        """)

        logout_btn = QPushButton("Log Out")
        logout_btn.setFixedHeight(36)
        logout_btn.setStyleSheet("""
            QPushButton {
                background-color: #6b5cff; color: white;
                border-radius: 10px; font-size: 14px; font-weight: 600;
            }
            QPushButton:hover { background-color: #5a4de0; }
        """)

        cancel_btn.clicked.connect(self.reject)
        logout_btn.clicked.connect(self.accept)

        btn_layout.addWidget(cancel_btn)
        btn_layout.addWidget(logout_btn)

        layout.addWidget(title)
        layout.addWidget(message)
        layout.addStretch()
        layout.addLayout(btn_layout)


# ============ SEARCH STORY ================= ✅ FULLY FIXED
class SearchDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.user_id = getattr(parent, 'current_user_id', None)
        self._main_app = parent   # ImagineInkApp reference for Open in Studio

        self.setWindowTitle("Search Stories")
        self.setMinimumSize(820, 660)
        self.resize(860, 680)
        self.setModal(True)

        self.setStyleSheet("""
            QDialog {
                background-color: #f4f3ff;
                border-radius: 18px;
            }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 20, 24, 20)
        main_layout.setSpacing(14)

        # ── HEADER ROW ──────────────────────────────────────────────
        header_row = QHBoxLayout()

        back_btn = QPushButton("← Back to Studio")
        back_btn.setFixedHeight(36)
        back_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                color: #6c5ce7;
                border: 1.5px solid #6c5ce7;
                border-radius: 10px;
                font-size: 13px;
                font-weight: 600;
                padding: 0 16px;
            }
            QPushButton:hover { background-color: #ede9ff; }
        """)
        back_btn.clicked.connect(self.reject)

        title = QLabel("🔍  Search Your Stories")
        title.setStyleSheet("font-size: 20px; font-weight: 700; color: #2c2c54;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Spacer to keep title centered
        spacer_right = QWidget()
        spacer_right.setFixedWidth(150)

        header_row.addWidget(back_btn, alignment=Qt.AlignmentFlag.AlignLeft)
        header_row.addStretch()
        header_row.addWidget(title)
        header_row.addStretch()
        header_row.addWidget(spacer_right)

        # ── SEARCH BAR ──────────────────────────────────────────────
        search_row = QHBoxLayout()
        search_row.setSpacing(10)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔎  Type keywords to search your stories...")
        self.search_input.setFixedHeight(44)
        self.search_input.setStyleSheet("""
            QLineEdit {
                background-color: white;
                border: 1.5px solid #d0c8ff;
                border-radius: 12px;
                padding-left: 14px;
                font-size: 14px;
                color: #1f1f4a;
            }
            QLineEdit:focus { border: 1.5px solid #6c5ce7; }
        """)

        search_btn = QPushButton("Search")
        search_btn.setFixedHeight(44)
        search_btn.setFixedWidth(110)
        search_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        search_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c5ce7;
                color: white;
                border-radius: 12px;
                font-size: 14px;
                font-weight: 700;
            }
            QPushButton:hover { background-color: #5a4bdc; }
        """)

        search_btn.clicked.connect(self.do_search)
        self.search_input.returnPressed.connect(self.do_search)

        search_row.addWidget(self.search_input)
        search_row.addWidget(search_btn)

        # ── STATUS LABEL ─────────────────────────────────────────────
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("font-size:13px; color:#666; font-weight:500;")

        # ── SCROLL AREA ──────────────────────────────────────────────
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("""
            QScrollArea { border: none; background: transparent; }
            QScrollBar:vertical {
                background: #ede9ff; width: 8px; border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: #a89cee; border-radius: 4px; min-height: 24px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0px; }
        """)

        self.scroll_content = QWidget()
        self.scroll_content.setStyleSheet("background: transparent;")

        self.results_layout = QVBoxLayout(self.scroll_content)
        self.results_layout.setContentsMargins(2, 4, 2, 4)
        self.results_layout.setSpacing(14)
        self.results_layout.addStretch()

        self.scroll_area.setWidget(self.scroll_content)

        # ── ASSEMBLE ─────────────────────────────────────────────────
        main_layout.addLayout(header_row)
        main_layout.addLayout(search_row)
        main_layout.addWidget(self.status_label)
        main_layout.addWidget(self.scroll_area, stretch=1)

    # ─────────────────────────────────────────────────────────────────
    def _clear_results(self):
        while self.results_layout.count():
            item = self.results_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    # ─────────────────────────────────────────────────────────────────
    def do_search(self):
        keyword = self.search_input.text().strip()

        if not keyword:
            self.status_label.setText("⚠️  Please enter a keyword to search.")
            self._clear_results()
            return

        if not self.user_id:
            self.status_label.setText("⚠️  User not logged in.")
            return

        try:
            results = database.search_stories(self.user_id, keyword)
            self._clear_results()

            if not results:
                self.status_label.setText("❌  No stories found for this keyword.")
                return

            self.status_label.setText(f"✅  {len(results)} result(s) found for \"{keyword}\"")

            for i, row in enumerate(results):
                prompt, story, mode, created_at = row
                card = self._make_card(i, prompt, story, mode, created_at)
                self.results_layout.addWidget(card)

            self.results_layout.addStretch()

        except Exception as e:
            self.status_label.setText(f"❌  Error: {str(e)}")

    # ─────────────────────────────────────────────────────────────────
    def _make_card(self, index, prompt, story, mode, created_at):
        """
        One clean white card per result.
        NO sub-borders on labels — only the outer card has a border.
        """
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 16px;
                border: 1.5px solid #ddd8ff;
            }
        """)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 16, 20, 14)
        layout.setSpacing(10)

        # ── Top row: number | genre badge | date ──
        top_row = QHBoxLayout()

        num = QLabel(f"📌  Result {index + 1}")
        num.setStyleSheet("font-size:13px; font-weight:700; color:#6c5ce7; background:transparent; border:none;")

        badge = QLabel(f"🎭  {mode.capitalize()}")
        badge.setStyleSheet("""
            background-color: #ede9ff;
            color: #4c3cce;
            font-size: 12px;
            font-weight: 600;
            padding: 3px 12px;
            border-radius: 8px;
            border: none;
        """)
        badge.setFixedHeight(24)

        date = QLabel(f"🗓  {created_at[:10]}")
        date.setStyleSheet("font-size:12px; color:#999; background:transparent; border:none;")

        top_row.addWidget(num)
        top_row.addStretch()
        top_row.addWidget(badge)
        top_row.addSpacing(8)
        top_row.addWidget(date)

        # ── Prompt ──
        prompt_lbl = QLabel(f"✏️  <b>Prompt:</b>  {prompt}")
        prompt_lbl.setWordWrap(True)
        prompt_lbl.setStyleSheet("font-size:13px; color:#333; background:transparent; border:none;")

        # ── Divider ──
        div = QFrame()
        div.setFrameShape(QFrame.Shape.HLine)
        div.setFixedHeight(1)
        div.setStyleSheet("background-color: #ede9ff; border:none;")

        # ── Preview heading ──
        prev_head = QLabel("📖  Story Preview")
        prev_head.setStyleSheet("font-size:12px; font-weight:700; color:#6c5ce7; background:transparent; border:none;")

        # ── Preview text ──
        prev_text = QLabel(story[:380] + ("..." if len(story) > 380 else ""))
        prev_text.setWordWrap(True)
        prev_text.setStyleSheet("font-size:13px; color:#444; background:transparent; border:none;")

        # ── Open in Studio button ──
        open_btn = QPushButton("📂  Open in Studio")
        open_btn.setFixedHeight(38)
        open_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        open_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c5ce7;
                color: white;
                border-radius: 10px;
                font-size: 13px;
                font-weight: 700;
                padding: 0 22px;
                border: none;
            }
            QPushButton:hover { background-color: #5a4bdc; }
        """)
        # ✅ Lambda captures THIS card's prompt/story/mode correctly
        open_btn.clicked.connect(
            lambda _, p=prompt, s=story, m=mode: self._open_in_studio(p, s, m)
        )

        btn_row = QHBoxLayout()
        btn_row.addStretch()
        btn_row.addWidget(open_btn)

        layout.addLayout(top_row)
        layout.addWidget(prompt_lbl)
        layout.addWidget(div)
        layout.addWidget(prev_head)
        layout.addWidget(prev_text)
        layout.addLayout(btn_row)

        return card

    # ─────────────────────────────────────────────────────────────────
    def _open_in_studio(self, prompt, story, genre):
        """
        Loads the searched story into ImagineInkApp studio.
        Widgets (from main_app.py):
          prompt_input  → QTextEdit
          output_area   → QTextEdit  (read-only)
          genre_box     → QComboBox  items like "Fantasy ✨", "Horror 😱", etc.
        """
        app = self._main_app
        if app is None:
            self.reject()
            return

        # Set prompt
        app.prompt_input.setPlainText(prompt)

        # Set story — temporarily enable if read-only
        was_readonly = app.output_area.isReadOnly()
        app.output_area.setReadOnly(False)
        app.output_area.setText(story)
        app.output_area.setReadOnly(was_readonly)

        # Match genre combo (partial, case-insensitive)
        genre_lower = genre.strip().lower()
        for i in range(app.genre_box.count()):
            if app.genre_box.itemText(i).lower().startswith(genre_lower):
                app.genre_box.setCurrentIndex(i)
                break

        # Close dialog
        self.accept()