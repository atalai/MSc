clc

% Load the example test example "Clinical.csv" into the Matlab Workbench first 

Temp_Test = Clinical; %ss
Temp_Test_Rand = Clinical;

% You may change 1000 to someother premutational value. Here we will perform a 1000 permutation test on the clinical.csv dataset 

for i=1:1000  
    
    Temp_Test_Rand.Class = Temp_Test.Class(randperm(length(Temp_Test.Class)));
    
    writetable(Temp_Test_Rand,['ValidationDataset_',num2str(i),'.csv'],'Delimiter',',','QuoteStrings',true);    
end

% The generated permutational versions of the original clinical.csv will be written in the same directory
