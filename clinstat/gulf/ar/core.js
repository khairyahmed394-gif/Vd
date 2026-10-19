const clamp=(x,a=0,b=1)=>Math.min(b,Math.max(a,x)),lerp=(a,b,x)=>a+(b-a)*x,P=(t,a,b)=>clamp((t-a)/(b-a));
const E={out:x=>1-Math.pow(1-x,3),io:x=>x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2};
function el(tag,at,par){const e=document.createElementNS(NS,tag);for(const k in at)e.setAttribute(k,at[k]);if(par)par.appendChild(e);return e;}
const EVENTS=[];const ev=(t,k,v=1,n=0)=>EVENTS.push({t:+t.toFixed(3),k,v,n});window.EVENTS=EVENTS;
const svg=document.getElementById("s"),defs=el("defs",{},svg);
function text(par,str,x,y,size,weight,fill,extra={}){const t=el("text",Object.assign({x,y,"font-size":size,"font-weight":weight,fill},extra),par);t.textContent=str;return t;}
function fitMax(t,max){const w=t.getBBox().width;if(w>max)t.setAttribute("font-size",parseFloat(t.getAttribute("font-size"))*max/w);return t;}
function setIn(g,p,dy=14,dx=0){const e=E.out(clamp(p));g.setAttribute("opacity",clamp(p).toFixed(3));g.setAttribute("transform",`translate(${((1-e)*dx).toFixed(2)},${((1-e)*dy).toFixed(2)})`);}
function pl(s){s.setAttribute("pathLength","1");s.setAttribute("stroke-dasharray","1");s.setAttribute("stroke-dashoffset","1");return s;}
function draw(s,p){s.setAttribute("stroke-dashoffset",(1-clamp(p)).toFixed(4));}
function spans(t,parts){parts.forEach(([s,b,c])=>{const ts=el("tspan",{},t);if(b)ts.setAttribute("font-weight",b);if(c)ts.setAttribute("fill",c);ts.textContent=s;});}
const R={};
// ---------------------------------------------------------------- official logo (traced 1:1 from the supplied file), split into animatable parts
const LCX=(LG.mark.x0+LG.word.x1)/2,LCY=(LG.mark.y0+LG.mark.y1)/2;
function lockup(parent,id="wclip"){const g=el("g",{},parent),inner=el("g",{},g);const o={g,inner};
 o.dots=LG.dots.map(d=>el("circle",{cx:d.cx,cy:d.cy,r:d.r,fill:d.color},inner));
 o.chev=LG.chev.map(c=>el("path",{d:c.d,fill:c.color,"fill-rule":"evenodd"},inner));
 o.div=el("path",{d:LG.divider.d,fill:LG.divider.color},inner);
 const cp=el("clipPath",{id},defs);o.wr=el("rect",{x:LG.word.x0-6,y:LG.word.y0-10,width:0,height:LG.word.y1-LG.word.y0+20},cp);
 o.word=el("g",{"clip-path":`url(#${id})`},inner);["clin","stat","res"].forEach(k=>LG[k].forEach(l=>el("path",{d:l.d,fill:l.color,"fill-rule":"evenodd"},o.word)));return o;}
function place(o,cx,cy,k){o.inner.setAttribute("transform",`translate(${cx},${cy}) scale(${k}) translate(${-LCX},${-LCY})`);}
// ---------------------------------------------------------------- drawing helpers (every piece registers a time function on its scene)
const ST={fill:"none","stroke-linecap":"round","stroke-linejoin":"round"};
function D(sc,par,tag,at,t0,d=.4){const e=pl(el(tag,Object.assign({},ST,at),par));sc.a.push(u=>draw(e,E.io(P(u,t0,t0+d))));return e;}
function G(sc,par,t0,d=.3,dy=10,dx=0){const g=el("g",{},par);sc.a.push(u=>setIn(g,P(u,t0,t0+d),dy,dx));return g;}
function PO(sc,par,cx,cy,t0,d=.3){const g=el("g",{},par);sc.a.push(u=>{const p=P(u,t0,t0+d),s=.55+.45*E.out(p);g.setAttribute("opacity",clamp(p*2.5).toFixed(3));g.setAttribute("transform",`translate(${cx},${cy}) scale(${s.toFixed(3)}) translate(${-cx},${-cy})`);});return g;}
function TX(sc,par,s,x,y,size,w,fill,anchor,t0,ex={}){const g=G(sc,par,t0,.28,8);return text(g,s,x,y,size,w,fill,Object.assign({"text-anchor":anchor||"start"},ex));}
function doc(sc,par,x,y,w,h,t0,d=.4,o={}){const f=Math.min(w,h)*.26,col=o.col||C.forest,sw=o.sw||4.5,n=o.lines==null?3:o.lines;
 D(sc,par,"path",{d:`M${x},${y} H${x+w-f} L${x+w},${y+f} V${y+h} H${x} Z`,stroke:col,"stroke-width":sw},t0,d);D(sc,par,"path",{d:`M${x+w-f},${y} V${y+f} H${x+w}`,stroke:col,"stroke-width":sw},t0,d);
 for(let i=0;i<n;i++){const ly=y+f+8+(h-f-26)*(i+.5)/n;D(sc,par,"line",{x1:x+w*.17,x2:x+w*(i==n-1?.55:.83),y1:ly,y2:ly,stroke:o.lc||C.gold,"stroke-width":Math.max(3,sw-1)},t0+.12+i*.05,d);}}
function mag(sc,par,r,t0,d=.4,sw=12){const g=el("g",{},par);D(sc,g,"circle",{cx:0,cy:0,r,stroke:C.forest,"stroke-width":sw},t0,d);D(sc,g,"line",{x1:r*.74,y1:r*.74,x2:r*1.58,y2:r*1.58,stroke:C.forest,"stroke-width":sw*1.4},t0+d*.4,d*.7);return g;}
function at(g,x,y){g.setAttribute("transform",`translate(${x.toFixed(1)},${y.toFixed(1)})`);}
function ck(sc,par,cx,cy,s,t0,d=.3,col=C.forest,w=8){return D(sc,par,"path",{d:`M${cx-s*.5},${cy} L${cx-s*.12},${cy+s*.38} L${cx+s*.55},${cy-s*.42}`,stroke:col,"stroke-width":w},t0,d);}
function head(par,x,y,ang,col=C.gold,s=1,w=4){return el("path",Object.assign({d:`M${-14*s},${-10*s} L0,0 L${-14*s},${10*s}`,transform:`translate(${x},${y}) rotate(${ang})`,stroke:col,"stroke-width":w},ST),par);}
function arrow(sc,par,d,tx,ty,ang,t0,dd=.35,col=C.gold,w=4){const p=D(sc,par,"path",{d,stroke:col,"stroke-width":w},t0,dd);const h=head(par,tx,ty,ang,col,1,w);sc.a.push(u=>h.setAttribute("opacity",P(u,t0+dd*.85,t0+dd).toFixed(2)));return p;}
function run(sc,par,path,t0,d=.5,col=C.gold,r=6){const c=el("circle",{r,fill:col,opacity:0},par);sc.a.push(u=>{const q=P(u,t0,t0+d);if(q>0&&q<1){const L=path.getTotalLength(),pt=path.getPointAtLength(L*E.io(q));c.setAttribute("cx",pt.x);c.setAttribute("cy",pt.y);c.setAttribute("opacity",Math.sin(Math.PI*q).toFixed(2));}else c.setAttribute("opacity",0);});return c;}
function person(par,cx,cy,k,col){const g=el("g",{},par);el("circle",{cx,cy:cy-.34*k,r:.27*k,fill:col},g);el("path",{d:`M${cx-.52*k},${cy+.56*k} Q${cx-.52*k},${cy+.02*k} ${cx},${cy+.02*k} Q${cx+.52*k},${cy+.02*k} ${cx+.52*k},${cy+.56*k} Z`,fill:col},g);return g;}
function star(par,cx,cy,r,col=C.gold){return el("path",{d:`M${cx},${cy-r} Q${cx+r*.18},${cy-r*.18} ${cx+r},${cy} Q${cx+r*.18},${cy+r*.18} ${cx},${cy+r} Q${cx-r*.18},${cy+r*.18} ${cx-r},${cy} Q${cx-r*.18},${cy-r*.18} ${cx},${cy-r} Z`,fill:col},par);}
function funnelD(cx,top,w,h,stemW,stemH){const a=cx-w/2,b=cx+w/2,s0=cx-stemW/2,s1=cx+stemW/2,my=top+h,bot=my+stemH;return `M${a},${top} H${b} L${s1},${my} V${bot-12} Q${s1},${bot} ${s1-12},${bot} H${s0+12} Q${s0},${bot} ${s0},${bot-12} V${my} Z`;}
const smallLabel=(sc,par,s,x,y,size,anchor,t0,col=C.ink,max)=>{const t=TX(sc,par,s,x,y,size,700,col,anchor,t0,{"letter-spacing":1.2});if(max)fitMax(t,max);return t;};
