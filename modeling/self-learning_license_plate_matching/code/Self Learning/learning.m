function [M,error] = learning(f, z, dth, gh_distance, prob_type,...
        min_speed, max_speed, no_sync, gtruth, listfile, directory_name, matrix_folder, z_value)
%%Routine execution :::::::::::::::::::::::::::::::::::::::::::::::::::::::
global A U
cd(directory_name)

%Unitary Matrix
U = ones(37)-eye(37);
A = U;
Initial=eye(37);

N = zeros(37,37);
perform = [];
error = [];
e = 100;
m = 0; 
while  m < 1 && e > 10^-3 

    m = m + 1;
    display(['Iteration :', num2str(m)]);
    
    if m > 1
        type = 'weight';        
        if prob_type == 1        
            t_min = 5;
            t_max = 17.5;
        elseif prob_type == 2
            t_min = 5;
            t_max = 20; 
        else
            t_min = 30;
            t_max = 45;
        end
    else               
        type = 'unitary';
        t_min = 0;
        t_max = 5;
    end
    
    [M, nm, nf, p] = matrixestimation(m, z, t_min, t_max, dth, gh_distance,...
        min_speed, max_speed, no_sync, type, gtruth, listfile, directory_name, Initial, matrix_folder, prob_type, z_value);
    
    
    ind_zero = find(diag(M)==0);
    ind_zero = ind_zero(ind_zero~=37);
    
    if isempty(ind_zero) == 0
        for i = 1:length(ind_zero)
            M(ind_zero(i),ind_zero(i)) = 1;
        end
    end
    
    N = A;
        
    if prob_type == 1
        A = M./(repmat(sum(M,2),1,37));           
    elseif prob_type == 2
        A = M./(repmat(sum(M,1),37,1));  
    else
        A = M./sum(sum(M));  
    end
    
    e = sqrt(sum(sum((A - N).^2))) / mean(mean(N));
    error = [error; e];
    
    perform = [perform; [nm, nf, p]];
    cd(matrix_folder);
    %Output file-------------------------------------------------------
    infilename = listfile.name;
    [infilename_split, delimiter]=strsplit(infilename,'.');
    output_name = [infilename_split{1,1}, '_Matrix'];
    xlswrite(output_name, M , ['M', num2str(m)], 'B2');
    %xlswrite([output_name, num2str(f)], M , ['M', num2str(m)], 'B2');
    %------------------------------------------------------------------
end

    %Final Matrix---------------------------------------------------------
    xlswrite(output_name, M , 'AssociationMatrix', 'B2');
    %xlswrite([output_name, num2str(f)], M , 'AssociationMatrix', 'B2');
    %---------------------------------------------------------------------

    %Error --------------------------------------------------------
    xlswrite(output_name, error , 'Error', 'A1');
    %xlswrite([output_name, num2str(f)], error , 'Error', 'A1');
    %--------------------------------------------------------------
    
    %Error --------------------------------------------------------
    xlswrite(output_name, perform , 'Perform', 'A1');
    %xlswrite([output_name, num2str(f)], perform , 'Perform', 'A1');
    
    display(['Completed to make Association Matrix :', output_name]);
    %--------------------------------------------------------------
    
    

%%::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::