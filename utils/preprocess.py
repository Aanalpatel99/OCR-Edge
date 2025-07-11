import json
from pathlib import Path

class OCRDatasetBuilder:
    def __init__(self, image_dir="data/raw/train/img", label_dir="data/raw/train/entities", output_path="data/processed/train_data.json"):
        self.project_root = Path(__file__).resolve().parent.parent
        self.image_dir = self.project_root / image_dir
        self.label_dir = self.project_root / label_dir
        self.output_path = self.project_root / output_path
        self.output_path.parent.mkdir(parents=True, exist_ok=True)

    def convertImageJson(self):
        dataset = []
        skipped = 0

        for label_file in self.label_dir.glob("*.txt"):
            image_filename = label_file.with_suffix(".jpg").name
            image_file = self.image_dir / image_filename

            if not image_file.exists():
                print(f"❌ Skipped - Missing image: {image_file}")
                skipped += 1
                continue

            raw_text = label_file.read_text(encoding="utf-8").strip()

            try:
                parsed = json.loads(raw_text)
                if isinstance(parsed, dict):
                    formatted_text = "; ".join([f"{k}: {v}" for k, v in parsed.items()])
                else:
                    formatted_text = str(parsed)
            except json.JSONDecodeError:
                try:
                    lines = raw_text.splitlines()
                    parsed_kv = dict(line.split('\t', 1) for line in lines if '\t' in line)
                    formatted_text = "; ".join([f"{k}: {v}" for k, v in parsed_kv.items()])
                except Exception as e:
                    print(f"⚠️ Skipped - Bad label in {label_file.name}: {e}")
                    skipped += 1
                    continue

            relative_path = image_file.relative_to(self.project_root).as_posix()
            dataset.append({
                "image_path": relative_path,
                "text": formatted_text
            })

        self.output_path.write_text(json.dumps(dataset, indent=2), encoding="utf-8")
        print(f"\n✅ Saved {len(dataset)} records to {self.output_path}")
        if skipped:
            print(f"⚠️ Skipped {skipped} files (missing images or bad labels).")

if __name__ == "__main__":
    builder = OCRDatasetBuilder(
        image_dir="data/raw/train/img",
        label_dir="data/raw/train/entities",
        output_path="data/processed/train_data.json"
    )
    builder.convertImageJson()
