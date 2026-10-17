---
name: stable-diffusion-webui
description: Install, run and script AUTOMATIC1111 Stable Diffusion web UI through its REST API (/sdapi/v1). Use for txt2img/img2img batches, extensions such as ControlNet, or when the user names A1111 / stable-diffusion-webui.
---
# AUTOMATIC1111 stable-diffusion-webui (https://github.com/AUTOMATIC1111/stable-diffusion-webui)

## Install and start
```bash
git clone --depth 1 https://github.com/AUTOMATIC1111/stable-diffusion-webui && cd stable-diffusion-webui
./webui.sh --api                        # Linux/macOS; webui-user.bat on Windows; first run builds a venv and installs torch
./webui.sh --api --listen               # reachable from other machines (secure it: --api-auth user:pass)
./webui.sh --api --skip-torch-cuda-test --use-cpu all --no-half   # CPU only, very slow
```
Put checkpoints in `models/Stable-diffusion/`, LoRAs in `models/Lora/`, VAEs in `models/VAE/`. UI: http://127.0.0.1:7860. API docs: http://127.0.0.1:7860/docs. (`--nowebui` starts API only.) The project is mature but slow-moving; for newer models (Flux and others) prefer ComfyUI.

## REST API
- `POST /sdapi/v1/txt2img`: `{"prompt","negative_prompt","width","height","steps","cfg_scale","seed","sampler_name":"DPM++ 2M Karras","batch_size":1}`; response `images[]` are base64 PNGs.
- `POST /sdapi/v1/img2img`: same plus `init_images[]` (base64) and `denoising_strength`.
- `GET /sdapi/v1/sd-models`, `/samplers`, `/loras`: discovery. `POST /sdapi/v1/options` with `{"sd_model_checkpoint": "<title>"}` switches the checkpoint.
- `GET /sdapi/v1/progress` for long jobs.

## Batch run in this repo
`python .claude/skills/image-generation/scripts/imggen.py a1111 prompts.json gooddays/creative/img/gen`

## Tips
SDXL: 1024x1280 (4:5), 30 steps, CFG 5-6, DPM++ 2M Karras. Use Hires fix or an upscaler only on chosen images. Network: models download from huggingface.co / civitai.com; when the host is blocked, report it instead of faking output.
