from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import QPainter, QPixmap
import os
import database
from backend.auth import check_login
from ui.dialogs import show_error


class LoginPage(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack

        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # ===== TITLE =====
        title = QLabel("✨ ImagineInk")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            font-size: 36px;
            font-weight: 800;
            color: #000000;
        """)

        subtitle = QLabel("Login to continue creating stories")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("""
            font-size: 14px;
            font-style: italic;
            color: #4a4a7a;
            margin-left: 50px;
        """)

        # ===== GLASS CARD =====
        card = QFrame()
        card.setFixedWidth(460)
        card.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.30);
                border-radius: 28px;
                padding: 35px;
            }
        """)

        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(18)

        # ===== EMAIL =====
        self.email = QLineEdit()
        self.email.setPlaceholderText("📧  Email")
        self.email.setFixedHeight(50)
        self.email.setStyleSheet("""
            QLineEdit {
                background-color: rgba(255,255,255,0.85);
                border-radius: 25px;
                padding-left: 18px;
                font-size: 14px;
                border: none;
            }
        """)

        
        # ===== PASSWORD =====
        pass_layout = QHBoxLayout()
        pass_layout.setContentsMargins(0,0,0,0)
        pass_layout.setSpacing(8)

        self.password = QLineEdit()
        self.password.setPlaceholderText("🔒  Password")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.password.setFixedHeight(50)
        self.password.setStyleSheet("""
            QLineEdit {
                background-color: rgba(255,255,255,0.85);
                border-radius: 25px;
                padding-left: 18px;
                font-size: 14px;
                border: none;
            }
        """)

        self.eye_btn = QPushButton("👁")
        self.eye_btn.setCheckable(True)
        self.eye_btn.setFixedSize(40,40)
        self.eye_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255,255,255,0.85);
                border-radius: 20px;
                border: none;
                font-size: 14px;
            }
        """)
        self.eye_btn.clicked.connect(self.toggle_password_visibility)

        pass_layout.addWidget(self.password)
        pass_layout.addWidget(self.eye_btn)

        # ===== LOGIN BUTTON =====
        login_btn = QPushButton("Login")
        login_btn.setFixedHeight(52)
        login_btn.setStyleSheet("""
    QPushButton {
        background: qlineargradient(
            x1:0, y1:0, x2:1, y2:0,
            stop:0 #a020f0,
            stop:1 #8000ff
        );
        color: white;
        border-radius: 26px;
        font-size: 15px;
        font-weight: 700;
    }

    QPushButton:hover {
        background: qlineargradient(
            x1:0, y1:0, x2:1, y2:0,
            stop:0 #7a4bf0,
            stop:1 #5b2ee0
        );
    }

    QPushButton:pressed {
        background: #5b2ee0;
    }
""")
        login_btn.clicked.connect(self.handle_login)

        # ===== FORGOT PASSWORD (RIGHT SIDE) =====
        forgot_btn = QPushButton("Forgot password?")
        forgot_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        forgot_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                color: #6b5cff;
                font-size: 12px;
            }
            QPushButton:hover {
                text-decoration: underline;
            }
        """)
        forgot_btn.clicked.connect(self.show_forgot_password)

        forgot_layout = QHBoxLayout()
        forgot_layout.addStretch()
        forgot_layout.addWidget(forgot_btn)

        # ===== BACK BUTTON =====
        back_btn = QPushButton("← Back")
        back_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        back_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                color: #6b5cff;
                font-size: 12px;
            }
            QPushButton:hover {
                text-decoration: underline;
            }
        """)
        back_btn.clicked.connect(lambda: self.stack.setCurrentIndex(1))

        # ===== ADD TO CARD =====
        card_layout.addWidget(self.email)
        card_layout.addLayout(pass_layout)
        card_layout.addWidget(login_btn)
        card_layout.addLayout(forgot_layout)
        card_layout.addSpacing(5)
        card_layout.addWidget(back_btn, alignment=Qt.AlignmentFlag.AlignLeft)

        # ===== ADD EVERYTHING =====
        main_layout.addWidget(title)
        main_layout.addSpacing(5)
        main_layout.addWidget(subtitle)
        main_layout.addSpacing(25)
        main_layout.addWidget(card)
        

    # ===== BACKGROUND =====
    def paintEvent(self, event):
        painter = QPainter(self)
        base_dir = os.path.dirname(__file__)
        image_path = os.path.join(base_dir, "assets", "auth_bg.png")
        pixmap = QPixmap(image_path)

        if not pixmap.isNull():
            scaled = pixmap.scaled(
                self.size(),
                Qt.AspectRatioMode.IgnoreAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            painter.drawPixmap(0, 0, scaled)

    # ===== PASSWORD TOGGLE =====
    def toggle_password_visibility(self):
        if self.eye_btn.isChecked():
            self.password.setEchoMode(QLineEdit.EchoMode.Normal)
            self.eye_btn.setText("🙈")
        else:
            self.password.setEchoMode(QLineEdit.EchoMode.Password)
            self.eye_btn.setText("👁")

    def handle_login(self):
        email = self.email.text().strip()
        password = self.password.text().strip()

        if not email or not password:
            show_error(self, "⚠️ Please fill in all fields")
            return

        if check_login(email, password):
            user = database.get_user_by_email(email)
            user_id = user[0]
            print(f"✅ User logged in! ID: {user_id}")

            main_app = self.stack.widget(5)
            main_app.current_user_id = user_id
            self.stack.setCurrentIndex(5)
        else:
            show_error(self, "⚠️ Invalid email or password")

    def show_forgot_password(self):
        self.stack.setCurrentIndex(4)   
    
    def reset_fields(self):
        self.email.clear()
        self.password.clear()