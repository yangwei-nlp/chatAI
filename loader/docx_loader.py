from docx import Document

def read_docx(docx_path):
    """
    读取doc文件返回纯文本
    """
    doc = Document(docx_path)
    output_text = ''
    for paragraph in doc.paragraphs:
        if paragraph.text.startswith('发言人') or paragraph.text == '':
            continue
        output_text += paragraph.text
    return output_text

