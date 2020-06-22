
#!/bin/bash
### Sahand Talai, B.Sc.
### Supervisor: Nils Daniel Forkert, Dr. rer. nat.
### Program : Classification Accuracy lister   
### DUE DATE: ---
###############################################
#
#
#
# This program lists all stratified classification accuracies from a weka text file 
#
#
#
###############################################
# Import required libraries 
import sys, os, math
import argparse
import string
# Clear Terminal
os.system('cls' if os.name == 'nt' else 'clear')
parser = argparse.ArgumentParser(description = """This script calculates mean of HC, PSP and IPD subject using NIFTI images""")
#Arguments:
parser.add_argument("--Text"  , type = str)

#Assign input arguments to variables
args = parser.parse_args()
Text = args.Text
My_text=Text
#######################################################################################
# Open the file containg subject names/labels
with open(My_text, "r") as myIfile:    #fill me
    Idata = myIfile.read()

Imagelist = Idata.split('\n') 
#######################################################################################
Keyword ='=== Cross-validation ==='
Num_of_Keywords = 0
Num_of_feature = 0
# Determine the total number of features to be used
for i in range(0,len(Imagelist)):

    if Keyword in Imagelist[i][0:24]:
        Num_of_Keywords=Num_of_Keywords + 1


# Create two repositories to save sorted and unsorted classification accuracies
Repository=[0]*(Num_of_Keywords + 1)
Accuracy_Repository=[0]*(Num_of_Keywords + 1)


# Main loop for unsorted classification accuracies
for i in range(0,len(Imagelist)):

    if Keyword in Imagelist[i][0:24]: 

        Num_of_feature=Num_of_feature+1
        Repository[Num_of_feature]=Imagelist[i+4]
        #print (Imagelist[i+4])


# Main loop for sorted classification accuracies
# Results are saved from high to low in Sorted list
for k in range (1,len(Accuracy_Repository)):

    Accuracy_Repository[k]=float(Repository[k][41:46])

    #print (Accuracy_Repository[k])





Sorted_List=sorted(Accuracy_Repository)

Highest_Accuracy=Sorted_List[1]

# Convert highest accuracy back into string to check for it in the original text file to find extended classification metrics
High_Accuracy=str(Sorted_List[1])

for i in range(0,len(Imagelist)):

    if Keyword in Imagelist[i][0:24]:

        if High_Accuracy in Imagelist[i+4][41:46]:

            High_Accuracy_row_number=i


###############################################################################################
with open("_".join(["Best",My_text]), 'a') as savefile:
    sys.stdout = savefile

    for q in range(High_Accuracy_row_number-2,High_Accuracy_row_number+10):
        print Imagelist[q]

    savefile.close()
