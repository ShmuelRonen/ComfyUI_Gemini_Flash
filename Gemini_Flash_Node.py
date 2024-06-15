import os
import json
import google.generativeai as genai
from io import BytesIO
from PIL import Image
import torch

p = os.path.dirname(os.path.realpath(__file__))

def get_gemini_api_key():
    try:
        config_path = os.path.join(p, 'config.json')
        with open(config_path, 'r') as f:  
            config = json.load(f)
        api_key = config["GEMINI_API_KEY"]
    except:
        print("Error: API key is required")
        return ""
    return api_key

def save_gemini_api_key(api_key):
    config_path = os.path.join(p, 'config.json')
    config = {"GEMINI_API_KEY": api_key}
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=4)

class Gemini_Flash:

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

    def generate_content(self, prompt, vision, api_key, image=None):
        if api_key:
            self.api_key = api_key
            save_gemini_api_key(api_key)
            genai.configure(api_key=self.api_key, transport='rest')
        if not self.api_key:
            raise ValueError("API key is required")

        model_name = 'gemini-1.5-flash'
        model = genai.GenerativeModel(model_name)

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
        
        return (textoutput,)

NODE_CLASS_MAPPINGS = {
    "Gemini_Flash": Gemini_Flash,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Gemini_Flash": "Gemini flash",
}
