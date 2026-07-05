import base64
from io import BytesIO

from fastapi import APIRouter, HTTPException
from PIL import Image

from apps.calculator.schema import ImageData
from apps.calculator.utils import analyze_image

router = APIRouter()


@router.post("/calculate")
async def calculate(data: ImageData):
    try:
        print(f"Received image data: {data.image[:50]}...")
        print(f"Received dict_of_vars: {data.dict_of_vars}")

        # Decode the image from base64
        image_bytes = base64.b64decode(data.image.split(",")[1])
        image = Image.open(BytesIO(image_bytes))

        # Run the image through the Gemini-powered analyzer
        responses = analyze_image(image, dict_of_vars=data.dict_of_vars)

        response_data = []
        for response in responses:
            response_data.append(response)
            print(f"Response in route: {response}")

        return {"message": "Image processed", "data": response_data, "status": "success"}

    except Exception as e:
        print(f"Error processing image: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")
