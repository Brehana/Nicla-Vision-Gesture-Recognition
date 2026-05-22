import sensor, image, time, tf

# ----------------------------
# Camera setup
# ----------------------------
import sensor, image, time, ml

# ----------------------------
# Camera setup
# ----------------------------
sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.B64X64)
sensor.set_auto_gain(False, gain_db=0)
sensor.set_auto_whitebal(False)
sensor.set_auto_exposure(False, exposure_us=15000)
sensor.skip_frames(time=2000)

# ----------------------------
# Load model
# ----------------------------
model = ml.Model("/flash/gesture_float.tflite")  # ← ml.Model() not tf.load()

# ----------------------------
# Labels — must match training order
# ----------------------------
LABELS = ["LEFT", "RIGHT", "NONE"]
CONFIDENCE_THRESHOLD = 0.7

print("Model loaded. Starting inference...")

# ----------------------------
# Inference loop
# ----------------------------
while True:
    img = sensor.snapshot()

    img_resized = img.copy(x_scale=0.5, y_scale=0.5)

    raw = model.predict([img_resized])
    scores = raw[0][0]  # shape (3,)

    best_idx = 0
    best_score = scores[0]
    for i in range(1, len(scores)):
        if scores[i] > best_score:
            best_score = scores[i]
            best_idx = i

    label = LABELS[best_idx]

    if best_score >= CONFIDENCE_THRESHOLD:
        print("Gesture: {} ({:.2f}%)".format(label, best_score * 100))
    else:
        print("Uncertain ({} at {:.2f}%)".format(label, best_score * 100))

    time.sleep_ms(100)
