# Flashcard.AI
This is a personal fullstack project that uses python's Flask fullstack frame work along side tesseract's OCR,a MongoDB database,openCV, pdf2file, bootstrap, and openAI's GPT-3.5-turbo model to parse characters from students notes and return flashcards that are saved to the database. Authemtication and login is handled using WTForms and the Werkzeug library for password hashing. A RESTful API implementation is also featured for handling CRUD operations.
## How it works
Students' notes are uploaded to the server and depending on the file type (image or pdf), file processing is handled accordingly. In the case of a pdf, the `pdf2image` library converts the image file to a pdf and the file can be passed to openCV. For image files, they are handled directly. OpenCV is used for image manipulation resulting in order to aid accurate character recognition by the OCR. `Pytesseract`(which is the OCR of choice) then detects characters in the page and returns a text object. The text object is passed to the openAI model and a (usually non-deterministic) response it returned. Routing, Jinja templates, and other processes handles the response which is then displayed and saved to the MongoDB database. 
 
## Major difficulty I ran into
The OpenAI model failed to return determinsitic responses even after configuring `seed` and `temperature` parameters. The work around however was a simple set of `JSON` and array manipulation methods to ensure the flashcards were displayed in the same project. 

### Deployment
Deployment is pending as I plan on utilizing Heroku Cloud Services.

> [!NOTE]
> This project is not affiliated with Indiana University. 
