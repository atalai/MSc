# WekaRegressionBest
This tool selects the result with the least amount of RMSE in the list of results produced by WekaRegression

This tool automatically extracts the top performing regression result from "WekaRegression" and identifies the best feature selection and regression pair for any given task. This step must be done after WekaRegression.

What are the requirments?

Linux based operating system
Python version above 3
Basic knowledge of bash scripting

What Does the program do? This tool automatically extracts the top performing regression result from "WekaRegression" and identifies the best feature selection and regression pair for any given task. This step must be done after WekaRegression.


What segments of the codes should I change if I want to use this tool?

Non! Make sure the Best.sh and BestResultFromText.py are in the same master file as the resulting text files from WekaRegression. The python code is written to calculate the best performing regression model with respect to "RMSE" value. It creates another text file with the corresponding name starting with the tag "Best_..."
