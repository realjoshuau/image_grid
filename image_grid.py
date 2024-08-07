from PIL import Image, ImageDraw
import os
import argparse

USE_MARGIN = True

def create_pages(image_paths, page_size=(2550, 3300), images_per_page=6):
    pages = []
    num_pages = (len(image_paths) + images_per_page - 1) // images_per_page
    images_per_row = 2
    images_per_col = 3
    
    for i in range(num_pages):
        page = Image.new('RGB', page_size, (255, 255, 255))
        
        for j in range(images_per_page):
            image_index = i * images_per_page + j
            if image_index < len(image_paths):
                img = Image.open(image_paths[image_index])
                
                slot_width = page_size[0] // images_per_row
                slot_height = page_size[1] // images_per_col
                img = img.resize((slot_width, slot_height))
                
                x = (j % images_per_row) * slot_width
                y = (j // images_per_row) * slot_height
                
                page.paste(img, (x, y))
        
        pages.append(page)
    return pages

def create_pages_margin(image_paths, page_size=(2550, 3300), images_per_page=6, margin=30):
    pages = []
    num_pages = (len(image_paths) + images_per_page - 1) // images_per_page
    images_per_row = 2
    images_per_col = 3
    
    slot_width = (page_size[0] - margin * (images_per_row + 1)) // images_per_row
    slot_height = (page_size[1] - margin * (images_per_col + 1)) // images_per_col
    
    for i in range(num_pages):
        page = Image.new('RGB', page_size, (255, 255, 255))
        
        for j in range(images_per_page):
            image_index = i * images_per_page + j
            if image_index < len(image_paths):
                img = Image.open(image_paths[image_index])
                img = img.resize((slot_width, slot_height))
                
                x = margin + (j % images_per_row) * (slot_width + margin)
                y = margin + (j // images_per_row) * (slot_height + margin)
                
                page.paste(img, (x, y))
        
        pages.append(page)
    return pages


parser = argparse.ArgumentParser(description='Create a PDF from a folder of images')
parser.add_argument('folder', type=str, help='Folder containing images')
parser.add_argument('--output', type=str, help='Output PDF file')
parser.add_argument('--margin', action='store_true', help='Add margin between images')
parser.add_argument('--images_per_page', type=int, help='Number of images per page')
parser.add_argument('--page_width', type=int, help='Width of the page')
parser.add_argument('--page_height', type=int, help='Height of the page')
parser.add_argument('--margin_size', type=int, help='Size of the margin')

args = parser.parse_args()
folder = args.folder
output = args.output if args.output else "output.pdf"
margin = args.margin if args.margin else USE_MARGIN
page_width = args.page_width if args.page_width else 2550
page_height = args.page_height if args.page_height else 3300
images_per_page = args.images_per_page if args.images_per_page else 6
margin_size = args.margin_size if args.margin_size else 30

image_paths = os.listdir(folder)
for i in range(len(image_paths)):
    image_paths[i] = f"{folder}/" + image_paths[i]

print(f"Found {len(image_paths)} images")

if margin:
    pages = create_pages_margin(image_paths, page_size=(page_width, page_height), images_per_page=images_per_page, margin=margin_size)
else:
    pages = create_pages(image_paths, page_size=(page_width, page_height), images_per_page=images_per_page)

output_path = output if output else "output.pdf"
pages[0].save(output_path, save_all=True, append_images=pages[1:])
print(f"PDF saved to {output_path}")
