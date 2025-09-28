import base64
import os
import random
from http.server import HTTPServer, BaseHTTPRequestHandler

# ====== 图片转换工具 ======
def convert_images_to_base64(folder_path):
    images = []
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path) and file_name.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
            with open(file_path, "rb") as f:
                img_b64 = base64.b64encode(f.read()).decode("utf-8")
                # 根据格式选择前缀
                ext = file_name.split(".")[-1].lower()
                mime = "jpeg" if ext in ["jpg", "jpeg"] else ext
                images.append(f"data:image/{mime};base64,{img_b64}")
    return images

# ====== 网页服务器处理 ======
class RandomImageHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            img = random.choice(images)
            html = f"""
            <html>
            <head><title>随机图片</title></head>
            <body style="text-align:center; margin-top:50px;">
                <h2>随机图片展示</h2>
                <img src="{img}" style="max-width:80%; height:auto; border:2px solid #333;">
                <br><br>
                <a href="/">换一张</a>
            </body>
            </html>
            """
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(html.encode("utf-8"))

# ====== 主程序入口 ======
if __name__ == "__main__":
    folder = "D:/potato"
    images = convert_images_to_base64(folder)

    if not images:
        print("❌ 没有找到有效的图片，请检查文件夹。")
    else:
        port = 8080
        server = HTTPServer(("0.0.0.0", port), RandomImageHandler)
        print(f"✅ 服务器已启动，在浏览器打开: http://localhost:{port}")
        server.serve_forever()
