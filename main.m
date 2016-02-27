data=['1' '2' 'A' '0' '6' '8' '9' '#'];
tonet=1;
dt=0.0001;
fs=1/dt;
freqx=[1209 1336 1477 1633];
freqy=[697 770 852 941];
table=['1' '2' '3' 'A';'4' '5' '6' 'B';'7' '8' '9' 'C'; '*' '0' '#' 'D'];
signal=[];
t=[0:dt:tonet];
N=size(t,2);
for i=1:size(data,2),
    for j=1:4,
        for k=1:4,
            if(table(j,k)==data(i))
                y=sin(2*pi*freqy(j)*t)+sin(2*pi*freqx(k)*t);
                signal=[signal y];
            end
        end
    end
end
t1=[1:size(signal,2)]*dt;
signal=awgn(signal,15,'measured');
plot(t1,signal);

resx=zeros(1,4);
resy=zeros(1,4);
%decoding
ans=[];
for i=1:round(size(signal,2)/N),
    rangel=(i-1)*N+1;
    rangeu=i*N;
    symsignal=signal(1,[rangel:rangeu]);
    for j=1:4,
        a=[1 -2*cos(2*pi*freqx(j)/fs) 1];
        b=[1];
        q=filter(b,a,symsignal);
        resx(j)=q(N)-q(N-1)*exp(-2*pi*1i*freqx(j)/fs);
    end
    %abs(resx)
    [temp, x]=max(abs(resx));
    for j=1:4,
        a=[1 -2*cos(2*pi*freqy(j)/fs) 1];
        b=[1];
        q=filter(b,a,symsignal);
        resy(j)=q(N)-q(N-1)*exp(-2*pi*1i*freqy(j)/fs);
    end
    %abs(resy)
    [temp, y]=max(abs(resy));
    %disp(table(y,x));
    ans=[ans table(y,x)];
end
disp(data);
disp(ans);

    