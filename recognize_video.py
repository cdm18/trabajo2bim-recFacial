# recognize_video.py
from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
import argparse
import imutils
import pickle
import time
import cv2

# Construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-e", "--encodings", required=True,
	help="path to serialized db of facial encodings")
ap.add_argument("-o", "--output", type=str,
	help="path to output video")
ap.add_argument("-y", "--display", type=int, default=1,
	help="whether or not to display output frame to screen")
ap.add_argument("-d", "--detection-method", type=str, default="hog",
	help="face detection model to use: either 'hog' or 'cnn'")
ap.add_argument("-t", "--tolerance", type=float, default=0.5,
	help="tolerance for face matching (lower = stricter, default 0.5)")
args = vars(ap.parse_args())

# Load the known faces and embeddings
print("[INFO] loading encodings...")
data = pickle.loads(open(args["encodings"], "rb").read())

# Initialize the video stream and pointer to output video file, then
# allow the camera sensor to warm up
print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
time.sleep(2.0)

# Start the FPS counter
fps = FPS().start()

# Loop over frames from the video file stream
while True:
	# Grab the frame from the threaded video stream
	frame = vs.read()
	
	# Resize the frame to have a width of 750px (to speed up processing)
	frame = imutils.resize(frame, width=750)
	
	# Convert the input frame from BGR to RGB (for dlib)
	rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

	# Detect the (x, y)-coordinates of the bounding boxes
	# corresponding to each face in the input frame
	boxes = face_recognition.face_locations(rgb,
		model=args["detection_method"])
	
	# Compute the facial embeddings for each face
	encodings = face_recognition.face_encodings(rgb, boxes)
	names = []
	confidences = []

	# Loop over the facial embeddings
	for encoding in encodings:
		# Calculate face distances (lower = more similar)
		distances = face_recognition.face_distance(data["encodings"], encoding)
		
		# Compare faces with the specified tolerance
		matches = face_recognition.compare_faces(data["encodings"],
			encoding, tolerance=args["tolerance"])
		name = "Unknown"
		confidence = 0.0

		# Check to see if we have found a match
		if True in matches:
			# Find the indexes of all matched faces
			matchedIdxs = [i for (i, b) in enumerate(matches) if b]
			
			# Find the match with the smallest distance (best match)
			best_match_idx = None
			best_distance = 1.0
			
			for i in matchedIdxs:
				if distances[i] < best_distance:
					best_distance = distances[i]
					best_match_idx = i
			
			if best_match_idx is not None:
				name = data["names"][best_match_idx]
				# Convert distance to confidence percentage (0.0 = 100%, 1.0 = 0%)
				confidence = (1.0 - best_distance) * 100
		
		# Update the list of names and confidences
		names.append(name)
		confidences.append(confidence)

	# Loop over the recognized faces
	for ((top, right, bottom, left), name, conf) in zip(boxes, names, confidences):
		# Choose color based on recognition
		if name == "Unknown":
			color = (0, 0, 255)  # Red for unknown
		else:
			color = (0, 255, 0)  # Green for known
		
		# Draw the predicted face name on the image
		cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
		y = top - 15 if top - 15 > 15 else top + 15
		
		# Show name with confidence percentage
		if name != "Unknown":
			label = f"{name} ({conf:.1f}%)"
		else:
			label = name
		cv2.putText(frame, label, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
			0.65, color, 2)

	# Check if we are supposed to display the output frame to the screen
	if args["display"] > 0:
		cv2.imshow("Frame", frame)
		key = cv2.waitKey(1) & 0xFF

		# If the `q` key was pressed, break from the loop
		if key == ord("q"):
			break

	# Update the FPS counter
	fps.update()

# Stop the timer and display FPS information
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# Cleanup
cv2.destroyAllWindows()
vs.stop()
