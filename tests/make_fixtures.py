from pathlib import Path
from reportlab.pdfgen import canvas
from PIL import Image, ImageDraw, ImageFont

FIXTURES = Path(__file__).resolve().parent / "fixtures"
FIXTURES.mkdir(exist_ok=True)

# Sample PDF
c = canvas.Canvas(str(FIXTURES / "sample_bill.pdf"))
lines = [
    "Electricity Bill",
    "Consumer No: 123456789",
    "Consumer Name: John Doe",
    "Billing Period: July 2026",
    "Billing Date: 01/07/2026",
    "Due Date: 15/07/2026",
    "Previous Reading: 1000",
    "Current Reading: 1300",
    "Total Units: 300",
    "Total Amount: Rs. 2500.00",
]
y = 800
for line in lines:
    c.drawString(50, y, line)
    y -= 20
c.save()

# Sample OCR image (needs a real truetype font for clean OCR - DejaVu ships on
# most systems; on Windows, swap the path for e.g. "C:/Windows/Fonts/arial.ttf")
img = Image.new("RGB", (1200, 500), color="white")
draw = ImageDraw.Draw(img)
try:
    font = ImageFont.truetype("arial.ttf", 30)
except OSError:
    font = ImageFont.load_default()
lines = [
    "Electricity Bill",
    "Consumer No: 987654321",
    "Consumer Name: Jane Smith",
    "Billing Period: August 2026",
    "Total Units: 250",
    "Total Amount: Rs. 2000.00",
]
y = 20
for line in lines:
    draw.text((20, y), line, fill="black", font=font)
    y += 60
img.save(FIXTURES / "sample_bill.png")

print("Fixtures created in", FIXTURES)