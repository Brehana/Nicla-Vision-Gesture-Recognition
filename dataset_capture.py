import sensor, image, time, os

# Configure camera
sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.B64X64)
sensor.set_auto_gain(False, gain_db=0)
sensor.set_auto_whitebal(False)
sensor.set_auto_exposure(False, exposure_us=25000)
sensor.skip_frames(time=2000)

# Dataset configuration
LABELS = ["LEFT", "RIGHT", "NONE"]
SAMPLES_PER_LABEL = 1
CAPTURE_INTERVAL_MS = 100
PREVIEW_SECONDS = 15
BASE_PATH = "/flash"

# ----------------------------
# Helper: clear a directory
# ----------------------------
def clear_directory(path):
    try:
        for fname in os.listdir(path):
            os.remove("%s/%s" % (path, fname))
        print("Cleared:", path)
    except OSError:
        print("Could not clear:", path)

# ----------------------------
# Helper: countdown with live
# preview in frame buffer
# ----------------------------
def live_preview_countdown(label, seconds):
    print("\n=============================")
    print("LABEL:", label)
    print("Position yourself now.")
    print("Capturing starts in", seconds, "seconds...")
    print("Watch the frame buffer in OpenMV IDE.")

    start = time.ticks_ms()
    last_printed = seconds

    while True:
        sensor.snapshot()

        elapsed = time.ticks_diff(time.ticks_ms(), start) // 1000
        remaining = seconds - elapsed

        if remaining != last_printed and remaining >= 0:
            print(remaining, "seconds remaining...")
            last_printed = remaining

        if elapsed >= seconds:
            print("GO — starting capture for:", label)
            break

# ----------------------------
# Create/clean directories
# ----------------------------
print("Preparing directories...")
for lbl in LABELS:
    path = "%s/%s" % (BASE_PATH, lbl)
    try:
        os.mkdir(path)
        print("Created:", path)
    except OSError:
        # already exists — clear it out
        clear_directory(path)

# ----------------------------
# Main capture loop
# ----------------------------
for label in LABELS:
    path = "%s/%s" % (BASE_PATH, label)

    live_preview_countdown(label, PREVIEW_SECONDS)

    counter = 0     # always start from 0 after cleanup
    print("CAPTURING", SAMPLES_PER_LABEL, "images for:", label)

    while counter < SAMPLES_PER_LABEL:
        img = sensor.snapshot()
        img = img.copy(x_scale=0.5, y_scale=0.5)   # 64x64 → 32x32
        filename = "%s/%03d.pgm" % (path, counter)
        img.save(filename)
        os.sync()
        counter += 1
        print("Saved:", filename, "(%d/%d)" % (counter, SAMPLES_PER_LABEL))
        time.sleep_ms(CAPTURE_INTERVAL_MS)

    print("Done with label:", label)

os.sync()
print("\n=== ALL LABELS CAPTURED ===")
