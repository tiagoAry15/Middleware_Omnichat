# Usa uma imagem base oficial de Python
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

# Expõe a porta 3000 para conexão
EXPOSE 3000

# Define o comando padrão para ser executado ao iniciar o contêiner com gunicorn
CMD ["gunicorn","-k","eventlet","-w","1","-b", "0.0.0.0:3000", "api:app"]
