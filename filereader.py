import cv2
import pytesseract
from PIL import Image
from openai import OpenAI
import os
from openai import OpenAI
from pdf2image import convert_from_path


# this helps use the tesseract OCR executable file from the directory specified
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# the match case statement is used to check the suffix of the file and print the appropriate message
try:
    path = input("Enter the path to the file: ")
    path.replace("\\", "/")

    suffix = path[-3:]
    text = ""
    match suffix:
        # in the case of a pdf file I want to convert it to an image and then read the text
        case "pdf":
            try:
                print("This is a PDF file")
                pages_index = []

                # poppler_path= r"C:\path\to\poppler-xx\bin"
                images = convert_from_path(path)
                for i in range(len(images)):
                    page = "note" + str(i) + ".jpg"
                    images[i].save(page, "JPEG")
                    pages_index.append(page)

                for j in pages_index:
                    n_file = cv2.imread(j)
                    Nimage = cv2.cvtColor(n_file, cv2.COLOR_BGR2GRAY)
                    text = pytesseract.image_to_string(Nimage)

            except Exception as e:
                print(e)

        # in the case of other files, we assume that they are images and then read the text
        # else we print an error message that we catch using the except statement
        case _:
            file = cv2.imread(path)
            # for better results using the OCR, we convert the image to grayscale
            Nimage = cv2.cvtColor(file, cv2.COLOR_BGR2GRAY)
            text = pytesseract.image_to_string(Nimage)
            print(text)


except FileNotFoundError:
    print("File not found, please check the path and try again")


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


prompt = f"from my notes = {text} Create 20 flashcards with concise information on the key concepts covered. Each flashcard should address a specific point from the notes. Ensure that the content is clear and suitable for learning purposes."

response = client.chat.completions.create(
    model="gpt-4-1106-preview",
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


print(response.choices[0].message.content)
