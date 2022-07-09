#!/usr/bin/env python3
import os
import re
import sys
import json
import pytesseract
import multiprocessing
from PIL import Image
from pdf2image import convert_from_path
from pathlib import Path


CUSTOM_CONFIG = r'-l tur --psm 6' # --psm 6 = treat image as single uniform block of text
USE_PDF_IMAGES_AGAIN = False # dont convert pdf to images again, if exists

max_threads = max(1, multiprocessing.cpu_count() // 2) # set the maximum number of threads to use


# TODO: chech builtin pdf2image methods to export directly
def export_images_from_pdf(pdf_path, pdf_name, image_directory):
    pages = convert_from_path(pdf_path, dpi=300) 
    image_names = []

    for i, page in enumerate(pages, start=1):
        image_name = f"{pdf_name}_{i:03}.jpg"
        image_names.append(image_name) # will be used while getting images for detection

        if(USE_PDF_IMAGES_AGAIN and Path(f"{image_directory}/{image_name}").is_file()):
            print(f"already exists, pass {image_name}")
        else:
            page.save(f"{image_directory}/{image_name}", "JPEG") # create new or overwrite

    return image_names


# get the name of the files and their tags
def get_file_names(directory):
    file_names = []

    for x in os.listdir(directory):
        if x.lower().endswith(".pdf"):
            file_names.append(x)

    file_names = sorted(file_names)
    return file_names


#  write text list to file
def write_list(file, list):
    for item in list:
        file.write(item)
        file.write('\\f\n') # page break as string


def process_pdf(image_path):
    text = str(pytesseract.image_to_string(Image.open(image_path), config=CUSTOM_CONFIG))
    # Delete Image from Storage
    if(not USE_PDF_IMAGES_AGAIN):
        os.remove(image_path)

    text = text[:-1] # delete page break
    return text


# TODO: progress bar
def main():
    pdf_directory = sys.argv[1]

    output_directory = f"{pdf_directory}-out"
    image_directory = f"{pdf_directory}-images"
    Path(output_directory).mkdir(parents=True, exist_ok=True)
    Path(image_directory).mkdir(parents=True, exist_ok=True)
    
    file_names = get_file_names(pdf_directory)

    for file_name in file_names:  # Iterate all files from input directory
        print(file_name, end=' ')
        try:
            with open(f"{output_directory}/{file_name}.txt", "w") as output_file:
                text_list = []
                image_names = []
                image_names = export_images_from_pdf(f"{pdf_directory}/{file_name}", file_name, image_directory)
                
                with multiprocessing.Pool(processes=max_threads) as pool:
                    results = []
                    for image_name in image_names:
                        image_path = f"{image_directory}/{image_name}"
                        results.append(pool.apply_async(process_pdf, (image_path,)))

                    for result in results:
                        text_list.append(result.get())
                        print('-', end='')

                # TODO: json and text output option
                # output_file.write(json.dumps(obj=text_list, ensure_ascii=False, indent=4))
                write_list(output_file, text_list)
                print("+")

                # # monitor the CPU utilization and adjust the number of threads dynamically
                # cpu_percent = psutil.cpu_percent()
                # if cpu_percent < 80 and max_threads < multiprocessing.cpu_count():
                #     max_threads += 1
                # elif cpu_percent > 95 and max_threads > 1:
                #     max_threads -= 1

                # # wait for a short time to avoid overloading the system
                # time.sleep(1)

        except Exception as e:
            print(f"An error occured on {file_name}, Error message = {e}")
        


    print("done")


if __name__ == "__main__":
    main()
