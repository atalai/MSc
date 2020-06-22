### Aron Sahand Talai, B.Sc.
### Supervisor: Nils Daniel Forkert, PhD
### BME 619 - ADVANCED MEDICAL IMAGE PROCESSING 
### Program : Mean Thickness Calculator  
### DUE DATE: April 20 2015
###############################################
#
#
#
# This program estimates cortical thickness of HC, PSP and IPD subject using T1-weighted in NIFTI images
#
#
#
###############################################

# Import required libraries 
import sys, vtk, os, math, imghdr, scipy, matplotlib,timeit,argparse, numpy
from vtk.util.misc import vtkGetDataRoot
from timeit import default_timer as timer
VTK_DATA_ROOT = vtkGetDataRoot()
VTK_DATA_ROOT = "/Users/sahandtalai/Desktop/Project/HC"

# Clear Terminal
os.system('cls' if os.name == 'nt' else 'clear')

parser = argparse.ArgumentParser(description = """This script calculates the cortical thickness by implementing the (Hildebrand & Ruegsegger., 1997) method .""")
#Arguments:
parser.add_argument('--prefix'  , type = str, default = '/Users/sahandtalai/Desktop/Project/HC'    , help = 'Prefix of the input images (default: %(default)s)')
parser.add_argument('--IntensityValue' , type = int, default = 13         , nargs = '?', help = 'Intensity to be thresholded (default: %(default)s)')
parser.add_argument('--NoiseMargin' , type = int, default = 0.5       , nargs = '?', help = 'Discard voxels with values less than this (default: %(default)s)')

#Assign input arguments to variables
args = parser.parse_args()
prefix   = args.prefix
IntensityValue  = args.IntensityValue
NoiseMargin  = args.NoiseMargin

# Start Timer
start = timer()

# VTK version
print "Your Python version is :",sys.version
print '--------------------------'
print "Your VTK version is :",vtk.VTK_MAJOR_VERSION
print '--------------------------'


# Read NIFTII Images
reader = vtk.vtkNIFTIImageReader()
reader.SetFileName(VTK_DATA_ROOT + "/PASIM_N002.nii")
reader.Update()
size = reader.GetOutput().GetDimensions()


# Create Threshold
Threshold = vtk.vtkImageThreshold()
Threshold.SetInputConnection(reader.GetOutputPort())
Threshold.ThresholdBetween(IntensityValue,IntensityValue)
Threshold.SetInValue(255)
Threshold.SetOutValue(0)
Threshold.SetOutputScalarTypeToUnsignedChar()
Threshold.Update()

# Write Threshold Image
writer = vtk.vtkNIFTIImageWriter()
writer.SetInputConnection(Threshold.GetOutputPort())
writer.SetFileName("BinaryImage.nii")
writer.Write()

# Calculate Euclidean distance
dist = vtk.vtkImageEuclideanDistance()
dist.SetInputConnection(Threshold.GetOutputPort())
dist.SetAlgorithmToSaitoCached()
dist.Update()

# Performs Square root to speed up processing time 
mathSqrt = vtk.vtkImageMathematics()
mathSqrt.SetInputConnection(dist.GetOutputPort())
mathSqrt.SetOperationToSquareRoot();
mathSqrt.Update()


# Second DeepCopy to be used as a reference
thickness = vtk.vtkImageData()
thickness.DeepCopy(mathSqrt.GetOutput())

# First DeepCopy to be used in the for loop
distance = vtk.vtkImageData()
distance.DeepCopy(mathSqrt.GetOutput())

spacing = thickness.GetSpacing()

# Enter the processing section and implement the (Hildebrand & Ruegsegger., 1997) method
for X in range(1,size[0]):
	for Y in range(1,size[1]):
		for Z in range (1,size[2]):

		 CenterValue = distance.GetScalarComponentAsDouble(X,Y,Z,0)
		 if (CenterValue != 0):

			distanceX = int (math.floor(CenterValue/spacing[0]))
			distanceY = int (math.floor(CenterValue/spacing[1]))
			distanceZ = int (math.floor(CenterValue/spacing[2]))

			for i in range(-distanceX, distanceX):
				for j in range(-distanceY, distanceY):
					for k in range(-distanceZ, distanceZ):
						if(k!=0 or j!=0 or k!= 0):
							if( math.sqrt( math.pow(i*spacing[0],2) + math.pow(j*spacing[1],2) + math.pow(k*spacing[2],2))  <= CenterValue):

								if(distance.GetScalarComponentAsDouble(X-i,Y-j,Z-k,0) != 0 and thickness.GetScalarComponentAsDouble(X-i,Y-j,Z-k,0) < CenterValue):
									thickness.SetScalarComponentFromDouble(X-i,Y-j,Z-k,0,CenterValue)




# Multiply all values by 2 since Thickness = radius * 2
mathMultThickness = vtk.vtkImageMathematics()
mathMultThickness.SetInputData(thickness)
mathMultThickness.SetOperationToMultiplyByK()
mathMultThickness.SetConstantK(2.0)
mathMultThickness.Update()


# Initialize counter values
EffectiveSegmentedVoxels = 0
total_sum = 0


# Calculate mean thickness 
# total_sum is the summation of all the voxel values (voxels with values less than 2*NoiseMargin are excluded from Total sum) 
# EffectiveSegmentedVoxels is the number of all the non zero voxels which have values bigger than 2*NoiseMargin
for X in range(1,size[0]):
	for Y in range(1,size[1]):
		for Z in range(1,size[2]):
		 if(thickness.GetScalarComponentAsDouble(X,Y,Z,0) > NoiseMargin):
			EffectiveSegmentedVoxels = EffectiveSegmentedVoxels + 1
			total_sum += thickness.GetScalarComponentAsDouble(X,Y,Z,0)

Mean = float(total_sum/EffectiveSegmentedVoxels)


# Print Program output
print 'Total number of voxels in this image are',size[0]*size[1]*size[2]
print '------------------------'
print 'Number of effective segmented Voxels are:',EffectiveSegmentedVoxels
print '------------------------'
print 'The total sum of all effective voxel values are:',2*float(total_sum)
print '------------------------'
print 'Mean Value is:', 2*float(Mean)
print '------------------------'

end = timer()
print "Total Running Time was (In seconds)",end - start

print '------------------------'

# Write Primary image 
writerDistance = vtk.vtkNIFTIImageWriter()
writerDistance.SetInputData(distance)
writerDistance.SetFileName("PreprocessedImage.nii")
writerDistance.Write()

# Write Final image
writerThickness = vtk.vtkNIFTIImageWriter()
writerThickness.SetInputConnection(mathMultThickness.GetOutputPort())
writerThickness.SetFileName("ProcessedImage.nii")
writerThickness.Write()

# End Program 