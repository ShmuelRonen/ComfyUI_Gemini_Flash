import os
import json
import google.generativeai as genai
from io import BytesIO
from PIL import Image
import torch
import requests

p = os.path.dirname(os.path.realpath(__file__))

def get_config():
    try:
        config_path = os.path.join(p, 'config.json')
        with open(config_path, 'r') as f:  
            config = json.load(f)
        return config
    except:
        return {}

def save_config(config):
    config_path = os.path.join(p, 'config.json')
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=4)

class Gemini_Flash:

    def __init__(self, api_key=None, proxy=None):
        config = get_config()
        self.api_key = api_key or config.get("GEMINI_API_KEY")
        self.proxy = proxy or config.get("PROXY")
        if self.api_key is not None:
            self.configure_genai()

    def configure_genai(self):
        genai.configure(api_key=self.api_key)

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"default": "Analyze the image and make a txt2img detailed prompt. no prefix!", "multiline": True}),
                "vision": ("BOOLEAN", {"default": True}),
                "api_key": ("STRING", {"default": ""}),
                "proxy": ("STRING", {"default": ""})
            },
            "optional": {
                "image": ("IMAGE",),  
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "generate_content"

    CATEGORY = "Gemini flash"

    def tensor_to_image(self, tensor):
        tensor = tensor.cpu()
        image_np = tensor.squeeze().mul(255).clamp(0, 255).byte().numpy()
        image = Image.fromarray(image_np, mode='RGB')
        return image

    def generate_content(self, prompt, vision, api_key, proxy, image=None):
        config_updated = False
        if api_key and api_key != self.api_key:
            self.api_key = api_key
            config_updated = True
        if proxy != self.proxy:
            self.proxy = proxy
            config_updated = True
        
        if config_updated:
            save_config({"GEMINI_API_KEY": self.api_key, "PROXY": self.proxy})
            self.configure_genai()

        if not self.api_key:
            raise ValueError("API key is required")

        model_name = 'gemini-1.5-flash'
        model = genai.GenerativeModel(model_name)

        # Set up environment variables for proxy
        if self.proxy:
            os.environ['HTTP_PROXY'] = self.proxy
            os.environ['HTTPS_PROXY'] = self.proxy
        else:
            # Clear proxy settings if no proxy is specified
            os.environ.pop('HTTP_PROXY', None)
            os.environ.pop('HTTPS_PROXY', None)

        try:
            if not vision:
                # Act like a text LLM
                response = model.generate_content(prompt)
                textoutput = response.text
            else:
                # Vision enabled
                if image is None:
                    raise ValueError(f"{model_name} needs image")
                else:
                    pil_image = self.tensor_to_image(image)
                    response = model.generate_content([prompt, pil_image])
                    textoutput = response.text
        except Exception as e:
            textoutput = f"Error: {str(e)}"
        
        return (textoutput,)

NODE_CLASS_MAPPINGS = {
    "Gemini_Flash": Gemini_Flash,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Gemini_Flash": "Gemini flash",
}