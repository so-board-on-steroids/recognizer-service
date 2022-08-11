FROM python:3.9-slim

RUN apt update && apt install -y python3-opencv tesseract-ocr && apt clean

# Download last language package from https://github.com/tesseract-ocr/tessdata
RUN mkdir -p /usr/share/tesseract-ocr/4.00/tessdata
ADD rus.traineddata /usr/share/tesseract-ocr/4.00/tessdata/rus.traineddata

# Check the installation status
RUN tesseract --list-langs    
RUN tesseract -v 

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

ADD utils.py utils.py
ADD recognizer.py recognizer.py

EXPOSE 5000

CMD [ "gunicorn", "--bind", "0.0.0.0:5000", "recognizer:app" ]