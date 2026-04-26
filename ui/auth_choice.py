import os
from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QPixmap, QFont

class AuthChoicePage(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)

        layout.addStretch()

        # ===== TITLE =====
        title = QLabel("✨ ImagineInk")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            font-size: 50px;
            font-weight: 800;
            color: #000000;
            margin-right: 70px;
        """)

        # ===== SUBTITLE =====
        subtitle = QLabel("Continue your creative journey")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("""
            font-size: 16px;
            font-style: italic;
            font-weight: 500;
            color: #4a4a7a;
        """)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        

        # ===== BUTTON CONTAINER =====
        button_container = QFrame()
        button_container.setFixedWidth(520)
        button_container.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.35);
                border-radius: 28px;
                padding: 40px;
            }
        """)

        btn_layout = QVBoxLayout(button_container)
        btn_layout.setSpacing(36)
        btn_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

                # ===== LOGIN BUTTON =====
        login_btn = QPushButton("Login")
        login_btn.setFixedSize(380, 70)
        login_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        login_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.92);
                color: #1f2a7a;
                font-size: 20px;
                font-weight: 700;
                border-radius: 35px;
                padding: 0px;
            }
            QPushButton:hover {
                background-color: white;
            }
        """)

        # ===== SIGNUP BUTTON =====
        signup_btn = QPushButton("Create Account")
        signup_btn.setFixedSize(380, 70)
        signup_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        signup_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.92);
                color: #1f2a7a;
                font-size: 20px;
                font-weight: 700;
                border-radius: 35px;
                padding: 0px;
            }
            QPushButton:hover {
                background-color: white;
            }
        """)

        login_btn.clicked.connect(lambda: self.stack.setCurrentIndex(2))
        signup_btn.clicked.connect(lambda: self.stack.setCurrentIndex(3))

        btn_layout.addWidget(login_btn)
        btn_layout.addWidget(signup_btn)

        layout.addWidget(button_container)

        layout.addSpacing(30)

        # ===== BACK BUTTON =====
        back_btn = QPushButton("← Back")
        back_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        back_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #5b6cff;
                font-size: 14px;
                font-weight: 600;
                border: none;
            }
            QPushButton:hover {
                text-decoration: underline;
            }
        """)

        back_btn.clicked.connect(lambda: self.stack.setCurrentIndex(0))

        layout.addWidget(back_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addStretch()

    # ===== BACKGROUND PAINT =====
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