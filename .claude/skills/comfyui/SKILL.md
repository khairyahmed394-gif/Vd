---
name: comfyui
description: Install, run and script ComfyUI (node-based Stable Diffusion/SDXL/Flux workflows) through its HTTP API. Use for batch image generation, custom workflows, inpainting, upscaling or ControlNet, and when a Stable Diffusion server must be driven from a script.
---
# ComfyUI (https://github.com/Comfy-Org/ComfyUI)

## Install and start
```bash
git clone --depth 1 https://github.com/Comfy-Org/ComfyUI && cd ComfyUI
python -m venv .venv && . .venv/bin/activate
pip install torch torchvision torchaudio     # pick the CUDA build for your GPU from pytorch.org
pip install -r requirements.txt
python main.py --listen 127.0.0.1 --port 8188          # GPU
python main.py --cpu                                  # CPU only: works, very slow
```
Put checkpoints in `models/checkpoints/` (`*.safetensors`), VAEs in `models/vae/`, LoRAs in `models/loras/`, ControlNet in `models/controlnet/`, upscalers in `models/upscale_models/`. Open http://127.0.0.1:8188 for the UI.

## HTTP API (used by `image-generation/scripts/imggen.py`)
- `POST /prompt` with `{"prompt": <graph>, "client_id": "<uuid>"}`; the graph is the "API format" JSON (UI: Settings > Enable dev mode > Save (API format)). Validation errors come back immediately (for example `ckpt_name` not in list = file missing).
- `GET /history/<prompt_id>` until it has `outputs`; `GET /view?filename=&subfolder=&type=output` downloads the image.
- `POST /upload/image` uploads an input image for image-to-image / ControlNet / inpainting.
- `GET /object_info` lists every node and its allowed values (use it to discover installed checkpoints, samplers, schedulers).
Basic graph: CheckpointLoaderSimple > CLIPTextEncode (positive + negative) > EmptyLatentImage > KSampler > VAEDecode > SaveImage (see `assets/sdxl_txt2img_api.json`).

## Settings that work for photoreal food and drinks (SDXL)
1024-class resolution (1024x1280 for 4:5, 832x1472 for 9:16), 28-35 steps, CFG 4.5-6.5, sampler `dpmpp_2m`, scheduler `karras`. Prompt in natural language, state lens, light and surface; keep negatives short. Generate at SDXL size then crop; upscale only the keepers.

## Batch run in this repo
`python .claude/skills/image-generation/scripts/imggen.py comfy --ckpt <file> prompts.json gooddays/creative/img/gen`

## Troubleshooting
- `value not in list: ckpt_name` = checkpoint not in `models/checkpoints`.
- Out of memory: `--lowvram` / `--novram`, smaller base size, or tiled VAE (`VAEDecodeTiled`).
- Slow on CPU: use a 512-768 px model (SD1.5/LCM or SDXL-Turbo at 1-4 steps) for drafts only.
- Network: model downloads need huggingface.co or civitai.com. If blocked, report the host and ask the user to allow it or to place the files manually.
