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

            return response.choices[0].message.content

        except Exception as e:
            return e
