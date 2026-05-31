FROM pytorch/pytorch:2.5.1-cuda12.4-cudnn9-runtime

WORKDIR /app

RUN pip install --no-cache-dir \
    "diffusers==0.30.3" \
    "transformers==4.44.2" \
    "accelerate>=0.26.0" \
    torchvision \
    fastapi \
    uvicorn

COPY app.py .

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]