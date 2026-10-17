"""Replace the model's face in the two Looqma designs with the supplied model photo (inswapper_128), then match hair colour and visible skin tone.
Models are NOT in the repo: buffalo_l (insightface) and inswapper_128.onnx (research / non-commercial licence), facexlib parsing_bisenet.
usage: python3 swap.py"""
import cv2, numpy as np, torch, insightface
from insightface.app import FaceAnalysis
from facexlib.parsing import init_parsing_model
SW = "/tmp/claude-0/swap/inswapper_128.onnx"
app = FaceAnalysis(name="buffalo_l", providers=["CPUExecutionProvider"]); app.prepare(ctx_id=0, det_size=(640, 640))
swapper = insightface.model_zoo.get_model(SW, providers=["CPUExecutionProvider"])
parser = init_parsing_model(model_name="bisenet", device="cpu").eval()
MEAN = np.array([0.485, 0.456, 0.406], np.float32); STD = np.array([0.229, 0.224, 0.225], np.float32)
def parse(img, face, scale=1.9):
    """face-parsing label map (full image size, 255 = outside the analysed crop)"""
    x0, y0, x1, y1 = face.bbox; cx, cy = (x0 + x1) / 2, (y0 + y1) / 2; s = max(x1 - x0, y1 - y0) * scale / 2
    X0, Y0, X1, Y1 = int(cx - s), int(cy - s), int(cx + s), int(cy + s)
    H, W = img.shape[:2]; pad = max(0, -X0, -Y0, X1 - W, Y1 - H)
    big = cv2.copyMakeBorder(img, pad, pad, pad, pad, cv2.BORDER_REFLECT); crop = big[Y0 + pad:Y1 + pad, X0 + pad:X1 + pad]
    inp = cv2.resize(cv2.cvtColor(crop, cv2.COLOR_BGR2RGB), (512, 512)).astype(np.float32) / 255.0; inp = ((inp - MEAN) / STD).transpose(2, 0, 1)[None]
    with torch.no_grad(): lab = parser(torch.from_numpy(inp))[0].argmax(1)[0].numpy().astype(np.uint8)
    lab = cv2.resize(lab, (X1 - X0, Y1 - Y0), interpolation=cv2.INTER_NEAREST)
    full = np.full((H + 2 * pad, W + 2 * pad), 255, np.uint8); full[Y0 + pad:Y1 + pad, X0 + pad:X1 + pad] = lab
    return full[pad:pad + H, pad:pad + W]
def soft(mask, k=9): return cv2.GaussianBlur(mask.astype(np.float32), (0, 0), k)
def lab_of(img): return cv2.cvtColor(img, cv2.COLOR_BGR2LAB).astype(np.float32)
def from_lab(l): return cv2.cvtColor(np.clip(l, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR)
def mean_lab(img, m): l = lab_of(img); return l[m > 0].mean(0)

src_img = cv2.imread("source_model.jpg"); src_face = app.get(src_img)[0]; src_lab = parse(src_img, src_face)
SRC_SKIN = mean_lab(src_img, np.isin(src_lab, [1, 10]).astype(np.uint8)); SRC_HAIR = mean_lab(src_img, (src_lab == 17).astype(np.uint8))
print("source skin LAB", SRC_SKIN.round(1), "hair LAB", SRC_HAIR.round(1))

def process(name, hair_strength=1.0, skin_strength=0.9, hand_boxes=(), skin_classes=(7, 8, 9, 14, 15)):
    img = cv2.imread(f"{name}_original.jpg"); tf = app.get(img)[0]
    lab_before = parse(img, tf)
    TGT_SKIN = mean_lab(img, np.isin(lab_before, [1, 10]).astype(np.uint8))
    sw = swapper.get(img.copy(), tf, src_face, paste_back=True)
    lab = parse(sw, app.get(sw)[0] if app.get(sw) else tf)
    out = sw.astype(np.float32)
    # ---- hair: move the target's hair colour to the model's hair colour (keep texture / highlights)
    hair = soft((lab == 17).astype(np.uint8), 3)[..., None] * hair_strength
    hl = lab_of(sw); hm = hl[(lab == 17)].mean(0)
    L = hl[..., 0:1]; ratio = (SRC_HAIR[0] + 8) / max(hm[0], 1)
    new = hl.copy(); new[..., 0:1] = np.clip((L - hm[0]) * min(1.0, ratio + .2) + SRC_HAIR[0] + 8, 0, 255)
    new[..., 1:] = (hl[..., 1:] - hm[1:]) * 0.6 + SRC_HAIR[1:]
    out = out * (1 - hair) + from_lab(new).astype(np.float32) * hair
    # ---- visible skin that was NOT swapped (ears, neck, hands): shift toward the model's skin tone
    delta = (SRC_SKIN - TGT_SKIN)
    skin_mask = np.isin(lab, list(skin_classes)).astype(np.uint8)
    full = lab_of(img); body = np.zeros(img.shape[:2], np.uint8)
    for (x0, y0, x1, y1) in hand_boxes:
        reg = np.zeros_like(body); reg[y0:y1, x0:x1] = 1
        dist = np.linalg.norm(full - TGT_SKIN, axis=2); body |= ((dist < 26) & (reg > 0)).astype(np.uint8)
    m = soft(np.clip(skin_mask | body, 0, 1), 3)[..., None] * skin_strength
    sl = lab_of(out.astype(np.uint8)); sl[..., 0] += delta[0] * 0.7; sl[..., 1] += delta[1]; sl[..., 2] += delta[2]
    out = out * (1 - m) + from_lab(sl).astype(np.float32) * m
    res = np.clip(out, 0, 255).astype(np.uint8); cv2.imwrite(f"{name}_with_model.png", res)
    cv2.imwrite(f"{name}_with_model.jpg", res, [cv2.IMWRITE_JPEG_QUALITY, 96])
    return img, sw, res
if __name__ == "__main__":
    process("design1", hand_boxes=[(380, 640, 640, 840), (250, 860, 520, 1180)])
    process("design2", hair_strength=0.0, skin_classes=(14, 15), hand_boxes=[(300, 640, 720, 860)])
    print("done")
