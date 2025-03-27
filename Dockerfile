FROM python:3.11-slim-bookworm

# Configuração para SSH (se necessário para o Git)
ENV GIT_SSH_COMMAND="ssh -o StrictHostKeyChecking=no"

# Instalação de dependências do sistema
RUN apt-get update \
    && apt-get install -y libgl1 libglib2.0-0 curl wget git procps \
    && rm -rf /var/lib/apt/lists/*

# Instalação do docling com suporte apenas para CPU
# Remova '--extra-index-url https://download.pytorch.org/whl/cpu' se precisar de suporte a GPU
RUN pip install --no-cache-dir docling --extra-index-url https://download.pytorch.org/whl/cpu

# Configuração de variáveis de ambiente
ENV HF_HOME=/tmp/
ENV TORCH_HOME=/tmp/
ENV OMP_NUM_THREADS=4

# Copia o requirements.txt e instala as dependências
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copia o app.py e a pasta /static para o contêiner
COPY app.py /app/app.py
COPY static /app/static

# Baixa os modelos do docling
RUN docling-tools models download

# Define o diretório de trabalho
WORKDIR /app

# Expõe a porta 5000 (ajuste se necessário)
EXPOSE 5000

# Comando para executar o app.py
CMD ["python", "app.py"]