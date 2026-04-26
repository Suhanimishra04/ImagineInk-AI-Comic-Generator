from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import QPixmap, QPainter, QColor
import os
import database


class UserProfilePage(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        self.current_user_id = None

        # ===== LOAD BACKGROUND IMAGE =====
        base_path = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(base_path, "assets", "auth_bg.png")
        self.background_pixmap = QPixmap(image_path)

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, False)

        # ===== SCROLL AREA (background safe) =====
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet("background: transparent;")

        container = QWidget()
        container.setStyleSheet("background: transparent;")

        scroll.setWidget(container)

        main_layout = QVBoxLayout(container)
        main_layout.setContentsMargins(60, 40, 60, 40)
        main_layout.setSpacing(20)

        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.addWidget(scroll)
        main_layout.setContentsMargins(60, 40, 60, 40)
        main_layout.setSpacing(20)

        # ===== HEADER =====
        header = QLabel("👤 Your Profile")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStyleSheet("""
            font-size: 34px;
            font-weight: 800;
            color: #2c2c54;
            background: transparent;
        """)

        # ===== PROFILE CARD =====
        self.card = QFrame()
        self.card.setMaximumWidth(720)
        self.card.setStyleSheet("""
            QFrame {
                background-color:#edeaff;
                border-radius: 25px;
                padding: 40px;
                border: 4px solid #6c5ce7;
            }
        """)

        card_layout = QVBoxLayout(self.card)
        card_layout.setSpacing(25)
        card_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        card_layout.setContentsMargins(40, 40, 40, 40)

        # ===== AVATAR =====
        self.avatar = QLabel("👩🏻‍💻")
        self.avatar.setFixedSize(140, 140)
        self.avatar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.avatar.setStyleSheet("""
            QLabel {
                background-color: #edeaff;
                border-radius: 70px;
                font-size: 55px;
                border: 4px solid #6c5ce7;
            }
        """)

        # ===== USERNAME =====
        self.username_big = QLabel("Username")
        self.username_big.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.username_big.setStyleSheet("""
            font-size: 28px;
            font-weight: 700;
            color: #2c2c54;
            background: transparent;
        """)

        # ===== INFO LABELS =====
        self.userid_label = QLabel()
        self.email_label = QLabel()
        self.created_label = QLabel()
        self.logout_label = QLabel()

        info_labels = [
            self.userid_label,
            self.email_label,
            self.created_label,
            self.logout_label
        ]

        for lbl in info_labels:
            lbl.setStyleSheet("""
                font-size: 15px;
                font-weight: 500;
                color: #2c2c54;
                background: transparent;
                padding: 8px;
            """)
            lbl.setWordWrap(True)

        # ===== GRID LAYOUT FOR INFO =====
        info_layout = QGridLayout()
        info_layout.setSpacing(15)

        info_layout.addWidget(self.userid_label, 0, 0)
        info_layout.addWidget(self.email_label, 0, 1)
        info_layout.addWidget(self.created_label, 1, 0)
        info_layout.addWidget(self.logout_label, 1, 1)

        # ===== ADD TO CARD =====
        card_layout.addWidget(self.avatar, alignment=Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(self.username_big)
        card_layout.addLayout(info_layout)

        # ===== BACK BUTTON =====
        back_btn = QPushButton("← Back to Studio")
        back_btn.setFixedHeight(50)
        back_btn.setMinimumWidth(260)
        back_btn.setCursor(Qt.CursorShape.PointingHandCursor)

        back_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c5ce7;
                color: white;
                border-radius: 18px;
                font-weight: 700;
                font-size: 16px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #5a4bdc;
            }
        """)

        back_btn.clicked.connect(lambda: self.stack.setCurrentIndex(5))

        # ===== MAIN LAYOUT STRUCTURE =====
        main_layout.addWidget(header)
        main_layout.addSpacing(20)
        main_layout.addWidget(self.card, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addSpacing(25)
        main_layout.addWidget(back_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        main_layout.addStretch()

    # ===== BACKGROUND DRAW =====
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        painter.drawPixmap(self.rect(), self.background_pixmap)
        painter.end()
        super().paintEvent(event)

    # ===== LOAD USER DATA =====
    def load_user_data(self, user_id):
        self.current_user_id = user_id

        conn = database.connect_db()
        cur = conn.cursor()
        cur.execute(
            "SELECT user_id, username, email, created_at, last_logout FROM users WHERE user_id = ?",
            (user_id,)
        )
        user = cur.fetchone()
        conn.close()

        if user:
            self.username_big.setText(user[1])
            self.userid_label.setText(f"🆔 User ID:\n{user[0]}")
            self.email_label.setText(f"📧 Email:\n{user[2]}")
            self.created_label.setText(f"📅 Account Created:\n{user[3]}")
            self.logout_label.setText(
                f"⏱ Last Logout:\n{user[4] if user[4] else 'First Login'}"
            )
        else:
            self.username_big.setText("User Not Found")
