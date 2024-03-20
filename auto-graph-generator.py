from openai import OpenAI
from pypdf import PdfReader, PdfWriter
import base64
import requests

api_key = "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"


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


reader = PdfReader("PDFlatex.pdf")

page = reader.pages[0]
count = 0

for image_file_object in page.images:
    image_path = str(count) + image_file_object.name
    with open(image_path, "wb") as fp:
        fp.write(image_file_object.data)
        count += 1

    base64_image = encode_image(image_path)

    client = OpenAI(api_key=api_key)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Describe this image"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }

    response = requests.post(
        "https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    print(response.json())
    # print(completion.choices[0].message)
