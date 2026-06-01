from imagekitio import ImageKit
from config import IMAGEKIT_PRIVATE_KEY

imagekit = ImageKit(private_key=IMAGEKIT_PRIVATE_KEY)


def upload_image(
    file_bytes: bytes,
    file_name: str,
    folder: str,
    content_type: str = "image/png",
) -> str:
    """Upload an image to ImageKit and return its public URL."""
    result = imagekit.files.upload(
        files=(file_bytes, file_name, content_type),
        file_name=file_name,
        folder=folder,
        is_private_file=False,
        use_unique_file_name=True,
    )
    return str(result.url)


def get_variants(base_url: str) -> dict[str, str]:
    """Return platform-specific ImageKit transformation URLs."""
    return {
        "youtube": f"{base_url}?tr=w-1280,h-720,c-maintain_ratio,fo-auto",
        "shorts": f"{base_url}?tr=w-1080,h-1920,c-maintain_ratio,fo-auto",
        "square": f"{base_url}?tr=w-1080,h-1080,c-maintain_ratio,fo-auto",
    }
