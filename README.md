# Nicla Vision Gesture Recognition

## Human Introduction - Nicla only rejects .tflite models quanticized to int8 or uint8 
Hey there, Brehana here. I wanted to chime in before my robot takes over to talk about an issue I discovered while working with the Arduino Nicla Vision. The Nicla Vision seems to refuse to allocate tensors for .tflite models quanticized some data types, regardless of whether the model fits within the memory constraints or not. Attempting to load a .tflite model quanticized to int8 or uint8 results in an error stating it failed to allocate tensor's for the model. You will notice in this repo I included a memory probing script (nicla_contiguous_memory_analyzer.py) that I was using to troubleshoot what I thought was a memory issue. The error it throws is misleading, as it's the same error it throws for trying to load a model that's too big. by dumb luck I discovered that it will accept mdels quanticized to float32, which this project ends up using.

Also, the Nicla Vision is very fragile. I had to reflash the firmware several times. Alright, handing it back to Copilot.

## Robot Introduction.
Edge AI gesture recognition project for **Arduino Nicla Vision / OpenMV** that classifies hand gestures as:

- `LEFT`
- `RIGHT`
- `NONE`

The repository includes data capture and on-device inference scripts, a training notebook, and an exported TensorFlow Lite model.

## Repository Contents

- `dataset_capture.py` — OpenMV script to capture grayscale images per label on device storage.
- `gesture_inference.py` — OpenMV runtime inference loop using `gesture_float.tflite`.
- `nicla_contiguous_memory_analyzer.py` — utility to estimate largest contiguous allocatable block and test model loading.
- `gesture_float.tflite` — exported TFLite model used on device.
- `dataset.zip` — captured training dataset archive.
- `EdgeAI_OpenMV_Gesture_Assignment_Student.ipynb` — end-to-end notebook (capture guidance, training, export, evaluation).
- `Gesture Inference Program on the Arduino Nicla Vison.pdf` — supporting project document.

## End-to-End Workflow

1. Capture gesture images on Nicla Vision/OpenMV (`dataset_capture.py`).
2. Export dataset to PC and train in the notebook (`EdgeAI_OpenMV_Gesture_Assignment_Student.ipynb`).
3. Export/download `gesture_float.tflite`.
4. Copy model to device storage (`/flash/gesture_float.tflite`).
5. Run `gesture_inference.py` on the board for live predictions.

## Device Setup (OpenMV IDE)

1. Connect the Nicla Vision board.
2. Open OpenMV IDE.
3. Copy either `dataset_capture.py` or `gesture_inference.py` into the IDE editor.
4. Save script/model to board flash as needed:
   - Script: `/flash/<script>.py`
   - Model: `/flash/gesture_float.tflite`
5. Run the script and monitor serial output.

## Inference Behavior

`gesture_inference.py`:

- Captures grayscale camera frames (`B64X64`), rescales to 32×32.
- Runs model prediction with `ml.Model("/flash/gesture_float.tflite")`.
- Uses label order: `["LEFT", "RIGHT", "NONE"]`.
- Prints the top gesture when score is above confidence threshold (`0.7`), otherwise prints an uncertain result.

## Notes

- Ensure model label order matches training/export order.
- Camera exposure/gain settings are fixed in scripts for more stable capture/inference.
- The scripts are intended for the OpenMV MicroPython environment on Nicla Vision.
