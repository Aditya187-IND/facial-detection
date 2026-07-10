import cv2

def compare_images(image_path1, image_path2):
    # 1. Load images in grayscale
    img1 = cv2.imread(image_path1, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(image_path2, cv2.IMREAD_GRAYSCALE)

    if img1 is None or img2 is None:
        return "Error: Could not load one or both images. Check your file paths."

    # 2. Initialize the ORB detector
    orb = cv2.ORB_create()

    # 3. Find the keypoints and descriptors with ORB
    kp1, des1 = orb.detectAndCompute(img1, None)
    kp2, des2 = orb.detectAndCompute(img2, None)

    # 4. Handle edge cases where an image is completely blank
    if des1 is None or des2 is None:
        return 0.0

    # 5. Create a Brute-Force Matcher
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

    # 6. Match descriptors
    matches = bf.match(des1, des2)

    # 7. Sort them in the order of their distance (best matches first)
    matches = sorted(matches, key=lambda x: x.distance)

    # 8. Calculate Match Percentage
    # We use the maximum keypoints between the two images to find the ratio
    max_keypoints = max(len(kp1), len(kp2))
    
    if max_keypoints == 0:
        return 0.0
        
    match_percentage = (len(matches) / max_keypoints) * 100

    return round(match_percentage, 2)
# --- Test the system ---
# Replace these with actual image paths on your machine
image_1 = "test_eye_1.jpg"
image_2 = "test_eye_2.jpg"

similarity = compare_images(image_1, image_2)

# Check if the result is text (an error) or a number (a success)
if isinstance(similarity, str):
    print(similarity) # This prints the error message cleanly without crashing
else:
    print(f"Match Results: {similarity}%")

    if similarity > 15.0: # You will need to tune this threshold!
        print("System Decision: MATCH")
    else:
        print("System Decision: NO MATCH")