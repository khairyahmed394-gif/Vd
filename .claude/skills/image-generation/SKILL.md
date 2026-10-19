---
name: image-generation
description: Generate campaign photography (product shots, lifestyle, food) with local Stable Diffusion tools (ComfyUI, AUTOMATIC1111, Fooocus) and place the results into the design pipeline. Use when a design needs a new, non-repeated photo, when asked to "generate the images", or to choose between ComfyUI, A1111 and Fooocus.
---
# Image generation for campaign designs

## Pick the tool
| Need | Use |
|---|---|
| Scripted batch of many images from a prompt list (this repo's pipeline) | **ComfyUI** (`comfyui` skill) or **AUTOMATIC1111** (`stable-diffusion-webui` skill) through `scripts/imggen.py` |
| One-off, quality-first, minimal tuning, a person at the keyboard | **Fooocus** (`fooocus` skill) |
| Complex workflows (inpainting, ControlNet, upscaling, image-to-video) | **ComfyUI** |

## Reality check before promising anything
- **Hardware:** all three need an NVIDIA GPU (4 GB min for Fooocus, 8 GB+ comfortable for SDXL). The cloud session has **no GPU** (4 CPU cores, 15 GB RAM): SDXL on CPU takes tens of minutes per image and quality at low steps is poor. Prefer running on the user's machine or a GPU runtime.
- **Weights:** checkpoints come from Hugging Face / CivitAI. Those hosts are **blocked** by the session network policy. Tell the user the host (`huggingface.co`, its CDN) and that they can allow it under Network access in the environment settings, or run the scripts locally. Never fake results.
- **Licences:** check the licence of the checkpoint before commercial use (SDXL base: OpenRAIL++; many community checkpoints restrict commercial use).

## GOOD DAYS pipeline
1. Prompts live in `gooddays/creative/art-direction.md` section 8 (new direction) and `gooddays/campaign/image-prompts.md` (earlier set). Convert to JSON: `[{"id": "d01", "prompt": "...", "ratio": "4:5"}]` (`gooddays/creative/prompts.json` is the starting file).
2. Start a backend, then run:
   `python .claude/skills/image-generation/scripts/imggen.py comfy --ckpt <file>.safetensors --master "<master block>" gooddays/creative/prompts.json gooddays/creative/img/gen`
3. Naming decides placement: `gooddays/creative/img/gen/<id>.jpg` replaces the vector stand-in in `designs.py`; `gooddays/campaign/posts/img/gen/<card>.jpg` and `s01..s24.jpg` replace photos in the posts/stories builders. Re-run the builder (`python3 designs.py`, `posts/build.py`, `stories.py`).
4. Add logo, text and prices in the design layer. Never let the model write the brand name.
5. Review every image: hands, cups (no printed text), duplicate faces, plastic skin. Regenerate with another `--seed` (use `--only id --seed N`).

## Verified in this repo
`imggen.py` was tested against a live ComfyUI 0.39 in CPU mode: the graph validates and is accepted; the only failure is the missing checkpoint (`ckpt_name not in []`), which is expected until weights are available.

## Rules
- One distinct scene per design; the same image is never reused across designs.
- No real person's likeness without consent. Do not generate images that imitate a real brand or person.
- Keep generated files out of git unless small; commit the prompts and scripts.
