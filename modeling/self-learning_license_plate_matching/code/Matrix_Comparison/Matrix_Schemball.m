clear all
close all

matrix_folder = 'C:\Users\Paul_010-4394-0929\Documents\MATLAB\001.Projects\20131210\all';

listmatrix = dir(fullfile(matrix_folder ,'*Matrix*.*'));


for n = 1:size(listmatrix,1) % to check Matrix
    display(['MatrixFile :', listmatrix(n).name]);
end

cd(matrix_folder)

for i = 1:length(listmatrix) % Matrix loop
    display(['File _', listmatrix(i).name]) ; 
    data = importdata(listmatrix(i).name); 
    A = data.AssociationMatrix;
    A = A./(repmat(sum(A,2),1,37));
    display('Data Import Completed'); 

    for j=1:length(A)
        A(j,j)=0;
        A(37,j)=0;A(j,37)=0;
    end
    
    A=A./(max(max(A)));
    
   
%     cal = 2;
%     for j=1:length(A)
%         A(j,j)=A(j,j)./cal;
%     end
%     A=A.*cal;
    

    Contents = {'0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','~'}
    h=schemaball(A, Contents,[1,1,0]);
    set(h.l(~isnan(h.l)), 'LineWidth',3)
    set(h.s, 'MarkerEdgeColor','red','LineWidth',2,'SizeData',100)
    set(h.t, 'EdgeColor','white','LineWidth',1)
    
    saveas(figure(i),[listmatrix(i).name,'_figure.bmp'],'bmp');
    
    [~,computer] = system('hostname');
    [~,user] = system('whoami');
    [~,alltask] = system(['tasklist /S ', computer, ' /U', user]);
    excelPID=regexp(alltask, 'EXCEL.EXE\s*(\d+)\s','tokens');
    for k=1:length(excelPID)
        killPID=cell2mat(excelPID{k});
        system(['taskkill /f /pid ', killPID]);
    end
end





