# Gemini Image Editor

Gemini Image Editor uses Gemini Flash Exp 2.0 Preview and is a custom node integration for ComfyUI designed specifically to leverage Google's Gemini 2.0 Flash (experimental) model. This node allows seamless image editing using Gemini’s multimodal capabilities, enabling you to transform and enhance images through intuitive, natural-language prompts.

## Features

- **Multimodal Image Editing**: Easily edit and transform images using simple textual instructions.
- **Automatic Image Resizing**: Optimizes images to Gemini API-compatible dimensions without compromising workflow integrity.
- **API Key Management**: Securely store and manage your Gemini API key.
- **Robust Error Handling**: Gracefully manages content moderation rejections, providing informative status messages without interrupting workflows.

## Installation

1. Clone this repository into your ComfyUI custom nodes directory:

```bash
git clone https://github.com/YourUsername/ComfyUI_Gemini_Flash.git
```

2. Install required dependencies:

```bash
pip install google-generativeai pillow
```

3. Obtain your Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey).

## Configuration

- Open or create the `config.json` file in your `ComfyUI_Gemini_Flash` directory.
- Replace the placeholder with your Gemini API key:

```json
{
  "GEMINI_API_KEY": "your_actual_api_key"
}
```

## Usage

1. Within ComfyUI, find the node labeled "Gemini Image Editor" in the node menu.
2. Connect your image tensor and enter your editing prompt.
3. Optionally, specify your Gemini API key directly within the node.
4. Execute the node to generate an edited image.

## Node Inputs

- **prompt**: *(STRING)* Natural language description of desired image edits.
- **image**: *(IMAGE)* Input image tensor from previous ComfyUI nodes.
- **api_key** *(optional)*: *(STRING)* Directly specify or override the stored API key.

## Node Outputs

- **edited_image** *(IMAGE)*: The resulting edited image tensor. If the API rejects the edit, this will be the original image.
- **status_code** *(INT)*: Status indicator:
  - `0`: Success, image was edited.
  - `1`: API request error.
  - `2`: Content moderation rejection.
  - `3`: Other unspecified issues.
- **llm_text_output** *(STRING)*: Any additional text response provided by the Gemini model, or an empty string if none.

## Error Handling

The node gracefully handles Gemini API errors:
- If content moderation rejects an image, the original input image is returned.
- A detailed status code informs you of the reason for failure, allowing further conditional processing within ComfyUI.

## Troubleshooting

- Ensure your Gemini API key is correctly configured in `config.json`.
- Verify images meet Gemini's content guidelines; sensitive content might trigger moderation.
- Check terminal logs for detailed API responses and debugging information.

## Contributing

Contributions, issues, and feature requests are welcome. Please open issues or pull requests in the repository.

## License

[Specify your license here]

---

Special thanks to the ComfyUI community and Google's Gemini team for their support.
