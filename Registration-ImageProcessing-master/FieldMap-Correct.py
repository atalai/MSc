
#!/bin/bash
### Aron Sahand Talai, B.Sc.
### Supervisor: Nils Daniel Forkert, Dr. rer. nat.
### Program : Correct +/- inconsistencies within GE based MRI scans   
### DUE DATE: ---
###############################################
#
#
#
# 
#
#
#
###############################################


# Import required libraries 
import vtk 
import sys, os, math, imghdr, scipy, matplotlib,timeit,argparse, numpy,csv,time

# Clear Terminal
os.system('cls' if os.name == 'nt' else 'clear')

# # Open the file containg subject names/labels
# with open("ImageFile", "r") as myIfile:
#     Idata = myIfile.read()

# Imagelist = Idata.split('\n') # Total number of 147

# # Open the file containg subject names/labels
# with open("RegFile", "r") as myRfile:
#     Rdata = myRfile.read()

# Reglist = Rdata.split('\n')

#print 'started'
#######################################################################################

ImageFilename = "/home/stalai/mricrogl_lx/test/TestFieldmap/GEfix/0000.nii.gz" #"/Users/sahandtalai/Desktop/NewProject/Image/"
outpath= "/home/stalai/mricrogl_lx/test/TestFieldmap/GEfix/Fixed.nii.gz"

# Read Original GE Nifti Image 
reader = vtk.vtkNIFTIImageReader()
reader.SetFileName(ImageFilename)
reader.Update()
size = reader.GetOutput().GetDimensions()

# Make the first deep copy of the original image
Mask = vtk.vtkImageData()
Mask.DeepCopy(reader.GetOutput())

# Make the second deep copy of the original image
Data = vtk.vtkImageData()
Data.DeepCopy(reader.GetOutput())


# # Correct for negative values in the image
# for X in range(1,size[0]):
#     for Y in range(1,size[1]):
#         for Z in range(1,size[2],2):

#         	Data.SetScalarComponentFromFloat(X,Y,Z,0, (-1)* Mask.GetScalarComponentAsFloat(X,Y,Z,0))


# Correct for negative values in the image
for X in range(1,size[0]):
    for Y in range(1,size[1]):
        for Z in range(1,size[2],2):

        	Data.SetScalarComponentFromFloat(X,Y,Z,0, (-1)* Data.GetScalarComponentAsFloat(X,Y,Z,0))


# Write Data as a nifti image
writer = vtk.vtkNIFTIImageWriter()
#writer.SetInputConnection(Data.GetOutput())
writer.SetInputData(Data)
#writer.SetInputConnection(Data)
writer.SetFileName(outpath)
# copy most information directoy from the header
writer.SetNIFTIHeader(reader.GetNIFTIHeader())
# this information will override the reader's header
writer.SetQFac(reader.GetQFac())
writer.SetTimeDimension(reader.GetTimeDimension())
writer.SetQFormMatrix(reader.GetQFormMatrix())
writer.SetSFormMatrix(reader.GetSFormMatrix())
writer.Write()
