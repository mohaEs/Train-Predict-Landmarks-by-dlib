#!/usr/bin/python
# The contents of this file are in the public domain. See LICENSE_FOR_EXAMPLE_PROGRAMS.txt
#
#   This example program shows how to use dlib's implementation of the paper:
#   One Millisecond Face Alignment with an Ensemble of Regression Trees by
#   Vahid Kazemi and Josephine Sullivan, CVPR 2014
#
#   In particular, we will train a face landmarking model based on a small
#   dataset and then evaluate it.  If you want to visualize the output of the
#   trained model on some images then you can run the
#   face_landmark_detection.py example program with predictor.dat as the input
#   model.
#
#   It should also be noted that this kind of model, while often used for face
#   landmarking, is quite general and can be used for a variety of shape
#   prediction tasks.  But here we demonstrate it only on a simple face
#   landmarking task.
#
# COMPILING/INSTALLING THE DLIB PYTHON INTERFACE
#   You can install dlib using the command:
#       pip install dlib
#
#   Alternatively, if you want to compile dlib yourself then go into the dlib
#   root folder and run:
#       python setup.py install
#
#   Compiling dlib should work on any operating system so long as you have
#   CMake installed.  On Ubuntu, this can be done easily by running the
#   command:
#       sudo apt-get install cmake
#
#   Also note that this example requires Numpy which can be installed
#   via the command:
#       pip install numpy

import os
import sys
import glob
import matplotlib
matplotlib.use('Agg') # Must be before importing matplotlib.pyplot or pylab!
import matplotlib.pyplot as plt
import dlib

# In this example we are going to train a face detector based on the small
# faces dataset in the examples/faces directory.  This means you need to supply
# the path to this faces folder as a command line argument so we will know
# where it is.
if len(sys.argv) != 5:
    print(
        "Give the path to the examples/faces directory as the argument to this "
        "program. For example, if you are in the python_examples folder then "
        "execute this program by running:\n"
        "    ./train_shape_predictor.py ../faces")
    exit()
image_folder = sys.argv[1]
checkpoint_folder = sys.argv[2]
result_folder = sys.argv[3]
Num_landmarks = int(sys.argv[4])
# Now let's use it as you would in a normal application.  First we will load it
# from disk. We also need to load a face detector to provide the initial
# estimate of the facial location.
predictor = dlib.shape_predictor(checkpoint_folder+"/predictor.dat")
from skimage import io as ioSK
import io
from contextlib import redirect_stdout
import numpy as np

if not os.path.exists(result_folder):
    os.makedirs(result_folder)


# Now let's run the detector and shape_predictor over the images in the faces
# folder and display the results.
print("Showing detections and predictions on the images in the faces folder...")

for f in glob.glob(os.path.join(image_folder, "*.jpg")):
    print("Processing file: {}".format(f))
    #img = dlib.load_rgb_image(f)
    img = ioSK.imread(f)


    # Ask the detector to find the bounding boxes of each face. The 1 in the
    # second argument indicates that we should upsample the image 1 time. This
    # will make everything bigger and allow us to detect more faces.
    dets=dlib.rectangle(left=1, top=1, right=255,  bottom=255)
    ### My comment: dets would be tuple of dlib.rectangles object contain 
    ## multi rectagls and corresponing points

    
    
    newLandmarks=np.zeros((Num_landmarks,3),dtype=np.float16)
    shape = predictor(img, dets)
    for k in range(Num_landmarks):
        # print('-',k)
        # print(shape.part(k))

        h = io.StringIO()
        with redirect_stdout(h):
            print(shape.part(k) )
        out = h.getvalue()
        # print(out)
        ind_n=out.find('\n', 0, len(out))
        ind_comma=out.find(',', 0, len(out))
        # print(ind_comma,ind_n)
        # print(out[1:ind_comma])
        # print(out[ind_comma+2:ind_n-1])
        newLandmarks[k,0]=k+1
        newLandmarks[k,1]=int(out[1:ind_comma])
        newLandmarks[k,2]=int(out[ind_comma+2:ind_n-1])
    # Draw the face landmarks on the screen.


    ind=f.rfind('\\')
    FileName=f[ind:]    


    fig=plt.figure()
    plt.imshow(img)
    plt.scatter(newLandmarks[:,1],newLandmarks[:,2], marker='x',color='blue')
    fig.savefig(result_folder+'/'+FileName)
    plt.close()


    np.savetxt(result_folder+'/'+FileName[:-4]+'_pred.csv', 
                   newLandmarks , delimiter=",", fmt='%i')
    # np.savetxt(result_folder+FileName+'_true.csv', 
    #                newLandmarks_true , delimiter=",", fmt='%i')

    #dlib.hit_enter_to_continue()
