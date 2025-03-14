import os
import json
from google import genai
from google.genai import types
from io import BytesIO
from PIL import Image
import torch
import numpy as np

directory = os.path.dirname(os.path.realpath(__file__))

def get_config():
    try:
        config_path = os.path.join(directory, 'config.json')
        with open(config_path, 'r') as f:
            return json.load(f)
    except:
        return {}

def save_config(config):
    with open(os.path.join(directory, 'config.json'), 'w') as f:
        json.dump(config, f, indent=4)

class Gemini_ImageEditor:

    def __init__(self, api_key=None):
        config = get_config()
        self.api_key = api_key or config.get("GEMINI_API_KEY")
        self.client = genai.Client(api_key=self.api_key)
        self.model_name = "gemini-2.0-flash-exp"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"default": "Modify the image accordingly.", "multiline": True}),
                "image": ("IMAGE",),
                "api_key": ("STRING", {"default": ""})
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("edited_image",)
    FUNCTION = "edit_image"
    CATEGORY = "Gemini Image Editor"

    def tensor_to_image(self, tensor):
        tensor = tensor.cpu()
        image_np = tensor.squeeze().mul(255).clamp(0, 255).byte().numpy()
        return Image.fromarray(image_np, mode='RGB')

    def resize_image(self, image, max_size=1024):
        width, height = image.size
        if width > height:
            if width > max_size:
                height = int(max_size * height / width)
                width = max_size
        else:
            if height > max_size:
                width = int(max_size * width / height)
                height = max_size
        return image.resize((width, height), Image.LANCZOS)

    def image_to_tensor(self, image):
        image = image.convert("RGB")
        tensor = torch.from_numpy(np.array(image)).float() / 255.0
        return tensor.unsqueeze(0)

    def edit_image(self, prompt, image, api_key):
        if api_key and api_key != self.api_key:
            self.api_key = api_key
            save_config({"GEMINI_API_KEY": api_key})
            self.client = genai.Client(api_key=self.api_key)

        pil_image = self.tensor_to_image(image)
        pil_image = self.resize_image(pil_image, 1024)

        temp_image_path = os.path.join(directory, "temp_image.png")
        pil_image.save(temp_image_path, format="PNG")

        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_uri(file_uri=temp_image_path, mime_type="image/png"),
                    types.Part.from_text(prompt),
                ],
            ),
        ]

        generate_content_config = types.GenerateContentConfig(
            temperature=1,
            top_p=0.95,
            top_k=40,
            max_output_tokens=8192,
            response_modalities=["image", "text"],
            response_mime_type="text/plain",
        )

        response = self.client.models.generate_content_stream(
            model=self.model_name,
            contents=contents,
            config=generate_content_config,
        )

        for chunk in response:
            if chunk.candidates and chunk.candidates[0].content.parts:
                inline_data = chunk.candidates[0].content.parts[0].inline_data
                if inline_data:
                    output_path = os.path.join(directory, "edited_image.png")
                    with open(output_path, "wb") as f:
                        f.write(inline_data.data)
                    edited_image = Image.open(output_path)
                    return (self.image_to_tensor(edited_image),)

        return (self.image_to_tensor(pil_image),)

NODE_CLASS_MAPPINGS = {"Gemini_ImageEditor": Gemini_ImageEditor}
NODE_DISPLAY_NAME_MAPPINGS = {"Gemini_ImageEditor": "Gemini Image Editor"}
