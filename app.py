import torch
from PIL import Image
from torchvision import transforms
from transformers import TrOCRProcessor, VisionEncoderDecoderModel

# Use your exact Hugging Face repo name
REPO_ID = "Aanal21/TeacherModel-EdgeOCR"

# Load processor and model from Hugging Face Hub
processor = TrOCRProcessor.from_pretrained(REPO_ID)
model = VisionEncoderDecoderModel.from_pretrained(REPO_ID)
model.eval()

# Preprocessing (match training time)
def preprocess_image(image_path):
    image = Image.open(image_path).convert("RGB")
    transform = transforms.Compose([
        transforms.Resize((384, 384)),
        transforms.ToTensor()
    ])
    return transform(image)

# Predict text from image
def predict(image_path):
    image = preprocess_image(image_path)
    pixel_values = image.unsqueeze(0)  # Add batch dimension
    with torch.no_grad():
        generated_ids = model.generate(pixel_values)
    prediction = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return prediction

# CLI loop
if __name__ == "__main__":
    while True:
        image_path = input("📷 Enter image path (or type 'exit'): ")
        if image_path.lower() == "exit":
            break
        try:
            result = predict(image_path)
            print("🔍 Predicted Text:", result)
        except Exception as e:
            print("❌ Error:", e)
