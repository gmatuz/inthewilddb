FROM python:alpine
COPY requirements.txt src/main.py ./
RUN wget https://pub-4c1eae2a180542b19ea7c88f1e4ccf07.r2.dev/inthewild.db
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "main.py"] 
