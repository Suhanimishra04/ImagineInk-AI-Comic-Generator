import requests

API_URL = "http://172.16.40.63:8000/generate-story"
COMIC_API = "http://172.16.40.63:8000/generate-comic"


def generate_story(prompt, mode, project_id):
    payload = {
        "prompt": prompt,
        "mode": mode,
        "project_id": project_id
    }

    response = requests.post(API_URL, json=payload)
    data = response.json()

    # story + prompt_id backend se aayega
    return data.get("story"), data.get("prompt_id")


def generate_comic(story, prompt_id):

    payload = {

        "story": story,

        "prompt_id": prompt_id

    }

    response = requests.post(

        COMIC_API,

        json=payload

    )

    data = response.json()

    print("FULL API RESPONSE:", data)

    return data