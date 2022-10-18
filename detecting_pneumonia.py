# -*- coding: utf-8 -*-
"""colab

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/github/Applied-Machine-Learning-2022/project-5-dasa-uark/blob/santi-4/colab.ipynb

#### Copyright 2020 Google LLC.
"""

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""# Image Classification Project

In this project we will build an image classification model and use the model to identify if the lungs pictured indicate that the patient has pneumonia. The outcome of the model will be true or false for each image.

The [data is hosted on Kaggle](https://www.kaggle.com/rob717/pneumonia-dataset) and consists of 5,863 x-ray images. Each image is classified as 'pneumonia' or 'normal'.

## Ethical Considerations

We will frame the problem as:

> *A hospital is having issues correctly diagnosing patients with pneumonia. Their current solution is to have two trained technicians examine every patient scan. Unfortunately, there are many times when two technicians are not available, and the scans have to wait for multiple days to be interpreted.*
>
> *They hope to fix this issue by creating a model that can identify if a patient has pneumonia. They will have one technician and the model both examine the scans and make a prediction. If the two agree, then the diagnosis is accepted. If the two disagree, then a second technician is brought in to provide their analysis and break the tie.*

Discuss some of the ethical considerations of building and using this model. 

* Consider potential bias in the data that we have been provided. 
* Should this model err toward precision or accuracy?
* What are the implications of massively over-classifying patients as having pneumonia?
* What are the implications of massively under-classifying patients as having pneumonia?
* Are there any concerns with having only one technician make the initial call?

The questions above are prompts. Feel free to bring in other considerations you might have.

### **Student Solution**

#Should this model err toward percision or accuracy? 
The model should eer towards accuracy because since we are determining if a patient has pneumonia or not, it's best if we be as close to our target value as possible so that we don't have any false positives or false negatives.

#What are the implications of massively over-classifying patients as having pneumonia?
Over classifying reduces the effeciency and accuracy of the model. This is not good considering the fact that we are trying to predict if a patient has pneumonia or not.

#What are the implications of massively over-classifying patients as having pneumonia?

By over-classifying patients as having pneumonia, when the system is put into place the likely hood for false-positives would increase as models would be trained on data in which non-pneumonic patients are categorized as pneumonic. Additionally, in terms of how this would be implemented in the health care system, if the systems result disagrees with the technician, then they would require an additional technician to break the tie which it seems they already do not have the resources for, causing for added burden on the healthcare system within the hospital while the system was meant to decrease the burden.

#What are the implications of massively under-classifying patients as having pneumonia?

By under-classifying patients as having pneumonia, patients could get screened and then possibly be told that they're non-pneumonic while in actuality being sick and increase their risk of a fatal outcome. Additionally, as with the situation of over-classifying, if the systems result disagrees with the technician, then they would require an additional technician to break the tie which would burden the healthcare system within the hospital, which is counter intuitive to the purpose of the system. 

#Are there any concerns with having only one technician make the initial call?

Depending on the accuracy of the model, the technician could continue to perpetuate the issues of misdiagnosis that has already been occurring. The technicians could have varying degrees of experience, which would lead to diagnoses in which the technician would be delayed in a decision due to a lack of sufficient information, or error due to not having had to diagnose this type of histopathology.

Should this model err toward percision or accuracy? The model should eer towards accuracy because since we are determining if a patient has pneumonia or not, it's best if we be as close to our target value as possible so that we don't have any false positives or false negatives.

What are the implications of massively over-classifying patients as having pneumonia? Over classifying reduces the effeciency and accuracy of the model. This is not good considering the fact that we are trying to predict if a patient has pneumonia or not.

---

## Modeling

In this section of the lab, you will build, train, test, and validate a model or models. The data is the ["Detecting Pneumonia" dataset](https://www.kaggle.com/rob717/pneumonia-dataset). You will build a binary classifier that determines if an x-ray image has pneumonia or not.

You'll need to:

* Download the dataset
* Perform EDA on the dataset
* Build a model that can classify the data
* Train the model using the training portion of the dataset. (It is already split out.)
* Test at least three different models or model configurations using the testing portion of the dataset. This step can include changing model types, adding and removing layers or nodes from a neural network, or any other parameter tuning that you find potentially useful. Score the model (using accuracy, precision, recall, F1, or some other relevant score(s)) for each configuration.
* After finding the "best" model and parameters, use the validation portion of the dataset to perform one final sanity check by scoring the model once more with the hold-out data.
* If you train a neural network (or other model that you can get epoch-per-epoch performance), graph that performance over each epoch.

Explain your work!

> *Note: You'll likely want to [enable GPU in this lab](https://colab.research.google.com/notebooks/gpu.ipynb) if it is not already enabled.*

If you get to a working solution you're happy with and want another challenge, you'll find pre-trained models on the [landing page of the dataset](https://www.kaggle.com/paultimothymooney/detecting-pneumonia-in-x-ray-images). Try to load one of those and see how it compares to your best model.

Use as many text and code cells as you need to for your solution.

### **Student Solution**
"""

#imports
import pandas as pd
import numpy as np
import tensorflow as tf
import random
import matplotlib.pyplot as plt
from keras import callbacks
from keras.models import Sequential
from keras.layers import Dense, Conv2D , MaxPooling2D , Flatten , Dropout , BatchNormalization
from keras.preprocessing.image import ImageDataGenerator

# Downloading Zip
! chmod 600 kaggle.json && (ls ~/.kaggle 2>/dev/null || mkdir ~/.kaggle) && cp kaggle.json ~/.kaggle/ && echo 'Done'
! kaggle datasets download paultimothymooney/chest-xray-pneumonia
! ls
! unzip chest-xray-pneumonia.zip

"""---"""

#Paths
train_path= ('/content/chest_xray/train')
test_path= ('/content/chest_xray/test')
val_path= ('/content/chest_xray/val')

#EDA and Image Preproccessing
train_data = tf.keras.preprocessing.image_dataset_from_directory(
                                                                train_path,
                                                                batch_size = 32
)
#Image normalization
train_datagen = ImageDataGenerator(rescale = 1./255,
                                   shear_range = 0.2,
                                   zoom_range = 0.2,
                                   horizontal_flip = True)

test_datagen = ImageDataGenerator(rescale = 1./255) 

val_generator = test_datagen.flow_from_directory(val_path,
    target_size=(64, 64),
    batch_size=32,
    class_mode='binary')

#Test and Training set from folder
test_set = test_datagen.flow_from_directory(test_path,
                                            target_size = (64, 64),
                                            batch_size = 32,
                                            class_mode = 'binary')
train_set = test_datagen.flow_from_directory(train_path,
                                            target_size = (64, 64),
                                            batch_size = 32,
                                            class_mode = 'binary')

#Allows me to set up my class name and display 12 images both with pneumonia and without
classes = train_data.class_names
plt.figure(figsize = (10, 10))
for images, labels in train_data.take(1):
    for i in range(12):
        plt.subplot(3, 4, i + 1)
        plt.imshow(images[i].numpy().astype("uint8"))
        plt.title(classes[labels[i]])
        plt.axis(False)

#Setting up Early Stopping
early_stopping = callbacks.EarlyStopping(
    monitor='val_loss',
    min_delta=0.001,
    patience=5,
    restore_best_weights=True,
)

"""#Model 1"""

#Constructing layers of CNN
#Model 1
model = Sequential([
  tf.keras.layers.experimental.preprocessing.Rescaling(1./255, input_shape=(64, 64, 3)),
  tf.keras.layers.Conv2D(16, (3,3), padding='same', activation='relu'),
  tf.keras.layers.MaxPooling2D(),
  tf.keras.layers.Conv2D(32, (3,3), padding='same', activation='relu'),
  tf.keras.layers.MaxPooling2D(),
  tf.keras.layers.Conv2D(64, (3,3), padding='same', activation='relu'),
  tf.keras.layers.MaxPooling2D(),
  tf.keras.layers.Conv2D(128, (3,3), padding='same', activation='relu'),
  tf.keras.layers.MaxPooling2D(),
  tf.keras.layers.Flatten(),
  tf.keras.layers.Dense(256, activation='relu'),
  tf.keras.layers.Dense(1, activation='sigmoid')
])

# Compile the Neural Network
model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

#Allows us to view our CNN set up
model.summary()

history = model.fit(train_set,
                         steps_per_epoch = 163,
                         epochs = 5,
                         validation_data = val_generator,
                         validation_steps = 624,
                         callbacks=[early_stopping]
                    )

#low 80's percentage accuracy
accuracy = model.evaluate(test_set)
print('The model has an accuracy of:',accuracy[1]*100, '%')

#Model Accuracy 
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Model Accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Training set', 'Validation set'], loc='upper left')
plt.show()

#Model Loss 
plt.plot(history.history['val_loss'])
plt.plot(history.history['loss'])
plt.title('Model Loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Training set', 'Test set'], loc='upper left')
plt.show()

"""#Model 2 using VGG16"""

#New Pretrained Model
#Very Deep Convolutional Networks for Large-Scale Image Recognition (VGG16)
#Model 2
from tensorflow.keras.applications.vgg16 import VGG16

pre_model = VGG16(input_shape = (64, 64, 3), # Shape of our images
include_top = False, # Leave out the last fully connected layer
weights = 'imagenet')

for layer in pre_model.layers:
    layer.trainable = False

#Layer Manipulation
x = tf.keras.layers.Flatten()(pre_model.output)
x = tf.keras.layers.Dense(512, activation='relu')(x)
x = tf.keras.layers.Dropout(0.5)(x)
x = tf.keras.layers.Dense(1, activation='sigmoid')(x)
x = tf.keras.layers.Dropout(0.5)(x)
x = tf.keras.layers.Dense(1, activation='sigmoid')(x)

model2 = tf.keras.models.Model(pre_model.input, x)

#Compile the model
model2.compile(optimizer = tf.keras.optimizers.RMSprop(learning_rate=0.0001),
              loss = 'binary_crossentropy',
              metrics = ['accuracy'])

#Fit the model
history2 = model2.fit(train_set,
                     validation_data = val_generator,
                     steps_per_epoch = 100,
                     epochs = 10,
                     callbacks=[early_stopping])

#Output the Accuracy (Mid 80's percentage accuracy using VGG16)
accuracy1 = model2.evaluate(test_set)
print('The model has an accuracy of:',accuracy1[1]*100, '%')

#Model Accuracy 
plt.plot(history2.history['accuracy'])
plt.plot(history2.history['val_accuracy'])
plt.title('Model Accuracy Using VGG16')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Training set', 'Validation set'], loc='upper left')
plt.show()

#Model Loss 
plt.plot(history2.history['val_loss'])
plt.plot(history2.history['loss'])
plt.title('Model Loss Using VGG16')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Training set', 'Test set'], loc='upper left')
plt.show()

"""#Model 3"""

#Model 3
model3 = Sequential([
  tf.keras.layers.experimental.preprocessing.Rescaling(1./255, input_shape=(64, 64, 3)),
  tf.keras.layers.Flatten(),
  tf.keras.layers.Dense(128, activation='relu'),
  tf.keras.layers.Dense(128, activation='relu'),
  tf.keras.layers.Dense(128, activation='relu'),
  tf.keras.layers.Dense(1, activation='sigmoid')
])

# Compile the Neural Network
model3.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

#Fit the model
history3 = model3.fit(train_set,
                     validation_data = val_generator,
                     steps_per_epoch = 100,
                     epochs = 10,
                     callbacks=[early_stopping])

#Output the Accuracy (low 80's percentage accuracy)
accuracy2 = model3.evaluate(test_set)
print('The model has an accuracy of:',accuracy2[1]*100, '%')

#Model Accuracy 
plt.plot(history3.history['accuracy'])
plt.plot(history3.history['val_accuracy'])
plt.title('Model Accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Training set', 'Validation set'], loc='upper left')
plt.show()

#Model Loss 
plt.plot(history3.history['val_loss'])
plt.plot(history3.history['loss'])
plt.title('Model Loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Training set', 'Test set'], loc='upper left')
plt.show()

"""#Model 4"""

#Model 4
model4 = Sequential([
  tf.keras.layers.experimental.preprocessing.Rescaling(1./255, input_shape=(64, 64, 3)),
  tf.keras.layers.Flatten(),
  tf.keras.layers.Dense(512, activation='relu'),
  tf.keras.layers.Dense(256, activation='relu'),
  tf.keras.layers.Dense(128, activation='relu'),
  tf.keras.layers.Dense(1, activation='sigmoid')
])

# Compile the Neural Network
model4.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])

#Fit the model
history4 = model4.fit(train_set,
                     validation_data = val_generator,
                     steps_per_epoch = 100,
                     epochs = 100,
                     callbacks=[early_stopping])

#Output the Accuracy (80's percentage accuracy)
accuracy3 = model4.evaluate(test_set)
print('The model has an accuracy of:',accuracy3[1]*100, '%')

#Model Accuracy 
plt.plot(history4.history['accuracy'])
plt.plot(history4.history['val_accuracy'])
plt.title('Model Accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Training set', 'Validation set'], loc='upper left')
plt.show()

#Model Loss 
plt.plot(history4.history['val_loss'])
plt.plot(history4.history['loss'])
plt.title('Model Loss Using VGG16')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Training set', 'Test set'], loc='upper left')
plt.show()

"""Our best performing model was the pre-trained model that used VGG16. It had an accuracy of around 86.5%. Our sequential models were consistently scoring between 80% and 84%."""