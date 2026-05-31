"""
title: SDXL-Turbo Image Generator
author: Open WebUI Community
version: 2.0.0
description: Generates images using SDXL-Turbo via local FastAPI service.
"""

import os
import httpx
import base64
from datetime import datetime
from typing import Callable, Any, Optional


class Tools:
    def __init__(self):
        self.api_url = "http://sdxl-turbo:7860"
        self.model_name = "sdxl-turbo"

    async def generate_local_image(
        self, prompt: str, __event_emitter__: Optional[Callable[[dict], Any]] = None
    ) -> str:
        """
        Generates an image using SDXL-Turbo from a descriptive prompt.
        :param prompt: The detailed description of the image to generate.
        """
        if __event_emitter__:
            await __event_emitter__({"type": "status", "data": {
                "description": "Generating with SDXL-Turbo...", "done": False
            }})

        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(
                    f"{self.api_url}/generate",
                    json={"prompt": prompt, "steps": 4, "width": 512, "height": 512}
                )
                data = response.json()
                b64 = data["image"]

            output_dir = "/app/backend/data/generated_images"
            os.makedirs(output_dir, exist_ok=True)
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            with open(f"{output_dir}/img_{ts}.png", "wb") as f:
                f.write(base64.b64decode(b64))

            if __event_emitter__:
                await __event_emitter__({"type": "status", "data": {
                    "description": "Image generated successfully!", "done": True
                }})

            return f"### Generated Image\n\n![Generated Image](data:image/png;base64,{b64})"

        except Exception as e:
            error_msg = f"Generation failed: {str(e)}"
            if __event_emitter__:
                await __event_emitter__({"type": "status", "data": {
                    "description": error_msg, "done": True
                }})
            return error_msg