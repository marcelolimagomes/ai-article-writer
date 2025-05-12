import os
from weasyprint import HTML


def coordenador(tema: str, escrever_introducao: str, escrever_secao: list, escrever_conclusao: str):
    slug = tema.lower().replace(" ", "_")
    md_file = f"artigo_{slug}.md"
    pdf_file = f"artigo_{slug}.pdf"

    with open(md_file, "w", encoding="utf-8") as f:
        f.write(f"# {tema}\n\n")
        f.write(escrever_introducao + "\n\n")
        for sec in escrever_secao:
            f.write(sec + "\n\n")
        f.write(escrever_conclusao + "\n")

    HTML(md_file).write_pdf(pdf_file)
    return os.path.abspath(pdf_file)
