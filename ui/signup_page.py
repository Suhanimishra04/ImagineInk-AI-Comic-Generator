from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import QPainter, QPixmap
import os
import hashlib
import database
import random
import smtplib
from email.mime.text import MIMEText
from backend.auth import (
    is_valid_email,
    is_strong_password,
    email_exists,
    is_valid_name
)
from ui.dialogs import show_error, show_success


class SignUpPage(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack

        self.generated_otp = None

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

        subtitle = QLabel("Create your account to begin")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("""
            font-size: 14px;
            font-style: italic;
            color: #4a4a7a;
            margin-left: 50px;
        """)

        # ===== GLASS CARD =====
        card = QFrame()
        card.setFixedWidth(480)
        card.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.30);
                border-radius: 28px;
                padding: 35px;
            }
        """)

        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(18)

        input_style = """
            QLineEdit {
                background-color: rgba(255,255,255,0.85);
                border-radius: 25px;
                padding-left: 18px;
                font-size: 14px;
                border: none;
            }
        """

        # ===== NAME =====
        self.name = QLineEdit()
        self.name.setPlaceholderText("Full Name")
        self.name.setFixedHeight(50)
        self.name.setStyleSheet(input_style)

        # ===== EMAIL =====
        self.email = QLineEdit()
        self.email.setPlaceholderText("Email")
        self.email.setFixedHeight(50)
        self.email.setStyleSheet(input_style)

        # ===== PASSWORD =====
        pass_layout = QHBoxLayout()
        pass_layout.setContentsMargins(0,0,0,0)
        pass_layout.setSpacing(8)

        self.password = QLineEdit()
        self.password.setPlaceholderText("🔒 Password")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.password.setFixedHeight(50)
        self.password.setStyleSheet(input_style)

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

        # ===== PASSWORD RULES LABEL =====
        self.password_rules = QLabel(
            "• 8+ characters | 1 uppercase | 1 lowercase | 1 number "
        )
        self.password_rules.setStyleSheet("color: red; font-size: 11px;")
        self.password_rules.hide()

        # live check
        self.password.textChanged.connect(self.check_password_strength)
        # ===== CONFIRM PASSWORD =====
        self.confirm = QLineEdit()
        self.confirm.setPlaceholderText("Confirm Password")
        self.confirm.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm.setFixedHeight(50)
        self.confirm.setStyleSheet(input_style)

        # ===== SIGN UP BUTTON (PURPLE GRADIENT) =====
        signup_btn = QPushButton("Create Account")
        signup_btn.setFixedHeight(60)
        signup_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #a020f0,
                    stop:1 #8000ff
                );
                color: white;
                border-radius: 25px;
                font-size: 15px;
                font-weight: 700;
            }

            QPushButton:hover {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #8b00ff,
                    stop:1 #6a00cc
                );
            }

            QPushButton:pressed {
                background: #6a00cc;
            }
        """)
        signup_btn.clicked.connect(self.create_account)

        # ===== LOGIN LINK =====
        login_link = QPushButton("Already have an account? Login")
        login_link.setCursor(Qt.CursorShape.PointingHandCursor)
        login_link.setStyleSheet("""
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
        login_link.clicked.connect(lambda: self.stack.setCurrentIndex(2))

        # ===== ADD TO CARD =====
        card_layout.addWidget(self.name)
        card_layout.addWidget(self.email)
        card_layout.addLayout(pass_layout)
        card_layout.addWidget(self.password_rules)
        card_layout.addWidget(self.confirm)
        # ===== OTP SECTION =====
        otp_layout = QHBoxLayout()

        self.otp_input = QLineEdit()
        self.otp_input.setPlaceholderText("Enter OTP")
        self.otp_input.setFixedHeight(50)
        self.otp_input.setStyleSheet(input_style)

        self.send_otp_btn = QPushButton("Send OTP")
        self.send_otp_btn.setFixedHeight(50)
        self.send_otp_btn.setStyleSheet("""
            QPushButton {
                background-color: #6b5cff;
                color: white;
                border-radius: 15px;
                font-size: 12px;
            }
        """)
        self.send_otp_btn.clicked.connect(self.send_otp)

        otp_layout.addWidget(self.otp_input)
        otp_layout.addWidget(self.send_otp_btn)

        card_layout.addLayout(otp_layout)
        card_layout.addWidget(signup_btn)
        card_layout.addWidget(login_link, alignment=Qt.AlignmentFlag.AlignCenter)

        # ===== ADD TO MAIN =====
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

    def check_password_strength(self):
        password = self.password.text()

        if not password:
            self.password_rules.hide()
            return

        self.password_rules.show()

        if is_strong_password(password):
            self.password_rules.setText("✔ Strong Password!")
            self.password_rules.setStyleSheet("color: green; font-size: 11px;")
        else:
            self.password_rules.setText(
                "• 8+ characters | 1 uppercase | 1 lowercase | 1 number "
            )
            self.password_rules.setStyleSheet("color: red; font-size: 11px;")
    
    def send_otp(self):
        email = self.email.text().strip()

        if not is_valid_email(email):
            show_error(self, "⚠️ Enter valid email first")
            return

        self.generated_otp = str(random.randint(100000, 999999))

        try:
            sender_email = "imagineinkk@gmail.com"
            sender_password = "frzn uzqt pzox uzqr"

            msg = MIMEText(f"Your OTP is {self.generated_otp}")
            msg["Subject"] = "ImagineInk OTP"
            msg["From"] = sender_email
            msg["To"] = email

            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            server.quit()

            show_success(self, "✅ OTP sent!")

        except Exception as e:
            show_error(self, str(e))

    # ===== ACCOUNT CREATION LOGIC =====
    def create_account(self):
        name = self.name.text().strip()
        email = self.email.text().strip()
        password = self.password.text().strip()
        confirm = self.confirm.text().strip()

        if not name or not email or not password or not confirm:
            show_error(self, "⚠️ Please fill in all fields")
            return

        if not is_valid_name(name):
            show_error(self, "⚠️ Name should contain only alphabets and spaces")
            return

        if not is_valid_email(email):
            show_error(self, "⚠️ Please enter a valid email address")
            return

        if email_exists(email):
            show_error(self, "⚠️ This email is already registered")
            return

        if not is_strong_password(password):
            show_error(self, "⚠️ Password must contain at least 8 characters,\n1 uppercase, 1 lowercase and 1 number")
            return

        if password != confirm:
            show_error(self, "⚠️ Passwords do not match")
            return

        if not self.generated_otp:
            show_error(self, "⚠️ Please send OTP first")
            return

        if self.otp_input.text().strip() != self.generated_otp:
            show_error(self, "⚠️ Invalid OTP")
            return

        password_hash = hashlib.sha256(password.encode()).hexdigest()
        database.create_user(name, email, password_hash)

        show_success(self, "✨ Account created successfully!")
        self.stack.setCurrentIndex(2)