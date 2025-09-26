# Copilot Instructions for heygen-dify-plugin

## 项目结构与核心组件
- `dify_plugin.py`：插件主入口，负责接收 Dify 输入、调用 HeyGen API、下载视频并输出结果。
- `requirements.txt`：声明依赖（如 requests）。
- `manifest.yaml`：插件元数据，定义参数、入口文件等。
- `README.md`：使用说明与注意事项。

## 主要开发模式
- 插件通过 stdin 读取 JSON 输入，通过 stdout 输出 JSON 结果。
- 插件参数（如 heygen_api_key）通过 config 传入，或由 Dify 平台注入环境变量。
- 视频生成采用轮询方式，最长等待 150 秒。
- 视频文件命名格式为 `{lang}_ai_{chapter}_v{num}_a.mp4`。

## 关键约定与建议
- 不要将 API Key 写死在代码中，需通过参数传递。
- 所有外部依赖必须写入 `requirements.txt`。
- 插件应捕获所有异常并返回结构化错误信息。
- 仅支持 Python 3.7+，推荐 requests 作为 HTTP 客户端。
- 入口文件名、manifest.yaml、README.md 必须同步更新。

## 典型用例
- 输入：`{"audio_url": "http://...", "lang": "zh", "chapter": 1}`
- 输出：`{"video_filename": "zh_ai_1_v001_a.mp4", ...}`

## 参考文件
- `dify_plugin.py`（主逻辑）
- `manifest.yaml`（参数定义）
- `README.md`（用法说明）

## 其他
- 插件应支持在 Dify 平台自动化测试。
- 代码风格建议遵循 PEP8。
