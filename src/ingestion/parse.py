from pathlib import Path

from docling.document_converter import DocumentConverter


def parse_html(html_path: str):
    """
    Parsează fișierul HTML și întoarce DoclingDocument.
    """

    converter = DocumentConverter()

    result = converter.convert(html_path)

    return result.document


import json


def save_docling_json(document, output_dir="tmp/docling"):
    """
    Salvează DoclingDocument în format JSON.
    """

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "cod_fiscal.json"

    data = document.export_to_dict()

    output_file.write_text(
        json.dumps(
            data,
            ensure_ascii=False,
            indent=2
        ),
        encoding="utf-8"
    )

def save_docling_html(document, output_dir="tmp/html"):
    """
    Salvează documentul convertit în HTML.
    """

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "cod_fiscal.html"

    output_file.write_text(
        document.export_to_html(),
        encoding="utf-8"
    )