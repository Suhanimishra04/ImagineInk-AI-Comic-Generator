from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import QPixmap, QPainter
import os
import database

DROPDOWN_STYLE = """
QComboBox {
    background-color: white;
    border-radius: 12px;
    padding: 6px 30px 6px 12px;
    font-size: 13px;
    font-weight: 500;
    border: 1px solid #c8bfff;
    color: #2c2c54;
}
QComboBox:hover {
    border: 1px solid #a897ff;
}
QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 26px;
    border: none;
    background: transparent;
}
QComboBox::down-arrow {
    width: 0px;
    height: 0px;
    border-left: 6px solid transparent;
    border-right: 6px solid transparent;
    border-top: 7px solid #6c5ce7;
    margin-right: 8px;
}
QComboBox QAbstractItemView {
    background-color: #f2edff;
    border: 1px solid #c8bfff;
    border-radius: 10px;
    padding: 6px;
    outline: none;
    color: #2c2c54;
    selection-background-color: #d9ccff;
    selection-color: #2c2c54;
}
QComboBox QAbstractItemView::item {
    padding: 8px 12px;
    border-radius: 6px;
    color: #2c2c54;
    background-color: #f2edff;
    min-height: 28px;
}
QComboBox QAbstractItemView::item:hover {
    background-color: #d9ccff;
    color: #2c2c54;
}
QComboBox QAbstractItemView::item:selected {
    background-color: #d9ccff;
    color: #2c2c54;
}
"""


class HistoryPage(QWidget):
    def __init__(self, stack):
        super().__init__()
        self.stack = stack
        self.current_user_id = None
        self.all_stories = []

        # ===== LOAD BACKGROUND IMAGE =====
        base_path = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(base_path, "assets", "auth_bg.png")
        self.background_pixmap = QPixmap(image_path)

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, False)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(60, 40, 60, 40)
        main_layout.setSpacing(25)

        # ===== HEADER =====
        header = QLabel("📜 Generation History")
        header.setStyleSheet("""
            font-size: 28px;
            font-weight: 700;
            color: #2c2c54;
        """)

        # ===== TOP CONTROLS =====
        controls_layout = QHBoxLayout()

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("🔍 Search stories...")
        self.search_bar.setFixedHeight(42)
        self.search_bar.setStyleSheet("""
            QLineEdit {
                background-color: white;
                border-radius: 12px;
                padding-left: 14px;
                font-size: 14px;
                color: #2c2c54;
            }
        """)
        self.search_bar.textChanged.connect(self.filter_stories)

        self.genre_filter = QComboBox()
        self.genre_filter.setView(QListView())
        self.genre_filter.addItems(["All Genres", "Fantasy", "Horror", "Fairytales", "Mystery"])
        self.genre_filter.setFixedHeight(42)
        self.genre_filter.setStyleSheet(DROPDOWN_STYLE)
        self.genre_filter.currentTextChanged.connect(self.filter_stories)

        self.sort_dropdown = QComboBox()
        self.sort_dropdown.setView(QListView())
        self.sort_dropdown.addItems(["Newest First", "Oldest First"])
        self.sort_dropdown.setFixedHeight(42)
        self.sort_dropdown.setStyleSheet(DROPDOWN_STYLE)
        self.sort_dropdown.currentTextChanged.connect(self.filter_stories)

        controls_layout.addWidget(self.search_bar, 2)
        controls_layout.addWidget(self.genre_filter, 1)
        controls_layout.addWidget(self.sort_dropdown, 1)

        # ===== SCROLL AREA =====
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("background: transparent;")

        self.container = QWidget()
        self.container.setStyleSheet("background: transparent;")

        self.cards_layout = QVBoxLayout(self.container)
        self.cards_layout.setSpacing(20)
        self.cards_layout.addStretch()

        scroll.setWidget(self.container)

        # ===== BACK BUTTON =====
        back_btn = QPushButton("← Back to Studio")
        back_btn.setFixedHeight(45)
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c5ce7;
                color: white;
                border-radius: 14px;
                font-weight: 600;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #5a4bdc;
            }
        """)
        back_btn.clicked.connect(lambda: self.stack.setCurrentIndex(5))

        main_layout.addWidget(header)
        main_layout.addLayout(controls_layout)
        main_layout.addWidget(scroll)
        main_layout.addWidget(back_btn)

    # ===== LOAD USER DATA =====
    def load_user_data(self, user_id):
        self.current_user_id = user_id
        self.load_stories()

    # ===== LOAD STORIES FROM DATABASE =====
    def load_stories(self):
        if not self.current_user_id:
            return
        try:
            self.all_stories = database.get_user_history(self.current_user_id)
            self.filter_stories()
        except Exception as e:
            print(f"Error loading stories: {str(e)}")

    # ===== FILTER & DISPLAY STORIES =====
    def filter_stories(self):
        while self.cards_layout.count() > 1:
            item = self.cards_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        search_text = self.search_bar.text().lower()
        selected_genre = self.genre_filter.currentText()
        sort_order = self.sort_dropdown.currentText()

        filtered = self.all_stories

        if selected_genre != "All Genres":
            filtered = [s for s in filtered if s[3] and s[3].lower() == selected_genre.lower()]

        if search_text:
            filtered = [s for s in filtered if search_text in s[1].lower() or search_text in s[2].lower()]

        if sort_order == "Oldest First":
            filtered = sorted(filtered, key=lambda x: x[4])
        else:
            filtered = sorted(filtered, key=lambda x: x[4], reverse=True)

        if not filtered:
            no_data = QLabel("No stories found")
            no_data.setAlignment(Qt.AlignmentFlag.AlignCenter)
            no_data.setStyleSheet("color: #666; font-size: 16px; padding: 40px;")
            self.cards_layout.insertWidget(0, no_data)
        else:
            for story in filtered:
                title, prompt, story_text, genre, date = story
                preview = story_text[:100] + "..." if len(story_text) > 100 else story_text
                card = self.create_story_card(
                    title=title,
                    genre=genre,
                    date=str(date),
                    prompt=prompt,
                    preview=preview,
                    story_text=story_text
                )
                self.cards_layout.insertWidget(self.cards_layout.count() - 1, card)

    # ===== OPEN STORY =====
    def open_story(self, title, prompt, story_text, genre, date):
        dialog = QDialog(self)
        dialog.setWindowTitle(f"📖 {title}")
        dialog.setGeometry(100, 100, 900, 700)
        dialog.setStyleSheet("QDialog { background-color: #f5f5f5; }")

        layout = QVBoxLayout(dialog)
        layout.setSpacing(15)

        info_label = QLabel(f"<b>{title}</b> | 🎭 {genre} | 📅 {date}")
        info_label.setStyleSheet("font-size: 14px; color: #2c2c54; padding: 10px;")

        prompt_label = QLabel(f"<b>Prompt:</b> {prompt}")
        prompt_label.setStyleSheet("font-size: 12px; color: #666; padding: 10px; background: white; border-radius: 8px;")
        prompt_label.setWordWrap(True)

        story_display = QTextEdit()
        story_display.setText(story_text)
        story_display.setReadOnly(True)
        story_display.setStyleSheet("""
            QTextEdit {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 8px;
                padding: 15px;
                font-size: 14px;
            }
        """)

        close_btn = QPushButton("Close")
        close_btn.setFixedHeight(40)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #6c5ce7;
                color: white;
                border-radius: 8px;
                font-weight: 600;
            }
            QPushButton:hover { background-color: #5a4bdc; }
        """)
        close_btn.clicked.connect(dialog.close)

        layout.addWidget(info_label)
        layout.addWidget(prompt_label)
        layout.addWidget(story_display)
        layout.addWidget(close_btn)

        dialog.exec()

    # ===== DELETE STORY =====
    def delete_story(self, title, prompt):
        reply = QMessageBox.question(
            self,
            "Delete Story",
            f"Are you sure you want to delete '{title}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                database.delete_story(self.current_user_id, prompt)
                self.load_stories()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete: {str(e)}")

    # ===== EXPORT STORY =====
    def export_story(self, title, story_text, genre, date):
        file_path, file_filter = QFileDialog.getSaveFileName(
            self,
            "Export Story",
            f"{title}",
            "Text Files (*.txt);;PDF Files (*.pdf)"
        )

        if file_path:
            try:
                if file_path.endswith('.pdf') or 'PDF' in file_filter:
                    try:
                        from reportlab.lib.pagesizes import letter
                        from reportlab.pdfgen import canvas

                        c = canvas.Canvas(file_path, pagesize=letter)
                        width, height = letter

                        c.setFont("Helvetica-Bold", 18)
                        c.setFillColorRGB(0.42, 0.36, 0.90)
                        c.drawString(50, height - 60, f"{title}")

                        c.setFont("Helvetica", 11)
                        c.setFillColorRGB(0.3, 0.3, 0.3)
                        c.drawString(50, height - 85, f"Genre: {genre}   |   Date: {date}")

                        c.setStrokeColorRGB(0.42, 0.36, 0.90)
                        c.setLineWidth(1.5)
                        c.line(50, height - 100, width - 50, height - 100)

                        c.setFont("Helvetica", 11)
                        c.setFillColorRGB(0.1, 0.1, 0.1)
                        text_object = c.beginText(50, height - 130)
                        text_object.setFont("Helvetica", 11)
                        text_object.setLeading(18)

                        for line in story_text.split('\n'):
                            if len(line) > 90:
                                words = line.split()
                                current_line = ""
                                for word in words:
                                    if len(current_line) + len(word) < 90:
                                        current_line += word + " "
                                    else:
                                        text_object.textLine(current_line.strip())
                                        current_line = word + " "
                                if current_line:
                                    text_object.textLine(current_line.strip())
                            else:
                                text_object.textLine(line)

                        c.drawText(text_object)
                        c.save()
                        QMessageBox.information(self, "Success", f"Story exported to PDF:\n{file_path}")

                    except Exception as pdf_error:
                        QMessageBox.warning(self, "Info", f"PDF export failed: {str(pdf_error)}\nExporting as TXT instead.")
                        txt_path = file_path.replace('.pdf', '.txt')
                        with open(txt_path, 'w', encoding='utf-8') as f:
                            f.write(f"Title: {title}\nGenre: {genre}\nDate: {date}\n")
                            f.write("=" * 50 + "\n\n")
                            f.write(story_text)
                        QMessageBox.information(self, "Saved", f"Exported as TXT:\n{txt_path}")
                else:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(f"Title: {title}\nGenre: {genre}\nDate: {date}\n")
                        f.write("=" * 50 + "\n\n")
                        f.write(story_text)
                    QMessageBox.information(self, "Success", f"Story exported to:\n{file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Export failed: {str(e)}")

    # ===== BACKGROUND DRAW METHOD =====
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.background_pixmap)

    # ===== STORY CARD CREATOR =====
    def create_story_card(self, title, genre, date, prompt, preview, story_text):
        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 255, 255, 0.92);
                border-radius: 18px;
                padding: 18px;
            }
        """)

        layout = QVBoxLayout(card)
        layout.setSpacing(8)

        title_label = QLabel(f"✨ {title}")
        title_label.setStyleSheet("font-size: 16px; font-weight: 600; color: #2c2c54;")

        genre_date_layout = QHBoxLayout()
        genre_label = QLabel(f"🎭 {genre}")
        genre_label.setStyleSheet("font-size: 12px; color: #6b5cff;")
        date_label = QLabel(f"📅 {date}")
        date_label.setStyleSheet("font-size: 12px; color: #6b5cff;")
        genre_date_layout.addWidget(genre_label)
        genre_date_layout.addWidget(date_label)
        genre_date_layout.addStretch()

        prompt_label = QLabel(f"Prompt: {prompt}")
        prompt_label.setWordWrap(True)
        prompt_label.setStyleSheet("font-size: 12px; color: #999; font-style: italic;")

        preview_label = QLabel(preview)
        preview_label.setWordWrap(True)
        preview_label.setStyleSheet("font-size: 13px; color: #444;")

        btn_layout = QHBoxLayout()
        open_btn = QPushButton("Open")
        delete_btn = QPushButton("Delete")
        export_btn = QPushButton("Export")

        open_btn.clicked.connect(lambda: self.open_story(title, prompt, story_text, genre, date))
        delete_btn.clicked.connect(lambda: self.delete_story(title, prompt))
        export_btn.clicked.connect(lambda: self.export_story(title, story_text, genre, date))

        for btn in (open_btn, delete_btn, export_btn):
            btn.setMinimumHeight(34)
            btn.setMinimumWidth(80)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #e6ddff;
                    border-radius: 10px;
                    padding: 6px 14px;
                    font-size: 13px;
                    font-weight: 500;
                    color: #2c2c54;
                }
                QPushButton:hover { background-color: #d4c7ff; }
            """)
            btn_layout.addWidget(btn)

        btn_layout.addStretch()

        layout.addWidget(title_label)
        layout.addLayout(genre_date_layout)
        layout.addWidget(prompt_label)
        layout.addWidget(preview_label)
        layout.addLayout(btn_layout)

        return card