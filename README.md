# ComfyUI_Gemini_Flash 002

ComfyUI_Gemini_Flash is a updated version of the custom node for ComfyUI that integrates the powerful Gemini 1.5 Flash 002 model from Google. This node allows users to leverage Gemini's capabilities for various AI tasks, including text generation, image analysis, video processing, and audio transcription.


https://github.com/user-attachments/assets/32ba1803-9c19-4c79-bdfc-15c61d05bf9f


## Features

- **Multimodal Input Support**: Process text, images, videos, and audio using the Gemini 1.5 Flash model.
- **Long Context Window**: Utilize Gemini 1.5 Flash's 1-million-token context window for processing large inputs.
- **API Key Management**: Securely save and manage your Gemini API key.
- **Proxy Support**: Configure proxy settings for API requests.
- **Output Control**: Adjust max output tokens and temperature for fine-tuned responses.

## Installation

1. Clone this repository to your ComfyUI custom nodes directory:
   ```
   git clone https://github.com/YourUsername/ComfyUI_Gemini_Flash.git
   ```
2. Install the required dependencies:
   ```
   pip install google-generativeai pillow torchaudio
   ```
3. Ensure you have a valid Gemini API key from Google AI Studio.

## Configuration

1. Open the `config.json` file in the `ComfyUI_Gemini_Flash` directory.
2. Replace `"your key"` with your actual Gemini API key.
3. Optionally, set a proxy if required.

## Proxy Configuration

The Gemini Flash 002 node supports the use of a proxy for API requests. This can be useful if you're behind a corporate firewall or need to route your requests through a specific server. To use a proxy:

1. In the ComfyUI interface, locate the "Gemini Flash 002" node.
2. Find the "proxy" input field.
3. Enter your proxy URL in the following format:
   ```
   http://username:password@proxy_host:proxy_port
   ```
   or if no authentication is required:
   ```
   http://proxy_host:proxy_port
   ```

For example:
- With authentication: `http://john:pass123@proxy.example.com:8080`
- Without authentication: `http://proxy.example.com:8080`

You can also set a default proxy in the `config.json` file:

```json
{
  "GEMINI_API_KEY": "your_api_key_here",
  "PROXY": "http://proxy.example.com:8080"
}
```

The proxy set in the node input will override the one in the config file.

Note: Make sure your proxy is compatible with HTTPS traffic, as the Gemini API uses secure connections.

## Usage

1. In ComfyUI, locate the "Gemini Flash 002" node in the "Gemini Flash 002" category.
2. Connect the appropriate inputs based on your use case (text, image, video, or audio).
3. Set the prompt and any additional parameters (max output tokens, temperature).
4. Run the workflow to generate content using Gemini 1.5 Flash.

## Input Types and Parameters

### Required Inputs:
- **prompt**: (STRING) The main instruction or question for the Gemini model.
- **input_type**: (["text", "image", "video", "audio"]) Specifies the type of input being processed.
- **api_key**: (STRING) Your Gemini API key.
- **proxy**: (STRING) Proxy settings (if needed).

### Optional Inputs:
- **text_input**: (STRING) Additional text input for text-based tasks.
- **image**: (IMAGE) Image input for image analysis tasks.
- **video**: (IMAGE) Video input (processed as a sequence of frames).
- **audio**: (AUDIO) Audio input for transcription or analysis.
- **max_output_tokens**: (INT, default: 1000) Controls the length of the generated output.
- **temperature**: (FLOAT, default: 0.4, range: 0.0 to 1.0) Adjusts the randomness of the output.

## Versions and Capabilities

### New Version (Gemini Flash 002)
- Supports text, image, video, and audio inputs.
- Improved video handling with frame sampling and resizing to manage payload size.
- Better prompts for video analysis, considering movement and changes across frames.
- Robust error handling and payload size management.

### Old Version (Gemini Flash)
- Supported text and image inputs.
- Basic video support (treated similarly to images).
- Limited audio support.

## Input Processing Details

### Text
- Directly processed by the Gemini model.

### Image
- Resized to a maximum of 512x512 pixels to manage payload size.
- Analyzed for content, objects, and visual elements.

### Video
- Processed as a sequence of frames.
- Samples up to 10 frames evenly distributed throughout the video.
- Each frame is resized to 256x256 pixels.
- The model analyzes changes and movements across frames.

### Audio
- Converted to mono and resampled to 16kHz if necessary.
- Sent to the Gemini model for transcription or analysis.

## Output

The node returns a STRING containing the generated content or analysis from the Gemini model.

## About Gemini 1.5 Flash

Gemini 1.5 Flash is designed to be the fastest and most cost-efficient model for high-volume tasks. It features a 1-million-token context window, enabling processing of large amounts of text, long videos, or extended audio clips in a single request.

## Troubleshooting

If you encounter any issues:
1. Ensure your API key is correctly set in the `config.json` file.
2. Check that your input size is not exceeding the model's limits (especially for video and audio).
3. Verify that all required dependencies are installed.

## Contributing

Contributions to improve ComfyUI_Gemini_Flash are welcome! Please feel free to submit issues or pull requests.

## Acknowledgements

This project was made possible thanks to the contributions of the ComfyUI community and the developers of the Gemini model at Google. Special thanks to all the contributors and users for their continuous support and feedback.

## License

[Specify your license here]

