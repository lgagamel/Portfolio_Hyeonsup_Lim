function [ed, C, w] = genedw(XString, YString, Type)
%**************************************************************************
%***General Levenshtein Distance
%**************************************************************************

w = weight(XString, YString, Type); %costs

%length of the strings
strlen = [size(w,1),size(w,2)];            
                            
%set up cost matrix                        
C = zeros(size(w));
                            
%Computing edit distance---------------------------------------------------
    C(1, 1,:) = 0;
    for i = 2:strlen(1)
        C(i, 1,:) = C(i - 1, 1,:) + w(i,1,:);
    end
    
    for j = 2:strlen(2)
        C(1, j,:) = C(1, j - 1,:) + w(1,j,:);
    end
    
    
    for i = 2:strlen(1)
        for j = 2:strlen(2)
    
            %Computing minimum distance
            C(i, j,:) = min([C(i - 1, j,:) + w(i,1,:),... delete
                C(i, j - 1,:) + w(1,j,:),...
                C(i - 1, j - 1,:) + w(i,j,:)],[],2);
        end
    end
ed = zeros(size(w,3),1);
ed(:,1) = C(strlen(1),strlen(2),:);
%--------------------------------------------------------------------------
%**************************************************************************