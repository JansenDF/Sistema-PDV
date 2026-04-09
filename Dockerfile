FROM python:3.13-slim

# Instala tzdata para suporte a fuso horário
RUN apt-get update && apt-get install -y tzdata

# Define o fuso horário (ex: America/Sao_Paulo para UTC-3)
# ENV TZ=America/Sao_Paulo

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]