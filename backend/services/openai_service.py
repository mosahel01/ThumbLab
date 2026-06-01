import base64

from config import OPENAI_API_KEY
from openai import AsyncOpenAI

client = AsyncOpenAI(api_key=OPENAI_API_KEY)

async def generate_thumbnail( prompt: str, style_prompt: str, headshot_url: str, ) -> bytes:
    """
    Use the Response API with gpt-image-2 as built-in image_generation tool.
    Pass the headshot URL directly as input_image.
    Return the raw PNG bytes
    """

    full_prompt = (
        f"{style_prompt} \n\n"
        f"User Request: {prompt} \n\n"
        "IMPORTANT: Generated Thumbnail must prominently feature the person"
        "shown in the provided reference headshot photo. Keep their likeness accurate."
    )

    response = await client.responses.create(
        model="gpt-4o",
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_image",
                        "url": headshot_url
                    },
                    {
                        "type": "text",
                        "url": full_prompt
                    }
                ]
            }
        ],
        tools = [
            {
                "type": "image_generation",
                "model": "gpt-image-2",
                "size": "1536x1024",
                "quality": "standard",
                "output_format": "png",
            }
        ]

    )

    for item in response.output:
        if item.type == "image_generation_call" and item.result:
            return base64.b64decode(item.result)

    raise RuntimeError("No image generation result found in this Response")
