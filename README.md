# FASTesseract
A console application to install and use Tesseract OCR on batch extracting text from PDF files.

### Usage
```bash
make setup                   # install dependencies
make run DIR=<pdf_directory> # run
make clean                   # clean output
```

### Run Tesseract with OpenCL Acceleration
OpenCL support is still experimental for the [docs](https://tesseract-ocr.github.io/tessdoc/TesseractOpenCL.html#:~:text=OpenCL%20support%20in%20Tesseract%20is%20still%20considered%20experimental.).

[Install OpenCL SDK with apt](https://github.com/KhronosGroup/OpenCL-Guide/blob/main/chapters/getting_started_linux.md).

[Build Tesseract](https://tesseract-ocr.github.io/tessdoc/TesseractOpenCL.html#:~:text=Building%20Tesseract%20on%20Linux%20with%20OpenCL).


### Alternative Trained Files

https://tesseract-ocr.github.io/tessdoc/Data-Files