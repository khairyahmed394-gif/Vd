const BND=[4.2,8.4,13.8,18.6];
const SCN=[0,...BND].map((a,i)=>({t0:a,t1:i<4?BND[i]:TOTAL,a:[],i}));
const mark=(par,cx,cy,k,id)=>{const g=el("g",{transform:`translate(${cx},${cy}) scale(${k}) translate(${-(LG.mark.x0+LG.mark.x1)/2},${-(LG.mark.y0+LG.mark.y1)/2})`},par);LG.dots.forEach(d=>el("circle",{cx:d.cx,cy:d.cy,r:d.r,fill:d.color},g));LG.chev.forEach(c=>el("path",{d:c.d,fill:c.color,"fill-rule":"evenodd"},g));return g;};
function staticLogo(par,cx,cy,k,id,pill){const g=el("g",{},par);if(pill)el("rect",{x:cx-215,y:cy-66,width:430,height:132,rx:66,fill:C.ivory,filter:"url(#sh)"},g);const o=lockup(g,id);o.wr.setAttribute("width",LG.word.x1-LG.word.x0+20);place(o,cx,cy,k);return g;}
function ivBg(sc,g,seed){
 const gid="ig"+sc.i;const rg=el("radialGradient",{id:gid,cx:".5",cy:".42",r:".75"},defs);el("stop",{offset:0,"stop-color":"#FFFFFF"},rg);el("stop",{offset:.55,"stop-color":C.ivory},rg);el("stop",{offset:1,"stop-color":"#EFE8DA"},rg);
 el("rect",{width:W,height:H,fill:`url(#${gid})`},g);
 const pid="gp"+sc.i,pt=el("pattern",{id:pid,width:60,height:60,patternUnits:"userSpaceOnUse"},defs);el("path",{d:"M60,0 H0 V60",fill:"none",stroke:C.gold,"stroke-width":1,opacity:.13},pt);el("rect",{width:W,height:H,fill:`url(#${pid})`,opacity:.7},g);
 const rings=el("g",{},g);[260,400,540,690,860].forEach(r=>el("ellipse",{cx:540,cy:880,rx:r,ry:r*1.12,fill:"none",stroke:C.gold,"stroke-width":1.5,opacity:.2},rings));
 sc.a.push(u=>rings.setAttribute("transform",`translate(540,880) scale(${(1+.025*u).toFixed(4)}) translate(-540,-880)`));
 amb(sc,g,seed,26,C.gold,.5);}
function dkBg(sc,g,seed){
 const gid="dg"+sc.i,rg=el("radialGradient",{id:gid,cx:".42",cy:".38",r:".95"},defs);el("stop",{offset:0,"stop-color":"#06583A"},rg);el("stop",{offset:.6,"stop-color":C.forest},rg);el("stop",{offset:1,"stop-color":C.deep},rg);
 el("rect",{width:W,height:H,fill:`url(#${gid})`},g);
 const pid="dp"+sc.i,pt=el("pattern",{id:pid,width:60,height:60,patternUnits:"userSpaceOnUse"},defs);el("path",{d:"M60,0 H0 V60",fill:"none",stroke:C.tan,"stroke-width":1,opacity:.07},pt);el("rect",{width:W,height:H,fill:`url(#${pid})`},g);
 amb(sc,g,seed,34,C.tan,.55);}
function amb(sc,g,seed,n,col,op){let s=seed;const r=()=>(s=(s*16807)%2147483647)/2147483647;const dots=[];
 for(let i=0;i<n;i++){dots.push({x:r()*W,y:260+r()*1400,r:1.5+r()*3.5,sp:6+r()*14,ph:r()*6.28,e:el("circle",{r:1,fill:col},g)});}
 sc.a.push(u=>dots.forEach(d=>{d.e.setAttribute("cx",d.x.toFixed(1));d.e.setAttribute("cy",(d.y-d.sp*u).toFixed(1));d.e.setAttribute("r",d.r);d.e.setAttribute("opacity",(op*(.5+.5*Math.sin(u*1.3+d.ph))).toFixed(2));}));}
const sparkle=(sc,g,x,y,r,t0)=>{const s=star(g,x,y,r);sc.a.push(u=>{const p=P(u,t0,t0+.5),q=.55+.45*Math.sin(u*2.2+x);s.setAttribute("opacity",(p*q).toFixed(2));s.setAttribute("transform",`rotate(${(u*20).toFixed(0)} ${x} ${y})`);});return s;};
function header(sc,g,pill,t0){const gg=G(sc,g,t0,.45,-10);gg.appendChild(staticLogo(gg,540,305,.5,"hl"+sc.i,pill));return gg;}
// ------------------------------------------------------------------ S1 brand reveal (ivory)
{const sc=SCN[0],g=sc.g=el("g",{},svg);ivBg(sc,g,11);
 const o=lockup(g,"w1");const cx=540,cy=850,k=1.3;place(o,cx,cy,k);
 sc.a.push(u=>{
  o.dots.forEach((d,i)=>{const p=E.out(P(u,.15+i*.12,.9+i*.12)),a=i*2.1+.7;d.setAttribute("opacity",clamp(p*3).toFixed(3));d.setAttribute("transform",`translate(${((1-p)*Math.cos(a)*300).toFixed(1)},${((1-p)*(Math.sin(a)*220-150)).toFixed(1)})`);});
  o.chev.forEach((c,i)=>{const p=E.out(P(u,.8+i*.14,1.3+i*.14));c.setAttribute("opacity",p.toFixed(3));c.setAttribute("transform",`translate(0,${((1-p)*-50).toFixed(1)})`);});
  o.div.setAttribute("opacity",E.out(P(u,1.3,1.6)).toFixed(3));o.wr.setAttribute("width",(E.io(P(u,1.35,2.1))*(LG.word.x1-LG.word.x0+20)).toFixed(1));});
 D(sc,g,"line",{x1:420,x2:660,y1:1025,y2:1025,stroke:C.gold,"stroke-width":3},2.1,.5);
 TX(sc,g,"CLINICAL BIOSTATISTICS",540,1095,30,500,C.forest,"middle",2.4,{"letter-spacing":9});
 [[160,430,16,1.8],[900,560,12,2.0],[820,1180,14,2.4],[200,1260,10,2.6]].forEach(([x,y,r,t])=>sparkle(sc,g,x,y,r,t));
 ev(.15,"swell",.35);o.dots.forEach((d,i)=>ev(.45+i*.12,"tick",.5));ev(.9,"pulse",.5,0);ev(1.05,"pulse",.5,2);ev(1.3,"chime",.8,0);ev(1.9,"chime",.6,2);ev(2.4,"soft",.5);}
// ------------------------------------------------------------------ S2 data integrity · accelerated trials (forest)
{const sc=SCN[1],g=sc.g=el("g",{},svg);dkBg(sc,g,23);header(sc,g,true,.3);
 const dot=PO(sc,g,84,640,.2,.4);el("circle",{cx:84,cy:640,r:18,fill:C.gold},dot);
 const hl=D(sc,g,"path",{d:"M102,640 L1080,610",stroke:C.gold,"stroke-width":2.5,opacity:.8},.3,.8);
 const L=[["DATA",830,168,C.ivory,.55],["INTEGRITY",985,134,C.ivory,.75],["ACCELERATED",1105,80,C.gold,1.0],["TRIALS",1245,150,C.gold,1.15]];
 L.forEach(([s,y,sz,col,t0])=>{const t=TX(sc,g,s,84,y,sz,700,col,"start",t0,{"letter-spacing":-1});fitMax(t,900);ev(sc.t0+t0,"tick",.55);});
 // data rows validated by a scan beam
 const ry=[1328,1362,1396,1430],wid=[640,520,600,460];
 ry.forEach((y,i)=>{const t0=1.5+i*.08;D(sc,g,"line",{x1:84,x2:84+wid[i],y1:y,y2:y,stroke:C.tan,"stroke-width":6,opacity:.55},t0,.3);const c=el("circle",{cx:900,cy:y,r:0,fill:"none"},g);ck(sc,g,900,y,22,2.0+i*.25,.2,C.gold,5);ev(sc.t0+2.0+i*.25,"check",.55);});
 const beam=el("rect",{x:70,y:1310,width:860,height:3,fill:C.gold,opacity:0},g);sc.a.push(u=>{const p=E.io(P(u,1.9,3.0));beam.setAttribute("y",(1310+p*130).toFixed(1));beam.setAttribute("opacity",(Math.sin(Math.PI*p)*.9).toFixed(2));});
 // accelerated timeline: milestones light up faster and faster
 const ty=1500,xs=[84,300,480,640,780,900,996];
 D(sc,g,"line",{x1:84,x2:996,y1:ty,y2:ty,stroke:C.tan,"stroke-width":3,opacity:.5},1.9,.5);
 const fill=el("line",{x1:84,x2:84,y1:ty,y2:ty,stroke:C.gold,"stroke-width":6,"stroke-linecap":"round"},g);
 xs.forEach((x,i)=>{const d=PO(sc,g,x,ty,2.4+i*.05,.2);el("circle",{cx:x,cy:ty,r:i==6?13:9,fill:i==6?C.gold:C.deep,stroke:C.gold,"stroke-width":4},d);});
 sc.a.push(u=>{const p=Math.pow(P(u,2.4,3.4),1.8);fill.setAttribute("x2",(84+912*p).toFixed(1));});
 [0,1,2,3,4,5].forEach(i=>ev(sc.t0+2.45+Math.pow(i/6,.55)*.95,"tick",.4));
 TX(sc,g,"CLINICAL · BIOSTATISTICS · GULF",84,1566,26,500,C.tan,"start",3.0,{"letter-spacing":5});
 ev(sc.t0+.1,"swell",.5);ev(sc.t0+3.4,"chime",.6,3);}
// ------------------------------------------------------------------ S3 medical insights in the Gulf (ivory)
{const sc=SCN[2],g=sc.g=el("g",{},svg);ivBg(sc,g,37);header(sc,g,false,.3);
 TX(sc,g,"Medical insights",84,455,68,700,C.ink,"start",.4,{"letter-spacing":-1});TX(sc,g,"in the Gulf",84,535,68,700,C.gold,"start",.55,{"letter-spacing":-1});
 const cx=540,cy=945,R=172,SW=62,seg=[[0,.38,C.forest],[.38,.66,C.mid],[.66,1,C.gold]],gap=.012;
 D(sc,g,"circle",{cx,cy,r:R+58,stroke:C.gold,"stroke-width":1.5,opacity:.5,"stroke-dasharray":"2 8"},.5,.01).removeAttribute("pathLength");
 const arcs=seg.map(([a,b,c],i)=>{const e=el("circle",{cx,cy,r:R,fill:"none",stroke:c,"stroke-width":SW,pathLength:1,transform:`rotate(${-90+(a+gap/2)*360} ${cx} ${cy})`,"stroke-dasharray":"0 1"},g);sc.a.push(u=>{const p=E.io(P(u,.7+i*.45,1.3+i*.45));e.setAttribute("stroke-dasharray",`${((b-a-gap)*p).toFixed(4)} 1`);});return e;});
 const mk=PO(sc,g,cx,cy,1.9,.4);mark(mk,cx,cy,.95);
 // legend cards with leader lines
 const card=(x,y,l1,l2,col,t0,tx,ty2,ex,ey)=>{const gg=G(sc,g,t0,.4,12);el("rect",{x,y,width:318,height:104,rx:12,fill:"#fff",filter:"url(#sh)"},gg);el("rect",{x,y,width:318,height:8,rx:4,fill:col},gg);text(gg,l1,x+22,y+52,28,600,C.ink);text(gg,l2,x+22,y+86,28,600,C.ink);
  D(sc,g,"path",{d:`M${tx},${ty2} L${ex},${ey}`,stroke:col,"stroke-width":3},t0+.3,.35);const d=PO(sc,g,ex,ey,t0+.6,.2);el("circle",{cx:ex,cy:ey,r:8,fill:col,stroke:"#fff","stroke-width":3},d);};
 const pa=a=>[cx+R*Math.cos(a*Math.PI/180),cy+R*Math.sin(a*Math.PI/180)];
 const gm=pa(-90+(.66+.17)*360),fm=pa(-90+.19*360);
 card(60,615,"Medical Insights","in Gulf",C.gold,2.0,200,719,gm[0],gm[1]);card(702,615,"Technical Research","Insights",C.forest,2.2,860,719,fm[0],fm[1]);
 // illustrative monthly bars
 const bx=84,bw=92,gp=34,base=1470,hs=[70,115,160,225,140,190,240],mo=["JAN","FEB","MAR","APR","MAY","JUN","JUL"];
 D(sc,g,"line",{x1:70,x2:1010,y1:base,y2:base,stroke:C.ink,"stroke-width":2,opacity:.5},2.6,.5);
 hs.forEach((h,i)=>{const x=bx+i*(bw+gp)-6,r=el("rect",{x,y:base,width:bw*.72,height:0,rx:4,fill:i%2?C.gold:C.forest},g);sc.a.push(u=>{const p=E.out(P(u,2.7+i*.1,3.3+i*.1));r.setAttribute("height",(h*p).toFixed(1));r.setAttribute("y",(base-h*p).toFixed(1));});
  TX(sc,g,mo[i],x+bw*.36,base+36,22,500,C.ink,"middle",3.0+i*.05,{"letter-spacing":2});});
 const pts=hs.map((h,i)=>[bx+i*(bw+gp)-6+bw*.36,base-h-34]);
 D(sc,g,"path",{d:"M"+pts.map(p=>p.join(",")).join(" L"),stroke:C.ink,"stroke-width":3},3.5,.8);pts.forEach(([x,y],i)=>{const d=PO(sc,g,x,y,3.5+i*.1,.2);el("circle",{cx:x,cy:y,r:7,fill:C.ivory,stroke:C.ink,"stroke-width":3.5},d);});
 TX(sc,g,"ILLUSTRATIVE VISUALIZATION · NOT REAL DATA",540,1560,20,500,C.gold,"middle",4.2,{"letter-spacing":3});
 ev(sc.t0+.1,"swell",.45);ev(sc.t0+.7,"draw",.5);ev(sc.t0+1.15,"draw",.5);ev(sc.t0+1.6,"draw",.5);ev(sc.t0+1.9,"chime",.7,1);ev(sc.t0+2.0,"tick",.5);ev(sc.t0+2.2,"tick",.5);hs.forEach((h,i)=>ev(sc.t0+2.8+i*.1,"pulse",.35,i%6));ev(sc.t0+4.1,"chime",.5,4);}
// ------------------------------------------------------------------ S4 map across the Gulf (forest)
{const sc=SCN[3],g=sc.g=el("g",{},svg);dkBg(sc,g,41);header(sc,g,true,.3);
 TX(sc,g,"MEDICAL INSIGHTS",84,470,76,700,C.ivory,"start",.4,{"letter-spacing":-.5});TX(sc,g,"ACROSS THE GULF",84,558,76,700,C.gold,"start",.55,{"letter-spacing":-.5});
 const lgm=el("linearGradient",{id:"mfade",x1:0,y1:0,x2:0,y2:1},defs);[[0,0],[.14,1],[.84,1],[1,0]].forEach(([o,v])=>el("stop",{offset:o,"stop-color":"#fff","stop-opacity":v},lgm));
 const mk2=el("mask",{id:"mmask",maskUnits:"userSpaceOnUse",x:0,y:640,width:W,height:900},defs);el("rect",{x:0,y:640,width:W,height:900,fill:"url(#mfade)"},mk2);
 const mg=el("g",{mask:"url(#mmask)"},g),mm=el("g",{transform:"translate(-110,775) scale(1.1)"},mg);
 const lg=G(sc,mm,.5,.8,0);
 Object.entries(MAP.countries).forEach(([n,c])=>{el("path",{d:c.d,fill:c.k=="gcc"?"#EAE2D0":"#0B4A33",stroke:c.k=="gcc"?C.forest:"#17664A","stroke-width":c.k=="gcc"?1.4:1,"stroke-linejoin":"round","fill-rule":"evenodd"},lg);});
 // sea haze
 const CI=MAP.cities,order=["Riyadh","Kuwait City","Manama","Doha","Abu Dhabi","Muscat"];
 const lab={"Kuwait City":[0,-66,"middle"],"Riyadh":[0,36,"middle"],"Manama":[-34,-30,"end"],"Doha":[-6,38,"end"],"Abu Dhabi":[30,34,"start"],"Muscat":[0,36,"middle"]};
 const pos=n=>[CI[n][0]*1.1-110,CI[n][1]*1.1+775];
 // connections from the Riyadh hub
 const hub=pos("Riyadh");
 order.slice(1).forEach((n,i)=>{const [x,y]=pos(n),mx=(hub[0]+x)/2,my=(hub[1]+y)/2,dx=x-hub[0],dy=y-hub[1],L=Math.hypot(dx,dy),cx=mx+dy/L*-L*.28,cy=my-dx/L*-L*.28;
  const p=D(sc,g,"path",{d:`M${hub[0]},${hub[1]} Q${cx},${cy} ${x},${y}`,stroke:C.gold,"stroke-width":3.5},1.7+i*.18,.7);run(sc,g,p,2.6+i*.12,.9,C.ivory,6);run(sc,g,p,3.6+i*.12,.9,C.gold,6);ev(sc.t0+1.7+i*.18,"draw",.35);});
 order.forEach((n,i)=>{const [x,y]=pos(n),t0=1.0+i*.2,gg=PO(sc,g,x,y,t0,.35);
  const ring=el("circle",{cx:x,cy:y,r:6,fill:"none",stroke:C.gold,"stroke-width":2.5},gg);sc.a.push(u=>{const q=((u-t0-.3)%2)/2;ring.setAttribute("r",(8+50*clamp(q)).toFixed(1));ring.setAttribute("opacity",(u>t0+.3?.8*(1-clamp(q)):0).toFixed(2));});
  el("path",{d:`M${x},${y} C${x-14},${y-22} ${x-22},${y-34} ${x-22},${y-46} A22,22 0 1 1 ${x+22},${y-46} C${x+22},${y-34} ${x+14},${y-22} ${x},${y}Z`,fill:C.gold,stroke:C.deep,"stroke-width":2},gg);el("circle",{cx:x,cy:y-46,r:8,fill:C.deep},gg);
  const [dx,dy,an]=lab[n];TX(sc,g,n.toUpperCase(),x+dx,y+dy-(n=="Kuwait City"?0:0),25,600,C.ivory,an,t0+.25,{"letter-spacing":2,stroke:C.deep,"stroke-width":5,"paint-order":"stroke"});ev(sc.t0+t0,"pulse",.5,i);});
 const hubp=PO(sc,g,hub[0],hub[1],1.0,.1);
 TX(sc,g,"ILLUSTRATIVE MAP · GCC CAPITALS",540,1565,22,500,C.tan,"middle",3.8,{"letter-spacing":4});
 ev(sc.t0+.1,"swell",.5);ev(sc.t0+3.9,"chime",.6,2);}
// ------------------------------------------------------------------ S5 close (ivory)
{const sc=SCN[4],g=sc.g=el("g",{},svg);ivBg(sc,g,59);
 const lg=G(sc,g,.35,.9,18);lg.appendChild(staticLogo(lg,540,780,1.3,"w5"));
 D(sc,g,"line",{x1:420,x2:660,y1:980,y2:980,stroke:C.gold,"stroke-width":3},1.1,.5);
 TX(sc,g,"DATA INTEGRITY",540,1090,54,700,C.ink,"middle",1.4,{"letter-spacing":6});TX(sc,g,"ACCELERATED TRIALS",540,1165,54,700,C.gold,"middle",1.6,{"letter-spacing":6});
 TX(sc,g,"EVIDENCE. INSIGHT. IMPACT.",540,1260,30,500,C.forest,"middle",2.0,{"letter-spacing":4});
 const ft=el("g",{},g);el("path",{d:"M360,1920 C730,1919 950,1872 1080,1778 L1080,1920 Z",fill:C.gold},ft);el("path",{d:"M360,1920 C730,1919 950,1872 1080,1778 L1080,1750 C960,1840 760,1896 470,1920 Z",fill:C.forest},ft);
 sc.a.push(u=>{const p=E.out(P(u,.5,1.5));ft.setAttribute("opacity",p.toFixed(3));ft.setAttribute("transform",`translate(0,${((1-p)*40).toFixed(1)})`);});
 [[170,420,16,.8],[910,520,12,1.2],[880,1380,14,1.6],[190,1300,10,1.9]].forEach(([x,y,r,t])=>sparkle(sc,g,x,y,r,t));
 ev(sc.t0+.1,"swell",.45);ev(sc.t0+.5,"chime",.8,5);ev(sc.t0+.7,"chime",.6,2);ev(sc.t0+1.4,"tick",.5);ev(sc.t0+1.6,"tick",.5);ev(sc.t0+2.0,"soft",.5);ev(sc.t0+2.2,"shimmer",.5);}
