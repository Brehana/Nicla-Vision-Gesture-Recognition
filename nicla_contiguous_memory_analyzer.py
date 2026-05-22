import gc

gc.collect()
gc.collect()
gc.collect()

def find_largest_contiguous_block():
    low  = 1024
    high = 1024 * 1024
    largest = 0
    while low <= high:
        mid = (low + high) // 2
        try:
            buf = bytearray(mid)
            del buf
            gc.collect()
            largest = mid
            low = mid + 1
        except MemoryError:
            high = mid - 1
    return largest

print("--- BEFORE load ---")
print("Total free:               %d bytes (%d KB)" % (gc.mem_free(), gc.mem_free() // 1024))
largest = find_largest_contiguous_block()
print("Largest contiguous block: %d bytes (%d KB)" % (largest, largest // 1024))

import ml
gc.collect()
gc.collect()

try:
    model = ml.Model("gesture_hybrid.tflite")
    print("\nModel loaded successfully!")
except ValueError as e:
    print("\nFailed:", e)

print("\n--- AFTER load attempt ---")
print("Total free:               %d bytes (%d KB)" % (gc.mem_free(), gc.mem_free() // 1024))
largest = find_largest_contiguous_block()
print("Largest contiguous block: %d bytes (%d KB)" % (largest, largest // 1024))
