"""Vector building blocks: cups, doodles, food. All return SVG/HTML strings."""
import math
def cup(x, y, w, h, layers, straw="#F2EBDD", ice=True, marble=None, uid="c", lid=False):
    """Iced cup. layers = [(color, fraction)] from top to bottom of the liquid. marble = colour of milk swirls."""
    tw, bw = w, w * .74; liq0 = y + h * .12; liqh = h * .86
    path = f"M{x},{y} L{x+tw},{y} L{x+tw/2+bw/2},{y+h} L{x+tw/2-bw/2},{y+h} Z"
    out = f'<defs><clipPath id="cl{uid}"><path d="{path}"/></clipPath></defs><path d="{path}" fill="rgba(255,255,255,.12)"/>'
    out += f'<g clip-path="url(#cl{uid})">'
    cy = liq0
    for col, fr in layers:
        hh = liqh * fr; out += f'<rect x="{x-10}" y="{cy}" width="{w+20}" height="{hh+2}" fill="{col}"/>'; cy += hh
    if marble:
        for i in range(6):
            sx = x + w * (.12 + .15 * i); out += f'<path d="M{sx},{liq0+8} C{sx-30},{liq0+liqh*.25} {sx+40},{liq0+liqh*.5} {sx-10},{liq0+liqh*.85}" stroke="{marble}" stroke-width="{10+4*(i%3)}" fill="none" opacity=".55" stroke-linecap="round"/>'
    if ice:
        for i, (cxx, cyy, s) in enumerate([(.28, .22, .26), (.62, .3, .24), (.4, .52, .25), (.7, .62, .22), (.3, .78, .2)]):
            ix = x + w * cxx; iy = liq0 + liqh * cyy; sz = w * s
            out += f'<rect x="{ix}" y="{iy}" width="{sz}" height="{sz}" rx="{sz*.18}" transform="rotate({(i*23)%40-18} {ix+sz/2} {iy+sz/2})" fill="rgba(255,255,255,.2)" stroke="rgba(255,255,255,.5)" stroke-width="3"/>'
    out += f'<path d="M{x+w*.1},{y+h*.1} L{x+w*.22},{y+h*.92}" stroke="rgba(255,255,255,.45)" stroke-width="7" fill="none" stroke-linecap="round"/></g>'
    out += f'<path d="{path}" fill="none" stroke="rgba(255,255,255,.55)" stroke-width="4" stroke-linejoin="round"/><rect x="{x-8}" y="{y-14}" width="{w+16}" height="16" rx="8" fill="rgba(255,255,255,.6)"/>'
    out += f'<path d="M{x+w*.58},{y-6} L{x+w*.76},{y-h*.28}" stroke="{straw}" stroke-width="{max(10,w*.04)}" stroke-linecap="round"/>'
    return out
def mug(x, y, w, h, col="#493020", liquid="#2a1a10", uid="m"):
    return (f'<path d="M{x},{y} h{w} v{h*.62} a{w*.3},{h*.3} 0 0 1 -{w*.3},{h*.38} h-{w*.4} a{w*.3},{h*.3} 0 0 1 -{w*.3},-{h*.38} z" fill="{col}"/>'
            f'<path d="M{x+w},{y+h*.18} h{w*.18} a{w*.16},{h*.2} 0 0 1 0,{h*.4} h-{w*.2}" fill="none" stroke="{col}" stroke-width="{w*.07}" stroke-linecap="round"/>'
            f'<ellipse cx="{x+w/2}" cy="{y}" rx="{w/2}" ry="{h*.08}" fill="{liquid}"/><ellipse cx="{x+w/2}" cy="{y}" rx="{w*.3}" ry="{h*.04}" fill="rgba(255,255,255,.35)"/>')
def strawberry(x, y, s, col="#C2273A"):
    return (f'<path d="M{x},{y} c{s*.5},-{s*.1} {s},{s*.4} {s*.5},{s} c-{s*.2},{s*.3} -{s*.5},{s*.3} -{s*.5},{s*.3} c0,0 -{s*.3},0 -{s*.5},-{s*.3} c-{s*.5},-{s*.6} {s*.0},-{s*1.1} {s*.5},-{s}z" transform="translate(0,0)" fill="{col}"/>'
            f'<path d="M{x+s*.1},{y+s*.02} l{s*.2},-{s*.14} l{s*.1},{s*.1} l{s*.15},-{s*.14} l{s*.1},{s*.16} l{s*.2},-{s*.1}" stroke="#4E7A3A" stroke-width="{s*.09}" fill="none" stroke-linecap="round"/>')
def croissant(x, y, s, col="#C98B4B"):
    segs = ""
    for i, (dx, dy, r) in enumerate([(0, 0, .5), (.3, -.08, .6), (.62, -.12, .7), (.98, -.08, .6), (1.28, 0, .5)]):
        segs += f'<ellipse cx="{x+dx*s}" cy="{y+dy*s}" rx="{r*s*.42}" ry="{r*s*.5}" fill="{col}" stroke="#8F5A28" stroke-width="{s*.03}" transform="rotate({(i-2)*14} {x+dx*s} {y+dy*s})"/>'
    return segs
def smiley(x, y, r=40, c="#17251D"): return f'<g stroke="{c}" stroke-width="5" fill="none" stroke-linecap="round"><circle cx="{x}" cy="{y}" r="{r}"/><path d="M{x-r*.35},{y-r*.2}v{r*.12}M{x+r*.35},{y-r*.2}v{r*.12}"/><path d="M{x-r*.5},{y+r*.15} Q{x},{y+r*.7} {x+r*.5},{y+r*.15}"/></g>'
def star(x, y, r=26, c="#17251D"): return f'<g stroke="{c}" stroke-width="5" stroke-linecap="round">' + "".join(f'<path d="M{x},{y} L{x+r*math.cos(a)},{y+r*math.sin(a)}"/>' for a in [i * math.pi / 4 for i in range(8)]) + "</g>"
def heart(x, y, s=40, c="#17251D"): return f'<path d="M{x},{y+s*.9} C{x-s*1.3},{y+s*.1} {x-s*.5},{y-s*.7} {x},{y-s*.15} C{x+s*.5},{y-s*.7} {x+s*1.3},{y+s*.1} {x},{y+s*.9}z" fill="none" stroke="{c}" stroke-width="5" stroke-linejoin="round"/>'
def arrow(x1, y1, x2, y2, bend=-60, c="#17251D"):
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2 + bend; a = math.atan2(y2 - my, x2 - mx)
    return (f'<path d="M{x1},{y1} Q{mx},{my} {x2},{y2}" stroke="{c}" stroke-width="5" fill="none" stroke-linecap="round"/>'
            f'<path d="M{x2-26*math.cos(a-.5)},{y2-26*math.sin(a-.5)} L{x2},{y2} L{x2-26*math.cos(a+.5)},{y2-26*math.sin(a+.5)}" stroke="{c}" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
def scribble(x, y, w, c="#17251D"): return f'<path d="M{x},{y} C{x+w*.25},{y-18} {x+w*.5},{y+16} {x+w},{y-12}" stroke="{c}" stroke-width="9" fill="none" stroke-linecap="round"/><path d="M{x+w*.1},{y+18} C{x+w*.4},{y+4} {x+w*.7},{y+22} {x+w*.92},{y+8}" stroke="{c}" stroke-width="6" fill="none" stroke-linecap="round"/>'
