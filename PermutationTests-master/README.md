# PermutationTests
A matlab code that performs 1000 permutation tests on a sample data set. 

What do I need first? 
1. Matlab 2014 > that's it
2. A test CSV file is provided

What is a permutation test and why is it used?

After the best classification/regression model is trained we need to check the statistical significance of said model. Consequently, the trained model is tested against 1000 random iterations of the complete dataset. In detail, the class labels of the original training dataset in each category are randomly reassigned. Therefore, the 1000 datasets with random labels are used to evaluated the top performing model. If the selected model performes in the top 5% of the overall obtained results,  statistical significance of said model can be infered. 
