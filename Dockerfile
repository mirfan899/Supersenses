FROM python:3.7.13-bullseye

COPY . .
RUN python -m pip install --upgrade pip
RUN python -m pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "api.py"]