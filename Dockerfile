FROM nvidia/cuda:11.8.0-cudnn8-devel-ubuntu22.04

# Устанавливаем системные пакеты
RUN apt-get update && apt-get install -y \
    git \
    wget \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Копируем файлы проекта
COPY . /app

# Устанавливаем зависимости
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# (Опционально) Предзагрузка модели
# RUN python3 -c "from transformers import AutoModelForCausalLM; AutoModelForCausalLM.from_pretrained('TheBloke/MythoMax-L2-13B-GPTQ')"

EXPOSE 7860

CMD ["python3", "app.py", "--listen", "--server_port=7860"]
