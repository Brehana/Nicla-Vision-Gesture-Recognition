# Nicla Vision Gesture Recognition

## Human Introduction — INT8 Quantization Broken on OpenMV v4.8.1
Hey there, Brehana here. I wanted to chime in before my robot takes over to talk about an issue I discovered while working with the Arduino Nicla Vision through OpenMV v4.8.1. OpenMV seems to refuse to load any INT8 or UINT8 quantized TFLite model, throwing a `Failed to allocate tensors` error regardless of model size. A float model of identical architecture loads and runs fine. See the **Known Issues** section below for full details and reproduction steps.

Also, the Nicla Vision is very fragile. I had to reflash the firmware several times. Alright, handing it back to Copilot.

## Project Overview
Edge AI gesture recognition project for **Arduino Nicla Vision / OpenMV** that classifies hand gestures as:

- `LEFT`
- `RIGHT`
- `NONE`

The repository includes data capture and on-device inference scripts, a training notebook, and exported TensorFlow Lite models.

## Requirements

- **Hardware:** Arduino Nicla Vision
- **Firmware:** OpenMV v4.8.1 / MicroPython v1.26.0-77 / STM32H747
- **IDE:** [OpenMV IDE](https://openmv.io/pages/download)
- **Training:** Google Colab (notebook is Colab-ready)
- **TensorFlow:** 2.x (tested on the default Colab TF version)

## Repository Contents

- `dataset_capture.py` — OpenMV script to capture grayscale images per label on device storage.
- `gesture_inference.py` — OpenMV runtime inference loop using `gesture_float.tflite`.
- `nicla_contiguous_memory_analyzer.py` — utility to estimate largest contiguous allocatable block and test model loading.
- `gesture_float.tflite` — exported float TFLite model used on device.
- `gesture_int8.tflite` — INT8 quantized model included for bug reproduction purposes only. **This model will not run on OpenMV v4.8.1.**
- `reproduce_int8_bug.ipynb` — Colab notebook to rebuild both models from scratch and reproduce the INT8 failure on device.
- `dataset.zip` — captured training dataset archive.
- `EdgeAI_OpenMV_Gesture_Assignment_Student.ipynb` — end-to-end notebook (capture guidance, training, export, evaluation).
- `Gesture Inference Program on the Arduino Nicla Vison.pdf` — supporting project document.

## Dataset Details

- **Classes:** `LEFT`, `RIGHT`, `NONE`
- **Samples per class:** 300
- **Image format:** 32×32 grayscale PGM
- **Capture device:** Arduino Nicla Vision via `dataset_capture.py`
- **Capture resolution:** 64×64 (`B64X64`), downscaled 0.5× on-device to 32×32 before saving

## End-to-End Workflow

1. Capture gesture images on Nicla Vision/OpenMV (`dataset_capture.py`).
2. Export dataset to PC and train in the notebook (`EdgeAI_OpenMV_Gesture_Assignment_Student.ipynb`).
3. Export/download `gesture_float.tflite`.
4. Copy model to device storage (`/flash/gesture_float.tflite`).
5. Run `gesture_inference.py` on the board for live predictions.

## Device Setup (OpenMV IDE)

1. Connect the Nicla Vision board.
2. Open OpenMV IDE.
3. Open `dataset_capture.py` or `gesture_inference.py` in the IDE.
4. Use the IDE's file manager to save files to board flash:
   - Script: `/flash/main.py`
   - Model: `/flash/gesture_float.tflite`
5. Run the script and monitor serial output.

## Inference Behavior

`gesture_inference.py`:

- Captures grayscale camera frames (`B64X64`) and rescales to 32×32 — required to match the model's input shape of `(32, 32, 1)`.
- Runs model prediction with `ml.Model("/flash/gesture_float.tflite")`.
- Uses label order: `["LEFT", "RIGHT", "NONE"]` — must match training order exactly.
- Prints the top gesture when confidence is at or above `0.7`, otherwise prints an uncertain result with the raw score.

## Known Issues

### INT8 Quantization Fails on OpenMV v4.8.1

**Hardware:** Arduino Nicla Vision
**Firmware:** OpenMV v4.8.1 / MicroPython v1.26.0-77 / STM32H747

**Symptom:**
Any fully INT8-quantized TFLite model fails to load on the Nicla with:
```
OSError: Failed to allocate tensors
```
This occurs regardless of model size. The TFLite file itself is valid — `tf.lite.Interpreter` allocates tensors successfully in Colab.

**Workaround:**
Use a float TFLite model. A float model of identical architecture loads and runs correctly on the same hardware.

**Reproduction:**
See [`reproduce_int8_bug.ipynb`](./reproduce_int8_bug.ipynb) — a self-contained Colab notebook that builds both models, confirms INT8 dtypes, and includes the on-device inference script to trigger the error.
A pre-built `gesture_int8.tflite` is also included in this repo so reproduction does not require running the notebook.

## Notes

- Ensure model label order matches training/export order exactly or predictions will be misclassified.
- Camera exposure, gain, and white balance settings are fixed in scripts for more stable and consistent capture/inference.
- The scripts are intended for the OpenMV MicroPython environment on Nicla Vision.
