FROM python:alpine
COPY requirements.txt inthewild.db src/main.py ./
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "main.py"] 
