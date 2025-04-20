function [w] = weight(XChr, YChr, type)
global A U

%s = 0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ ;
s = char([48:48+9,65:65+25,32]);
XChr = [char(32),XChr];
YChr = [char(32),YChr];

for i=1:length(XChr)
    x(i) = strfind(s,XChr(i));
end

for i=1:length(YChr)
    y(i) = strfind(s,YChr(i));
end

   
%Weight Functions
if strcmp(type, 'weight')
    % Probability
    p = A(x,y);
    
    warning off all
    w = log(1./p);
    %w = (log(1./(p+0.001))-log(1./(1+0.001))).*(1./log(1./(0+0.001)));
    warning on all
    
else
    % Traditional Cost
    p = U(x,y);
    w = p;
end