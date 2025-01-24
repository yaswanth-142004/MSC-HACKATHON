from google.cloud import vision

def initialize_client():
    """
    Initializes and returns the Google Vision API client.
    """
    try:
        client = vision.ImageAnnotatorClient.from_service_account_file('./key.json')
        return client
    except Exception as e:
        raise RuntimeError(f"Failed to initialize Google Vision API client: {e}")

def perform_ocr(client, image_content):
    """
    Performs OCR using Google Vision API.

    Args:
        client: Initialized Vision API client.
        image_content: The binary content of the image.

    Returns:
        str: The detected text or an appropriate message.
    """
    try:
        image = vision.Image(content=image_content)
        response = client.text_detection(image=image)

        # Check for API errors
        if response.error.message:
            raise RuntimeError(f"Google Vision API Error: {response.error.message}")

        # Extract and return detected text
        if response.text_annotations:
            detected_text = response.text_annotations[0].description
            return detected_text
        else:
            return "No text detected in the image."
    except Exception as e:
        raise RuntimeError(f"Error during text detection: {e}")
