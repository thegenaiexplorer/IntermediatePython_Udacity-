"""QuoteModel object for Meme."""


class QuoteModel():
    """Class for creating QuoteModel object."""

    def __init__(self, body, author):
        """Create a new QuoteModel Object.

        Arguments:
            body {str} -- Quote supplied by calling program
            author {str} -- Author of the Quote supplied by calling program
        """
        self.body = body
        self.author = author

    def __repr__(self):
        """Represent object in string format.

        < self.body, self.author >
        """
        obj_return = '<  ' + self.body + ', ' + self.author + ' >'
        return obj_return
