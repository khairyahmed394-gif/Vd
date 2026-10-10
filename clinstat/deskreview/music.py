"""Original ambient score + sound design for 'The Desk Review' (30 s). Pure numpy, no samples, no voice."""
import numpy as np, json, wave
SR=44100; D=30.0; N=int(SR*D); t=np.arange(N)/SR; rs=np.random.RandomState(7)
mid=lambda m:440.0*2**((m-69)/12)
def ss(x): x=np.clip(x,0,1); return x*x*(3-2*x)
# harmony: tense minor through the gates, hard drop at the stamp, lift to major after the review
CH=[(0,3.4,[33,45,52,57,60,64]),(3.4,5.6,[31,43,50,55,59,62]),(5.6,9.1,[38,45,50,53,57,62]),(9.1,12.6,[34,46,50,53,57,62]),(12.6,15.9,[31,43,46,50,55,58]),
    (15.9,18.3,[33,45,52,55,58,61]),(18.3,23.0,[29,41,48,53,57,60]),(23.0,25.3,[24,36,48,52,55,59]),(25.3,31,[29,41,48,53,57,60,64,67])]
L=np.zeros(N); R=np.zeros(N)
for ci,(a,b,notes) in enumerate(CH):
    fi=ss((t-(a-.9 if ci else -1.0))/(1.8 if ci else 1.6)); fo=1-ss((t-(b-.9))/1.8) if ci<len(CH)-1 else 1.0
    env=fi*fo
    for k,m in enumerate(notes):
        f=mid(m)
        for side,det,arr in ((0,-2.5,L),(1,2.5,R)):
            ff=f*2**(det/1200); lfo=1+.12*np.sin(2*np.pi*(.07+.013*k)*t+k+side)
            w=sum(amp*np.sin(2*np.pi*ff*h*t+k*1.3+h) for h,amp in ((1,1),(2,.28),(3,.1),(4,.04)))
            amp=.034 if k else .085/ (1 if m<40 else 1.6)
            arr+=env*lfo*w*amp*(1 if m>=40 else 1.0)
# soft pluck, sparse
step=.3; PL=np.zeros(N); PR=np.zeros(N); pat=[0,2,4,2,3,1,4,2]
for i in range(int(3.6/step),int(D/step)-2):
    tt=i*step
    if 15.7<tt<17.0: continue
    if rs.rand()<.42 or (i%4==0 and rs.rand()<.5): continue
    ch=next(c for c in CH if c[0]<=tt<c[1]); m=ch[2][1+pat[i%len(pat)]%(len(ch[2])-1)]+24
    n=int(1.6*SR); k=np.arange(n)/SR; f=mid(m)
    x=(np.sin(2*np.pi*f*k)+.35*np.sin(2*np.pi*f*2.01*k)+.12*np.sin(2*np.pi*f*4.1*k))*np.exp(-k*3.2)*np.minimum(k/.004,1)*.05
    s=int(tt*SR); pan=.5+.35*np.sin(i*1.7)
    for dly,g in ((0,1),(.45,.3),(.9,.12)):
        o=s+int(dly*SR); e=min(N,o+n)
        if o<N: PL[o:e]+=x[:e-o]*g*(1-pan); PR[o:e]+=x[:e-o]*g*pan
L+=PL*1.3; R+=PR*1.3
def reverb(sl,sr,wet):
    n=int(2.8*SR); k=np.arange(n)/SR; irs=[]
    for _ in range(2):
        ir=rs.randn(n)*np.exp(-k*6.9/2.8); ir=np.convolve(ir,np.ones(6)/6,"same"); ir[:int(.012*SR)]*=np.linspace(0,1,int(.012*SR)); irs.append(ir/np.sqrt((ir**2).sum()))
    m=1<<int(np.ceil(np.log2(N+n))); F=lambda x:np.fft.rfft(x,m)
    return [np.fft.irfft(F(s)*F(ir),m)[:N]*wet for s,ir in ((sl,irs[0]),(sr,irs[1]))]
rl,rr=reverb(L,R,.55); L=L*.75+rl; R=R*.75+rr
# music ducks for the beat before the rejection stamp, then returns
duck=1-.7*ss((t-15.55)/.3)*(1-ss((t-16.05)/1.6)); L*=duck; R*=duck
# sound design
SL=np.zeros(N); SRr=np.zeros(N)
def put(x,at,vol,pan=.5):
    s=int(at*SR)
    if s<0: x=x[-s:]; s=0
    e=min(N,s+len(x))
    if s<N and e>s: SL[s:e]+=x[:e-s]*vol*(1-pan)*1.4; SRr[s:e]+=x[:e-s]*vol*pan*1.4
def tone(f,d,dec,amp=1,parts=((1,1),)):
    k=np.arange(int(d*SR))/SR; return sum(a*np.sin(2*np.pi*f*h*k) for h,a in parts)*np.exp(-k*dec)*np.minimum(k/.003,1)*amp
def noise(d,lo,hi):
    x=rs.randn(int(d*SR)); X=np.fft.rfft(x); fr=np.fft.rfftfreq(len(x),1/SR); X[(fr<lo)|(fr>hi)]=0; return np.fft.irfft(X,len(x))
PEN=[0,2,4,7,9,12]; chimeF=[784,988,1175,1319,1175,1568]
for i,e in enumerate(json.load(open("events.json"))):
    k,at,v,n=e["k"],e["t"],e["v"],e["n"]; pan=.5+.3*np.sin(i*2.1)
    if k=="chime": put(tone(chimeF[n%6],2.2,2.4,.5,((1,1),(2.76,.32),(5.4,.13),(8.93,.05))),at,.17*v,pan)
    elif k=="tick": put(noise(.035,3000,9000)*np.exp(-np.arange(int(.035*SR))/SR*120)*.5+tone(1800,.035,60,.4),at,.1*v,.5)
    elif k=="pulse": put(tone(mid(55+PEN[n%6]),.5,9,.7,((1,1),(2,.3))),at,.12*v,.5)
    elif k=="scan": put(noise(.75,800,6000)*np.sin(np.pi*np.linspace(0,1,int(.75*SR)))**2*np.linspace(.5,1,int(.75*SR))*.4,at,.07*v,.5)
    elif k=="flag": put(tone(466,.28,9,.6,((1,1),(1.5,.5))),at,.12*v,.5); put(tone(466*1.06,.28,9,.6,((1,1),(1.5,.5))),at+.12,.1*v,.5)
    elif k=="thud":
        d=int(1.1*SR); kk=np.arange(d)/SR; f=45+110*np.exp(-kk*18); ph=2*np.pi*np.cumsum(f)/SR
        x=np.sin(ph)*np.exp(-kk*5)*.9+noise(1.1,200,3500)[:d]*np.exp(-kk*22)*.7
        put(x,at,.34*v,.5)
    elif k=="check": put(tone(988,.16,24,.5),at,.09*v,.45); put(tone(1480,.28,16,.5,((1,1),(2.01,.15))),at+.07,.1*v,.55)
    elif k=="confirm": put(tone(660,.2,14,.5),at,.1*v,.4); put(tone(990,.3,11,.5,((1,1),(2,.2))),at+.09,.1*v,.6)
    elif k=="whoosh": put(noise(.7,500,4500)*np.sin(np.pi*np.linspace(0,1,int(.7*SR)))**2*.45,at-.1,.1*v,.5)
    elif k=="swell": put(noise(1.3,400,3200)*np.sin(np.pi*np.linspace(0,1,int(1.3*SR)))**2*.4,at-.5,.12*v,.5)
    elif k=="soft": put(tone(392,.5,7,.5,((1,1),(2,.25))),at,.09*v,pan)
    elif k=="shimmer": [put(tone(1568*2**(j/6),1.0,5,.4),at+j*.07,.05*v,.3+.4*(j%2)) for j in range(6)]
sl,sr=reverb(SL,SRr,.4); SL=SL*.85+sl; SRr=SRr*.85+sr
mixL=L+SL; mixR=R+SRr
g=np.minimum(1,ss(t/.4))*(1-ss((t-29.0)/1.0)); mixL*=g; mixR*=g
pk=max(np.abs(mixL).max(),np.abs(mixR).max()); out=np.stack([mixL,mixR],1)/pk*.85
w=wave.open("score_raw.wav","wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out*32767).astype(np.int16).tobytes()); w.close(); print("score ok",out.shape)
