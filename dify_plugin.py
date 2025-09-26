import requests
import os
import time

class DifyPlugin:
    def __init__(self, config):
        # 初始化插件配置
        self.config = config
        self.api_key = config.get("heygen_api_key")
        self.video_count = 0
        self.default_template_id = "f5816b4a65764e068f0ada4f7b15162e"

    def run(self, input_data):
        template_id = input_data.get("template_id", self.default_template_id)
        variables = input_data.get("variables")
        title = input_data.get("title", "New Video")
        lang = input_data.get("lang", "xx")
        chapter = input_data.get("chapter", 1)

        # 新增：如果直接传入 audio_url，则自动构造 variables
        if not variables and "audio_url" in input_data:
            audio_url = input_data["audio_url"]
            variables = {
                "audio": {
                    "name": "audio",
                    "type": "audio",
                    "properties": {
                        "url": audio_url
                    }
                }
            }

        if not variables:
            return {"error": "缺少 variables 或 audio_url"}
        if not self.api_key:
            return {"error": "缺少 heygen_api_key"}

        # 1. 生成视频
        url = f"https://api.heygen.com/v2/template/{template_id}/generate"
        headers = {
            "X-Api-Key": self.api_key,
            "Content-Type": "application/json",
        }
        payload = {
            "caption": False,
            "title": title,
            "variables": variables
        }
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=60)
            resp.raise_for_status()
            result = resp.json()
            video_id = result.get("video_id")
            if not video_id:
                return {"error": "HeyGen API 未返回 video_id"}

            # 2. 轮询获取视频状态和下载链接
            status_url = f"https://api.heygen.com/v1/video_status.get?video_id={video_id}"
            video_url = None
            for _ in range(30):  # 最多轮询30次
                status_resp = requests.get(status_url, headers={"X-Api-Key": self.api_key}, timeout=10)
                status_data = status_resp.json()
                if status_data.get("status") == "completed":
                    video_url = status_data.get("video_url")
                    break
                elif status_data.get("status") == "failed":
                    return {"error": "视频生成失败"}
                time.sleep(5)
            if not video_url:
                return {"error": "视频生成超时"}

            # 3. 按指定格式顺序命名并下载视频
            self.video_count += 1
            video_num = f"{self.video_count:03d}"
            video_filename = f"{lang}_ai_{chapter}_v{video_num}_a.mp4"
            video_save_path = os.path.join(os.getcwd(), video_filename)
            video_resp = requests.get(video_url, stream=True)
            with open(video_save_path, "wb") as f:
                for chunk in video_resp.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            return {
                "video_filename": video_filename,
                "video_save_path": video_save_path,
                "video_url": video_url,
                "video_id": video_id
            }
        except Exception as e:
            return {"error": str(e)}

    def config(self):
        return {
            "name": "HeyGen API 插件",
            "description": "将 HeyGen API 集成到 Dify 工作流",
            "parameters": [
                {
                    "name": "heygen_api_key",
                    "type": "string",
                    "required": True,
                    "description": "HeyGen API Key",
                }
            ],
        }

if __name__ == "__main__":
    import sys
    import json
    input_data = json.loads(sys.stdin.read())
    config = json.loads(os.environ.get("DIFY_PLUGIN_CONFIG", "{}"))
    plugin = DifyPlugin(config=config)
    output = plugin.run(input_data)
    print(json.dumps(output, ensure_ascii=False))
