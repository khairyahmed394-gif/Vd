// ================================================================ 6 · effect sizes & confidence intervals
PRIN.push({n:6,sz:1.08,w:1.7,ts:1,cap:["Report effect sizes and","confidence intervals,","not only p-values"],build(sc,st){
 const PY=-120;
 // reference line + CI + marker
 const ref=D(sc,st,"line",{x1:-20,x2:-20,y1:PY-48,y2:PY+48,stroke:C.forest,"stroke-width":3.5,"stroke-dasharray":"8 8"},.1,.4);ref.removeAttribute("pathLength");ref.setAttribute("stroke-dashoffset",0);
 const rc=el("clipPath",{id:"c6"},defs),rr=el("rect",{x:-40,y:PY-48,width:40,height:0},rc);ref.setAttribute("clip-path","url(#c6)");sc.a.push(u=>rr.setAttribute("height",(96*E.io(P(u,.1,.5))).toFixed(1)));
 D(sc,st,"line",{x1:-20,x2:-230,y1:PY,y2:PY,stroke:C.gold,"stroke-width":10},.3,.45);D(sc,st,"line",{x1:-20,x2:190,y1:PY,y2:PY,stroke:C.gold,"stroke-width":10},.3,.45);
 [-230,190].forEach((x,i)=>D(sc,st,"line",{x1:x,x2:x,y1:PY-26,y2:PY+26,stroke:C.gold,"stroke-width":10},.65,.2));
 const mk=PO(sc,st,-20,PY,.7,.3);el("rect",{x:-20-24,y:PY-24,width:48,height:48,rx:6,fill:C.forest,transform:`rotate(45 -20 ${PY})`},mk);el("circle",{cx:-20,cy:PY,r:8,fill:C.ivory},mk);
 smallLabel(sc,st,"EFFECT SIZE",-20,PY-70,30,"middle",.85);
 smallLabel(sc,st,"CONFIDENCE INTERVAL",-20,PY+82,28,"middle",.95,C.forest);
 // ruler (scale) · growth bars · p-value document
 D(sc,st,"rect",{x:-430,y:20,width:64,height:250,rx:10,stroke:C.forest,"stroke-width":5},.4,.4);
 for(let i=0;i<8;i++)D(sc,st,"line",{x1:-430,x2:-430+(i%2?24:38),y1:48+i*28,y2:48+i*28,stroke:C.forest,"stroke-width":4},.5+i*.02,.2);
 [[-260,55],[-195,100],[-130,150]].forEach(([x,h],i)=>{const g=el("g",{},st),r=el("rect",{x,y:270,width:44,height:0,fill:i==2?C.gold:C.forest},g);sc.a.push(u=>{const p=E.out(P(u,.55+i*.1,.9+i*.1));r.setAttribute("height",(h*p).toFixed(1));r.setAttribute("y",(270-h*p).toFixed(1));});});
 arrow(sc,st,"M-280,150 L-100,50",-96,48,-25,1.0,.3);
 doc(sc,st,150,40,150,200,.7,.4,{lines:2});
 const pg=PO(sc,st,225,150,1.0,.3);el("circle",{cx:225,cy:150,r:34,fill:C.ivory,stroke:C.gold,"stroke-width":5},pg);text(pg,"p",225,163,40,600,C.gold,{"text-anchor":"middle"});
 const xx=PO(sc,st,300,226,1.15,.25);el("circle",{cx:300,cy:226,r:22,fill:C.forest},xx);el("path",{d:"M291,217 L309,235 M309,217 L291,235",stroke:C.ivory,"stroke-width":5,"stroke-linecap":"round"},xx);
 evs(sc,.3,"pulse",.4,5);evs(sc,.7,"confirm",.5);evs(sc,1.0,"tick",.5);
}});
// ================================================================ 7 · sensitivity & robustness
PRIN.push({n:7,sz:1.0,w:2.4,ts:1,cap:["Perform sensitivity and","robustness analyses"],build(sc,st){
 const CX=0,CY=-10,RR=190,ang=k=>(-90+72*k)*Math.PI/180,pt=(k,r=RR)=>[CX+r*Math.cos(ang(k)),CY+r*Math.sin(ang(k))];
 // five workflow nodes (mini icons + labels)
 const labs=[["Exclude influential","observations"],["Use alternative","statistical models"],["Change assumptions","regarding missing data"],["Leave one out","analyses"],["Test stability","of results"]];
 const icon=(k,g,x,y)=>{
  if(k==0){[[-22,12],[-8,-6],[8,4],[22,-14]].forEach(([a,b])=>el("circle",{cx:x+a,cy:y+b,r:5,fill:C.gold},g));el("circle",{cx:x+30,cy:y-26,r:7,fill:"none",stroke:C.forest,"stroke-width":3.5},g);el("path",{d:`M${x-30},${y-28} V${y+24} H${x+34}`,fill:"none",stroke:C.forest,"stroke-width":4,"stroke-linecap":"round"},g);}
  if(k==1){el("path",{d:`M${x-34},${y+10} C${x-18},${y-34} ${x-4},${y+30} ${x+10},${y-10} S${x+30},${y-20} ${x+36},${y-8}`,fill:"none",stroke:C.forest,"stroke-width":4.5,"stroke-linecap":"round"},g);el("path",{d:`M${x-34},${y+22} C${x-18},${y-16} ${x-4},${y+36} ${x+10},${y+4} S${x+30},${y-2} ${x+36},${y+8}`,fill:"none",stroke:C.gold,"stroke-width":4.5,"stroke-dasharray":"6 6","stroke-linecap":"round"},g);}
  if(k==2){el("path",{d:`M${x-24},${y-32} H${x+8} L${x+26},${y-14} V${y+32} H${x-24} Z`,fill:C.ivory,stroke:C.forest,"stroke-width":4.5,"stroke-linejoin":"round"},g);text(g,"?",x,y+8,34,700,C.gold,{"text-anchor":"middle"});el("circle",{cx:x+24,cy:y+30,r:13,fill:C.forest},g);el("path",{d:`M${x+17},${y+30} L${x+22},${y+36} L${x+31},${y+24}`,fill:"none",stroke:C.ivory,"stroke-width":3.5,"stroke-linecap":"round"},g);}
  if(k==3){person(g,x-18,y+4,36,C.forest);person(g,x+20,y+4,36,C.forest);el("path",{d:`M${x-9},${y-36} L${x+9},${y-20} M${x+9},${y-36} L${x-9},${y-20}`,stroke:C.gold,"stroke-width":4.5,"stroke-linecap":"round"},g);}
  if(k==4){[-18,0,18].forEach((dy,i)=>{el("line",{x1:x-32,x2:x+32,y1:y+dy,y2:y+dy,stroke:C.forest,"stroke-width":4,"stroke-linecap":"round"},g);el("circle",{cx:x+[-10,14,-18][i],cy:y+dy,r:7,fill:C.gold,stroke:C.forest,"stroke-width":3},g);});}
 };
 labs.forEach((lb,k)=>{const [x,y]=pt(k),g=PO(sc,st,x,y,.35+k*.17,.3);icon(k,g,x,y);
  const right=k==1||k==2,left=k==3||k==4,top=k==0;
  lb.forEach((s,j)=>{const lt=TX(sc,st,s,top?x:right?x+54:x-54,top?y-72+j*28:y-6+j*28+(right||left?0:0),25,500,C.ink,top?"middle":right?"start":"end",.4+k*.17);fitMax(lt,right||left?(k==2?262:240):300);});});
 // circular flow arrows
 [0,1,2,3,4].forEach(k=>{const a0=ang(k)+.30,a1=ang(k+1)-.30,[x0,y0]=[CX+RR*Math.cos(a0),CY+RR*Math.sin(a0)],[x1,y1]=[CX+RR*Math.cos(a1),CY+RR*Math.sin(a1)];
  const d=`M${x0.toFixed(1)},${y0.toFixed(1)} A${RR},${RR} 0 0 1 ${x1.toFixed(1)},${y1.toFixed(1)}`,tg=Math.atan2(Math.cos(a1),-Math.sin(a1))*180/Math.PI;
  const p=arrow(sc,st,d,x1,y1,tg,.55+k*.17,.3,C.gold,3.5);p.setAttribute("stroke-dasharray","1");});
 // central shield with confirmation
 const shp="M0,-62 L48,-44 V6 C48,38 22,58 0,70 C-22,58 -48,38 -48,6 V-44 Z";
 const shf=el("path",{d:shp,fill:C.forest,opacity:0,transform:`translate(${CX},${CY-45})`},st);sc.a.push(u=>shf.setAttribute("opacity",(.14*E.out(P(u,1.5,1.8))).toFixed(3)));
 D(sc,st,"path",{d:shp,stroke:C.gold,"stroke-width":7,transform:`translate(${CX},${CY-45})`},.5,.5);
 ck(sc,st,CX,CY-38,52,1.4,.35,C.forest,10);
 ["SENSITIVITY &","ROBUSTNESS","ANALYSES"].forEach((s,i)=>smallLabel(sc,st,s,CX,CY+68+i*27,22,"middle",.9+i*.08));
 // orbiting marker
 const dot=el("circle",{r:8,fill:C.gold,opacity:0},st);sc.a.push(u=>{const q=P(u,.9,1.5);if(q>0&&q<1){const a=ang(0)+q*Math.PI*2;dot.setAttribute("cx",CX+RR*Math.cos(a));dot.setAttribute("cy",CY+RR*Math.sin(a));dot.setAttribute("opacity",Math.sin(Math.PI*q).toFixed(2));}else dot.setAttribute("opacity",0);});
 evs(sc,.3,"pulse",.4,0);[0,1,2,3,4].forEach(k=>evs(sc,.4+k*.17,"tick",.4));evs(sc,.9,"draw",.5);evs(sc,1.4,"check",.9);
}});
// ================================================================ 8 · missing data
PRIN.push({n:8,sz:1.1,w:2.0,ts:1,cap:["Address missing","data appropriately"],build(sc,st){
 const tx=-220,ty=-260,cw=95,rh=62,cols=4,rows=3;
 D(sc,st,"rect",{x:tx,y:ty,width:cw*cols,height:rh*rows,rx:8,stroke:C.forest,"stroke-width":5},.05,.45);
 for(let r=1;r<rows;r++)D(sc,st,"line",{x1:tx,x2:tx+cw*cols,y1:ty+rh*r,y2:ty+rh*r,stroke:C.forest,"stroke-width":4},.12+r*.04,.3);
 for(let c=1;c<cols;c++)D(sc,st,"line",{x1:tx+cw*c,x2:tx+cw*c,y1:ty,y2:ty+rh*rows,stroke:C.forest,"stroke-width":4},.16+c*.04,.3);
 const miss={"1,0":1,"2,1":1,"0,2":1,"3,2":1};
 for(let r=0;r<rows;r++)for(let c=0;c<cols;c++){const x=tx+cw*(c+.5),y=ty+rh*(r+.5);if(miss[c+","+r]){const g=PO(sc,st,x,y,.4+(r*cols+c)*.04,.25);text(g,"?",x,y+14,40,700,C.gold,{"text-anchor":"middle"});}else D(sc,st,"line",{x1:x-22,x2:x+22,y1:y,y2:y,stroke:C.forest,"stroke-width":5},.3+(r*cols+c)*.03,.2);}
 // magnifier scans the table
 const m=mag(sc,st,66,.6,.3,12),lens=el("circle",{r:56,fill:C.ivory,opacity:.9},m);m.insertBefore(lens,m.firstChild);
 const bars=el("g",{},m);[[-22,14],[-6,26],[10,38]].forEach(([x,h])=>el("rect",{x:x-5,y:20-h,width:12,height:h,fill:C.gold},bars));
 sc.a.push(u=>{const p=E.io(P(u,.6,1.0));at(m,lerp(tx+60,tx+cw*cols-20,p),lerp(ty+rh*1.3,ty+rh*1.0,p)+Math.sin(p*Math.PI)*-18);m.setAttribute("opacity",clamp(P(u,.6,.75)).toFixed(2));});
 // flow: checklist document → organised dataset
 arrow(sc,st,"M-180,-52 C-180,-10 -300,-30 -300,20",-300,34,90,.9,.35);
 doc(sc,st,-370,50,140,170,1.0,.35,{lines:3});
 const cg=PO(sc,st,-300,168,1.15,.25);el("circle",{cx:-300,cy:168,r:26,fill:C.ivory,stroke:C.forest,"stroke-width":4.5},cg);
 ck(sc,st,-300,168,24,1.25,.2,C.forest,6);
 arrow(sc,st,"M-200,135 H-120",-112,135,0,1.2,.25);
 const gx=-70,gy=50,gw=320,gh=170;
 D(sc,st,"rect",{x:gx,y:gy,width:gw,height:gh,rx:8,stroke:C.forest,"stroke-width":5},1.2,.35);
 [1,2,3].forEach(r=>D(sc,st,"line",{x1:gx,x2:gx+gw,y1:gy+gh/4*r,y2:gy+gh/4*r,stroke:C.forest,"stroke-width":4},1.28+r*.03,.2));[1,2].forEach(c=>D(sc,st,"line",{x1:gx+gw/3*c,x2:gx+gw/3*c,y1:gy,y2:gy+gh,stroke:C.forest,"stroke-width":4},1.28+c*.03,.2));
 for(let r=0;r<4;r++)for(let c=0;c<3;c++){const g=G(sc,st,1.4+(r*3+c)*.015,.2,0);el("line",{x1:gx+gw/3*(c+.5)-18,x2:gx+gw/3*(c+.5)+18,y1:gy+gh/4*(r+.5),y2:gy+gh/4*(r+.5),stroke:r==0?C.gold:C.forest,"stroke-width":5,"stroke-linecap":"round"},g);}
 evs(sc,.3,"pulse",.4,3);evs(sc,.7,"draw",.4);evs(sc,1.1,"check",.8);evs(sc,1.3,"soft",.4);
}});
// ================================================================ 9 · multiple testing correction
PRIN.push({n:9,sz:1.0,w:2.0,ts:1,cap:["Correct for multiple","testing when necessary"],build(sc,st){
 const DX=[-300,-110,230];
 DX.forEach((x,i)=>{doc(sc,st,x-52,-292,104,128,.05+i*.1,.35,{lines:2});const g=TX(sc,st,"H",x-6,-226,34,700,C.ink,"middle",.2+i*.1);const sub=el("tspan",{"font-size":22,dy:8},g);sub.textContent=["1","2","n"][i];});
 [50,80,110].forEach((x,i)=>{const d=PO(sc,st,x,-228,.4+i*.06,.2);el("circle",{cx:x,cy:-228,r:6,fill:C.gold},d);});
 // funnel
 const FY=-120,fx=-20,fd=funnelD(fx,FY,520,100,130,56);
 const arrs=DX.map((x,i)=>{const ex=fx+(i-1)*140;return arrow(sc,st,`M${x},-160 C${x},-146 ${ex},-146 ${ex},${FY-6}`,ex,FY-4,90,.5+i*.08,.3,C.gold,3.5);});
 D(sc,st,"path",{d:fd,stroke:C.forest,"stroke-width":5.5},.7,.5);
 TX(sc,st,"MULTIPLE TESTING",fx,FY+36,25,700,C.ink,"middle",1.0,{"letter-spacing":1.2});TX(sc,st,"CORRECTION",fx,FY+68,25,700,C.ink,"middle",1.05,{"letter-spacing":1.2});
 arrow(sc,st,`M${fx},${FY+160} V${FY+196}`,fx,FY+198,90,1.1,.25);
 const bx=fx-175,by=FY+210;D(sc,st,"rect",{x:bx,y:by,width:350,height:62,rx:10,stroke:C.forest,"stroke-width":5},1.2,.35);TX(sc,st,"ADJUSTED P-VALUES",fx,by+41,27,700,C.ink,"middle",1.35,{"letter-spacing":1});
 // outcomes: reduced false positives · control false discoveries
 const lm=G(sc,st,1.3,.3,0);el("circle",{cx:-410,cy:200,r:34,fill:C.ivory,stroke:C.forest,"stroke-width":6},lm);el("line",{x1:-386,y1:224,x2:-362,y2:248,stroke:C.forest,"stroke-width":9,"stroke-linecap":"round"},lm);el("path",{d:"M-424,212 C-418,180 -402,180 -396,212",fill:"none",stroke:C.gold,"stroke-width":4},lm);
 TX(sc,st,"REDUCED",-330,200,26,700,C.forest,"start",1.4,{"letter-spacing":1.2});TX(sc,st,"FALSE POSITIVES",-330,230,26,700,C.forest,"start",1.45,{"letter-spacing":1.2});
 const sc2=G(sc,st,1.45,.3,0);el("path",{d:"M60,175 V245 M30,245 H90 M15,196 H105",stroke:C.forest,"stroke-width":5,"stroke-linecap":"round",fill:"none"},sc2);el("path",{d:"M15,196 L-2,230 H32 Z M105,196 L88,230 H122 Z",fill:C.gold},sc2);
 TX(sc,st,"CONTROL",125,200,25,700,C.forest,"start",1.5,{"letter-spacing":1.2});TX(sc,st,"FALSE DISCOVERIES",125,230,25,700,C.forest,"start",1.55,{"letter-spacing":1.2});
 evs(sc,.3,"pulse",.4,4);evs(sc,.8,"draw",.4);evs(sc,1.2,"tick",.5);evs(sc,1.45,"confirm",.7);
}});
// ================================================================ 10 · meta-analysis
PRIN.push({n:10,sz:1.0,w:2.5,ts:1,cap:["Use meta-analysis when appropriate","to evaluate the consistency of","evidence across studies"],cs:36,build(sc,st){
 const DX=[-290,-60,260],DT=-300,FY=-110;
 DX.forEach((x,i)=>{doc(sc,st,x-52,DT,104,128,.05+i*.12,.4,{lines:0});
  // forest-plot glyph inside each study document
  const g=G(sc,st,.3+i*.12,.3,0);el("line",{x1:x-34,x2:x+34,y1:DT+78,y2:DT+78,stroke:C.forest,"stroke-width":4,"stroke-linecap":"round"},g);el("rect",{x:x-8,y:DT+70,width:16,height:16,fill:C.forest},g);el("line",{x1:x-34,x2:x-34,y1:DT+68,y2:DT+88,stroke:C.forest,"stroke-width":4},g);el("line",{x1:x+34,x2:x+34,y1:DT+68,y2:DT+88,stroke:C.forest,"stroke-width":4},g);
  [DT+46,DT+108].forEach(yy=>el("line",{x1:x-34,x2:x+34,y1:yy,y2:yy,stroke:C.gold,"stroke-width":4,"stroke-linecap":"round"},g));
  smallLabel(sc,st,["STUDY 1","STUDY 2","STUDY n"][i],x,DT-14,26,"middle",.2+i*.12);});
 [0,1].forEach(i=>{const d=PO(sc,st,95+i*34,DT+70,.5+i*.06,.2);el("circle",{cx:95+i*34,cy:DT+70,r:7,fill:C.gold},d);});
 const fx=-15,fd=funnelD(fx,FY,560,110,130,70);
 const arrs=DX.map((x,i)=>{const ex=fx+(i-1)*150,p=arrow(sc,st,`M${x},${DT+142} C${x},${DT+190} ${ex},${FY-70} ${ex},${FY-10}`,ex,FY-4,90,.7+i*.1,.45,C.gold,3.5);run(sc,st,p,1.0+i*.1,.6);return p;});
 D(sc,st,"path",{d:fd,stroke:C.forest,"stroke-width":5.5},.9,.55);
 D(sc,st,"line",{x1:fx-240,x2:fx+240,y1:FY+16,y2:FY+16,stroke:C.gold,"stroke-width":3.5},1.2,.35);
 TX(sc,st,"META-",fx,FY+62,28,700,C.ink,"middle",1.3,{"letter-spacing":2});TX(sc,st,"ANALYSIS",fx,FY+94,28,700,C.ink,"middle",1.35,{"letter-spacing":2});
 const dn=arrow(sc,st,`M${fx},${FY+184} V${FY+222}`,fx,FY+226,90,1.4,.3);
 const bx=fx-215,by=FY+232,bw=430,bh=100;
 D(sc,st,"rect",{x:bx,y:by,width:bw,height:bh,rx:12,stroke:C.forest,"stroke-width":5},1.5,.4);
 TX(sc,st,"OVERALL EFFECT",fx,by+30,23,700,C.ink,"middle",1.7,{"letter-spacing":2});
 const py=by+64;D(sc,st,"line",{x1:fx-150,x2:fx+150,y1:py,y2:py,stroke:C.forest,"stroke-width":4.5},1.7,.35);D(sc,st,"line",{x1:fx,x2:fx,y1:by+40,y2:by+bh-8,stroke:C.forest,"stroke-width":3.5,"stroke-dasharray":"6 6"},1.65,.3).removeAttribute("pathLength");
 const dm=PO(sc,st,fx,py,1.85,.3);el("path",{d:`M${fx-48},${py} L${fx},${py-20} L${fx+48},${py} L${fx},${py+20} Z`,fill:C.gold,stroke:C.forest,"stroke-width":3.5,"stroke-linejoin":"round"},dm);
 TX(sc,st,"MORE PRECISE ESTIMATE",fx,by+bh+36,24,700,C.forest,"middle",2.0,{"letter-spacing":1.5});
 evs(sc,.3,"pulse",.4,0);evs(sc,.7,"draw",.4);evs(sc,1.0,"pulse",.5,1);evs(sc,1.5,"draw",.4);evs(sc,1.85,"confirm",.8);evs(sc,1.95,"chime",.6,2);
}});
