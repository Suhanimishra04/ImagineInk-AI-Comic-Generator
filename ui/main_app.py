from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import QGraphicsDropShadowEffect
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QApplication
from api_client import generate_story,generate_comic
from backend.comic_worker import ComicWorker
from backend.story_service import StoryWorker

import requests

import datetime
import database

from ui.dialogs import HelpDialog, LogoutDialog, SearchDialog
from ui.comic_window import ComicWindow
from PyQt6.QtGui import QPainter
from PyQt6.QtGui import QPixmap
class ImagineInkApp(QWidget):

    def __init__(self,stack):
        super().__init__()
        QApplication.setStyle("Fusion")
        self.stack = stack

        
        
        self.current_user_id = None
        self.current_project_id = None
        self.last_prompt_id = None

        self.story_generated = False
        self.comic_generated = False

        self.setWindowTitle("ImagineInk – Comic Creation Studio")
        self.setGeometry(100, 100, 950, 620)

        import os
        from PyQt6.QtGui import QPixmap

        base_path = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(base_path, "assets", "main_background.png")

        self.background_pixmap = QPixmap(image_path)


        title = QLabel("✨ ImagineInk")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            font-size: 32px;
            font-weight: bold;
            color: #2c2c54;
        """)

        subtitle = QLabel("Turn your imagination into AI-powered stories ")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("""
            font-size: 15px;
            color: #5a4b81;
            margin-left:30px;                   
        """)

       

        # ===== LEFT CARD =====
        prompt_card = QFrame()
        prompt_card.setStyleSheet("""
              QFrame {
                background: rgba(255, 255, 255, 0.25);
                backdrop-filter: blur(20px);
                -webkit-backdrop-filter: blur(20px);
                border: 2px solid #8b5cf6;
                border-radius: 18px;
                padding: 18px;

              }
        """)

        prompt_label = QLabel("📝 Story Prompt")
        prompt_label.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: #2c2c54;
        """)

        self.prompt_input = QTextEdit()
        self.prompt_input.setPlaceholderText(
           
            "🌙Write your imagination here ✨"
        )
        self.prompt_input.setMinimumHeight(300)
        self.prompt_input.setSizePolicy(
        QSizePolicy.Policy.Expanding,
        QSizePolicy.Policy.Expanding
        )
        self.prompt_input.setStyleSheet("""
            QTextEdit {
                
                border: 1px solid #ddd;
                border-radius: 12px;
                padding: 10px;
                font-size: 14px;
            }
        """)

        genre_label = QLabel("🎭 Select Genre")
        genre_label.setStyleSheet("""
            font-size: 15px;
            font-weight: bold;
            color: #2c2c54;
        """)

        self.genre_box = QComboBox()

        self.genre_box.setView(QListView())
        self.genre_box.addItems([
            "Fantasy ✨",
            "Horror 😱",
            "Fairytales❤️",
            "Mystery 🕵️",
            
        ])
        self.genre_box.setStyleSheet("""
            QComboBox {
                background: rgba(255, 255, 255, 0.25);   /* glass */
                border: 2px solid #8b5cf6;
                border-radius: 14px;
                padding: 8px 12px;
                font-size: 14px;
                color: #2c2c54;
            }

            QComboBox:hover {
                background: rgba(255, 255, 255, 0.35);
            }

            /* dropdown arrow area */
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }

            /* arrow */
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 6px solid #6d28d9;
                margin-right: 8px;
            }

            /* POPUP LIST */
            QComboBox QAbstractItemView {
                background-color: #E6E0FF;
                border: 2px solid #8b5cf6;
                border-radius: 12px;
                padding: 4px;
            }

            QComboBox QAbstractItemView::item {
                background-color: #E6E0FF;
                padding: 6px;
                color: #2c2c54;
            }

            QComboBox QAbstractItemView::item:selected {
                background-color: #8b5cf6;
                color: white;
            }
            """)

        self.generate_button = QPushButton("✨ Create My Story")
        self.generate_button.setFixedHeight(44)
        self.generate_button.setStyleSheet("""
            QPushButton {
                background-color: #6c5ce7;
                color: white;
                border-radius: 14px;
                font-size: 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5a4bdc;
            }
        """)
        self.generate_button.clicked.connect(self.generate_story)

        # ===== CONVERT TO COMIC BUTTON =====
        self.convert_comic_btn = QPushButton("🖼 Convert Story to Comic")
        self.convert_comic_btn.hide()
        self.convert_comic_btn.setFixedHeight(42)
        self.convert_comic_btn.setStyleSheet("""
            QPushButton {
              background-color: #4338ca;
              color: white;
              border-radius: 14px;
              font-size: 14px;
              font-weight: bold;
            }
             QPushButton:hover {
                 background-color: #3730a3;
            }
        """)
        self.convert_comic_btn.clicked.connect(self.show_comic_view)

        left_layout = QVBoxLayout()
        left_layout.setSpacing(12)
        left_layout.addWidget(prompt_label)
        left_layout.addWidget(self.prompt_input)
        left_layout.addWidget(genre_label)
        left_layout.addWidget(self.genre_box)
        left_layout.addWidget(self.generate_button)
        left_layout.addWidget(self.convert_comic_btn)
        prompt_card.setLayout(left_layout)
        glow1 = QGraphicsDropShadowEffect()
        glow1.setBlurRadius(80)
        glow1.setXOffset(0)
        glow1.setYOffset(0)
        glow1.setColor(QColor(120, 80, 255, 255)) 
        prompt_card.setGraphicsEffect(glow1)

        # ===== RIGHT CARD =====
        output_card = QFrame()
        output_card.setStyleSheet("""
    QFrame {
       background: rgba(255, 255, 255, 0.25);
       backdrop-filter: blur(20px);
       -webkit-backdrop-filter: blur(20px);
        border: 2px solid #8b5cf6;
        border-radius: 20px;
        padding: 18px;

    }
""")

        output_label = QLabel("📖 Your Story")
        output_label.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: #2c2c54;
        """)

        self.output_area = QTextEdit()
        self.output_area.setMinimumHeight(200)
        self.output_area.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding
        )
        self.output_area.setReadOnly(True)
        self.output_area.setPlaceholderText(
            "✨ Your magical story will appear here...\n\n"
            "Choose a genre and start creating ✨"
        )
        self.output_area.setStyleSheet("""
     QTextEdit {
       
        border-radius: 14px;
        padding: 10px;
        font-size: 14px;
        border: none;
    }
""")
        right_layout = QVBoxLayout()
        right_layout.setSpacing(12)
        right_layout.addWidget(output_label)
        right_layout.addWidget(self.output_area)
        output_card.setLayout(right_layout)
        glow2 = QGraphicsDropShadowEffect()
        glow2.setBlurRadius(80)
        glow2.setXOffset(0)
        glow2.setYOffset(0)
        glow2.setColor(QColor(120, 80, 255, 255)) 

        output_card.setGraphicsEffect(glow2)
        # ===== SIDEBAR =====
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setMinimumWidth(60)
        sidebar.setMaximumWidth(240)

        self.sidebar = sidebar
        self.sidebar_expanded_width = 240
        self.sidebar_collapsed_width = 60
        self.sidebar_visible = False   
        self.sidebar.setMaximumWidth(self.sidebar_collapsed_width)
        
        self.sidebar.setMaximumWidth(self.sidebar_collapsed_width)

        sidebar.setStyleSheet("""
            #sidebar {
                background-color: #312e81;
                border-radius: 18px;
            }

            #sidebar QPushButton {
                background-color: transparent;
                color: white;
                font-size: 14px;
                font-weight: 600;
                text-align: left;
                padding: 8px 14px;
                border: none;
            }

            #sidebar QPushButton:hover {
                background-color: #4338ca;
                border-radius: 10px;
            }

            #sidebar QLabel {
                color: #e0e7ff;
                font-size: 15px;
                font-weight: bold;
            }
            """)


        sidebar_layout = QVBoxLayout()
        sidebar_layout.setSpacing(4)

       # ----  TOGGLE AREA ----
        toggle_btn = QPushButton("☰")
        toggle_btn.setFixedSize(36, 36)
        toggle_btn.setStyleSheet("""
            QPushButton {
                color: white;
                font-size: 18px;
                background-color: transparent;
                border: none;
            }
            QPushButton:hover {
                background-color: #4338ca;
                border-radius: 8px;
            }
        """)
        toggle_btn.clicked.connect(self.toggle_sidebar)

        btn_menu = QPushButton("📌 Menu")
        btn_menu.setFixedHeight(42)
        btn_menu.setStyleSheet("""
            color: white;
            font-size: 18px;
            font-weight: bold;
            background-color: transparent;
            border: none;
            text-align: left;
            padding-left: 8px;
        """)

        sidebar_layout.addWidget(toggle_btn)
        sidebar_layout.addWidget(btn_menu)



         # ---- CORE FEATURES ----
        btn_new = QPushButton("🆕 New Story Generation")
        btn_new.clicked.connect(self.new_story)
        btn_search = QPushButton("🔍 Search Story")
        btn_search.clicked.connect(self.open_search_dialog)
        btn_history = QPushButton("⏱ Generation History")
        btn_history.clicked.connect(self.open_history_page)

            
        for btn in (
        btn_new,
        btn_search,
        btn_history,
        ):
                btn.setFixedHeight(42)
                btn_menu.setContentsMargins(0, 0, 0, 0)
                btn.setStyleSheet("color: white; font-size: 14px;")
                sidebar_layout.addWidget(btn)


        # ---- DIVIDER ----
        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setStyleSheet("color: #a5b4fc;")
        divider.setFixedHeight(1)
        sidebar_layout.addWidget(divider)



        # ---- ABOUT & HELP ----
        btn_about = QPushButton("ℹ️ About ImagineInk")
        btn_about.clicked.connect(self.show_about)
        btn_help = QPushButton("❓ Help / Guide")
        btn_help.clicked.connect(self.show_help)

        for btn in (
            btn_about,
            btn_help,
        ):
            sidebar_layout.addWidget(btn)
        # ---- DIVIDER ----
        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setStyleSheet("color: #a5b4fc;")
        divider.setFixedHeight(1)
        sidebar_layout.addWidget(divider)


        # ---- ACCOUNT ----
        btn_profile = QPushButton("👤 Profile")
        btn_logout = QPushButton("🔐 Log Out")

        btn_profile.clicked.connect(self.open_profile_page)
        btn_logout.clicked.connect(self.confirm_logout)


        for btn in (btn_profile, btn_logout):
            sidebar_layout.addWidget(btn)

        sidebar_layout.addStretch()
        sidebar.setLayout(sidebar_layout)


        body_layout = QHBoxLayout()
        body_layout.setSpacing(22)
        body_layout.addWidget(prompt_card, 1)
        body_layout.addWidget(output_card, 1)

        content_layout = QVBoxLayout()
        content_layout.setSpacing(18)

        content_layout.addWidget(title)
        content_layout.addSpacing(5)
        content_layout.addWidget(subtitle)

        content_layout.addSpacing(40)

        content_layout.addLayout(body_layout)

       

       # ===== SCROLLABLE CONTENT =====
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        

        scroll.setStyleSheet("""
            QScrollArea {
               background: transparent;
               border: none;
            }
        """)

        content_widget = QWidget()
        content_widget.setStyleSheet("background: transparent;")
        content_widget.setLayout(content_layout)
        scroll.setWidget(content_widget)

        final_layout = QHBoxLayout()
        final_layout.setSpacing(18)
        final_layout.addWidget(sidebar)
        final_layout.addWidget(scroll, 1)

        self.setLayout(final_layout)
        QTimer.singleShot(100, self.adjustSize)

    def toggle_sidebar(self):
        animation = QPropertyAnimation(self.sidebar, b"maximumWidth")
        animation.setDuration(250)
        animation.setEasingCurve(QEasingCurve.Type.InOutCubic)

        current_width = self.sidebar.maximumWidth()

        if self.sidebar_visible:
            animation.setStartValue(current_width)
            animation.setEndValue(self.sidebar_collapsed_width)
        else:
            animation.setStartValue(current_width)
            animation.setEndValue(self.sidebar_expanded_width)

        self.sidebar_visible = not self.sidebar_visible

        animation.start()
        self.sidebar_animation = animation 

    
        

    def generate_story(self):

        prompt = self.prompt_input.toPlainText().strip()
        genre_ui = self.genre_box.currentText()

        if not prompt:
            self.output_area.setText("⚠️ Please write a story prompt first.")
            return

        print(f"DEBUG: current_user_id = {self.current_user_id}")
        print(f"DEBUG: current_project_id = {self.current_project_id}")
        
        if not self.current_user_id:
            self.output_area.setText("⚠️ Please login first!")
            return

        try:

            # show loading text
            self.output_area.setText("⏳ Generating story, please wait...")

            # disable button while generating
            self.generate_button.setEnabled(False)

            # convert UI genre
            genre = genre_ui.split()[0].lower()

            # CREATE PROJECT BEFORE GENERATING STORY
            if not self.current_project_id:
                project_title = f"Project_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
                self.current_project_id = database.create_project(
                    user_id=self.current_user_id,
                    title=project_title,
                    description="Auto-generated"
                )
                print(f"DEBUG: Project created! ID = {self.current_project_id}")

            # start worker thread
            self.worker = StoryWorker(prompt, genre, self.current_project_id)

            self.worker.finished.connect(self.on_story_finished)
            self.worker.error.connect(self.show_error)

            self.worker.start()

        except Exception as e:

            self.output_area.setText(
                f"❌ Story generation failed:\n{str(e)}"
            )
            import traceback
            traceback.print_exc()

            self.generate_button.setEnabled(True)

    def new_story(self):
        self.prompt_input.clear()
        self.output_area.clear()
        self.genre_box.setCurrentIndex(0)
        self.current_project_id = None   

        self.story_generated = False
        self.comic_generated = False

        self.generate_button.setText("✨ Create My Story")
        self.convert_comic_btn.setText("🖼 Convert Story to Comic")
        self.convert_comic_btn.hide()

    def on_story_finished(self, story, prompt_id):
        """Receives story and prompt_id from backend"""
        print(f"DEBUG: Backend returned prompt_id = {prompt_id}")
        self.last_prompt_id = prompt_id
        self.show_story(story)

    def show_story(self, story):
        self.output_area.setText(story)

        try:
            if not hasattr(self, 'current_project_id') or self.current_project_id is None:
                project_title = f"Project_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
                database.create_project(
                    user_id=self.current_user_id,
                    title=project_title,
                    description="Auto-generated project"
                )
                
                conn = database.connect_db()
                cur = conn.cursor()
                cur.execute("SELECT project_id FROM projects WHERE user_id = ? ORDER BY created_at DESC LIMIT 1", 
                           (self.current_user_id,))
                result = cur.fetchone()
                conn.close()
                
                if result:
                    self.current_project_id = result[0]
            
            if self.current_project_id:
                prompt = self.prompt_input.toPlainText().strip()
                genre_ui = self.genre_box.currentText()
                genre = genre_ui.split()[0].lower()
                
                database.save_prompt(
                    project_id=self.current_project_id,
                    prompt=prompt,
                    story=story,
                    mode=genre
                )
                print(f"✅ Story saved! Project ID: {self.current_project_id}")
        
        except Exception as e:
            print(f"❌ Database save error: {str(e)}")

        self.generate_button.setEnabled(True)
        # ===== UI UPDATE AFTER STORY =====
        self.story_generated = True

        self.generate_button.setText("Regenerate Story")

        self.convert_comic_btn.show()

    def show_error(self, error):
        self.output_area.setText(f"❌ {error}")   
        self.generate_button.setEnabled(True)        

    def show_about(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("About ImagineInk")
        dialog.setFixedSize(520, 420)

        dialog.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        dialog.setStyleSheet("""
            QDialog {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #f3e7ff,
                    stop:1 #e0d4ff
                );
                border-radius: 18px;
            }

            QLabel {
                background: transparent;
            }
        """)

        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(30, 25, 30, 25)

        title = QLabel("✨ ImagineInk")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            font-size: 22px;
            font-weight: bold;
            color: #2c2c54;
        """)

        text = QLabel(
            "ImagineInk is an AI-powered storytelling and comic creation application.\n\n"
            "✨ Generate creative stories using simple text prompts\n"
            "🎭 Choose genres like Fantasy, Horror, Romance & more\n"
            "🎨 Convert generated stories into comic panels\n"
            "📤 Export stories & comics in PDF or image format\n"
            "🗂 Manage your projects in one place\n\n"
            "Built using Python & PyQt6."
        )

        text.setWordWrap(True)
        text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        text.setStyleSheet("""
            font-size: 15px;
            font-weight: 500;
            color: #374151;
        """)

        close_btn = QPushButton("Close")
        close_btn.setFixedHeight(40)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c5ce7;
                color: white;
                border-radius: 14px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #5a4bdc;
            }
        """)
        close_btn.clicked.connect(dialog.close)

        layout.addWidget(title)
        layout.addSpacing(10)
        layout.addWidget(text)
        layout.addStretch()
        layout.addWidget(close_btn)

        dialog.exec()

    def show_comic_view(self):
        # prevent double click
        if not self.convert_comic_btn.isEnabled():
            return
        # prevent multiple worker running
        if hasattr(self, "comic_worker") and self.comic_worker.isRunning():
            return

        story = self.output_area.toPlainText().strip()

        if not story:
            QMessageBox.warning(
                self,
                "No Story",
                "Please generate a story first."
            )
            return

        # UI update
        self.convert_comic_btn.setText("Generating Comic...")
        self.convert_comic_btn.setEnabled(False)

        # ✅ USE THREAD (IMPORTANT)
        self.comic_worker = ComicWorker(story, self.last_prompt_id)

        self.comic_worker.finished.connect(self.on_comic_ready)
        self.comic_worker.error.connect(self.show_error)

        self.comic_worker.start()

    def on_comic_ready(self, comic_response):

        print("DEBUG: on_comic_ready called")
        print("FULL RESPONSE:", comic_response)

        # ❌ no response
        if not comic_response:
            QMessageBox.critical(self, "Error", "No response from comic API")
            self.convert_comic_btn.setEnabled(True)
            return

        try:
            # 🔥 SAFE EXTRACTION
            job_id = comic_response.get("job_id", None)
            comic = comic_response.get("panels", None)

            print("Comic received:", comic)

            # ❌ panels missing or empty
            if not comic or not isinstance(comic, list) or len(comic) == 0:
                QMessageBox.warning(
                    self,
                    "Error",
                    "Comic not generated.\n\nTry:\n- Shorter prompt\n- Click only once\n- Restart backend"
                )
                self.convert_comic_btn.setEnabled(True)
                return

            # ✅ SAVE TO DB
            for comic_path in comic:
                try:
                    database.save_comic(
                        prompt_id=self.last_prompt_id,
                        comic_path=comic_path
                    )
                except Exception as e:
                    print("DB error:", e)

            # ✅ SHOW WINDOW
            self.comic_window = ComicWindow(comic, job_id)
            self.comic_window.show()

            # ✅ UI UPDATE
            self.comic_generated = True
            self.convert_comic_btn.setText("🔁 Regenerate Comic")

        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

        self.convert_comic_btn.setEnabled(True)

    def reset_app_state(self):
        self.prompt_input.clear()
        self.output_area.clear()
        self.genre_box.setCurrentIndex(0)
        self.current_project_id = None

        
    def confirm_logout(self):
        dialog = LogoutDialog(self)

        if dialog.exec() == QDialog.DialogCode.Accepted:

            if self.current_user_id:
                now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                conn = database.connect_db()
                cur = conn.cursor()
                cur.execute(
                    "UPDATE users SET last_logout = ? WHERE user_id = ?",
                    (now, self.current_user_id)
                )
                conn.commit()
                conn.close()

            self.current_user_id = None

            login_page = self.stack.widget(2)
            login_page.reset_fields()

            self.reset_app_state()

            self.sidebar.setMaximumWidth(self.sidebar_collapsed_width)
            self.sidebar_visible = False

            self.stack.setCurrentIndex(0)

    def show_help(self):
        dialog = HelpDialog(self)
        dialog.exec()

    def open_search_dialog(self):
        dialog = SearchDialog(self)
        dialog.exec()

    def open_history_page(self):
        stack = self.parent()
        history_page = stack.widget(6)
        history_page.load_user_data(self.current_user_id)
        stack.setCurrentIndex(6)

    def open_profile_page(self):
        stack = self.parent()
        profile_page = stack.widget(7)
        profile_page.load_user_data(self.current_user_id)
        stack.setCurrentIndex(7)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.background_pixmap)