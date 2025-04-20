function [w] = edweight(XChr, YChr, W, type)
%% Function to calculate edit weight
% Input: two strings, weight matrix, type of weight
%% Main code
% s = 0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ ;
s = char([48:48+9,65:65+25,32]);
XChr = [char(32),XChr];
YChr = [char(32),YChr];

for i=1:length(XChr)
    x(i) = strfind(s,XChr(i));
end

for i=1:length(YChr)
    y(i) = strfind(s,YChr(i));
end

% Probabilities
p = W(x,y);
    
% Weight Functions
if strcmp(type, 'weight')
    warning off all
    w = log(1./p);
    warning on all
else
    w = p;
end