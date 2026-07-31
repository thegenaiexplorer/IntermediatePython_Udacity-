"""CLI for Meme Generation."""


import os
import random
import argparse as ap
# @TODO Import your Ingestor and MemeEngine classes
from MemeEngine import MemeGenerator
from QuoteEngine import Ingestor
from QuoteEngine import QuoteModel


def generate_meme(path=None, body=None, author=None):
    """Generate a meme given a path and a quote."""
    img = None
    quote = None

    if path is None:
        images = "./_data/photos/dog/"
        imgs = []
        for root, dirs, files in os.walk(images):
            imgs = [os.path.join(root, name) for name in files]
        try:
            if (len(imgs) == 0):
                raise Exception("No Valid Image Files")
        except Exception as e:
            print(f'Error Occurred: "{e}"')

        img = random.choice(imgs)
    else:
        img = path
    if body is None:
        quote_files = ['./_data/DogQuotes/DogQuotesTXT.txt',
                       './_data/DogQuotes/DogQuotesDOCX.docx',
                       './_data/DogQuotes/DogQuotesPDF.pdf',
                       './_data/DogQuotes/DogQuotesCSV.csv']
        quotes = []
        try:
            for f in quote_files:
                quotes.extend(Ingestor.parse(f))
        except Exception as e:
            print(e)
            print('Allowed File Extensions are csv, docx, pdf, txt')
        try:
            if (len(quotes) == 0):
                raise Exception("Quote Body is empty")
        except Exception as e:
            print(f'Error occcured: "{e}"')
        quote = random.choice(quotes)
    else:
        try:
            if author is None:
                raise Exception('Author Required if Body is Used')
        except Exception as e:
            print(f'Error Occurred : "{e}"')
            return None
        quote = QuoteModel(body, author)
    if not (os.path.exists('./tmp')):
        os.mkdir('./tmp')
    meme = MemeGenerator('./tmp')
    try:
        path = meme.make_meme(img, quote.body, quote.author)
        return path
    except Exception as e:
        print(f'Error Creating Meme : "{e}"')


if __name__ == "__main__":
    # @TODO Use ArgumentParser to parse the following CLI arguments
    # path - path to an image file
    # body - quote body to add to the image
    # author - quote author to add to the image
    args = None
    descr = "Please enter Image File Path, Quote and Author"
    parser = ap.ArgumentParser(description=descr)
    h_path = "Image File Path Including File Name"
    h_body = "Quote which needs to be displayed in Meme"
    h_author = "Author of the Quote"
    parser.add_argument('--path', type=str, default=None, help=h_path)
    parser.add_argument('--body', type=str, default=None, help=h_body)
    parser.add_argument('--author', type=str, default=None, help=h_author)
    args = parser.parse_args()
    path_meme = generate_meme(args.path, args.body, args.author)
    if path_meme is None:
        print("No Meme generated. Please refer to error message")
    else:
        print(f'The path of generated meme is {path_meme}')
