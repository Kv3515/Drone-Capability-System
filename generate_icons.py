#!/usr/bin/env python3
"""
Generate placeholder icons for the PWA.
Requires: pip install Pillow
"""

try:
    from PIL import Image, ImageDraw
    
    # Create 192x192 icon
    img_192 = Image.new('RGBA', (192, 192), color=(14, 17, 23, 255))
    draw_192 = ImageDraw.Draw(img_192)
    
    # Draw a simple helicopter icon
    cx, cy = 96, 96
    # Background circle
    draw_192.ellipse([cx-80, cy-80, cx+80, cy+80], fill=(33, 150, 243, 255), outline=(25, 118, 210, 255))
    # Helicopter blades
    draw_192.line([cx-60, cy-30, cx+60, cy-30], fill=(255, 255, 255, 255), width=8)
    draw_192.line([cx-30, cy-60, cx-30, cy+60], fill=(255, 255, 255, 255), width=8)
    # Fuselage
    draw_192.ellipse([cx-20, cy+20, cx+20, cy+60], fill=(255, 255, 255, 255))
    
    img_192.save('static/icon-192.png')
    print("✓ Created static/icon-192.png")
    
    # Create 512x512 icon
    img_512 = Image.new('RGBA', (512, 512), color=(14, 17, 23, 255))
    draw_512 = ImageDraw.Draw(img_512)
    
    cx, cy = 256, 256
    draw_512.ellipse([cx-210, cy-210, cx+210, cy+210], fill=(33, 150, 243, 255), outline=(25, 118, 210, 255))
    draw_512.line([cx-160, cy-80, cx+160, cy-80], fill=(255, 255, 255, 255), width=20)
    draw_512.line([cx-80, cy-160, cx-80, cy+160], fill=(255, 255, 255, 255), width=20)
    draw_512.ellipse([cx-50, cy+50, cx+50, cy+160], fill=(255, 255, 255, 255))
    
    img_512.save('static/icon-512.png')
    print("✓ Created static/icon-512.png")
    
    print("\n✅ Icons generated successfully!")
    print("Note: These are placeholder icons. Consider creating custom ones.")

except ImportError:
    print("❌ Error: Pillow not installed")
    print("Run: pip install Pillow")
    print("\nAlternative: Manually add icon-192.png and icon-512.png to the static/ folder")
