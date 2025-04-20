function [ind, ind_alphanum] = gedbtracking(W, w, XChr, YChr)
%**************************************************************************
%***Compute the path of edit distance
%**************************************************************************

%s = 0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ ;
AlphaNumList = {'NN', 'NA', 'AA', 'AN', 'N ', ' N', 'A ', ' A'};
CharType = 'NNNNNNNNNNAAAAAAAAAAAAAAAAAAAAAAAAAA ';
L = char([48:48+9,65:65+25,32]);

XChr = [char(32),XChr];
YChr = [char(32),YChr];

strlen = [size(w,1),size(w,2)];

i = strlen(1); j = strlen(2);
ind = [];
path_alphanum = [];
while i ~= 1 || j ~= 1
    
    if i > 1
        if W(i,j) == W(i-1,j) + w(i,1)
            %display "deletion"
            ind_char = [strfind(L,XChr(i)),strfind(L,YChr(1))];
            i = i - 1;
        end
    end
    
    if j > 1
        if W(i,j) == W(i,j-1) + w(1,j)
            %display "insertion"
            ind_char = [strfind(L,XChr(1)),strfind(L,YChr(j))];                 
            j = j - 1;
            
        end
    end
    
    if i > 1 && j > 1
        if W(i,j) == W(i-1,j-1) + w(i,j)
            %display "substition"
            ind_char = [strfind(L,XChr(i)),strfind(L,YChr(j))];            
            i = i - 1;
            j = j - 1;
        end
    end
    
    ind = [ind; ind_char];
    path_alphanum = [path_alphanum; ...
               strmatch([CharType(ind_char(1)),CharType(ind_char(2))],...
                                                AlphaNumList, 'exact')];
end

ind_alphanum = [9, path_alphanum(end)];
for k = length(path_alphanum):-1:2 
 ind_alphanum = [ind_alphanum; [path_alphanum(k),path_alphanum(k-1)]];  
end
%--------------------------------------------------------------------------
%**************************************************************************