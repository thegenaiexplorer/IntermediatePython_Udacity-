"""Abstract Class to be inherited by other Ingestors."""


from abc import ABC, abstractmethod
from typing import List
from .QuoteModel import QuoteModel


class IngestorInterface(ABC):
    """Abstract Class for Different Ingestors.

    allowed_extensions -- List type variable
    can_ingest is a class method
    parse is an abstract/class method
    """

    allowed_extensions = []

    @classmethod
    def can_ingest(cls, path: str) -> bool:
        """Determine Ingestibility of supplied file type.

        Returns Boolean value
        """
        ext = path.split('.')[-1]
        return ext in cls.allowed_extensions

    @classmethod
    @abstractmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        """Parse File and return List of QuoteModel Objects."""
        pass
