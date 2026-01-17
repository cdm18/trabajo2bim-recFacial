# Dataset Instructions

Please create a folder for each student inside this `dataset` directory.
The name of the folder should be the name of the student.
Inside each folder, place multiple images of that student (JPG or PNG).
We recommend **10 to 20 images** per person for better accuracy, covering different angles and lighting conditions.
However, the system can work with as few as 1 or 2 images.

Example structure:
```
dataset/
├── Juan_Perez/
│   ├── image1.jpg
│   ├── image2.jpg
│   └── ...
├── Maria_Lopez/
│   ├── photo_1.png
│   └── ...
└── ...
```
After populating these folders, run the training script:
`python train_model.py --dataset dataset --encodings encodings.pickle`
