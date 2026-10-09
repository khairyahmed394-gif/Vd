// ================================================================ 1 · data quality
PRIN.push({n:1,sz:1.12,w:1.8,ts:1.1,cap:["Ensure high-quality","and accurate data."],build(sc,st){
 const X0=-250,HH=56,RH=63,CW=115;
 // flagged inputs (left) – dotted links into the table
 [["×",-150],["!",-60],["?",30]].forEach(([s,y],i)=>{const t0=.12+i*.1,g=PO(sc,st,-405,y,t0);el("circle",{cx:-405,cy:y,r:30,fill:C.ivory,stroke:C.gold,"stroke-width":4},g);text(g,s,-405,y+13,38,600,C.gold,{"text-anchor":"middle"});
  D(sc,st,"line",{x1:-370,x2:-300,y1:y,y2:y,stroke:C.gold,"stroke-width":3.5,"stroke-dasharray":"2 9"},t0+.1,.3).removeAttribute("pathLength");});
 // table
 const hdr=G(sc,st,.1,.35,0);el("rect",{x:X0,y:-250,width:CW*4,height:HH,rx:6,fill:C.forest},hdr);
 D(sc,st,"rect",{x:X0,y:-250,width:CW*4,height:HH+RH*4,rx:6,stroke:C.forest,"stroke-width":5},.05,.5);
 for(let r=0;r<4;r++)D(sc,st,"line",{x1:X0,x2:X0+CW*4,y1:-250+HH+RH*r,y2:-250+HH+RH*r,stroke:C.forest,"stroke-width":4},.15+r*.04,.3);
 for(let c=1;c<4;c++)D(sc,st,"line",{x1:X0+CW*c,x2:X0+CW*c,y1:-250,y2:-250+HH+RH*4,stroke:C.forest,"stroke-width":4},.2+c*.04,.3);
 // data points fly into the cells
 const cell=(c,r)=>[X0+CW*(c+.5),-250+HH+RH*(r+.5)],fl={"1,1":"?","2,2":"!"},seeds=[[-440,-230],[-300,210],[360,-120],[330,210],[-120,240],[120,-290],[-380,60],[300,-260],[0,280],[400,40],[-200,-300],[200,240],[-60,-310],[440,-200]];
 let k=0;for(let r=0;r<4;r++)for(let c=0;c<4;c++){const key=c+","+r,[cx,cy]=cell(c,r);if(fl[key])continue;const s=seeds[k%seeds.length],t0=.25+k*.035,col=k%3==0?C.gold:C.forest;k++;
  const d=el("circle",{r:9,fill:col},st);sc.a.push(u=>{const p=E.io(P(u,t0,t0+.45));d.setAttribute("cx",lerp(s[0],cx,p).toFixed(1));d.setAttribute("cy",lerp(s[1],cy,p).toFixed(1));d.setAttribute("opacity",clamp(P(u,t0,t0+.1)).toFixed(2));d.setAttribute("r",lerp(9,6,p).toFixed(1));});}
 Object.keys(fl).forEach((key,i)=>{const [c,r]=key.split(",").map(Number),[cx,cy]=cell(c,r),g=PO(sc,st,cx,cy,.7+i*.1);text(g,fl[key],cx,cy+14,40,700,C.gold,{"text-anchor":"middle"});});
 // magnifier with the green check
 const m=mag(sc,st,80,.85,.4,13),lens=el("circle",{r:70,fill:C.ivory,opacity:0},m);m.insertBefore(lens,m.firstChild);
 sc.a.push(u=>{at(m,lerp(300,235,E.out(P(u,.85,1.2))),lerp(40,150,E.out(P(u,.85,1.2))));lens.setAttribute("opacity",(.92*P(u,.9,1.1)).toFixed(2));});
 const c1=el("g",{},m);ck(sc,c1,0,2,64,1.1,.3,C.forest,12);
 [[-310,-250,14],[-338,-214,9]].forEach(([x,y,r],i)=>{const s=star(st,430-i*30,-90+i*40,r+6);sc.a.push(u=>s.setAttribute("opacity",P(u,1.2+i*.1,1.4+i*.1).toFixed(2)));});
 evs(sc,.25,"pulse",.4,0);evs(sc,.7,"tick",.5);evs(sc,1.1,"check",.9);
}});
// ================================================================ 2 · study design & sample size
PRIN.push({n:2,sz:1.18,w:1.7,ts:1.0,cap:["Use an appropriate","study design and","adequate sample size"],build(sc,st){
 D(sc,st,"rect",{x:-330,y:-270,width:310,height:320,rx:18,stroke:C.forest,"stroke-width":6},.05,.5);
 const tab=G(sc,st,.2,.3,-6);el("rect",{x:-235,y:-296,width:120,height:40,rx:12,fill:C.forest},tab);
 // pie + lines
 const pie=PO(sc,st,-255,-170,.3);el("circle",{cx:-255,cy:-170,r:38,fill:"none",stroke:C.forest,"stroke-width":5},pie);el("path",{d:"M-255,-170 V-208 A38,38 0 0 1 -219,-158 Z",fill:C.gold},pie);
 [-190,-160].forEach((y,i)=>D(sc,st,"line",{x1:-190,x2:-190+(i?90:140),y1:y,y2:y,stroke:i?C.gold:C.forest,"stroke-width":5},.4+i*.06,.25));
 [-100,-50,0].forEach((y,i)=>{ck(sc,st,-290,y,28,.5+i*.12,.2,C.forest,6);D(sc,st,"line",{x1:-250,x2:-60,y1:y,y2:y,stroke:C.gold,"stroke-width":5},.52+i*.12,.25);});
 // calculator
 D(sc,st,"rect",{x:30,y:-170,width:170,height:220,rx:16,stroke:C.gold,"stroke-width":6},.35,.4);
 const scr=G(sc,st,.55,.25,0);el("rect",{x:48,y:-152,width:134,height:44,rx:7,fill:C.gold},scr);
 for(let r=0;r<3;r++)for(let c=0;c<3;c++){const g=PO(sc,st,66+c*48,-72+r*40,.6+(r*3+c)*.025,.2);el("circle",{cx:66+c*48,cy:-72+r*40,r:9,fill:C.gold},g);}
 // participants
 [[-300,60,C.gold],[-150,76,C.forest],[0,120,C.forest],[150,76,C.forest],[300,60,C.gold]].forEach(([x,k,c],i)=>{const g=PO(sc,st,x,170,.7+Math.abs(i-2)*-.0+i*.07,.3);person(g,x,170,k,c);});
 evs(sc,.3,"pulse",.4,1);evs(sc,.7,"tick",.5);evs(sc,.78,"tick",.5);evs(sc,.9,"soft",.5);
}});
// ================================================================ 3 · appropriate statistical analysis
PRIN.push({n:3,sz:1.12,w:1.7,ts:1.1,cap:["Use the appropriate","statistical analysis."],build(sc,st){
 D(sc,st,"rect",{x:-340,y:-270,width:470,height:340,rx:22,stroke:C.forest,"stroke-width":12},.05,.55);
 D(sc,st,"path",{d:"M-110,70 V140 M-200,142 H-20",stroke:C.gold,"stroke-width":12},.3,.35);
 // bar chart
 [40,75,55,100].forEach((h,i)=>{const g=el("g",{},st);const r=el("rect",{x:-310+i*34,y:-100,width:22,height:0,fill:C.forest},g);sc.a.push(u=>{const p=E.out(P(u,.3+i*.06,.6+i*.06));r.setAttribute("height",(h*p).toFixed(1));r.setAttribute("y",(-100-h*p).toFixed(1));});});
 // line chart
 const lc=D(sc,st,"path",{d:"M-130,-130 L-85,-175 L-45,-148 L5,-205 L55,-180 L95,-225",stroke:C.gold,"stroke-width":6},.4,.5);
 [[-130,-130],[-85,-175],[-45,-148],[5,-205],[55,-180],[95,-225]].forEach(([x,y],i)=>{const g=PO(sc,st,x,y,.5+i*.07,.2);el("circle",{cx:x,cy:y,r:7,fill:C.gold},g);});
 // scatter + fit
 [[-300,-10],[-270,-30],[-250,0],[-225,-45],[-200,-25],[-175,-60],[-150,-40],[-130,-78]].forEach(([x,y],i)=>{const g=PO(sc,st,x,y+20,.5+i*.04,.2);el("circle",{cx:x,cy:y+20,r:6,fill:C.gold},g);});
 D(sc,st,"line",{x1:-305,x2:-120,y1:30,y2:-50,stroke:C.forest,"stroke-width":4},.8,.3);
 // pie
 const pie=PO(sc,st,10,0,.55);el("circle",{cx:10,cy:0,r:44,fill:C.forest},pie);el("path",{d:"M10,0 V-44 A44,44 0 0 1 48,22 Z",fill:C.gold},pie);
 // magnifier sweeps across and lands on Σ
 const m=mag(sc,st,98,.5,.4,15),lens=el("circle",{r:84,fill:C.ivory,opacity:0},m);m.insertBefore(lens,m.firstChild);
 const sg=el("g",{opacity:0},m);text(sg,"Σ",0,38,120,500,C.gold,{"text-anchor":"middle"});
 sc.a.push(u=>{const p=E.io(P(u,.6,1.15));at(m,lerp(-250,175,p),lerp(-120,-10,p)+Math.sin(p*Math.PI)*-20);const q=P(u,1.1,1.35);lens.setAttribute("opacity",(.94*q).toFixed(2));sg.setAttribute("opacity",q.toFixed(2));});
 evs(sc,.3,"pulse",.4,2);evs(sc,.6,"draw",.5);evs(sc,1.15,"check",.7);
}});
// ================================================================ 4 · test the assumptions
PRIN.push({n:4,sz:1.1,w:2.0,ts:1.2,cap:["Test the assumptions of","the statistical methods"],build(sc,st){
 const cx=-70,cy=-10,r=232;
 const cp=el("clipPath",{id:"c4"},defs);el("circle",{cx,cy,r:r-10},cp);
 D(sc,st,"circle",{cx,cy,r,stroke:C.forest,"stroke-width":18},.05,.55);
 D(sc,st,"line",{x1:cx-232*.72,y1:cy+232*.72,x2:cx-232*1.2,y2:cy+232*1.2,stroke:C.forest,"stroke-width":26},.35,.3);
 const inn=el("g",{"clip-path":"url(#c4)"},st);
 D(sc,inn,"line",{x1:cx,x2:cx,y1:cy-r,y2:cy+r,stroke:C.forest,"stroke-width":3.5},.3,.35);D(sc,inn,"line",{x1:cx-r,x2:cx+r,y1:cy,y2:cy,stroke:C.forest,"stroke-width":3.5},.33,.35);
 // top-left: distribution curve
 D(sc,inn,"path",{d:"M-250,-52 C-205,-52 -195,-190 -160,-190 C-125,-190 -115,-52 -75,-52",stroke:C.gold,"stroke-width":6},.45,.4);
 [-215,-190,-165,-140,-115,-90].forEach((x,i)=>{const h=[16,44,70,56,30,12][i],g=el("g",{},inn),rc=el("rect",{x,y:-52,width:20,height:0,fill:C.forest},g);sc.a.push(u=>{const p=E.out(P(u,.5+i*.04,.8+i*.04));rc.setAttribute("height",(h*p).toFixed(1));rc.setAttribute("y",(-52-h*p).toFixed(1));});});
 // top-right: bars with error indicators
 [[-20,50],[20,80],[60,62],[100,95]].forEach(([x,h],i)=>{const g=el("g",{},inn),rc=el("rect",{x,y:-52,width:26,height:0,fill:C.forest},g);sc.a.push(u=>{const p=E.out(P(u,.55+i*.05,.85+i*.05));rc.setAttribute("height",(h*p).toFixed(1));rc.setAttribute("y",(-52-h*p).toFixed(1));});
  D(sc,inn,"path",{d:`M${x+13},${-52-h-16} V${-52-h+14} M${x+3},${-52-h-16} H${x+23} M${x+3},${-52-h+14} H${x+23}`,stroke:C.gold,"stroke-width":4},.8+i*.04,.25);});
 // bottom-left: scatter + fit
 [[-235,130],[-210,100],[-195,125],[-170,85],[-150,100],[-130,60],[-110,78],[-95,40]].forEach(([x,y],i)=>{const g=PO(sc,inn,x,y,.6+i*.04,.2);el("circle",{cx:x,cy:y,r:6,fill:C.gold},g);});
 D(sc,inn,"line",{x1:-245,x2:-90,y1:140,y2:38,stroke:C.forest,"stroke-width":4},.9,.3);
 // bottom-right: relationship diagram
 const nodes=[[10,50],[90,50],[10,125],[90,125],[50,88]];
 [[0,4],[1,4],[2,4],[3,4],[0,1],[2,3]].forEach(([a,b],i)=>D(sc,inn,"line",{x1:nodes[a][0],y1:nodes[a][1],x2:nodes[b][0],y2:nodes[b][1],stroke:C.gold,"stroke-width":3.5},.7+i*.05,.25));
 nodes.forEach(([x,y],i)=>{const g=PO(sc,inn,x,y,.65+i*.05,.2);el("circle",{cx:x,cy:y,r:i==4?13:9,fill:i==4?C.forest:C.ivory,stroke:C.forest,"stroke-width":4},g);});
 // clipboard with three sequential checks
 D(sc,st,"rect",{x:195,y:-30,width:215,height:285,rx:16,stroke:C.forest,"stroke-width":6},.7,.4);
 const tab=G(sc,st,.8,.25,-5);el("rect",{x:270,y:-52,width:65,height:34,rx:10,fill:C.forest},tab);
 [0,1,2].forEach(i=>{const y=40+i*66,t0=1.0+i*.16;D(sc,st,"rect",{x:222,y:y-16,width:34,height:34,rx:6,stroke:C.forest,"stroke-width":4},t0-.15,.2);ck(sc,st,239,y+2,22,t0,.2,C.forest,6);D(sc,st,"line",{x1:276,x2:386,y1:y,y2:y,stroke:C.gold,"stroke-width":5},t0,.25);evs(sc,t0,"check",.65);});
 evs(sc,.3,"pulse",.4,3);evs(sc,.6,"draw",.5);
}});
// ================================================================ 5 · confounding factors
PRIN.push({n:5,sz:1.0,w:1.9,ts:1.35,cap:["Control for potential","confounding factors"],build(sc,st){
 const nodes=[[-290,-170],[-390,10],[-190,10]];
 // scattered participants
 [[-440,-200],[-410,-130],[-190,-210],[-130,-150],[-110,-60],[-470,-40],[-300,100],[-210,110],[-420,110],[-120,60],[-330,-250]].forEach(([x,y],i)=>{const g=PO(sc,st,x,y,.05+i*.025,.25);el("circle",{cx:x,cy:y,r:i%3==0?10:8,fill:i%3==0?C.forest:C.ivory,stroke:C.gold,"stroke-width":3.5},g);});
 const lk=[[0,1],[0,2],[1,2]].map(([a,b],i)=>D(sc,st,"line",{x1:nodes[a][0],y1:nodes[a][1],x2:nodes[b][0],y2:nodes[b][1],stroke:C.gold,"stroke-width":3.5,"stroke-dasharray":"7 8"},.25+i*.06,.3));lk.forEach(l=>l.removeAttribute("pathLength"));
 nodes.forEach(([x,y],i)=>{const g=PO(sc,st,x,y,.2+i*.07,.28);el("circle",{cx:x,cy:y,r:36,fill:C.forest},g);person(g,x,y+4,40,C.ivory);});
 // funnel with sliders
 const fp=D(sc,st,"path",{d:funnelD(-20,-70,150,70,34,70),stroke:C.forest,"stroke-width":5.5,fill:"none"},.5,.45);
 [[-55,-40,.0],[-20,-20,.4]].forEach(([x,y,f],i)=>{const g=G(sc,st,.75+i*.1,.25,0);el("line",{x1:x-34,x2:x+34,y1:y,y2:y,stroke:C.forest,"stroke-width":4,"stroke-linecap":"round"},g);el("circle",{cx:x-8+f*30,cy:y,r:8,fill:C.gold,stroke:C.forest,"stroke-width":3},g);});
 arrow(sc,st,"M-120,-30 H-92",-86,-30,0,.4,.25);
 arrow(sc,st,"M30,-10 H88",96,-10,0,.9,.3);
 // validated output
 [-170,-105,-40].forEach((y,i)=>{const g=G(sc,st,1.0+i*.08,.3,0,16);el("rect",{x:110,y,width:330,height:52,rx:9,fill:C.ivory,stroke:C.forest,"stroke-width":4},g);person(g,138,y+30,28,C.forest);el("circle",{cx:175,cy:y+26,r:14,fill:"none",stroke:C.gold,"stroke-width":3.5},g);el("line",{x1:200,x2:410,y1:y+26,y2:y+26,stroke:C.gold,"stroke-width":4,"stroke-linecap":"round"},g);});
 D(sc,st,"rect",{x:110,y:30,width:330,height:200,rx:9,stroke:C.forest,"stroke-width":4},1.15,.35);
 D(sc,st,"path",{d:"M135,200 V70 M135,200 H420",stroke:C.forest,"stroke-width":4},1.25,.3);
 D(sc,st,"line",{x1:150,x2:400,y1:180,y2:90,stroke:C.gold,"stroke-width":5},1.35,.3);
 [[165,160],[200,170],[230,130],[270,140],[310,115],[355,100],[385,112]].forEach(([x,y],i)=>{const g=PO(sc,st,x,y,1.35+i*.03,.2);el("circle",{cx:x,cy:y,r:5,fill:C.gold},g);});
 const sh=PO(sc,st,410,210,1.45,.3);el("path",{d:"M410,170 L445,184 V214 C445,238 428,250 410,260 C392,250 375,238 375,214 V184 Z",fill:C.forest,stroke:C.ivory,"stroke-width":5},sh);
 ck(sc,st,410,214,30,1.55,.25,C.ivory,7);
 evs(sc,.3,"pulse",.4,4);evs(sc,.9,"draw",.4);evs(sc,1.5,"check",.8);
}});
