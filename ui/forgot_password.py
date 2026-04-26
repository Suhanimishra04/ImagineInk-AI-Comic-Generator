from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
import random, smtplib, hashlib
from email.mime.text import MIMEText
from PyQt6.QtGui import QPainter, QLinearGradient, QColor
from backend.auth import is_valid_email, is_strong_password
from ui.dialogs import show_error, show_success
import database

class OTPWorker(QThread):
    success = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, email, otp):
        super().__init__()
        self.email = email
        self.otp = otp

    def run(self):
        try:
            import smtplib
            from email.mime.text import MIMEText

            sender_email = "imagineinkk@gmail.com"
            sender_password = "frzn uzqt pzox uzqr"

            msg = MIMEText(f"Your OTP is {self.otp}")
            msg["Subject"] = "Reset Password OTP"
            msg["From"] = sender_email
            msg["To"] = self.email

            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            server.quit()

            self.success.emit()

        except Exception as e:
            self.error.emit(str(e))
class ForgotPasswordPage(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        self.generated_otp = None

        # ===== INPUT FIELDS =====
        self.email = QLineEdit()
        self.email.setPlaceholderText("Email")

        self.otp = QLineEdit()
        self.otp.setPlaceholderText("Enter OTP")

        self.new_pass = QLineEdit()
        self.new_pass.setPlaceholderText("New Password")
        self.new_pass.setEchoMode(QLineEdit.EchoMode.Password)

        # ===== MAIN LAYOUT (REPLACE OLD ONE) =====
        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("✨ ImagineInk")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 36px; font-weight: 800; color: #000;")

        subtitle = QLabel("Reset your password securely")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("font-size: 14px; color: #4a4a7a;")

        card = QFrame()
        card.setFixedWidth(480)
        card.setStyleSheet("""
            QFrame {
                background-color: rgba(255,255,255,0.30);
                border-radius: 28px;
                padding: 35px;
            }
        """)

        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(20)

        input_style = """
        QLineEdit {
            background-color: rgba(255,255,255,0.6);
            border-radius: 28px;
            padding: 14px 20px;
            font-size: 15px;
            border: none;
            color: #333;
        }

        QLineEdit:focus {
            background-color: rgba(255,255,255,0.9);
        }
        """

        self.email.setStyleSheet(input_style)
        self.otp.setStyleSheet(input_style)
        self.new_pass.setStyleSheet(input_style)
        self.email.setFixedHeight(55)
        self.otp.setFixedHeight(55)
        self.new_pass.setFixedHeight(55)

        self.send_btn = QPushButton("Send OTP")
        self.reset_btn = QPushButton("Reset Password")
        # ===== BUTTON STYLE =====
        button_style = """
        QPushButton {
            background: qlineargradient(
                x1:0, y1:0, x2:1, y2:0,
                stop:0 #a855f7,
                stop:1 #6b5cff
            );
            color: white;
            border-radius: 25px;
            font-size: 15px;
            font-weight: bold;
            padding: 12px;
        }

        QPushButton:hover {
            background: qlineargradient(
                x1:0, y1:0, x2:1, y2:0,
                stop:0 #9333ea,
                stop:1 #5746d8
            );
        }

        QPushButton:pressed {
            background-color: #4c1d95;
        }
        """

        self.send_btn.clicked.connect(self.send_otp)
        self.reset_btn.clicked.connect(self.reset_password)
        self.send_btn.setStyleSheet(button_style)
        self.reset_btn.setStyleSheet(button_style)
        self.send_btn.setFixedHeight(55)
        self.reset_btn.setFixedHeight(55)

        self.back_btn = QPushButton("← Back to Login")
        self.back_btn.clicked.connect(lambda: self.stack.setCurrentIndex(2))
        self.back_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                color: #6b5cff;
                font-size: 13px;
            }
            QPushButton:hover {
                text-decoration: underline;
            }
        """)

        card_layout.addWidget(self.email)
        card_layout.addWidget(self.otp)
        card_layout.addWidget(self.new_pass)
        card_layout.addWidget(self.send_btn)
        card_layout.addWidget(self.reset_btn)
        card_layout.addWidget(self.back_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        card_layout.addSpacing(10)


        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)
        main_layout.addWidget(card)

    def paintEvent(self, event):
        painter = QPainter(self)
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0, QColor(230, 220, 255))
        gradient.setColorAt(1, QColor(200, 220, 255))
        painter.fillRect(self.rect(), gradient)

    def send_otp(self):
        email = self.email.text().strip()

        if not is_valid_email(email):
            show_error(self, "Invalid email")
            return

        import random
        self.generated_otp = str(random.randint(100000, 999999))

        # disable button
        self.send_btn.setEnabled(False)
        self.send_btn.setText("Sending...")

        self.worker = OTPWorker(email, self.generated_otp)

        self.worker.success.connect(self.on_otp_sent)
        self.worker.error.connect(self.on_otp_error)

        self.worker.start()

    def on_otp_sent(self):
        self.send_btn.setEnabled(True)
        self.send_btn.setText("Send OTP")
        show_success(self, "OTP Sent!")

    def on_otp_error(self, err):
        self.send_btn.setEnabled(True)
        self.send_btn.setText("Send OTP")
        show_error(self, err)

    def reset_password(self):
        email = self.email.text().strip()
        otp = self.otp.text().strip()
        new_pass = self.new_pass.text().strip()

        if otp != self.generated_otp:
            show_error(self, "Invalid OTP")
            return

        if not is_strong_password(new_pass):
            show_error(self, "Weak password")
            return

        new_hash = hashlib.sha256(new_pass.encode()).hexdigest()
        database.update_password(email, new_hash)

        show_success(self, "Password reset successful!")
        self.stack.setCurrentIndex(2)