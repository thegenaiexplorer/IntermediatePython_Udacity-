"""Web Interface for Meme Generation."""


import random
import os
import requests
from flask import Flask, render_template, abort, request
# @TODO Import your Ingestor and MemeEngine classes
from QuoteEngine import QuoteModel
from QuoteEngine import Ingestor
from MemeEngine import MemeGenerator

app = Flask(__name__)
if not (os.path.exists('./static')):
    os.mkdir('./static')
if not (os.path.exists('./tmp')):
    os.mkdir('./tmp')

meme = MemeGenerator('./static')


def setup():
    """Load all resources."""
    quote_files = ['./_data/DogQuotes/DogQuotesTXT.txt',
                   './_data/DogQuotes/DogQuotesDOCX.docx',
                   './_data/DogQuotes/DogQuotesPDF.pdf',
                   './_data/DogQuotes/DogQuotesCSV.csv']

    # TODO: Use the Ingestor class to parse all files in the
    # quote_files variable
    quotes = []
    try:
        for f in quote_files:
            quotes.extend(Ingestor.parse(f))
    except Exception as e:
        print(e)
        print('Allowed File Extensions are csv, docx, pdf, txt')

    images_path = "./_data/photos/dog/"

    # TODO: Use the pythons standard library os class to find all
    # images within the images images_path directory
    imgs = []
    for root, dirs, files in os.walk(images_path):
        imgs = [os.path.join(root, name) for name in files]
    return quotes, imgs


quotes, imgs = setup()


@app.route('/')
def meme_rand():
    """Generate a random meme."""
    # @TODO:
    # Use the random python standard library class to:
    # 1. select a random image from imgs array
    # 2. select a random quote from the quotes array

    img = random.choice(imgs)
    quote = random.choice(quotes)
    path = meme.make_meme(img, quote.body, quote.author)
    print(f'Path generated is {path}')
    return render_template('meme.html', path=path)


@app.route('/create', methods=['GET'])
def meme_form():
    """User input for meme information."""
    return render_template('meme_form.html')


@app.route('/create', methods=['POST'])
def meme_post():
    """Create a user defined meme."""
    # @TODO:
    # 1. Use requests to save the image from the image_url
    #    form param to a temp local file.
    # 2. Use the meme object to generate a meme using this temp
    #    file and the body and author form paramaters.
    # 3. Remove the temporary saved image.

    path = None
    url = request.form.get("image_url")
    file_ext = url.split('.')[-1]
    body = request.form.get("body")
    author = request.form.get("author")
    print(url, body, author)
    try:
        if not (url.startswith("http://") or url.startswith("https://")):
            raise Exception("Please provide Valid URL")
        if (len(body) < 3):
            raise Exception("Please provide valid Quote")
        if (len(author) < 2):
            raise Exception("Please provide valid Author Name")
    except Exception as e:
        print(e)
        return render_template('meme_form.html')

    file_name = "./tmp/user_defined_image." + file_ext
    try:
        image_data = requests.get(url)
        with open(file_name, 'wb') as f:
            f.write(image_data.content)
    except (requests.exceptions.ConnectionError, Exception) as e:
        print("Cannot connect to specified URL")
        print(e)
        return render_template('meme_error.html')
    try:
        path = meme.make_meme(file_name, body, author)
    except Exception as e:
        print(f'Please check the file type provided in URL "{e}"')
        os.remove(file_name)
        return render_template('meme_incorrect_file.html')
    os.remove(file_name)
    return render_template('meme.html', path=path)


if __name__ == "__main__":
    app.run()
