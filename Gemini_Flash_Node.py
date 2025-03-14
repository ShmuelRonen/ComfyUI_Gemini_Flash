import os
import json
from google import genai
from google.genai import types
from PIL import Image
import torch
import numpy as np
from io import BytesIO

directory = os.path.dirname(os.path.realpath(__file__))

def get_config():
    try:
        config_path = os.path.join(directory, 'config.json')
        with open(config_path) as f:
            return json.load(f)
    except Exception:
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

    RETURN_TYPES = ("IMAGE", "INT")
    RETURN_NAMES = ("edited_image", "status_code")
    FUNCTION = "edit_image"
    CATEGORY = "Gemini Image Editor"

    def tensor_to_image(self, tensor):
        tensor = tensor.cpu()
        image_np = tensor.squeeze().mul(255).clamp(0, 255).byte().numpy()
        return Image.fromarray(image_np)

    def resize_image(self, image, max_size):
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
        tensor = torch.from_numpy(np.array(image).astype(np.float32) / 255.0)
        return tensor.unsqueeze(0)

    def edit_image(self, prompt, image, api_key):
        if api_key and api_key != self.api_key:
            self.api_key = api_key
            self.client = genai.Client(api_key=self.api_key)

        original_image = self.tensor_to_image(image)
        upload_image = self.resize_image(original_image, 1024)

        temp_path = os.path.join(directory, "temp_image.png")
        upload_image.save(temp_path, format="PNG")

        try:
            uploaded_file = self.client.files.upload(file=temp_path)

            contents = [
                {
                    "role": "user",
                    "parts": [
                        {
                            "fileData": {
                                "mimeType": "image/png",
                                "fileUri": uploaded_file.uri,
                            },
                        },
                        {"text": prompt},
                    ],
                },
            ]

            generation_config = genai.types.GenerateContentConfig(
                temperature=1,
                top_k=40,
                top_p=0.95,
                max_output_tokens=8192,
                response_modalities=["image", "text"],
                response_mime_type="text/plain",
                safety_settings=[
                    types.SafetySetting(category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="BLOCK_NONE"),
                    types.SafetySetting(category="HARM_CATEGORY_CIVIC_INTEGRITY", threshold="BLOCK_NONE"),
                    types.SafetySetting(category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="BLOCK_NONE"),
                    types.SafetySetting(category="HARM_CATEGORY_HARASSMENT", threshold="BLOCK_NONE"),
                    types.SafetySetting(category="HARM_CATEGORY_HATE_SPEECH", threshold="BLOCK_NONE"),
                ],
            )

            response = self.client.models.generate_content(
                model="gemini-2.0-flash-exp",
                contents=contents,
                config=generation_config,
            )

            for candidate in response.candidates:
                content = candidate.content
                if hasattr(content, 'parts'):
                    for part in content.parts:
                        if part.inline_data:
                            image_data = part.inline_data.data
                            edited_image = Image.open(BytesIO(image_data))
                            return (self.image_to_tensor(edited_image), 0)
                else:
                    return (self.image_to_tensor(original_image), 2)

            return (self.image_to_tensor(original_image), 3)

        except Exception:
            return (self.image_to_tensor(original_image), 1)

NODE_CLASS_MAPPINGS = {"Gemini_ImageEditor": Gemini_ImageEditor}
NODE_DISPLAY_NAME_MAPPINGS = {"Gemini_ImageEditor": "Gemini Image Editor"}