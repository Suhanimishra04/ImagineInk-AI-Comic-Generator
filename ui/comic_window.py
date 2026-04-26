import requests
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from io import BytesIO


class ComicWindow(QWidget):

    def __init__(self, comic_urls, job_id):
        super().__init__()

        self.setWindowTitle("Comic Reader")
        self.setGeometry(200,100,900,650)

        self.urls = comic_urls
        self.job_id = job_id
        self.index = 0

        layout = QVBoxLayout()

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(self.image_label)

        btn_layout = QHBoxLayout()

        prev_btn = QPushButton("◀ Previous")
        next_btn = QPushButton("Next ▶")

        prev_btn.clicked.connect(self.prev_page)
        next_btn.clicked.connect(self.next_page)

        export_btn = QPushButton("Export Comic")
        export_btn.clicked.connect(self.export_comic)

        btn_layout.addWidget(prev_btn)

        btn_layout.addWidget(next_btn)

        btn_layout.addWidget(export_btn)

        layout.addLayout(btn_layout)

        self.setLayout(layout)

        self.load_image()


    def load_image(self):

        try:

            # ✅ SIRF YEH 3 LINES BADLI HAIN
            item = self.urls[self.index]
            url = item["image"] if isinstance(item, dict) else item
            if url.startswith("/outputs/"):
                url = f"http://172.16.40.63:8000{url}"

            print("Loading:", url)

            response = requests.get(url, timeout=30)

            print("Status:", response.status_code)
            print("Content-Type:", response.headers.get("Content-Type"))
            print("Size:", len(response.content))

            if response.status_code != 200:
                self.image_label.setText("Image download failed")
                return

            pixmap = QPixmap()

            success = pixmap.loadFromData(response.content)

            print("Pixmap success:", success)

            if not success:
                self.image_label.setText("Pixmap load failed")
                return

            scaled = pixmap.scaled(
                750,
                550,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )

            self.image_label.setPixmap(scaled)

        except Exception as e:

            self.image_label.setText(str(e))

    def next_page(self):

        if self.index < len(self.urls)-1:

            self.index += 1

            self.load_image()


    def prev_page(self):

        if self.index > 0:

            self.index -= 1

            self.load_image()
    def export_comic(self):

        try:

            url = f"http://172.16.40.63:8000/export-comic/{self.job_id}"

            response = requests.get(url)

            path, _ = QFileDialog.getSaveFileName(

                self,

                "Save Comic",

                "comic.zip",

                "Zip Files (*.zip)"

            )

            if path:

                with open(path,"wb") as f:

                    f.write(response.content)

                QMessageBox.information(

                    self,

                    "Success",

                    "Comic exported successfully"

                )

        except Exception as e:

            QMessageBox.warning(

                self,

                "Error",

                str(e)

            )

        except Exception as e:

            QMessageBox.warning(

                self,
                "Error",
                str(e)

            )


if __name__ == "__main__":

    import sys

    app = QApplication(sys.argv)

    test_urls = [
        "http://172.16.40.63:8000/outputs/panel_1.png",
        "http://172.16.40.63:8000/outputs/panel_2.png",
        "http://172.16.40.63:8000/outputs/panel_3.png"
    ]

    window = ComicWindow(test_urls,"test")
    window.show()

    sys.exit(app.exec())