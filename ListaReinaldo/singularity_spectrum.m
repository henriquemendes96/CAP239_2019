clearvars
close all
clc

load S3.txt
load S7.txt
load S8.txt

X1 = cumsum(S8-mean(S8));
X2 = cumsum(S7-mean(S7));
X3 = cumsum(S3-mean(S3));
X1 = X1';
X2 = X2';
X3 = X3';

min_scale = 16;
max_scale = 1024;
res_scale = 19;

exponents = linspace(log2(min_scale),log2(max_scale),res_scale);
scale = round(2.^exponents);
q1 = linspace(-5,5,101);
m = 1;

for ns = 1:length(scale)
    segments1(ns) = floor(length(X1)/scale(ns));
    for v = 1:segments1(ns)
        Index1 = (((v-1)*scale(ns))+1):(v*scale(ns));
        C1 = polyfit(Index1,X1(Index1),m);
        C2 = polyfit(Index1,X2(Index1),m);
        C3 = polyfit(Index1,X3(Index1),m);
        fit1 = polyval(C1,Index1);
        fit2 = polyval(C2,Index1);
        fit3 = polyval(C3,Index1);
        RMS_scale1{ns}(v) = sqrt(mean((X1(Index1)-fit1).^2));
        RMS_scale2{ns}(v) = sqrt(mean((X2(Index1)-fit2).^2));
        RMS_scale3{ns}(v) = sqrt(mean((X3(Index1)-fit3).^2));
    end
    for nq = 1:length(q1)
        qRMS1{ns} = RMS_scale1{ns}.^q1(nq);
        qRMS2{ns} = RMS_scale2{ns}.^q1(nq);
        qRMS3{ns} = RMS_scale3{ns}.^q1(nq);
        Fq1(nq,ns) = mean(qRMS1{ns}).^(1/q1(nq));
        Fq2(nq,ns) = mean(qRMS2{ns}).^(1/q1(nq));
        Fq3(nq,ns) = mean(qRMS3{ns}).^(1/q1(nq));
    end
end

for nq = 1:length(q1)
    Ch1 = polyfit(log2(scale),log2(Fq1(nq,:)),1);
    Hq1(nq) = Ch1(1);
    
    Ch2 = polyfit(log2(scale),log2(Fq2(nq,:)),1);
    Hq2(nq) = Ch2(1);

    Ch3 = polyfit(log2(scale),log2(Fq3(nq,:)),1);
    Hq3(nq) = Ch3(1);
end

if isempty(find(q1==0, 1))==0
    qzero=find(q1==0);
    Hq1(qzero)=(Hq1(qzero-1)+Hq1(qzero+1))/2;
    Hq2(qzero)=(Hq2(qzero-1)+Hq2(qzero+1))/2;
    Hq3(qzero)=(Hq3(qzero-1)+Hq3(qzero+1))/2;
end
tq1 = Hq1.*q1-1;
tq2 = Hq2.*q1-1;
tq3 = Hq3.*q1-1;

hq1 = diff(tq1)./(q1(2)-q1(1));
Dq1 = (q1(1:end-1).*hq1)-tq1(1:end-1); 
hq2 = diff(tq2)./(q1(2)-q1(1));
Dq2 = (q1(1:end-1).*hq2)-tq2(1:end-1); 
hq3 = diff(tq3)./(q1(2)-q1(1));
Dq3 = (q1(1:end-1).*hq3)-tq3(1:end-1); 

psi1 = (hq1(1)-hq1(end))/max(Dq1);
psi2 = (hq2(1)-hq2(end))/max(Dq2);
psi3 = (hq3(1)-hq3(end))/max(Dq3);

figure('name','S3')
plot(hq1,Dq1,'linewidth',2)
xlabel('\alpha')
ylabel('F(\alpha)')
legend(['\Psi=' num2str(psi1)]);
grid
print('MDDFA_S3.png','-dpng')

figure('name','S7')
plot(hq2,Dq2,'linewidth',2)
xlabel('\alpha')
ylabel('F(\alpha)')
legend(['\Psi=' num2str(psi2)]);
grid
print('MDDFA_S7.png','-dpng')

figure('name','S8')
plot(hq3,Dq3,'linewidth',2)
xlabel('\alpha')
ylabel('F(\alpha)')
legend(['\Psi=' num2str(psi3)]);
grid
print('MDDFA_S8.png','-dpng')