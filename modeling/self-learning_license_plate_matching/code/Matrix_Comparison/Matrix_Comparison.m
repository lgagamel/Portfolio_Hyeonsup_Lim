clear all
close all

matrix_folder = 'C:\Users\Paul_010-4394-0929\Documents\MATLAB\001.Projects\20131210\all';

listmatrix = dir(fullfile(matrix_folder ,'*Matrix*.*'));

cd(matrix_folder)


for i = 1:length(listmatrix) % Matrix loop
    data = importdata(listmatrix(i).name); 
    M(i).data = data.AssociationMatrix;
    M(i).name = listmatrix(i).name;
    display(['MatrixFile :', listmatrix(i).name,' _ Data Import Completed']);     
end

temp_i=length(M); temp_max=length(M);

for i=1:temp_max
    for j=1:temp_max
        temp_i=temp_i+1;
        M(temp_i).name = [M(i).name,'*',M(j).name];
        M(temp_i).data = M(i).data*M(j).data;
    end
end

M(temp_i+1).data=eye(37); M(temp_i+1).name='eye';
M(temp_i+2).data=ones(37); M(temp_i+2).name='ones';


for i = 1:length(M) % Matrix loop
    for j = 1:length(M) 
        
        A = M(i).data;
        B = M(j).data;
        
        A = A./(repmat(sum(A,2),1,37));
        B = B./(repmat(sum(B,2),1,37));           
                
        e = sqrt(sum(sum((A - B).^2))); %/ mean(mean(B));
%         e_A = sqrt(sum(sum((A - eye(length(A))).^2))) / mean(mean(eye(length(A))));
%         e_B = sqrt(sum(sum((B - eye(length(B))).^2))) / mean(mean(eye(length(B))));
        
        Result(i,j) = e;

%         Result={file_A_name,file_B_name,e_A, e_B, e};

        display([num2str(((i-1).*length(M)+j)/(length(M).*length(M)).*100), ' % Completed'])    
    end
end

[~,computer] = system('hostname');
[~,user] = system('whoami');
[~,alltask] = system(['tasklist /S ', computer, ' /U', user]);
excelPID=regexp(alltask, 'EXCEL.EXE\s*(\d+)\s','tokens');
for k=1:length(excelPID)
    killPID=cell2mat(excelPID{k});
    system(['taskkill /f /pid ', killPID]);
end

output_name='Comparison_Result';
Contents = {M(:).name};
xlswrite(output_name, Contents , 'Results', 'B1');
xlswrite(output_name, Contents' , 'Results', 'A2');
xlswrite(output_name, Result , 'Results', 'B2');

%% Test
for i=[1,65,94,2,79,108,3,67,96,4,81,110]
    A=M(i).data;
    A = A./(repmat(sum(A,2),1,37));
    for j=1:length(A)
        A(j,j)=0;
        A(37,j)=0;A(j,37)=0;
    end

    A=A./(max(max(A)));


    Contents = {'0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','~'}
    h=schemaball(A, Contents,[1,1,0]);
    set(h.l(~isnan(h.l)), 'LineWidth',3)
    set(h.s, 'MarkerEdgeColor','red','LineWidth',2,'SizeData',100)
    set(h.t, 'EdgeColor','white','LineWidth',1)
    title(M(i).name);
end
