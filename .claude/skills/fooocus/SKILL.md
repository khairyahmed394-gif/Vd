---
name: fooocus
description: Install and use Fooocus (SDXL image generator with minimal tuning, built-in prompt expansion and style presets) for quality-first one-off images, image prompts and inpainting. Use when the user names Fooocus or wants good results without managing workflows.
---
# Fooocus (https://github.com/lllyasviel/Fooocus)

Status: limited long-term support (bug fixes only), SDXL-only. Great quality per click, little control, no official REST API. For scripted batches use ComfyUI or A1111.

## Install and start
```bash
git clone --depth 1 https://github.com/lllyasviel/Fooocus && cd Fooocus
python -m venv fooocus_env && . fooocus_env/bin/activate
pip install -r requirements_versions.txt      # install the matching PyTorch for your GPU first if needed
python entry_with_update.py                   # first run downloads SDXL models (many GB)
python entry_with_update.py --preset realistic   # photoreal preset (others: default, anime, lcm, lightning, playground_v2.5, pony_v6, sai)
python entry_with_update.py --listen          # reachable from other machines
```
Minimum 4 GB NVIDIA VRAM. Windows has a one-click zip in the repo README.

## Using it for campaign photography
1. Preset `realistic` (or `default` with Photograph/Cinematic styles), performance Quality, aspect ratio 1024x1280 (4:5) or 832x1472 (9:16).
2. Paste one prompt from `gooddays/creative/art-direction.md` section 8; Fooocus expands it automatically, so keep prompts plain and visual. Put unwanted things in the Negative field.
3. Use **Image Prompt** to keep a consistent person or place (upload the reference), **Inpaint/Outpaint** to fix hands, cups and empty areas for text, **Upscale** for the keepers.
4. Save as `gooddays/creative/img/gen/<id>.jpg` (the id decides which design uses it).
Scripting: the UI is Gradio, so a script can call it with `gradio_client`, but the endpoint layout is not a stable public API. If automation is required, use ComfyUI or the third-party Fooocus-API project and say so.

## Limits
No GPU in the cloud session; model downloads need huggingface.co (blocked by default). Say so rather than faking output.
