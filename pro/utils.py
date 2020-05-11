from base64 import b64encode
from PIL import Image
from io import BytesIO

from utils.decorators import decorator


def pro_required(func):
    return decorator(func, lambda u: u.user_type == "pro")


def convert_to_base64(file):
    img = Image.open(file.file)
    img = img.resize((10, 10))
    output = BytesIO()
    img.save(output, format=file.content_type[file.content_type.find("/") + 1:], quality=100)
    output.seek(0)
    return b64encode(output.read()).decode()
