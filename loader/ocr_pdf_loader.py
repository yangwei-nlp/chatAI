"""
读取图片PDF
"""
from magic_pdf.dict2md.ocr_mkcontent import union_make
from magic_pdf.model.doc_analyze_by_custom_model import doc_analyze
from loader.utils.pdf_parse_union_core import pdf_parse_union

from magic_pdf.model.doc_analyze_by_custom_model import ModelSingleton

model_manager = ModelSingleton()
txt_model = model_manager.get_model(False, False)
ocr_model = model_manager.get_model(True, False)



def read_pdf(pdf_path):
    pdf_bytes = open(pdf_path, "rb").read()

    model_json = doc_analyze(pdf_bytes, ocr=True, start_page_id=0, end_page_id=None)

    new_pdf_info_dict = pdf_parse_union(pdf_bytes,
                                        model_json,
                                        "ocr",
                                        start_page_id=0,
                                        end_page_id=None,
                                        debug_mode=True,
                                        )

    content = union_make(new_pdf_info_dict["pdf_info"], "standard_format", drop_mode="none", img_buket_path=None)
    output_text = '\n'.join([line['text'] for line in content if 'text' in line])

    return output_text



if __name__ == "__main__":
    pdf_path = '/home/qilixin/桌面/普通高中教科书·历史必修 中外历史纲要（上）.pdf'

    all_texts = read_pdf(pdf_path)
    print(all_texts)
