from abc import ABC, abstractmethod

class BaseLoader(ABC):

    @abstractmethod
    def load(self, file_path: str) -> str:
        """
        Reads a file and returns extracted text
        """
        pass
