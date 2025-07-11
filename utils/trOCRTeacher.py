from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import Image
from pathlib import Path
import torch

class TrOCRTeacher:
    def __init__(self, model_name: str = "microsoft/trocr-base-stage1"):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.processor = TrOCRProcessor.from_pretrained(model_name, use_fast=True)
        self.model = VisionEncoderDecoderModel.from_pretrained(model_name).to(self.device)

    def predict(self, image_path: str | Path) -> str:
        image_path = Path(image_path)
        image = Image.open(image_path).convert("RGB")
        image = image.resize((384, 384))

        pixel_values = self.processor(images=image, return_tensors="pt").pixel_values.to(self.device)
        generated_ids = self.model.generate(pixel_values)
        text = self.processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

        return text


# test
if __name__ == "__main__":
    teacher_model = TrOCRTeacher()
    text = teacher_model.predict(r"C:\Users\aanal\Documents\OCR-Edge\data\raw\test\img\X00016469670.jpg")
    print("📝 OCR Prediction:", text)
