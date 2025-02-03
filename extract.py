import fitz  # PyMuPDF
import os
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

def extract_text(page):
    text = page.get_text()
    return text


def extract_image(page,page_num,pdf_document):
    image_list = page.get_images(full=True)
    directory = "extracted_images"

    image_paths = []  
    for img_index, img in enumerate(image_list):
        xcoord = img[0]  
        base_image = pdf_document.extract_image(xcoord)
        image_bytes = base_image["image"]

        # Save the image to a file
        img_filename = f"{directory}/{page_num + 1}_img{img_index + 1}.png"
        with open(img_filename, "wb") as img_file:
            img_file.write(image_bytes)
        
        image_paths.append(img_filename)  # Add the image path to the list

    return image_paths

def main():
    pdf_path = "uploads/jenkins-user-handbook.pdf"
    pdf_document = fitz.open(pdf_path)
    page_text = []
    # Define the directory path
    directory = "extracted_images"

    # Create the directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)  # Load the page
        page_text.append(extract_text(page))
        images = extract_image(page,page_num,pdf_document)
    
    return page_text