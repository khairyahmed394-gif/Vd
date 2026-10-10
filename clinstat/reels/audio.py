"""Original score + sound design for the ClinStat reels (20 s). Pure numpy, no samples, no voice. usage: python3 audio.py r01"""
import numpy as np, json, wave, sys
reel=sys.argv[1]; SR=44100; D=20.0; N=int(SR*D); t=np.arange(N)/SR; rs=np.random.RandomState({"r01":3,"r02":5,"r03":9,"r04":13}[reel])
SH={"r01":0,"r02":-7,"r03":-5,"r04":-2}[reel]          # transposition per reel so the four reels do not sound identical
mid=lambda m:440.0*2**((m+SH-69)/12)
def ss(x): x=np.clip(x,0,1); return x*x*(3-2*x)
def noise(d,lo,hi):
    x=rs.randn(int(d*SR)); X=np.fft.rfft(x); fr=np.fft.rfftfreq(len(x),1/SR); X[(fr<lo)|(fr>hi)]=0; return np.fft.irfft(X,len(x))
def tone(f,d,dec,amp=1,parts=((1,1),)):
    k=np.arange(int(d*SR))/SR; return sum(a*np.sin(2*np.pi*f*h*k) for h,a in parts)*np.exp(-k*dec)*np.minimum(k/.003,1)*amp
def reverb(sl,sr,wet,sec=2.6):
    n=int(sec*SR); k=np.arange(n)/SR; irs=[]
    for _ in range(2):
        ir=rs.randn(n)*np.exp(-k*6.9/sec); ir=np.convolve(ir,np.ones(6)/6,"same"); ir[:int(.012*SR)]*=np.linspace(0,1,int(.012*SR)); irs.append(ir/np.sqrt((ir**2).sum()))
    m=1<<int(np.ceil(np.log2(N+n))); F=lambda x:np.fft.rfft(x,m)
    return [np.fft.irfft(F(s)*F(ir),m)[:N]*wet for s,ir in ((sl,irs[0]),(sr,irs[1]))]
# harmony: tension in the hook, curious and open through the beats, resolved on the call to action
CH=[(0,3.4,[33,45,52,57,60,64]),(3.4,7.6,[38,45,50,53,57,62]),(7.6,11.6,[34,46,50,53,57,62]),(11.6,15.6,[41,48,53,57,60,64]),(15.6,21,[41,48,53,57,60,64,67])]
L=np.zeros(N); R=np.zeros(N)
for ci,(a,b,notes) in enumerate(CH):
    fi=ss((t-(a-.9 if ci else -1.0))/(1.8 if ci else 1.6)); fo=1-ss((t-(b-.8))/1.6) if ci<len(CH)-1 else 1.0
    env=fi*fo
    for k,m in enumerate(notes):
        f=mid(m)
        for side,det,arr in ((0,-2.5,L),(1,2.5,R)):
            ff=f*2**(det/1200); lfo=1+.12*np.sin(2*np.pi*(.07+.013*k)*t+k+side)
            w=sum(amp*np.sin(2*np.pi*ff*h*t+k*1.3+h) for h,amp in ((1,1),(2,.28),(3,.1),(4,.04)))
            arr+=env*lfo*w*(.04 if k else .09)
def put(aL,aR,x,at,vol,pan=.5):
    s=int(at*SR)
    if s<0: x=x[-s:]; s=0
    e=min(N,s+len(x))
    if s<N and e>s: aL[s:e]+=x[:e-s]*vol*(1-pan)*1.4; aR[s:e]+=x[:e-s]*vol*pan*1.4
KL=np.zeros(N); KR=np.zeros(N)
beat=.5                                                    # soft pulse from the first beat onward
for i in range(int(D/beat)):
    at=i*beat
    if at<3.3 or at>19.0: continue
    kk=np.arange(int(.3*SR))/SR; x=np.sin(2*np.pi*np.cumsum(50+60*np.exp(-kk*28))/SR)*np.exp(-kk*10)
    if i%2==0: put(KL,KR,x,at,.17*(.7+.3*ss((at-3.3)/6)),.5)
    if i%2==1: put(KL,KR,noise(.05,6000,12000)*np.exp(-np.arange(int(.05*SR))/SR*80),at,.05,.5)
pat=[0,2,4,2,3,1,4,2]; step=.25
for i in range(int(3.6/step),int(D/step)-2):
    tt=i*step
    if rs.rand()<.42 or (i%4==0 and rs.rand()<.4): continue
    ch=next(c for c in CH if c[0]<=tt<c[1]); m=ch[2][1+pat[i%len(pat)]%(len(ch[2])-1)]+24
    n=int(1.5*SR); k=np.arange(n)/SR; f=mid(m)
    x=(np.sin(2*np.pi*f*k)+.35*np.sin(2*np.pi*f*2.01*k)+.12*np.sin(2*np.pi*f*4.1*k))*np.exp(-k*3.4)*np.minimum(k/.004,1)*.045
    pan=.5+.35*np.sin(i*1.7)
    for dly,g in ((0,1),(.375,.28),(.75,.1)): put(KL,KR,x,tt+dly,g,pan)
FL=np.zeros(N); FR=np.zeros(N)
chimeF=[784,988,1175,1319,1175,1568]
for i,e in enumerate(json.load(open(f"events_{reel}.json"))):
    k,at,v,n=e["k"],e["t"],e["v"],e["n"]; pan=.5+.3*np.sin(i*2.1)
    if k=="hit":
        kk=np.arange(int(.9*SR))/SR; x=np.sin(2*np.pi*np.cumsum(60+110*np.exp(-kk*16))/SR)*np.exp(-kk*5)+noise(.9,200,3000)[:len(kk)]*np.exp(-kk*26)*.5
        put(FL,FR,x,at,.22*v); put(FL,FR,tone(mid(57+(n%3)*2)*2,.5,5,.3,((1,1),(2.01,.2))),at+.02,.07*v,.5)
    elif k=="pop": put(FL,FR,tone(900+120*(n%4),.12,40,.6,((1,1),(2,.15))),at,.1*v,pan)
    elif k=="tick": put(FL,FR,noise(.035,3000,9000)*np.exp(-np.arange(int(.035*SR))/SR*120)*.5+tone(1800,.035,60,.4),at,.09*v,.5)
    elif k=="check": put(FL,FR,tone(988,.16,24,.5),at,.09*v,.45); put(FL,FR,tone(1480,.28,16,.5,((1,1),(2.01,.15))),at+.07,.1*v,.55)
    elif k=="cross": put(FL,FR,tone(196,.35,8,.6,((1,1),(1.5,.6),(2.02,.2))),at,.12*v,.5); put(FL,FR,tone(185,.35,8,.6,((1,1),(1.5,.5))),at+.06,.1*v,.5)
    elif k=="crack":
        d=int(.9*SR); x=noise(.9,1500,9000)*np.exp(-np.arange(d)/SR*7)*(1+3*(rs.rand(d)>.995)); put(FL,FR,x,at,.16*v)
    elif k=="spin":
        for j in range(8): put(FL,FR,tone(700+60*j,.04,70,.4),at+j*.1,.06*v,.5)
    elif k=="click": put(FL,FR,tone(2200,.03,120,.6)+noise(.03,1000,6000)[:int(.03*SR)]*.2,at,.16*v,.5)
    elif k=="lock": put(FL,FR,tone(330,.2,14,.6,((1,1),(2,.3))),at,.1*v,.5); put(FL,FR,tone(520,.25,12,.6,((1,1),(2.5,.2))),at+.1,.1*v,.5)
    elif k=="whoosh": n_=int(.6*SR); put(FL,FR,noise(.6,400,5000)*np.sin(np.pi*np.linspace(0,1,n_))**2*.5,at-.25,.13*v)
    elif k=="swell": put(FL,FR,noise(1.3,400,3200)*np.sin(np.pi*np.linspace(0,1,int(1.3*SR)))**2*.4,at-.5,.12*v,.5)
    elif k=="chime": put(FL,FR,tone(chimeF[n%6],2.2,2.4,.5,((1,1),(2.76,.32),(5.4,.13),(8.93,.05))),at,.15*v,pan)
    elif k=="cta":
        for j,m in enumerate((72,76,79)): put(FL,FR,tone(mid(m),1.8,3,.5,((1,1),(2.76,.2),(5.4,.08))),at+j*.09,.1*v,.3+.2*j)
        for j in range(6): put(FL,FR,tone(1568*2**(j/6),1.0,5,.4),at+.4+j*.07,.045*v,.3+.4*(j%2))
rl,rr=reverb(L+KL,R+KR,.5); L=L*.8+rl; R=R*.8+rr
fl,fr=reverb(FL,FR,.4,2.2); FL=FL*.85+fl; FR=FR*.85+fr
mixL=L+KL*.7+FL; mixR=R+KR*.7+FR
g=np.minimum(1,ss(t/.3))*(1-ss((t-19.5)/.5)); mixL*=g; mixR*=g
pk=max(np.abs(mixL).max(),np.abs(mixR).max()); out=np.stack([mixL,mixR],1)/pk*.85
w=wave.open(f"raw_{reel}.wav","wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out*32767).astype(np.int16).tobytes()); w.close(); print("audio ok",reel)
