// ================================================================ 11 · risk of bias & methodological quality
PRIN.push({n:11,sz:1.06,w:1.6,ts:1.1,cap:["Assess the risk of bias","and methodological quality"],build(sc,st){
 [[-440,-250],[-256,-250],[-440,-106],[-256,-106],[-440,38],[-256,38]].forEach(([x,y],i)=>{
  D(sc,st,"rect",{x,y,width:172,height:134,rx:12,stroke:C.forest,"stroke-width":5},.05+i*.05,.35);
  const g=PO(sc,st,x+86,y+67,.2+i*.05,.25);person(g,x+86,y+66,64,i%2?C.gold:C.forest);
  const d=PO(sc,st,x+148,y+24,.45+i*.05,.2);el("circle",{cx:x+148,cy:y+24,r:11,fill:i%3==1?C.gold:C.forest},d);});
 doc(sc,st,20,-280,370,440,.15,.5,{lines:0});
 for(let i=0;i<5;i++){const y=-190+i*70,t0=.35+i*.08;D(sc,st,"rect",{x:56,y:y-17,width:34,height:34,rx:6,stroke:C.forest,"stroke-width":4},t0,.2);D(sc,st,"line",{x1:112,x2:112+(i%2?150:200),y1:y,y2:y,stroke:C.gold,"stroke-width":5},t0+.05,.25);}
 const m=mag(sc,st,82,.5,.35,13),lens=el("circle",{r:72,fill:C.ivory,opacity:.9},m);m.insertBefore(lens,m.firstChild);
 sc.a.push(u=>{const p=E.io(P(u,.5,1.1)),q=P(u,.5,1.1);at(m,lerp(130,230,p*p),lerp(-190,150,p));m.setAttribute("opacity",clamp(P(u,.5,.65)).toFixed(2));});
 for(let i=0;i<5;i++){const y=-190+i*70,t0=.62+i*.11;const g=PO(sc,st,330,y,t0,.2);el("circle",{cx:330,cy:y,r:17,fill:i%2?C.gold:C.forest},g);if(i%2==0)el("path",{d:`M322,${y} L328,${y+7} L339,${y-8}`,fill:"none",stroke:C.ivory,"stroke-width":4,"stroke-linecap":"round","stroke-linejoin":"round"},g);evs(sc,t0,"tick",.35);}
 evs(sc,.3,"pulse",.4,2);evs(sc,1.15,"check",.8);
}});
// ================================================================ 12 · independent check
PRIN.push({n:12,sz:1.0,w:1.6,ts:1.2,cap:["Have the analysis","independently checked"],build(sc,st){
 D(sc,st,"rect",{x:-225,y:-280,width:450,height:350,rx:20,stroke:C.forest,"stroke-width":11},.05,.5);
 D(sc,st,"path",{d:"M0,70 V125 M-90,127 H90",stroke:C.gold,"stroke-width":11},.25,.3);
 [30,62,48,88].forEach((h,i)=>{const g=el("g",{},st),r=el("rect",{x:-190+i*30,y:20,width:20,height:0,fill:C.forest},g);sc.a.push(u=>{const p=E.out(P(u,.3+i*.05,.6+i*.05));r.setAttribute("height",(h*p).toFixed(1));r.setAttribute("y",(20-h*p).toFixed(1));});});
 D(sc,st,"path",{d:"M-60,-60 L-20,-110 L20,-80 L70,-150 L120,-120 L170,-170",stroke:C.gold,"stroke-width":6},.4,.45);
 D(sc,st,"path",{d:"M-190,-120 L-190,-230 M-190,-120 H-70 M-120,-150 V-230",stroke:C.forest,"stroke-width":4},.45,.3);
 const pie=PO(sc,st,95,-30,.5);el("circle",{cx:95,cy:-30,r:42,fill:C.forest},pie);el("path",{d:"M95,-30 V-72 A42,42 0 0 1 130,-6 Z",fill:C.gold},pie);
 // two reviewers (geometric silhouettes) on either side, each gazing at the same dashboard
 [[-380,1],[380,-1]].forEach(([x,s],i)=>{const g=PO(sc,st,x,110,.15+i*.12,.35);person(g,x,110,150,i?C.gold:C.forest);
  const mg=mag(sc,st,38,.6+i*.1,.3,8);at(mg,x*.62,-40+i*20);});
 // two confirmations
 [[-110,.95],[110,1.15]].forEach(([x,t0],i)=>{const g=PO(sc,st,x,200,t0,.25);el("circle",{cx:x,cy:200,r:36,fill:C.ivory,stroke:i?C.gold:C.forest,"stroke-width":6},g);ck(sc,st,x,203,36,t0+.1,.22,i?C.gold:C.forest,8);evs(sc,t0+.1,"check",.7);});
 D(sc,st,"line",{x1:-62,x2:62,y1:200,y2:200,stroke:C.gold,"stroke-width":4,"stroke-dasharray":"2 9"},1.1,.25).removeAttribute("pathLength");
 evs(sc,.3,"pulse",.4,3);
}});
// ================================================================ 13 · reproducibility
PRIN.push({n:13,sz:1.0,w:1.6,ts:1.1,cap:["Ensure reproducibility","of the analysis"],build(sc,st){
 const loop="M-300,-170 H260 A150,150 0 0 1 260,130 H-300 A150,150 0 0 1 -300,-170 Z";
 const lp=D(sc,st,"path",{d:loop,stroke:C.forest,"stroke-width":9},.05,.8);
 head(st,100,-170,0,C.forest,1.6,9).setAttribute("opacity",0);
 const h1=head(st,60,-170,0,C.forest,1.8,9),h2=head(st,-120,130,180,C.forest,1.8,9);[h1,h2].forEach((h,i)=>sc.a.push(u=>h.setAttribute("opacity",P(u,.7,.9).toFixed(2))));
 // dataset → code → check
 [[0,0],[14,-12],[28,-24]].forEach(([dx,dy],i)=>doc(sc,st,-370+dx,-60+dy,84,104,.2+i*.07,.3,{lines:2,sw:4}));
 [[-440,-125],[-415,-140]].forEach(([x,y],i)=>{const g=PO(sc,st,x+70,y+130,.35+i*.05,.2);el("circle",{cx:x+70,cy:y+130,r:7,fill:C.gold},g);});
 arrow(sc,st,"M-270,-10 H-190",-182,-10,0,.5,.25);
 D(sc,st,"rect",{x:-170,y:-100,width:200,height:150,rx:16,stroke:C.forest,"stroke-width":6},.45,.35);
 const cd=G(sc,st,.65,.3,0);text(cd,"{code}",-70,-34,36,600,C.ink,{"text-anchor":"middle"});text(cd,"f(x)",-70,22,42,500,C.gold,{"text-anchor":"middle","font-style":"italic"});
 arrow(sc,st,"M50,-25 H110",118,-25,0,.8,.25);
 D(sc,st,"rect",{x:130,y:-70,width:80,height:90,rx:12,stroke:C.forest,"stroke-width":6},.85,.3);ck(sc,st,170,-26,42,1.0,.25,C.forest,9);
 smallLabel(sc,st,"DATASET",-325,92,22,"middle",.6);smallLabel(sc,st,"ANALYSIS SCRIPTS",-70,92,22,"middle",.75);smallLabel(sc,st,"VALIDATION",170,92,22,"middle",1.0);
 TX(sc,st,"REPRODUCIBILITY",-20,215,40,700,C.ink,"middle",.9,{"letter-spacing":3});
 run(sc,st,lp,1.0,.5,C.gold,9);
 evs(sc,.3,"pulse",.4,5);evs(sc,.8,"tick",.5);evs(sc,1.0,"check",.8);
}});
// ================================================================ 14 · compare with previous evidence
PRIN.push({n:14,sz:1.06,w:1.6,ts:1.25,cap:["Compare the findings","with previous evidence"],build(sc,st){
 [[-420,"PREVIOUS EVIDENCE",-200],[40,"NEW FINDINGS",200]].forEach(([x,lab,dx],i)=>{
  const g=G(sc,st,.05+i*.1,.45,0,dx);const col=i?C.gold:C.forest;
  el("rect",{x,y:-290,width:380,height:460,rx:16,fill:C.ivory,stroke:C.forest,"stroke-width":5},g);el("rect",{x,y:-290,width:380,height:52,rx:12,fill:C.forest},g);
  const t=text(g,lab,x+190,-251,26,700,C.ivory,{"text-anchor":"middle","letter-spacing":1.8});fitMax(t,340);
  // bar chart + trend line, drawn identically so they visibly align
  [60,100,80,130].forEach((h,k)=>el("rect",{x:x+40+k*52,y:-30-h,width:34,height:h,fill:i?C.gold:C.forest,opacity:.95},g));
  el("path",{d:`M${x+40},-130 L${x+120},-175 L${x+200},-150 L${x+330},-205`,fill:"none",stroke:col,"stroke-width":5,"stroke-linecap":"round","stroke-linejoin":"round"},g);
  [0,1,2,3].forEach(k=>el("circle",{cx:x+[40,120,200,330][k],cy:[-130,-175,-150,-205][k],r:6,fill:col},g));
  el("line",{x1:x+30,x2:x+350,y1:-24,y2:-24,stroke:C.forest,"stroke-width":4},g);
  [0,1,2].forEach(k=>el("line",{x1:x+40,x2:x+40+(k==2?140:300),y1:30+k*34,y2:30+k*34,stroke:C.gold,"stroke-width":4,"stroke-linecap":"round",opacity:.9},g));});
 // alignment guide + magnifier comparing both charts
 D(sc,st,"line",{x1:-440,x2:440,y1:-90,y2:-90,stroke:C.gold,"stroke-width":3.5,"stroke-dasharray":"2 9"},.6,.35).removeAttribute("pathLength");
 const m=mag(sc,st,86,.65,.4,14),lens=el("circle",{r:74,fill:C.ivory,opacity:0},m);m.insertBefore(lens,m.firstChild);
 sc.a.push(u=>{const p=E.out(P(u,.65,1.0));at(m,lerp(-60,0,p),-90);lens.setAttribute("opacity",(.55*P(u,.9,1.05)).toFixed(2));});
 const eq=el("g",{opacity:0},m);el("path",{d:"M-24,-12 H24 M-24,12 H24",stroke:C.forest,"stroke-width":7,"stroke-linecap":"round"},eq);sc.a.push(u=>eq.setAttribute("opacity",P(u,.95,1.1).toFixed(2)));
 // arrow back to the previous evidence
 arrow(sc,st,"M230,196 C230,296 -230,296 -230,206",-230,200,-90,1.05,.4,C.gold,5);
 evs(sc,.3,"pulse",.4,1);evs(sc,.75,"tick",.5);evs(sc,1.05,"confirm",.7);
}});
// ================================================================ 15 · selective reporting & data-driven conclusions
PRIN.push({n:15,sz:1.06,w:1.7,ts:1.3,cap:["Avoid selective reporting","and data-driven conclusions"],build(sc,st){
 [[-430,-150],[-390,-110],[-350,-70]].forEach(([x,y],i)=>doc(sc,st,x,y,140,180,.05+i*.08,.35,{lines:i==2?0:3,sw:5}));
 const gl=G(sc,st,.4,.3,0);el("path",{d:"M-335,-10 L-300,-40 L-270,-20 L-235,-60",fill:"none",stroke:C.gold,"stroke-width":5,"stroke-linecap":"round","stroke-linejoin":"round"},gl);[[-30,-60],[-22,-8]].forEach(()=>{});[[-335,-10],[-300,-40],[-270,-20],[-235,-60]].forEach(([x,y])=>el("circle",{cx:x,cy:y,r:5,fill:C.gold},gl));[0,1,2].forEach(k=>el("rect",{x:-335+k*26,y:30-[24,40,30][k],width:16,height:[24,40,30][k],fill:C.forest},gl));
 const m=mag(sc,st,82,.4,.35,13),lens=el("circle",{r:72,fill:C.ivory,opacity:.35},m);m.insertBefore(lens,m.firstChild);
 sc.a.push(u=>{const p=E.io(P(u,.45,1.0));at(m,lerp(-210,-300,p),lerp(-120,-60,p));});
 smallLabel(sc,st,"EXPLORATORY",-340,150,27,"middle",.7);smallLabel(sc,st,"DATA MINING",-340,184,27,"middle",.76);
 // question mark → arrow → post-hoc analysis checklist
 const q=PO(sc,st,115,-120,.5,.35);text(q,"?",115,-65,170,300,C.gold,{"text-anchor":"middle"});
 arrow(sc,st,"M-165,-30 H250 V12",250,18,90,.75,.45,C.gold,5);
 doc(sc,st,170,20,160,150,1.0,.4,{lines:3,sw:5});
 const cg=PO(sc,st,310,168,1.15,.25);el("circle",{cx:310,cy:168,r:28,fill:C.ivory,stroke:C.forest,"stroke-width":5},cg);ck(sc,st,310,170,26,1.25,.2,C.forest,7);
 smallLabel(sc,st,"POST-HOC",250,232,27,"middle",1.05);smallLabel(sc,st,"ANALYSIS",250,264,27,"middle",1.1);
 evs(sc,.3,"pulse",.4,0);evs(sc,.8,"draw",.5);evs(sc,1.25,"check",.9);
}});
