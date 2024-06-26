# ComfyUI_Gemini_Flash

**ComfyUI_Gemini_Flash** is a custom node for ComfyUI, integrating the capabilities of the Gemini 1.5 Flash model. This node supports text and vision-based prompts, allowing users to analyze and adapt images to text prompts for text2image tasks.


![Flash](https://github.com/ShmuelRonen/ComfyUI_Gemini_Flash/assets/80190186/6daa2aaf-72c6-4e2a-98bb-f75620b34717)

## Features

- **Text and Vision Integration**: Toggle between text-only or vision-enabled mode for versatile content generation.
- **API Key Management**: Securely save and manage your Gemini API key.
- **Simple Configuration**: Easy setup with automated configuration file creation.

## Installation

1. Clone the repository to your ComfyUI custom nodes directory.
2. Ensure `config.json` is in the root directory of the node.
3. Start using the Gemini Flash node in ComfyUI!

## Usage

1. Enter your Gemini API key in the provided input.
2. Toggle the `vision` option as needed.
3. Provide your prompt and optional image input.
4. Generate content using the powerful Gemini 1.5 Flash model.

## About Gemini 1.5 Flash

The Gemini 1.5 Flash model by Google is designed to be the fastest and most cost-efficient model for high volume tasks. It addresses developers' needs for lower latency and cost, making it ideal for large-scale applications. With a rate limit increased to 1000 requests per minute and the removal of the request per day limit, Gemini 1.5 Flash provides robust performance for demanding applications. Additionally, tuning support for the model is available, allowing for customization to meet specific performance thresholds without additional per-token costs.

## Acknowledgements

This project was made possible thanks to the contributions of the ComfyUI community and the developers of the Gemini model at Google. Special thanks to all the contributors and users for their continuous support and feedback.
