import os
import json
import google.generativeai as genai
from contextlib import contextmanager
from PIL import Image


CONFIG_PATH = os.path.dirname(os.path.realpath(__file__))


def get_gemini_api_key() -> str:
    try:
        config_path = os.path.join(CONFIG_PATH, 'config.json')
        with open(config_path, 'r') as f:
            config = json.load(f)
        return config["GEMINI_API_KEY"]
    except:
        print("Error: API key is required")
        return ""


def save_gemini_api_key(api_key) -> None:
    config_path = os.path.join(CONFIG_PATH, 'config.json')
    config = {"GEMINI_API_KEY": api_key}
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=4)


@contextmanager
def temporary_env_var(key: str, new_value):
    old_value = os.environ.get(key)  # Save the old value
    if new_value:
        os.environ[key] = new_value  # Assign the new value
    try:
        yield
    finally:
        if new_value:  # Only if something was set
            if old_value is not None:
                os.environ[key] = old_value  # Restore the old value
            else:
                del os.environ[key]  # Remove temporary value


class GeminiFlash:

    def __init__(self, api_key=None):
        self.api_key = api_key or get_gemini_api_key()
        if self.api_key is not None:
            genai.configure(api_key=self.api_key, transport='rest')

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"default": "Analyze the image and make a txt2img detailed prompt. No prefix!", "multiline": True}),
                "vision": ("BOOLEAN", {"default": True}),  # Default vision to True
                "api_key": ("STRING", {"default": ""})  # Add api_key as an input
            },
            "optional": {
                "image": ("IMAGE",),
                "proxy": ("STRING", {"default": ""})
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "generate_content"

    CATEGORY = "Gemini flash"

    @staticmethod
    def tensor_to_image(tensor):
        tensor = tensor.cpu()
        image_np = tensor.squeeze().mul(255).clamp(0, 255).byte().numpy()
        image = Image.fromarray(image_np, mode='RGB')
        return image

    def generate_content(self, prompt, vision, api_key, image=None, proxy=None):
        if not api_key and not self.api_key:
            api_key = os.environ.get("GOOGLE_API_KEY")
        if api_key:
            self.api_key = api_key
            save_gemini_api_key(api_key)
            genai.configure(api_key=self.api_key, transport='rest')
        if not self.api_key:
            raise ValueError("API key is required")

        model_name = 'gemini-1.5-flash'
        model = genai.GenerativeModel(model_name)

        with temporary_env_var("HTTPS_PROXY", proxy):
            if not vision:
                # Act like a text LLM
                response = model.generate_content(prompt)
                text_output = response.text
            else:
                # Vision enabled
                if image is None:
                    raise ValueError(f"{model_name} needs image")

                pil_image = self.tensor_to_image(image)
                response = model.generate_content([prompt, pil_image])
                text_output = response.text

        return (text_output,)


NODE_CLASS_MAPPINGS = {
    "Gemini_Flash": GeminiFlash,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Gemini_Flash": "Gemini flash",
}
