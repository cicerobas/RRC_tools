import datetime

from jinja2 import Environment, FileSystemLoader
from pandas import DataFrame
from weasyprint import HTML

from utils.assets_path import resource_path

template_dir = resource_path('assets/template')
env = Environment(loader=FileSystemLoader(template_dir))
template = env.get_template('template.html')


def generate_pdf(formated_data: dict, save_path: str) -> str:
    html_document = template.render(formated_data)
    file_name = f'RRC ASSTEC {formated_data["ASSTEC"]} {formated_data["GRUPO"]} - {formated_data["CLIENTE"]}'
    file_path = f"{save_path}/{file_name}.pdf"

    HTML(string=html_document, base_url=template_dir).write_pdf(file_path)

    return file_path


def handle_asstec_data(document_data: dict, items_data: DataFrame) -> dict:
    num_serie = items_data["num_serie"].to_list()
    descricao = [f"{row['num_serie']}: {row['defeito_c']}" for _, row in items_data.iterrows()]
    situacao = [f"{row['num_serie']}: {row['situacao']}" for _, row in items_data.iterrows()]
    causa = [f"{row['num_serie']}: {row['causa']}" for _, row in items_data.iterrows()]
    acao = [f"{row['num_serie']}: {row['acao']}" for _, row in items_data.iterrows()]
    parecer = [f"{row['num_serie']}: {row['parecer']}" for _, row in items_data.iterrows()]

    return {**document_data,
            "DATA": datetime.date.today().strftime('%d/%m/%Y'),
            "NUM_SERIE": ', '.join(num_serie),
            "DESCRICAO": descricao,
            "SITUACAO": situacao,
            "CAUSA": causa,
            "ACAO": acao,
            "PARECER": parecer
            }
