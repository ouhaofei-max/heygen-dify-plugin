# HeyGen Dify Plugin

This plugin integrates the HeyGen API into Dify, allowing you to automate text-to-video generation by providing an audio URL. It's designed to work as a Dify Tool and leverages the HeyGen API to create videos from audio inputs.

## 🚀 Features

- **Automated Video Generation**: Converts an audio file (via URL) into a video using a default HeyGen template.
- **Simple Configuration**: Requires only a HeyGen API key and the audio URL to get started.
- **Customizable Naming**: Allows specifying language and chapter for output file naming conventions.
- **Real-time Feedback**: Provides status updates during the video generation process.

## 📦 Installation & Usage

1.  **Package the Plugin**: Compress the entire plugin directory into a `zip` file. The zip file should contain `manifest.yaml`, `requirements.txt`, the `tools/` directory, and other necessary files at the root level.
2.  **Upload to Dify**:
    *   Navigate to the "Tools" section in Dify.
    *   Click "Create Tool" and select "Upload".
    *   Upload the `zip` file you created.
3.  **Add to Your App**: Once uploaded, you can add the HeyGen plugin to your Dify application and use it in your workflows.

## 🛠️ Configuration

When adding the tool, you will need to configure the following:

### Credentials

-   **HeyGen API Key** (`heygen_api_key`): Your API key from the HeyGen platform. You can obtain it from your [HeyGen account settings](https://app.heygen.com/settings/api-key).

### Parameters

-   **Audio URL** (`audio_url`): **(Required)** The public URL of the audio file you want to convert into a video.
-   **Language** (`lang`): (Optional) The language code for the video (e.g., `en`, `zh`). Defaults to `zh`. This is used for naming the output file.
-   **Chapter** (`chapter`): (Optional) The chapter number. Defaults to `1`. This is also used for naming the output file.

## 📝 Output

The plugin will return a JSON object containing the following information upon successful video generation:

```json
{
  "video_filename": "zh_ai_1_v001_a.mp4",
  "video_url": "https://.../video.mp4",
  "video_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
}
```

-   `video_filename`: The generated name for the video file.
-   `video_url`: The direct URL to download the generated video.
-   `video_id`: The unique identifier for the video on the HeyGen platform.

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.




