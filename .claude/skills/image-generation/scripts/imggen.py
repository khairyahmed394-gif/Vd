#!/usr/bin/env python3
"""Batch text-to-image through a running ComfyUI or AUTOMATIC1111 server, saved as <outdir>/<id>.jpg cropped to the requested ratio.

usage:
  imggen.py comfy  --server http://127.0.0.1:8188 --ckpt <checkpoint filename in ComfyUI/models/checkpoints> prompts.json outdir
  imggen.py a1111  --server http://127.0.0.1:7860 prompts.json outdir
prompts.json: [{"id": "d01", "prompt": "...", "negative": "...", "ratio": "4:5"}, ...]   (negative/ratio optional)
options: --steps 30 --cfg 5.5 --seed 1234 --base 1024 --sampler dpmpp_2m --scheduler karras --master "text prepended to every prompt" --only id1,id2 --skip-existing
Needs: pip install requests pillow
"""
import argparse, base64, io, json, os, sys, time, uuid
import requests
from PIL import Image
def size_for(ratio, base):
    a, b = (float(x) for x in ratio.split(":")); s = (base * base) ** .5; w = s * (a / b) ** .5; h = s / (a / b) ** .5
    r8 = lambda v: max(512, int(round(v / 64)) * 64); return r8(w), r8(h)
def crop_to(img, ratio):
    a, b = (float(x) for x in ratio.split(":")); tw = img.height * a / b
    if tw <= img.width: l = (img.width - tw) / 2; return img.crop((int(l), 0, int(l + tw), img.height))
    th = img.width * b / a; t = (img.height - th) / 2; return img.crop((0, int(t), img.width, int(t + th)))
def comfy_graph(a, p, n, w, h, seed):
    return {"1": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": a.ckpt}},
            "2": {"class_type": "CLIPTextEncode", "inputs": {"text": p, "clip": ["1", 1]}},
            "3": {"class_type": "CLIPTextEncode", "inputs": {"text": n, "clip": ["1", 1]}},
            "4": {"class_type": "EmptyLatentImage", "inputs": {"width": w, "height": h, "batch_size": 1}},
            "5": {"class_type": "KSampler", "inputs": {"model": ["1", 0], "positive": ["2", 0], "negative": ["3", 0], "latent_image": ["4", 0], "seed": seed, "steps": a.steps, "cfg": a.cfg, "sampler_name": a.sampler, "scheduler": a.scheduler, "denoise": 1.0}},
            "6": {"class_type": "VAEDecode", "inputs": {"samples": ["5", 0], "vae": ["1", 2]}},
            "7": {"class_type": "SaveImage", "inputs": {"images": ["6", 0], "filename_prefix": "gooddays"}}}
def run_comfy(a, p, n, w, h, seed):
    r = requests.post(f"{a.server}/prompt", json={"prompt": comfy_graph(a, p, n, w, h, seed), "client_id": str(uuid.uuid4())}, timeout=60)
    if r.status_code != 200: sys.exit(f"ComfyUI rejected the graph: {r.text[:600]}")
    pid = r.json()["prompt_id"]
    while True:
        hist = requests.get(f"{a.server}/history/{pid}", timeout=60).json()
        if pid in hist and hist[pid].get("outputs"): break
        time.sleep(2)
    im = next(iter(hist[pid]["outputs"].values()))["images"][0]
    raw = requests.get(f"{a.server}/view", params={"filename": im["filename"], "subfolder": im["subfolder"], "type": im["type"]}, timeout=120).content
    return Image.open(io.BytesIO(raw)).convert("RGB")
def run_a1111(a, p, n, w, h, seed):
    r = requests.post(f"{a.server}/sdapi/v1/txt2img", json={"prompt": p, "negative_prompt": n, "width": w, "height": h, "steps": a.steps, "cfg_scale": a.cfg, "seed": seed, "sampler_name": "DPM++ 2M Karras"}, timeout=3600)
    r.raise_for_status(); return Image.open(io.BytesIO(base64.b64decode(r.json()["images"][0]))).convert("RGB")
def main():
    ap = argparse.ArgumentParser(); ap.add_argument("backend", choices=["comfy", "a1111"]); ap.add_argument("prompts"); ap.add_argument("outdir")
    ap.add_argument("--server", default=None); ap.add_argument("--ckpt", default=""); ap.add_argument("--steps", type=int, default=30); ap.add_argument("--cfg", type=float, default=5.5); ap.add_argument("--seed", type=int, default=1234)
    ap.add_argument("--base", type=int, default=1024); ap.add_argument("--sampler", default="dpmpp_2m"); ap.add_argument("--scheduler", default="karras"); ap.add_argument("--master", default=""); ap.add_argument("--only", default=""); ap.add_argument("--skip-existing", action="store_true")
    a = ap.parse_args(); a.server = (a.server or ("http://127.0.0.1:8188" if a.backend == "comfy" else "http://127.0.0.1:7860")).rstrip("/")
    if a.backend == "comfy" and not a.ckpt: sys.exit("--ckpt is required for ComfyUI (file name inside models/checkpoints)")
    os.makedirs(a.outdir, exist_ok=True); only = set(filter(None, a.only.split(",")))
    for item in json.load(open(a.prompts)):
        if only and item["id"] not in only: continue
        out = os.path.join(a.outdir, item["id"] + ".jpg")
        if a.skip_existing and os.path.exists(out): continue
        ratio = item.get("ratio", "4:5"); w, h = size_for(ratio, a.base); p = (a.master + " " + item["prompt"]).strip(); n = item.get("negative", "text, letters, logo, watermark, deformed hands, extra fingers, plastic skin, cartoon")
        t0 = time.time(); img = (run_comfy if a.backend == "comfy" else run_a1111)(a, p, n, w, h, a.seed)
        crop_to(img, ratio).save(out, quality=95); print(f"{item['id']} saved {out} ({time.time()-t0:.0f}s)", flush=True)
if __name__ == "__main__": main()
