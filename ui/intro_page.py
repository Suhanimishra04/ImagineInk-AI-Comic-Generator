from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from ui.dialogs import HelpDialog
import os
class IntroPage(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)

        container = QWidget()
        scroll.setWidget(container)
        base_dir = os.path.dirname(__file__)
        bg_path = os.path.join(base_dir, "assets", "background.png")
        bg_path = bg_path.replace("\\", "/")
       
        container.setStyleSheet(f"""

        border-image: url({bg_path}) 0 0 0 0 stretch stretch;

""")

        self.setMinimumWidth(1100)   

        # ===== MAIN LAYOUT =====
        main_layout = QVBoxLayout(container)
        main_layout.setSpacing(28)
        main_layout.setContentsMargins(80, 40, 80, 40)

        # ===== TITLE =====
        title = QLabel("✨ ImagineInk")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
    font-size: 36px;
    font-weight: 800;
    color: #1f1f4a;
    background: transparent;
""")

        title.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        subtitle = QLabel(
            "AI-Powered Interactive Storytelling & Comic Generation"
        )
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("""
    font-size: 18px;
    font-weight: 600;   /* हल्का bold */
    color: #6b5cff;
    background: transparent;
""")
        

        subtitle.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        # ===== DESCRIPTION CARD =====
        desc_card = QFrame()
        desc_card = QFrame()
        desc_card.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        desc_card.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred
        )
        desc_card.setStyleSheet("""
    QFrame {
        background-color: rgba(255, 255, 255, 230);
        border-radius: 22px;
        padding: 28px;
        border: none;
    }
""")

        desc_text = QLabel(
            "Transform your ideas into stunning stories and visual comics.\n"
            "ImagineInk blends creativity with AI to help you write, visualize,\n"
            "and bring your imagination to life — effortlessly."
        )
        desc_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_text.setWordWrap(True)
        desc_text.setStyleSheet("""
    font-size: 15px;
    font-weight: 700;   
    color: #333;
    border: none;
""")

        desc_layout = QVBoxLayout(desc_card)
        desc_layout.setContentsMargins(0, 0, 0, 0)
        desc_layout.addWidget(desc_text)

        # ===== START CREATING BUTTON =====
        btn_layout = QHBoxLayout()
        btn_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        start_btn = QPushButton("✨ Start Creating")
        start_btn.setFixedSize(280, 54)
        
        start_btn.setStyleSheet("""
QPushButton {
    background-color: rgba(255, 255, 255, 140);
    color: #1f1f4a;
    border: 2px solid rgba(255, 255, 255, 200);
    border-radius: 27px;
    font-size: 18px;
    font-weight: 800;
    padding: 14px 28px;
}

QPushButton:hover {
    background-color: rgba(255, 255, 255, 190);
}

QPushButton:pressed {
    background-color: rgba(255, 255, 255, 230);
}
""")
        from PyQt6.QtGui import QColor
        from PyQt6.QtWidgets import QGraphicsDropShadowEffect

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(60)              
        shadow.setOffset(0, 8)                
        shadow.setColor(QColor(255, 122, 198, 200))   

        start_btn.setGraphicsEffect(shadow)
        start_btn.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        btn_layout.addWidget(start_btn)

        help_btn = QPushButton("❓ Help")
        help_btn.setFixedSize(90, 36)
        help_btn.setStyleSheet("""
            QPushButton {
                background-color: #edeaff;
                color: #6b5cff;
                border: 2px solid #6b5cff;
                border-radius: 18px;
                font-size: 13px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #edeaff;
            }
        """)
        help_btn.clicked.connect(self.show_help)

       
        top_bar = QHBoxLayout()
        top_bar.addStretch()          
        top_bar.addWidget(help_btn)

        # ===== FEATURE CARDS =====
        features_layout = QHBoxLayout()
        features_layout.setSpacing(20)

        def feature_card(icon, title, text):
            card = QFrame()
            card.setSizePolicy(                      
                QSizePolicy.Policy.Expanding,
                QSizePolicy.Policy.Preferred
            )
            card.setStyleSheet("""
    QFrame {
        background-color: rgba(255, 255, 255, 220);
        border-radius: 18px;
        padding: 18px;
    }
""")
            v = QVBoxLayout(card)

            lbl_title = QLabel(f"{icon}  {title}")
            lbl_title.setStyleSheet("""
                font-size: 15px;
                font-weight: 600;
                color: #1f1f4a;
            """)

            lbl_text = QLabel(text)
            lbl_text.setWordWrap(True)
            lbl_text.setStyleSheet("""
                font-size: 13px;
                font-weight: 600;                   
                color: #555;
            """)

            v.addWidget(lbl_title)
            v.addWidget(lbl_text)
            return card

        features_layout.addWidget(
            feature_card("✨", "AI Story Generation",
                         "Generate engaging stories from simple prompts.")
        )
        features_layout.addWidget(
            feature_card("🎨", "Smart Comic Creation",
                         "Turn stories into beautiful comic panels.")
        )
        features_layout.addWidget(
            feature_card("📤", "Export & Share",
                         "Download stories and comics in multiple formats.")
        )

        # ===== FOOTER =====
        footer = QLabel("Create • Imagine • Visualize ✨")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer.setStyleSheet("""
    font-size: 13px;
    color: #1f1f4a;
    background: transparent;
""")

        footer.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        footer.setAutoFillBackground(False)

        # ===== ADD TO MAIN LAYOUT =====
        main_layout.addLayout(top_bar)  
        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)
        main_layout.addSpacing(10)
        main_layout.addWidget(desc_card)
        main_layout.setStretchFactor(desc_card, 1)   
        main_layout.addLayout(btn_layout)
        main_layout.addSpacing(12)
        main_layout.addLayout(features_layout)
        main_layout.addStretch()
        main_layout.addWidget(footer)
        root = QVBoxLayout(self)
        root.addWidget(scroll)

    def show_help(self):
        dialog = HelpDialog(self)
        dialog.exec()