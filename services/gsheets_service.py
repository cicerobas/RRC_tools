import json

import gspread


class GSheetsService:
    def __init__(self, access_data: tuple):
        self._spreadsheet_id = access_data[0]
        self._credentials = json.loads(access_data[1])
        self._gsheets_client = gspread.service_account_from_dict(self._credentials)
        self.spreadsheet = self._gsheets_client.open_by_key(self._spreadsheet_id)
        self.asstec_worksheet = self.spreadsheet.get_worksheet(0)
        self.items_worksheet = self.spreadsheet.get_worksheet(1)

    def check_valid_asstec(self, asstec_number: str) -> int:
        asstec = self.asstec_worksheet.find(asstec_number, in_column=2)
        return asstec.row if asstec is not None else -1

    def validate_asstec_required_fields(self, row: int) -> str:
        asstec_data = self.asstec_worksheet.row_values(row)
        required_fields = {
            2: "CLIENTE",
            3: "GRUPO",
            4: "NFe",
            8: "RESPONSÁVEL",
        }
        for i in required_fields.keys():
            if not asstec_data[i]:
                return f"O campo [{required_fields[i]}] é obrigatório!"

        return ""

    def get_items_data(self, asstec_number: str) -> list[list[str]]:
        data_range = self.items_worksheet.findall(asstec_number, in_column=1)
        if len(data_range) > 0:
            items_data = self.items_worksheet.get(f"B{data_range[0].row}:J{data_range[-1].row}")
            return items_data
        return []
