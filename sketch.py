import numpy as np
import cv2
from tkinter import Tk, filedialog

# Initialize Tkinter root window but hide it
# This is necessary to use the filedialog without a visible Tkinter window.
root = Tk()
root.withdraw()
# Bring the file dialog to the front on all OS.
# This makes sure the dialog is not hidden behind other applications.
root.call('wm', 'attributes', '.', '-topmost', True)

# Open a file dialog to allow the user to select an image file.
# Filters for common image file types (JPG, JPEG, PNG, BMP).
img_path = filedialog.askopenfilename(
    title="Select an image file",
    filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")]
)

# Check if a file was selected. If not, print a message and exit.
if not img_path:
    print("No image selected. Exiting...")
    exit()

# Read the selected image using OpenCV (cv2.imread).
# OpenCV is generally preferred for image processing in Python due to its efficiency.
img = cv2.imread(img_path)

# Check if the image was loaded successfully.
# If img is None, it means the file path was invalid or the file was corrupted.
if img is None:
    print(f"Failed to load image from: {img_path}. Please check the file path and integrity. Exiting...")
    exit()

# Convert the loaded image from BGR (OpenCV's default) to grayscale.
# Grayscale is essential for sketch effects as it simplifies color information to intensity.
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Invert the grayscale image.
# This flips the light and dark values: black becomes white, white becomes black.
# This inverted image will serve as the 'blend' layer for the dodge effect.
inverted = 255 - gray

# Apply a Gaussian blur to the inverted image.
# The Gaussian blur smooths the image, which helps create the 'pencil stroke' effect.
# (0, 0) for ksize means the kernel size is automatically determined by sigmaX.
# sigmaX (standard deviation in X direction) controls the blur strength:
# - A smaller sigmaX results in sharper, finer lines.
# - A larger sigmaX results in softer, thicker lines.
# If sigmaX is too large, the inverted image becomes too uniform, which can lead to a black sketch.
# A value of 20 is a good starting point; experiment to find what works best for your images.
blurred = cv2.GaussianBlur(inverted, (0, 0), sigmaX=20)

# Define the dodge blend function.
# This function applies the 'color dodge' blend mode, which is commonly used
# for creating pencil sketch effects.
# 'front' is the base layer (original grayscale image).
# 'back' is the blend layer (inverted and Gaussian blurred image).
def dodge(front, back):
    # Convert inputs to float to ensure accurate floating-point division.
    # Add a small epsilon (1e-5) to the denominator to prevent division by zero,
    # which can occur if 'back' is exactly 255 (pure white).
    result = front.astype(float) * 255.0 / (255.0 - back.astype(float) + 1e-5)

    # Clamp values to a maximum of 255.
    # Any pixel value exceeding 255 (which can happen with the division) is set to 255.
    result[result > 255] = 255

    # This line ensures that areas which were pure white in the 'back' (inverted blurred) layer
    # also become pure white in the final result. This is often useful for backgrounds.
    result[back == 255] = 255

    # Convert the result back to an 8-bit unsigned integer (0-255 range).
    return result.astype('uint8')

# Create the sketch by applying the dodge blend.
# 'gray' (original grayscale) is the base layer.
# 'blurred' (inverted and blurred grayscale) is the blend layer.
sketch = dodge(gray, blurred)

# Construct the output file path.
# It appends '_sketch_hd' before the file extension.
output_path_parts = img_path.rsplit('.', 1)
output_path = f"{output_path_parts[0]}_sketch_hd.{output_path_parts[1]}"

# Save the generated sketch image to the specified output path.
cv2.imwrite(output_path, sketch)

# Print a confirmation message with the saved file path.
print(f"HD Sketch saved as: {output_path}")

# Optional: You can uncomment the lines below for debugging purposes
# to see the intermediate steps and the final sketch.
# cv2.imshow("Original Image", img)
# cv2.imshow("Grayscale", gray)
# cv2.imshow("Inverted Grayscale", inverted)
# cv2.imshow("Blurred Inverted", blurred)
# cv2.imshow("Final Sketch", sketch)
# cv2.waitKey(0) # Waits indefinitely for a key press
# cv2.destroyAllWindows() # Closes all OpenCV windows
