import cv2
import pytesseract
from PIL import Image
from openai import OpenAI
import os
from openai import OpenAI
from pdf2image import convert_from_path
import json
from skimage import io


class Handler:
    def getText(filename, suffix):
        pytesseract.pytesseract.tesseract_cmd = r"tesseract\tesseract.exe"

        filename = filename.replace("\\", "/")
        text = ""
        try:
            if suffix == "pdf":
                pages_index = []

                # poppler_path= r"C:\path\to\poppler-xx\bin"
                images = convert_from_path(filename)
                for i in range(len(images)):
                    page = "note" + str(i) + ".jpg"
                    images[i].save(page, "JPEG")
                    pages_index.append(page)

                for j in pages_index:
                    n_file = cv2.imread(j)
                    Nimage = cv2.cvtColor(n_file, cv2.COLOR_BGR2GRAY)
                    text += pytesseract.image_to_string(Nimage)

            else:
                print("This is an image file")
                n_file = io.imread(filename)
                Nimage = cv2.cvtColor(n_file, cv2.COLOR_BGR2GRAY)
                text = pytesseract.image_to_string(Nimage)

            os.remove(filename)

            return text

        except Exception as e:
            return e

    def return_flashcards(text):
        try:
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

            prompt = f"from my notes = {text} Create 20 flashcards with concise information on the key concepts covered. Each flashcard should address a specific point from the notes. Ensure that the content is clear and suitable for learning purposes."

            response = client.chat.completions.create(
                model="gpt-3.5-turbo-1106",
                response_format={"type": "json_object"},
                seed=10,
                temperature=0.2,
                n=20,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant designed to output JSON",
                    },
                    {"role": "user", "content": prompt},
                ],
            )
            # currently response is in format 'flashcards'-> id ->  front -> back

            """
            """

            return response.choices[0].message.content

        except Exception as e:
            return e

    def json_toflashcards(response):
        rKey = response
        flashcards = []
        iter_list = rKey["flashcards"]
        # for my_dict in iter_list:
        #     for key, value in my_dict.items():
        #         flashcards.append(value)

        # for key in iter_list:
        #     count = 0
        #     n_list = list(key.values())

        #     for i in range(len(n_list[::2])):
        #         index = {"front": n_list[count], "back": n_list[count + 1]}
        #         flashcards.append(index)
        #         count += 1

        # flashcard should be in format 'front' -> 'back'
        for card in rKey.get("flashcards", []):
            card_data = {}
            for key, value in card.items():
                # Assuming keys other than 'concept' and 'description' are used as 'front' and 'back'
                card_data[key.lower()] = value

            flashcards.append(card_data)

        return flashcards

    """
    { "flashcards": [ { "concept": "Verb suffixes for imperative and declarative sentences", "description": "Verb suffixes like aye or ye denote imperative sentences, while kSto and yelo denote declarative sentences in Yatk language." }, { "concept": "Gender-specific speech in imperative and declarative sentences", "description": "Women use aye/ye in imperative speech and ksto in declarative speech, while men use ayo/yo in imperative speech and yelo in declarative speech in Yatk language." }, { "concept": "Imperative suffixes for woman and man speaking", "description": "Imperative suffixes for woman speaking are -ye and -we, while for man speaking are -yo and -wo in Yatk language." }, { "concept": "Phoneme 'y' changes to 'w' in certain contexts", "description": "The 'y' changes to 'w' when the stem ends with 'u', 'y', and 'o' phonemes in Yatk language." }, { "concept": "Reason for changing 'y' to 'w' sound", "description": "Changing from 'y' to 'w' sound makes it easier to pronounce neighboring phonemes, especially nasal vowels, in Yatk language." }, { "concept": "Example of imperative sentences", "description": "Examples of imperative sentences in Yatk language: 'inquire secretly!' (woman speaking) - pasiye, 'be hungry!' (man speaking) - jtukheyo" } ] }
    """
