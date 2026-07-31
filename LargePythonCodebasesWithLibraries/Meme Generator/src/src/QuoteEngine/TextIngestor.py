"""Ingest Content from TXT Files."""


from typing import List
from .IngestorInterface import IngestorInterface
from .QuoteModel import QuoteModel


class TextIngestor(IngestorInterface):
    """Class to Ingest TEXT File Content.

    overrides allowed_extensions
    extends IngestorInterface
    implements parse class method
    """

    allowed_extensions = ['txt']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse Text Files.

        Arguments: path for TEXT File
        Returns List of QuoteModel Objects
        """
        if not cls.can_ingest(path):
            raise Exception('Cannot Ingest File Type Exception')

        quotes = []
        with open(path, 'r') as f:
            for line in f:
                line = str(line).strip()
                qt = line.split('-')[0]
#                qt = "".join(ch for ch in qt if ch.isalnum())
                author = line.split('-')[-1]
                new_quote = QuoteModel(qt, author)
                quotes.append(new_quote)
        return quotes
