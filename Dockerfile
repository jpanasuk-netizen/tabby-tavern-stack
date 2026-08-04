FROM ghcr.io/theroyallab/tabbyapi:latest
USER root
RUN apt-get update && apt-get install -y python3-dev python3.12-dev build-essential && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /app/logs && chmod 777 /app/logs

# ---- CUDA / GPU Environment Defaults ----
ENV CUDA_VISIBLE_DEVICES=0
ENV CUDA_DEVICE_ORDER=PCI_BUS_ID
ENV PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:128
ENV OMP_NUM_THREADS=8

# ---- ExLlamaV2/EXL3 Defaults ----
ENV EXLLAMA_GPU_LAYERS=999
ENV EXLLAMA_KV_CACHE=q8_0
ENV EXLLAMA_FLASH_ATTENTION=1