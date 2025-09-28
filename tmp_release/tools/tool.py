import requests
import os
import time
from collections.abc import Generator
from typing import Any, Optional

from dify_plugin import Tool, ToolInvokeMessage, ToolErrorMessage


class HeyGenTool(Tool):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.video_count = 0
        self.default_template_id = "f5816b4a65764e068f0ada4f7b15162e"

    def _format_filename(self, lang: str, chapter: int) -> str:
        self.video_count += 1
        video_num = f"{self.video_count:03d}"
        return f"{lang}_ai_{chapter}_v{video_num}_a.mp4"

    def _create_video(self, api_key: str, template_id: str, title: str, variables: dict) -> str:
        url = f"https://api.heygen.com/v2/template/{template_id}/generate"
        headers = {"X-Api-Key": api_key, "Content-Type": "application/json"}
        payload = {"caption": False, "title": title, "variables": variables}

        resp = requests.post(url, headers=headers, json=payload, timeout=60)
        resp.raise_for_status()
        result = resp.json()
        video_id = result.get("video_id")
        if not video_id:
            raise RuntimeError("HeyGen API did not return video_id")
        return video_id

    def _poll_status(self, api_key: str, video_id: str, timeout_seconds: int = 150) -> Optional[str]:
        status_url = f"https://api.heygen.com/v1/video_status.get?video_id={video_id}"
        attempts = max(1, timeout_seconds // 5)
        for i in range(attempts):
            resp = requests.get(status_url, headers={"X-Api-Key": api_key}, timeout=10)
            resp.raise_for_status()
            status_data = resp.json()
            status = status_data.get("status")
            if status == "completed":
                return status_data.get("video_url")
            if status == "failed":
                raise RuntimeError(f"Video generation failed: {status_data.get('error', 'unknown')}")
            # sleep and retry
            time.sleep(5)
        return None

    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage, None, None]:
        api_key = self.credentials.get("heygen_api_key")
        if not api_key:
            yield ToolErrorMessage(err="heygen_api_key is not configured")
            return

        audio_url = tool_parameters.get("audio_url")
        if not audio_url:
            yield ToolErrorMessage(err="audio_url is required")
            return

        lang = tool_parameters.get("lang", "zh")
        chapter = int(tool_parameters.get("chapter", 1))
        title = tool_parameters.get("title", "New Video")
        template_id = tool_parameters.get("template_id", self.default_template_id)

        variables = {
            "audio": {"name": "audio", "type": "audio", "properties": {"url": audio_url}}
        }

        try:
            yield self.create_text_message("Starting HeyGen video generation...")

            video_id = self._create_video(api_key=api_key, template_id=template_id, title=title, variables=variables)
            yield self.create_text_message(f"Submitted generation job, video_id={video_id}")

            yield self.create_text_message("Polling for completion...")
            video_url = self._poll_status(api_key=api_key, video_id=video_id)
            if not video_url:
                yield ToolErrorMessage(err="Video generation timed out after waiting period")
                return

            filename = self._format_filename(lang=lang, chapter=chapter)

            # Instead of attempting to download the file in a sandboxed environment,
            # return the URL and metadata so the consumer can download it.
            yield self.create_json_message({"video_filename": filename, "video_url": video_url, "video_id": video_id})

        except requests.exceptions.RequestException as e:
            yield ToolErrorMessage(err=f"HTTP request failed: {e}")
        except Exception as e:
            yield ToolErrorMessage(err=f"Unexpected error: {e}")
