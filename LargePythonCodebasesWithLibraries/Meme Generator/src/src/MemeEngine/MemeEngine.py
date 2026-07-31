"""Implements Functionality to generate Meme."""


from PIL import Image, ImageDraw, ImageFont
import random
import textwrap


class MemeGenerator():
    """Class to generate Meme.

    Implements methods to load, modify and generate Meme
    """

    def __init__(self, output_dir):
        """Initialize MemeGenerator Object.

        Arguments: path for output directory to store memes
        output_dir : Path for generated memes
        img_path: Path of Image to be modified into Meme
        body: Quote
        author: Author of the Quote
        """
        self.output_dir = output_dir
        self.img_path = None
        self.body = None
        self.author = None

    def load_image(self):
        """Load supplied Image and return Image object."""
        try:
            img = Image.open(self.img_path)
            return img
        except:
            return None

    def transform_image(self, img, width):
        """Resize the Image.

        Calculates aspect ratio
        Resizes Image
        Returns Resized/Transformed Image
        """
        ratio = width/float(img.size[0])
        height = int(ratio*float(img.size[1]))
        transformed_img = img.resize((width, height), Image.NEAREST)
        return transformed_img

    def add_caption(self, img, file_ext):
        """Generate and Save Meme.

        Arguments: transformed/resized image and file extention
        Using Pillow Library, it combines image and quote
        Saves the combined image file(Meme)
        Returns the Path of generated Meme file
        """
        draw = ImageDraw.Draw(img)
        x = random.randint(0, img.size[0] - 400)
        y = random.randint(0, img.size[1] - 25)
        message = self.body + " - " + self.author
        list_message = "\n".join(textwrap.wrap(message, width=30))
        font = ImageFont.truetype("./arial/arial.ttf", 20)
        draw.multiline_text((x, y),
                             list_message,
                             font=font, fill='white',
                             spacing=2, align="left")
        rand_file = random.randint(0, 1000000)
        if (file_ext is None):
            file_ext = "jpg"
        out_path = self.output_dir + "/img_" + str(rand_file) + "." + file_ext
        img.save(out_path)
        return out_path

    def make_meme(self, img_path, text, author, width=500) -> str:
        """Master Method to generate Meme.

        Arguments: Image Path, Quote and Author
        Initializes Object Variables(img_path, body and author)
        Checks and Stores File extension of supplied image
        calls appropriate methods to:
            1) Load Image
            2) Transform/Resize Image
            3) Generate and Store Meme
            4) Returns path to Generated Meme
        """
        self.img_path = img_path
        self.body = text
        self.author = author
        file_ext = img_path.split('.')[-1]
        img = self.load_image()
        if img is None:
            raise Exception("Cannot Load Image. Invalid Image File")
        img = self.transform_image(img, width)
        mod_img_path = self.add_caption(img, file_ext)
        return mod_img_path
