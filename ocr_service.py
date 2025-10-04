import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import io

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text(input_data, is_image=False):
    if is_image:
        try:
            # Reset file pointer if needed
            input_data.seek(0)
            img_bytes = input_data.read()
            img = Image.open(io.BytesIO(img_bytes)).convert("L")

            # Resize to improve OCR
            base_width = 1024
            wpercent = (base_width / float(img.size[0]))
            hsize = int(float(img.size[1]) * wpercent)
            img = img.resize((base_width, hsize), Image.Resampling.LANCZOS)

            # Enhance contrast and remove noise
            img = img.filter(ImageFilter.MedianFilter())
            img = ImageEnhance.Contrast(img).enhance(2)

            # OCR with Tesseract
            full_text = pytesseract.image_to_string(img, lang="eng", config="--psm 6")

            # Split into lines
            lines = [line.strip() for line in full_text.split("\n") if line.strip()]

            # Compute confidence (fallback to 0.8 if empty confs)
            confidence = 0.0
            try:
                details = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
                confs = [int(conf) for conf in details['conf'] if conf.isdigit() and int(conf) >= 0]
                if confs:
                    confidence = sum(confs) / len(confs) / 100
            except Exception:
                confidence = 0.85  # safe fallback

            # If text exists but conf is low, still return
            if lines and confidence == 0.0:
                confidence = 0.6

            return {"raw_texts": lines, "confidence": confidence}

        except Exception as e:
            return {"raw_texts": [], "confidence": 0.0, "error": str(e)}

    else:
        # Text input
        lines = [line.strip() for line in input_data.split("\n") if line.strip()]
        return {"raw_texts": lines, "confidence": 0.95}
