import cv2
from sanic import Sanic, response
from paddleocr import PaddleOCR
import base64
import numpy as np
from sanic.worker.manager import WorkerManager
import logging
import os
from dotenv import load_dotenv

load_dotenv()

use_gpu = True

WorkerManager.THRESHOLD = 6000

logger = logging.getLogger('ocr_server')
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)


logger.info(f"OCR_USE_GPU parameter is set to {use_gpu}")

# 创建 Sanic 应用
app = Sanic("OCRService")

# 初始化 PaddleOCR 引擎
ocr_engine = PaddleOCR(use_angle_cls=True, lang="ch", use_gpu=use_gpu, show_log=False)


# 定义 OCR API 路由
@app.post("/ocr")
async def ocr_request(request):
    """
    Arg:
        img64: 图片的base64编码
    Return：
        文本识别结果
    """
    # 获取上传的文件
    inp = request.json
    image_string = inp['img64']

    # 无文件上传，返回错误
    if not image_string:
        return response.json({'error': 'No file was uploaded.'}, status=400)

    binary_data = base64.b64decode(image_string)
    nparr = np.frombuffer(binary_data, np.uint8)
    img_array = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    logger.info("shape: {}".format(img_array.shape))

    # 调用 PaddleOCR 进行识别
    res = ocr_engine.ocr(img_array)
    logger.info("ocr result: {}".format(res))

    # 返回识别结果
    return response.json({'results': res})


# 启动服务
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8010, workers=4, access_log=False)
