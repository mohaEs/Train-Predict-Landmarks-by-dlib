This is how to train and use dlib shape predictior for landmark detection/localization
I wanted to train it on my own dataset which is not face and I dont have more than one subject in each image.
Also I was not interested to use any detector before landmark predictior.
So, I tried to modify following codes to reach my aims.

setups:

Take care! 
create and exploit new environment for your setup!
because dlib is not compatibale with many new version of other papckages and it will downgrade them seriously.

My python version was 3.5.2
dlib and cv2 shoudl be installed.
my versions were:
dlib 19.4.0
opencv-contrib-python         4.1.0.25
opencv-python                 4.1.0.25


data preparation:

My dataset contains images with size 256x256 and landmarks were localized on it.
first I need to create the xml file for training should be created based on the dlib template.
You can modify code which is on MATLAB for generating your own xml file:


The created xml file would be placed at the path_trainin_png folder. Note that, the bounding box for all images are fixed around image which is one of my goal.
Also note that, in dlib x and y are assumed such as follow:
![Alt text](./Results/Untitled_picture.png?raw=true "Title")

Trainig predicting:

For training: suppose or set the path of input_folder (folder contains images and xml file) 
and output_folder (folder for saving trained model)

> python Pr_Train.py input_folder output_folder
e.g.
> python Pr_Train.py ./NewFaces256 ./Trained_Model

For prediction: suppose or set input_folder(folder contains test images (xml is not required)),
trained checkpoint_folder (folder contains trained model), output_folder (folder for saving results)
and Num_landmarks integer shows the number of landmarks which you trained (for this face example it is 68), 

> python Pr_test.py input_folder checkpoint_folder output_folder Num_landmarks
e.g.
> python Pr_test.py ./NewFaces256 ./Trained_Model ./Results 68

result image file and corresponding csv file would be created.

![Alt text](./Results/47858348.jpg?raw=true "Title")
![Alt text](./Results/45289597.jpg?raw=true "Title")
and notice that, as expected, because we do not use any detector it can not find faces in larger images: 
![Alt text](./Results/2007_007763.jpg?raw=true "Title")


Notice that, on your own dataset, the dlib predictor may not preserve the landmark orderings. in my case:
![Alt text](./Results/ordering_changes.png?raw=true "Title")



