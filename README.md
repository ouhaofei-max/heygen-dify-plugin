<<<<<<< HEAD
# HeyGen Dify 插件

## 简介
本插件用于将 HeyGen API 集成到 Dify 工作流，实现音频转视频自动化。

## 使用说明
1. 上传 `dify_plugin.py` 和 `requirements.txt` 到 Dify 插件管理页面。
2. 在插件参数中填写 `heygen_api_key`。
3. 输入数据需包含 `audio_url` 或完整的 `variables` 字段。
4. 输出为视频文件名、保存路径、视频下载链接等信息。

## 依赖
- Python 3.7+
- requests

## 主要文件
- `dify_plugin.py`：插件主逻辑
- `requirements.txt`：依赖声明
- `manifest.yaml`：插件元数据

## 注意事项
- 建议不要将 API Key 写死在代码中，使用参数传递。
- 视频命名格式为 `{lang}_ai_{chapter}_v{num}_a.mp4`，可根据实际需求调整。
- 轮询等待视频生成，最长等待 150 秒。
=======
# heygen-dify-plugin
/
>>>>>>> 9722b7b1273ea75d8d705557ae03599f959393a3
