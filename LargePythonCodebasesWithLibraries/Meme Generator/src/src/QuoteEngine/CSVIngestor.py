"""Ingest content from CSV Files."""


from typing import List
import pandas as pd
from .IngestorInterface import IngestorInterface
from .QuoteModel import QuoteModel


class CSVIngestor(IngestorInterface):
    """Class to Ingest CSV file Content.

    overrides allowed_extensions
    extends IngestorInterface
    implements parse class method
    """

    allowed_extensions = ['csv']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse  CSV Files.

        Arguments: path for CSV File
        returns list of QuoteModel Objects
        """
        if not cls.can_ingest(path):
            raise Exception('Cannot Ingest File Type Exception')

        quotes = []
        df_quote = pd.read_csv(path, header=0)
        for index, row in df_quote.iterrows():
            new_quote = QuoteModel(row['body'], row['author'])
            quotes.append(new_quote)

        return quotes
