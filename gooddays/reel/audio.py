"""Original sound bed + sound design for the GOOD DAYS 20 s reel. Pure numpy, no samples, no voice."""
import numpy as np, wave
SR=44100; D=20.0; N=int(SR*D); t=np.arange(N)/SR; rs=np.random.RandomState(21)
CUT=9.625
mid=lambda m:440.0*2**((m-69)/12)
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
# ------------------------------------------------ harmony: tense minor in the gym, warm major after the cut
CH=[(0,4.8,[45,52,57,60,64]),(4.8,CUT,[41,48,53,57,60]),(CUT,12.2,[41,48,53,57,60,64]),(12.2,14.8,[38,45,50,53,57,60]),(14.8,17.2,[34,46,50,53,57,62]),(17.2,21,[41,48,53,57,60,64,67])]
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
cafe=ss((t-CUT)/.6); L*=(.75+.3*cafe); R*=(.75+.3*cafe)       # the pad opens up after the cut
# ------------------------------------------------ rhythm: soft kick + hats in the gym (tension), airy plucks in the cafe
KL=np.zeros(N); KR=np.zeros(N); beat=.5
def put(arrL,arrR,x,at,vol,pan=.5):
    s=int(at*SR)
    if s<0: x=x[-s:]; s=0
    e=min(N,s+len(x))
    if s<N and e>s: arrL[s:e]+=x[:e-s]*vol*(1-pan)*1.4; arrR[s:e]+=x[:e-s]*vol*pan*1.4
for i in range(int(CUT/beat)):
    at=i*beat
    if at<.9 or at>CUT-1.2: continue
    kk=np.arange(int(.35*SR))/SR; x=np.sin(2*np.pi*np.cumsum(46+90*np.exp(-kk*30))/SR)*np.exp(-kk*9)*.9
    if i%2==0: put(KL,KR,x,at,.26*(.6+.4*ss((at-1)/5)),.5)
    if at>2.4 and i%2==1: put(KL,KR,noise(.05,6000,12000)*np.exp(-np.arange(int(.05*SR))/SR*80),at,.06,.5)
    if at>6.5 and i%2==0: put(KL,KR,noise(.05,6000,12000)*np.exp(-np.arange(int(.05*SR))/SR*80),at+.25,.05,.6)
pat=[0,2,4,2,3,1,4,2]; step=.25
for i in range(int(CUT/step)+2,int(D/step)-2):
    tt=i*step
    if rs.rand()<.38 or (i%4==0 and rs.rand()<.4): continue
    ch=next(c for c in CH if c[0]<=tt<c[1]); m=ch[2][1+pat[i%len(pat)]%(len(ch[2])-1)]+24
    n=int(1.5*SR); k=np.arange(n)/SR; f=mid(m)
    x=(np.sin(2*np.pi*f*k)+.35*np.sin(2*np.pi*f*2.01*k)+.12*np.sin(2*np.pi*f*4.1*k))*np.exp(-k*3.4)*np.minimum(k/.004,1)*.05
    pan=.5+.35*np.sin(i*1.7)
    for dly,g in ((0,1),(.375,.28),(.75,.1)): put(KL,KR,x,tt+dly,g,pan)
for i,at in enumerate(np.arange(CUT+.4,D-.6,.5)):                       # soft cafe pulse
    kk=np.arange(int(.3*SR))/SR; x=np.sin(2*np.pi*np.cumsum(52+40*np.exp(-kk*30))/SR)*np.exp(-kk*10)
    if i%2==0: put(KL,KR,x,at,.12,.5)
# ------------------------------------------------ ambience
AL=np.zeros(N); AR=np.zeros(N)
gym_env=1-ss((t-CUT+.2)/.5)
rumble=noise(D,25,200); rumble/=np.abs(rumble).max(); AL+=rumble*.08*gym_env; AR+=np.roll(rumble,900)*.08*gym_env
for at in (1.3,2.9,5.2,7.6):                                            # distant plate clanks
    put(AL,AR,tone(1900+rs.rand()*500,.5,12,.5,((1,1),(2.7,.4),(4.4,.2)))*.5+noise(.04,2000,8000)[:int(.5*SR)].mean()*0,at,.05,.3+rs.rand()*.4)
for at in (1.1,6.9):                                                    # exhale
    n=int(.9*SR); x=noise(.9,500,3200)*np.sin(np.pi*np.linspace(0,1,n))**2; put(AL,AR,x,at,.16,.5)
caf_env=ss((t-CUT)/.4)
leaf=noise(D,2500,7000); mod=.5+.5*np.sin(2*np.pi*.23*t)*np.sin(2*np.pi*.11*t+1); leaf=leaf/np.abs(leaf).max()*mod
AL+=leaf*.05*caf_env; AR+=np.roll(leaf,700)*.05*caf_env
mur=noise(D,250,900); mur/=np.abs(mur).max(); mm=np.clip(np.sin(2*np.pi*3.3*t+np.sin(2*np.pi*.4*t)*3),0,1)*(.5+.5*np.sin(2*np.pi*.17*t))
AL+=mur*mm*.05*caf_env; AR+=np.roll(mur,1500)*mm*.05*caf_env
# ------------------------------------------------ cuts, riser, hits
FL=np.zeros(N); FR=np.zeros(N)
def whoosh(at,vol,d=.5): n=int(d*SR); put(FL,FR,noise(d,300,5000)*np.sin(np.pi*np.linspace(0,1,n))**2*.5,at-d*.45,vol)
for at in (3.25,6.5,13.25,15.75): whoosh(at,.16)
n=int(1.4*SR); rise=noise(1.4,400,6000)*np.linspace(0,1,n)**2.2*.6; put(FL,FR,rise,CUT-1.4-.02,.22)       # riser, dead stop before the cut
sw=np.arange(n)/SR; put(FL,FR,np.sin(2*np.pi*np.cumsum(180+900*(sw/1.4)**2)/SR)*np.linspace(0,1,n)**2*.3,CUT-1.42,.12)
whoosh(CUT,.3,.45)
kk=np.arange(int(1.2*SR))/SR; boom=np.sin(2*np.pi*np.cumsum(70+120*np.exp(-kk*14))/SR)*np.exp(-kk*4.5)+noise(1.2,150,3000)[:len(kk)]*np.exp(-kk*20)*.5
put(FL,FR,boom,CUT,.34)
for j,(f,dl,g) in enumerate(((2100,0,1),(2790,.045,.7),(3540,.11,.55),(4300,.19,.4))):   # ice-and-cup clink
    put(FL,FR,tone(f,1.0,7,.4,((1,1),(2.76,.3),(5.4,.12))),CUT+.02+dl,.09*g,.35+.3*(j%2))
put(FL,FR,noise(.25,3000,9000)*np.exp(-np.arange(int(.25*SR))/SR*14)*.5,CUT+.12,.07)
for at in (11.0,13.9,16.2): put(FL,FR,tone(2300+rs.rand()*600,.5,9,.4,((1,1),(2.76,.3))),at,.05,.6)   # ice tinkles
# text reveal + logo
put(FL,FR,np.sin(2*np.pi*np.cumsum(120+60*np.exp(-np.arange(int(.5*SR))/SR*10))/SR)*np.exp(-np.arange(int(.5*SR))/SR*8),17.4,.2)
for at,m in ((17.4,72),(17.62,76)): put(FL,FR,tone(mid(m),1.6,3,.5,((1,1),(2.76,.2),(5.4,.08))),at,.1)
for j in range(6): put(FL,FR,tone(1568*2**(j/6),1.0,5,.4),18.5+j*.07,.045,.3+.4*(j%2))
# ------------------------------------------------ reverbs, mix, master
rl,rr=reverb(L+KL,R+KR,.5); L=L*.8+rl; R=R*.8+rr
fl,fr=reverb(FL,FR,.4,2.2); FL=FL*.85+fl; FR=FR*.85+fr
mixL=L+KL*.7+AL+FL; mixR=R+KR*.7+AR+FR
g=np.minimum(1,ss(t/.3))*(1-ss((t-19.55)/.45)); mixL*=g; mixR*=g
pk=max(np.abs(mixL).max(),np.abs(mixR).max()); out=np.stack([mixL,mixR],1)/pk*.85
w=wave.open("score_raw.wav","wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((out*32767).astype(np.int16).tobytes()); w.close(); print("audio ok")
