"""Ingest Content from PDF Files."""


from typing import List
import os
import subprocess as sp
from .IngestorInterface import IngestorInterface
from .QuoteModel import QuoteModel


class PDFIngestor(IngestorInterface):
    """Class to Ingest PDF File Content.

    overrides allowed_extensions
    extends IngestorInterface
    implements parse class method
    """

    allowed_extensions = ['pdf']

    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse PDF Files.

        Arguments: path for PDF File
        Returns List of QuoteModel Objects
        """
        if not cls.can_ingest(path):
            raise Exception('Cannot Ingest File Type Extension')

        quotes = []
        binary = 'pdftotext.exe'
        arg = '-layout'
        target_file = 'temppdftxt.txt'
        p = sp.Popen([binary, arg, path, target_file], stdout=sp.PIPE)
        output, err = p.communicate()
        p_status = p.wait()
        with open('temppdftxt.txt', 'r') as t:
            for line in t:
                if line.strip() != "":
                    line_list = line.split('-')
                    quote, author = line_list[0].strip(), line_list[-1].strip()
                    new_qm = QuoteModel(quote, author)
                    qt_tmp = "".join(ch for ch in new_qm.body if ch.isalnum())
                    if (len(qt_tmp) > 4):
                        quotes.append(new_qm)
        print(quotes)
        os.remove(target_file)
        return quotes
