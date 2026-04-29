"""One-shot: resize portfolio images to max 1800px on long edge, strip EXIF, keep originals."""
from PIL import Image, ImageOps
from pathlib import Path

SRC = Path(__file__).parent / "images"
MAX = 1800
QUALITY = 85

for p in sorted(SRC.iterdir()):
    if p.suffix.lower() not in {".jpg", ".jpeg", ".png"}:
        continue
    img = Image.open(p)
    img = ImageOps.exif_transpose(img)  # apply rotation, then strip
    w, h = img.size
    if max(w, h) > MAX:
        scale = MAX / max(w, h)
        img = img.resize((int(w * scale), int(h * scale)), Image.LANCZOS)
    img = img.convert("RGB")
    out = p.with_suffix(".jpg")  # normalize extension to lowercase .jpg
    img.save(out, "JPEG", quality=QUALITY, optimize=True)
    if p != out:
        p.unlink()  # remove uppercase .JPG version
    print(f"{out.name}: {p.stat().st_size if p.exists() else out.stat().st_size:>10} bytes  {img.size}")
