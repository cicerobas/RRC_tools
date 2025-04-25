import json

import gspread
import pandas as pd
from pandas import DataFrame


class GSheetsService:
    REQUIRED_FIELDS = {
        2: "CLIENTE",
        3: "GRUPO",
        4: "NFe",
        8: "RESPONSÁVEL",
    }

    COLUMN_NAMES = [
        "num_serie",
        "data",
        "retorno",
        "situacao",
        "defeito_c",
        "defeito_r",
        "causa",
        "acao",
        "parecer",
    ]

    def __init__(self, access_data: tuple):
        self._spreadsheet_id = access_data[0]
        self._credentials = json.loads(access_data[1])
        self._gsheets_client = gspread.service_account_from_dict(self._credentials)
        self.spreadsheet = self._gsheets_client.open_by_key(self._spreadsheet_id)
        self.asstec_sheet = self.spreadsheet.get_worksheet(0)
        self.items_sheet = self.spreadsheet.get_worksheet(1)

    def find_asstec_row(self, asstec_number: str) -> int:
        result = self.asstec_sheet.find(asstec_number, in_column=2)
        return result.row if result else -1

    def validate_asstec_required_data(self, row: int) -> str | list[str]:
        asstec_data = self.asstec_sheet.row_values(row)
        missing_field = self._has_required_fields(asstec_data)
        return f"O campo [{missing_field}] é obrigatório!" if missing_field else asstec_data

    def _has_required_fields(self, asstec_data: list[str]) -> str | None:
        for index, field_name in self.REQUIRED_FIELDS.items():
            if not asstec_data[index]:
                return field_name
        return None

    def get_items_data(self, asstec_number: str) -> DataFrame | None:
        data_range = self.items_sheet.findall(asstec_number, in_column=1)
        if data_range:
            return pd.DataFrame(
                self.items_sheet.get(f"B{data_range[0].row}:J{data_range[-1].row}"),
                columns=self.COLUMN_NAMES,
            )
        return None
