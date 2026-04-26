from PyQt6.QtCore import QThread, pyqtSignal
from api_client import generate_comic

class ComicWorker(QThread):
    finished = pyqtSignal(object)
    error = pyqtSignal(str)

    def __init__(self, story, prompt_id):
        super().__init__()
        self.story = story
        self.prompt_id = prompt_id

    def run(self):
        try:
            print("🔥 ComicWorker started")

            response = generate_comic(self.story, self.prompt_id)

            print("🔥 ComicWorker response:", response)

            if response is None:
                raise Exception("No response from API")

            self.finished.emit(response)

        except Exception as e:
            print("❌ Worker Error:", str(e))
            self.error.emit(str(e))