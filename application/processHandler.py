import cv2
import pytesseract
from PIL import Image
from openai import OpenAI
import os
from openai import OpenAI
from pdf2image import convert_from_path
import json


class Handler:
    def getText(filename, suffix):
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
                n_file = cv2.imread(filename)
                Nimage = cv2.cvtColor(n_file, cv2.COLOR_BGR2GRAY)
                text = pytesseract.image_to_string(Nimage)

            return text

        except Exception as e:
            return e
