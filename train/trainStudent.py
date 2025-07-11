import json
import torch
import sys
from pathlib import Path
from PIL import Image
from transformers import TrOCRProcessor
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from tqdm import tqdm
import torch.nn.functional as F

# Fix Python path so local modules load correctly
sys.path.append(str(Path(__file__).resolve().parent.parent))

from utils.trOCRTeacher import TrOCRTeacher
from train.studentModel import get_student_model  # Mini TrOCR
from transformers import VisionEncoderDecoderModel

# -----------------------------
# OCR Dataset
# -----------------------------
class OCRDataset(Dataset):
    def __init__(self, json_path, transform=None):
        self.project_root = Path(__file__).resolve().parent.parent
        self.data = json.load(open(json_path, encoding="utf-8"))
        self.transform = transform or transforms.Compose([
            transforms.Resize((384, 384)),
            transforms.ColorJitter(brightness=0.2, contrast=0.2),
            transforms.RandomRotation(degrees=2),
            transforms.ToTensor()
        ])
        self.processor = TrOCRProcessor.from_pretrained("microsoft/trocr-base-stage1")

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        sample = self.data[idx]
        image_path = self.project_root / sample["image_path"]
        try:
            image = Image.open(image_path).convert("RGB")
        except FileNotFoundError:
            raise RuntimeError(f"Image not found: {image_path}")
        image = self.transform(image)
        return image, sample["text"]

# -----------------------------
# Knowledge Distillation Loss (KL only)
# -----------------------------
def distillation_loss(student_logits, teacher_logits, temperature=2.0):
    s_logits = F.log_softmax(student_logits / temperature, dim=-1)
    t_logits = F.softmax(teacher_logits / temperature, dim=-1)
    return F.kl_div(s_logits, t_logits, reduction='batchmean') * (temperature ** 2)

# -----------------------------
# Train Mini TrOCR Student
# -----------------------------
def train_student():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    print("🔧 Loading teacher model...")
    teacher = TrOCRTeacher()
    processor = TrOCRProcessor.from_pretrained("microsoft/trocr-base-stage1")

    print("🧠 Building student model...")
    student = get_student_model().to(device)

    dataset_path = Path(__file__).resolve().parent.parent / "data/processed/train_data.json"
    dataset = OCRDataset(str(dataset_path))
    loader = DataLoader(dataset, batch_size=4, shuffle=True)

    optimizer = torch.optim.Adam(student.parameters(), lr=1e-4)

    student.train()
    for epoch in range(30):
        running_loss = 0.0
        for images, label_texts in tqdm(loader, desc=f"Epoch {epoch+1}"):
            images = images.to(device)

            # Encode text with tokenizer
            tokenized = processor.tokenizer(
                list(label_texts),
                padding="max_length",
                truncation=True,
                max_length=128,
                return_tensors="pt"
            )
            decoder_input_ids = tokenized.input_ids.to(device)

            # Prepare pixel values for both models
            pixel_values = images.to(device)

            with torch.no_grad():
                teacher_outputs = teacher.model(pixel_values, decoder_input_ids=decoder_input_ids)
                teacher_logits = teacher_outputs.logits  # [B, T, V]

            student_outputs = student(pixel_values=pixel_values, decoder_input_ids=decoder_input_ids)
            student_logits = student_outputs.logits  # [B, T, V]

            # Match sequence lengths
            min_len = min(student_logits.size(1), teacher_logits.size(1))
            student_logits = student_logits[:, :min_len, :]
            teacher_logits = teacher_logits[:, :min_len, :]

            loss = distillation_loss(student_logits, teacher_logits)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            running_loss += loss.item()

        print(f"✅ Epoch {epoch+1} Loss: {running_loss / len(loader):.4f}")

    # Save student model
    save_path = Path(__file__).resolve().parent.parent / "Student/studentMiniTrOCR"
    save_path.mkdir(exist_ok=True)
    student.save_pretrained(str(save_path))
    processor.save_pretrained(str(save_path))
    print(f"🎉 Mini TrOCR student saved to: {save_path}")

# -----------------------------
if __name__ == "__main__":
    train_student()
