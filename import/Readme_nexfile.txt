# Please look at the class method documentation strings in nexfile.py

# To read .nex or .nex5 files, use the following code:

import nexfile
reader = nexfile.Reader()
fileData = reader.ReadNexFile('C:\\Data\\file.nex')
fileData1 = reader.ReadNexFile('C:\\Data\\file.nex5')

# If your files are larger than a few MB, use numpy version of the reader:

import nexfile
reader = nexfile.Reader(useNumpy=True)
fileData = reader.ReadNexFile('C:\\Data\\LargeFile.nex')


# To write .nex file, use this code:

timestampFrequency = 50000
writer = nexfile.NexWriter(timestampFrequency)

# then, add variable data using Add... methods in NexWriter class 
# (see method doc strings in nexfile.py):

writer.AddContVarWithSingleFragment('cont1', 0, 10000, [5, 6, 7, 8])
writer.AddContVarWithSingleFragment('cont2', 0, 10000, [9, 10, 11, 12])

# then, use WriteNexFile method:

writer.WriteNexFile('C:\\Data\\python.nex')


# If your files are larger than a few MB, use numpy version of the NexWriter:

import nexfile
import numpy as np
timestampFrequency = 50000
writer = nexfile.NexWriter(timestampFrequency, useNumpy=True)
writer.AddNeuron('neuron1', np.array([1, 2, 3, 4]))
writer.AddContVarWithSingleFragment('cont1', 2, 10000, np.array([5, 6, 7, 8]))
writer.WriteNexFile('C:\\Data\\pythonWithFloatContValues.nex5', 1)
