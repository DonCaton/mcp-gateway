from fastapi import FastAPI
from pydantic import BaseModel
from diffusers import AutoPipelineForText2Image
import torch, base64, io

app = FastAPI()

print("Loading SDXL-Turbo model...")
pipe = AutoPipelineForText2Image.from_pretrained(
    "stabilityai/sdxl-turbo",
    torch_dtype=torch.float16,
    variant="fp16"
)
pipe.to("cuda")
print("Model ready!")

class GenerateRequest(BaseModel):
    prompt: str
    steps: int = 1
    width: int = 512
    height: int = 512

@app.post("/generate")
async def generate(req: GenerateRequest):
    image = pipe(
        prompt=req.prompt,
        num_inference_steps=req.steps,
        guidance_scale=0.0,
        width=req.width,
        height=req.height,
    ).images[0]

    buf = io.BytesIO()
    image.save(buf, format="PNG")
    b64 = base64.b64encode(buf.getvalue()).decode()
    return {"image": b64}

@app.get("/health")
async def health():
    return {"status": "ok"}