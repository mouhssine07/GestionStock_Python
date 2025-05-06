from PIL import Image, ImageDraw

# Create a new image with a white background
size = (256, 256)
img = Image.new('RGBA', size, (255, 255, 255, 0))
draw = ImageDraw.Draw(img)

# Draw a simple chart icon
# Background circle
draw.ellipse([20, 20, 236, 236], fill='#2196F3')
# Chart lines
draw.line([(60, 180), (100, 120), (140, 160), (180, 80), (220, 140)], fill='white', width=8)
# Save as ICO
img.save('smartstock.ico', format='ICO', sizes=[(256, 256)]) 