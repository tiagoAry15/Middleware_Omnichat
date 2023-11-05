# Usa a imagem base oficial de Python 3.11
FROM python:3.9-slim

# Define o diretório de trabalho no contêiner
WORKDIR /app

# Copia os arquivos de dependência e instala os pacotes necessários
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copia os arquivos restantes do aplicativo para o contêiner
COPY . .

# Define a variável de ambiente para indicar que o Flask deve ser executado em modo de produção
ENV FLASK_ENV=production

# Expõe as portas 3000 para o Flask e 8089 para o Locust
EXPOSE 8080

# Define o comando padrão para ser executado ao iniciar o contâiner com gunicorn e Locust
CMD ["python", "app.py"]

