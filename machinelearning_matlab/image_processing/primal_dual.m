% primal-dual
x1=imread('coffee.jpg');
n=256;
x1=imresize(x1,[n,n]); % zmiana rozmiaru
x1=rgb2gray(x1); 
x1=im2double(x1);
figure
imshow(x1);

rho=0.5;
Lambda=rand(n,n)>0.5;
Psi=@(x) Lambda.*x;

y=Psi(x1);  % W randomowych miejscach czarne kwadraty
figure
imshow(y);


gradF=@(x) cat(3,x-x(:,[end,1:(end-1)]),x-x([end,1:(end-1)],:));
divf=@(w) ( w(:,[2:end,1],1)-w(:,:,1)+w([2:end,1],:,2)-w(:,:,2)); % sprzężony do gradientu obrazu
NormEps=@(u) sqrt(sum(u.^2,3)); % norma l2 dla elemtu macierzy
J=@(x) sum(sum(NormEps(gradF(x)))); %  l1 norma skomponowana

ProxF= @(s,sigma) max(0,1-sigma./repmat(NormEps(s),[1 1 2])).*s;
ProxFs= @(s,sigma) s - sigma*ProxF(s/sigma,1/sigma);

ProxG=@(x,tau) x+ Lambda.*(y-Lambda.*x); % wzór na projekcje (prox)

sigma=10; % wsp dla kroku dualnego
tau=0.9/80; % wsp dla kroku prymalne

niter=100;
E=zeros(1,niter);
S=zeros(1,niter); % SNR

x=y; % inicjalizcja obrazu przez zaszumiony
xbar=y; % inicjalizcja obrazu przez zaszumiony
xold=y; % inicjalizcja obrazu przez zaszumiony
s=gradF(y)*0; % macierz zerowa o wymiarach dualnych
theta=0; % 0 - bez relaksacji

for i=1:niter
    s=ProxFs( s+sigma* gradF(xbar)  ,sigma); % krok dualny
    xold=x; % pomocnicze
    x=ProxG( x+tau*divf(s)   ,tau);
    xbar=x+theta*(x-xold);
    E(i)=J(xbar);
    S(i)=snr(x1,xbar); % relacja snr pomiędzy orginałem i procesowanym
end

figure
imshow(xbar);

figure
plot(E); %wykres zmiany wartości funkcji celu

figure
plot(S); %wykres zmiany wartości wskaźnika SNR (stosunek sygnału do szumu)



