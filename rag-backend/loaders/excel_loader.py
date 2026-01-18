import pandas as pd
from loaders.base_loader import BaseLoader

class ExcelLoader(BaseLoader):

    def load(self, file_path: str) -> str:
        sheets = pd.read_excel(file_path, sheet_name=None)
        text = []

        for sheet_name, df in sheets.items():
            text.append(f"Sheet: {sheet_name}")
            text.append(df.astype(str).to_string(index=False))

        return "\n".join(text)
