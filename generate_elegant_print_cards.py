from PIL import Image, ImageDraw, ImageFont
import os

# Create print directory
if not os.path.exists("print"):
    os.makedirs("print")

# Dimensions for 3.5x2 inch card with 1/8 inch bleed on all sides
# Total size: 3.75 x 2.25 inches at 300 DPI
WIDTH = 1125
HEIGHT = 675

# Split position
SPLIT_X = 450 # 40% for photo

# Colors
BG_COLOR = "#0A0A0A"
GOLD = "#D4AF37"
WHITE = "#FFFFFF"
LIGHT_GRAY = "#CCCCCC"

# Create base image
img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
draw = ImageDraw.Draw(img)

# --- 1. Left side: Profile Photo (Full Bleed) ---
try:
    profile = Image.open("profile.jpg")
    # Target size for profile: SPLIT_X by HEIGHT
    # Profile is 713x960.
    # Scale to match HEIGHT
    scale_factor = HEIGHT / profile.height
    new_w = int(profile.width * scale_factor)
    new_h = HEIGHT
    profile = profile.resize((new_w, new_h), Image.Resampling.LANCZOS)

    # Crop horizontally to fit SPLIT_X
    # Center crop horizontally
    left = (new_w - SPLIT_X) // 2
    profile_cropped = profile.crop((left, 0, left + SPLIT_X, new_h))

    img.paste(profile_cropped, (0, 0))
except Exception as e:
    print(f"Error loading profile image: {e}")

# Draw a subtle gold dividing line
draw.line([(SPLIT_X, 0), (SPLIT_X, HEIGHT)], fill=GOLD, width=3)

# --- 2. Right side: Logo ---
right_width = WIDTH - SPLIT_X # 675
right_center_x = SPLIT_X + right_width // 2

try:
    logo = Image.open("logo.jpg")
    # Resize logo
    target_logo_width = int(right_width * 0.7)
    logo_scale = target_logo_width / logo.width
    logo_h = int(logo.height * logo_scale)
    logo = logo.resize((target_logo_width, logo_h), Image.Resampling.LANCZOS)

    # Paste logo at top right
    logo_y = 50
    logo_x = right_center_x - target_logo_width // 2
    img.paste(logo, (logo_x, logo_y))
except Exception as e:
    print(f"Error loading logo: {e}")
    logo_y = 50
    logo_h = 100

# --- 3. Fonts ---
try:
    font_name = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", 46)
    font_title = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22)
    font_text = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
except:
    font_name = ImageFont.load_default()
    font_title = ImageFont.load_default()
    font_text = ImageFont.load_default()

# --- 4. Typography (Name & Title) ---
name_text = "MARY HENNEDY"
title_text = "REALTOR® | GOLDSTONE REALTY"

# Get text bounding boxes
if hasattr(font_name, 'getbbox'):
    name_bbox = font_name.getbbox(name_text)
    name_w = name_bbox[2] - name_bbox[0]
else:
    name_w = draw.textsize(name_text, font=font_name)[0]

if hasattr(font_title, 'getbbox'):
    title_bbox = font_title.getbbox(title_text)
    title_w = title_bbox[2] - title_bbox[0]
else:
    title_w = draw.textsize(title_text, font=font_title)[0]

text_y_start = logo_y + logo_h + 30
draw.text((right_center_x - name_w//2, text_y_start), name_text, font=font_name, fill=GOLD)
draw.text((right_center_x - title_w//2, text_y_start + 60), title_text, font=font_title, fill=LIGHT_GRAY)

# --- 5. Contact Info & QR Code ---
# QR Code
try:
    qr = Image.open("qrcode_vcard_direct.png")
    # Give it a white background or keep it if it is already
    # Let's resize it
    qr_size = 150
    qr = qr.resize((qr_size, qr_size), Image.Resampling.LANCZOS)
    # Give QR a thin white border
    qr_with_border = Image.new("RGB", (qr_size + 10, qr_size + 10), WHITE)
    qr_with_border.paste(qr, (5, 5))

    qr_x = right_center_x + 50
    qr_y = text_y_start + 120
    img.paste(qr_with_border, (qr_x, qr_y))
except Exception as e:
    print(f"Error loading QR code: {e}")
    qr_x = right_center_x + 50
    qr_y = text_y_start + 120
    qr_size = 150

# Contact Info
contact_info = [
    "P: +1 (609) 500-8446",
    "E: maryhennedy@goldstonerealty.com",
    "W: goldstonerealty.com"
]

info_y = qr_y + 20
info_x_start = SPLIT_X + 40

for line in contact_info:
    draw.text((info_x_start, info_y), line, font=font_text, fill=WHITE)
    info_y += 40

# Save Print Front
img.save("print/Mary_Hennedy_Business_Card_Front_Elegant.png")

# Generate Back (Just Logo centered)
back_img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
try:
    logo_back = Image.open("logo.jpg")
    target_logo_width_back = int(WIDTH * 0.5)
    logo_scale_back = target_logo_width_back / logo_back.width
    logo_h_back = int(logo_back.height * logo_scale_back)
    logo_back = logo_back.resize((target_logo_width_back, logo_h_back), Image.Resampling.LANCZOS)

    back_img.paste(logo_back, ((WIDTH - target_logo_width_back)//2, (HEIGHT - logo_h_back)//2))
except:
    pass

back_img.save("print/Mary_Hennedy_Business_Card_Back_Elegant.png")

print("Elegant print cards generated successfully!")
