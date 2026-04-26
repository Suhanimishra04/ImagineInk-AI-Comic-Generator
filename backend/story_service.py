import requests
from PyQt6.QtCore import QThread, pyqtSignal

# DGX SERVER ADDRESS
API_URL = "http://172.16.40.63:8000/generate-story"


class StoryWorker(QThread):

    finished = pyqtSignal(str, int)
    error = pyqtSignal(str)

    def __init__(self, prompt, genre, project_id):
        super().__init__()
        self.prompt = prompt
        self.genre = genre
        self.project_id = project_id

    def run(self):
        try:
            payload = {
                "prompt": self.prompt,
                "mode": self.genre,
                "project_id": self.project_id
            }

            response = requests.post(API_URL, json=payload)
            data = response.json()

            if "story" in data:
                # story + prompt_id emit
                self.finished.emit(data["story"], data["prompt_id"])
            else:
                self.error.emit(data.get("error", "Story generation failed"))

        except Exception as e:
            self.error.emit(str(e))