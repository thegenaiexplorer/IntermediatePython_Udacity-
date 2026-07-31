"""Ingest Content from DOCX Files."""


from typing import List
import docx
from .IngestorInterface import IngestorInterface
from .QuoteModel import QuoteModel


class DocxIngestor(IngestorInterface):
    """Class to Ingest DOCX File Content.

    Overrides allowed_extensions
    extends IngestorInterface
    implements parse class method
    """

    allowed_extensions = ['docx']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse DOCX Files.

        Arguments: Path for DOCX File
        Returns List of QuoteModel Objects
        """
        if not cls.can_ingest(path):
            raise Exception('Cannot Ingest Supplied File Type Exception')

        quotes = []
        doc = docx.Document(path)

        for para in doc.paragraphs:
            if para.text != "":
                parsed = para.text.split('-')
                new_quote = QuoteModel(parsed[0], parsed[1])
                quotes.append(new_quote)
        return quotes
