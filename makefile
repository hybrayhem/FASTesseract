target: run

DIR = orneklem

setup:
	sudo apt install tesseract-ocr
	sudo apt install tesseract-ocr-tur
	pip3 install -r requirements.txt

run:
	python3 main.py $(DIR)

clean:
	rm -r orneklem-images orneklem-out
    