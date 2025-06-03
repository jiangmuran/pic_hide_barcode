from PIL import Image
import tkinter as tk
from tkinter import filedialog
from tkinter import simpledialog
import numpy as np

def select_file(title):
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    file_path = filedialog.askopenfilename(title=title)
    return file_path

def overlay_qr_code(base_image_path, qr_code_path, position, size):
    imgPutong = Image.open(base_image_path)
    imgBarcode = Image.open(qr_code_path).resize(size)  # 调整二维码图像到指定大小

    # 创建新图片，使用RGBA模式，方便稍后保存为png
    imgMix = Image.new("RGBA", (imgPutong.width, imgPutong.height))

    # 三个窗口调整显示位置
    x_offset, y_offset = position

    # 填充新图片上的每一个像素
    for w in range(imgMix.width):
        for h in range(imgMix.height):
            pxlPutong = imgPutong.getpixel((w, h))

            if (x_offset < w < x_offset + imgBarcode.width) and (y_offset < h < y_offset + imgBarcode.height):
                # 如果在二维码的位置范围内，使用二维码像素
                pxlBarcode = imgBarcode.getpixel((w - x_offset, h - y_offset))
                if pxlBarcode[0] > 200:  # 如果二维码上的这个像素为白色
                    imgMix.putpixel((w, h), (pxlPutong[0], pxlPutong[1], pxlPutong[2], 255))
                else:  # 如果二维码上的这个像素为黑色，使用透明度混合
                    alpha = 150
                    imgMix.putpixel((w, h), (
                        int((pxlPutong[0] - (255 - alpha)) / alpha * 255),
                        int((pxlPutong[1] - (255 - alpha)) / alpha * 255),
                        int((pxlPutong[2] - (255 - alpha)) / alpha * 255),
                        alpha))
            else:
                imgMix.putpixel((w, h), (pxlPutong[0], pxlPutong[1], pxlPutong[2], 255))

    # 保存图片
    imgMix.save("合成图片.png")
    print("生成完毕，快去查看合成图片。")


if __name__ == "__main__":
    # 选择原图和二维码
    base_img_path = select_file("选择原图")
    qr_code_path = select_file("选择二维码")

    # 使用简单对话框获取二维码覆盖位置和大小
    x = simpledialog.askinteger("位置", "输入二维码左上角X坐标:", minvalue=0)
    y = simpledialog.askinteger("位置", "输入二维码左上角Y坐标:", minvalue=0)
    width = simpledialog.askinteger("大小", "输入二维码宽度:", minvalue=1)
    height = simpledialog.askinteger("大小", "输入二维码高度:", minvalue=1)

    # 调用函数生成合成图
    overlay_qr_code(base_img_path, qr_code_path, (x, y), (width, height))
