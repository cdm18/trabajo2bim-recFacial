# train_model.py
from imutils import paths
import face_recognition
import argparse
import pickle
import cv2
import os

# Construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--dataset", required=True,
	help="path to input directory of faces + images")
ap.add_argument("-e", "--encodings", required=True,
	help="path to serialized db of facial encodings")
ap.add_argument("-d", "--detection-method", type=str, default="hog",
	help="face detection model to use: either 'hog' or 'cnn'")
args = vars(ap.parse_args())

# Grab the paths to the input images in our dataset
print("[INFO] quantifying faces...")
imagePaths = list(paths.list_images(args["dataset"]))

# Initialize the list of known encodings and known names
knownEncodings = []
knownNames = []

# Loop over the image paths
for (i, imagePath) in enumerate(imagePaths):
	# Extract the person name from the image path
	print("[INFO] processing image {}/{}".format(i + 1,
		len(imagePaths)))
	name = imagePath.split(os.path.sep)[-2]

	# Load the input image and convert it from RGB (OpenCV ordering)
	# to dlib ordering (RGB)
	image = cv2.imread(imagePath)
	if image is None:
		print("[WARNING] Could not read image: {}".format(imagePath))
		continue
	rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

	# Detect the (x, y)-coordinates of the bounding boxes
	# corresponding to each face in the input image
	boxes = face_recognition.face_locations(rgb,
		model=args["detection_method"])

	# Compute the facial embedding for the face
	encodings = face_recognition.face_encodings(rgb, boxes)

	# Loop over the encodings
	for encoding in encodings:
		# Add each encoding + name to our set of known names and
		# encodings
		knownEncodings.append(encoding)
		knownNames.append(name)

# Dump the facial encodings + names to disk
print("[INFO] serializing encodings...")
data = {"encodings": knownEncodings, "names": knownNames}
f = open(args["encodings"], "wb")
f.write(pickle.dumps(data))
f.close()
