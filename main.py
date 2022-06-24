#!/usr/bin/env python3
import os
import json
import pytesseract
from PIL import Image
from pdf2image import convert_from_path

def export_images_from_pdf(pdf_path, pdf_name, image_directory):
    pages = convert_from_path(pdf_path, dpi=300)
    image_names = []

    for i, page in enumerate(pages, start=1):
        image_name = f"{pdf_name}_{i:03}.jpg"
        page.save(f"{image_directory}/{image_name}", "JPEG")
        image_names.append(image_name)

    return image_names

# get the name of the files and their tags
def get_file_names(directory):
    file_names = []

    for x in os.listdir(directory):
        if x.endswith(".pdf") or x.endswith(".PDF"):
            file_names.append(x)

    file_names = sorted(file_names)
    return file_names


def main():
    output_directory = "out"
    image_directory = "images"
    pdf_directory = "orneklem"
    
    file_names = get_file_names(pdf_directory)

    for file_name in file_names:
        print(file_name, end=' ')
        try:
            with open(f"{output_directory}/{file_name}.txt", "w") as output_file:
                text_list = []
                image_names = []
                image_names = export_images_from_pdf(f"{pdf_directory}/{file_name}", file_name, image_directory)
                for image_name in image_names:
                    image_path = f"{image_directory}/{image_name}"

                    custom_config = r'-l tur' # --psm 6
                    text = str(pytesseract.image_to_string(Image.open(image_path), config=custom_config))
                    # text = text.replace("-\n", "")

                    text_list.append(text)
                    print('-', end='')

                json.dump(fp=output_file, obj=text_list, ensure_ascii=False)
                print("+")
        except Exception as e:
            print("An error occured on " + file_name + ", Error message = " + e)

    print("done")

if __name__ == "__main__":
    main()