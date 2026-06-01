import base64

from config import OPENAI_API_KEY
from openai import AsyncOpenAI

client = AsyncOpenAI(api_key=OPENAI_API_KEY)

async def generate_thumbnail(
    prompt: str,
    style_prompt: str,
    headshot_url: str,
    timeout_secs: int = 120,
) -> bytes:
    """
    Generate a thumbnail image using OpenAI's Response API with gpt-image-2.

    Args:
        prompt: The user's thumbnail description.
        style_prompt: Visual style guidance for the generation.
        headshot_url: Public URL of the reference headshot photo.
        timeout_secs: Request timeout in seconds.

    Returns:
        Raw PNG bytes of the generated thumbnail.
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
                        "url": headshot_url,
                    },
                    {
                        "type": "text",
                        "text": full_prompt,
                    },
                ],
            }
        ],
        tools=[
            {
                "type": "image_generation",
                "model": "gpt-image-2",
                "size": "1536x1024",
                "quality": "standard",
                "output_format": "png",
            }
        ],
        timeout=timeout_secs,
    )

    for item in response.output:
        if item.type == "image_generation_call" and item.result:
            return base64.b64decode(item.result)

    raise RuntimeError("No image generation result found in this Response")
