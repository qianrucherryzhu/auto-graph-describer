from openai import OpenAI
from pypdf import PdfReader, PdfWriter
import base64
import requests

with open('.env', 'r') as env_file:
    api_key = env_file.read().split('=')[1]

result = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My HTML Page</title>
</head>
<body>
    <h1>Welcome to My HTML Page</h1>

    <p>This is a paragraph of text. You can add any content you want here.</p>
"""


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


reader = PdfReader("PDFlatex.pdf")
writer = PdfWriter()

count = 0

for page in reader.pages:
    # new_page = writer.add_page(page)
    # page_content = new_page.get_contents()
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
        describe = response.json()["choices"][0]["message"]["content"]
        print(describe)
        # page_content.append(describe)

        result += '<img src = '+image_path + \
            ' alt = "Image Description" ><p> '+describe + '</p>'
    if count >= 3:
        break
result += """
</body >
</html >
"""

print(result)
with open('modified.html', 'w') as output_file:
    output_file.write(result)
