# get the images and make 10 vertical line
import cv2
import os
from openai import OpenAI


images = ["./assets/1.jpg", "./assets/2.jpg", "./assets/3.jpg", "./assets/4.jpg"]
# Ensure the "converted" directory exists
os.makedirs("converted", exist_ok=True)

for i in range(4):
  image = cv2.imread(images[i])
  # Get the height and width of the image
  height, width = image.shape[:2]
  # Divide the width by 10
  step = width // 10
  # Draw 10 vertical lines and add text
  for j in range(1, 10):
    cv2.line(image, (j * step, 0), (j * step, height), (0, 0, 0), 10)  # Thicker and black lines
    # Add text next to each line
    cv2.putText(image, str(j * 10), (j * step + 5, height // 2), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 5, cv2.LINE_AA)
  # Save the image without changing the resolution
  cv2.imwrite(f"converted/{i + 1}.jpg", image, [cv2.IMWRITE_JPEG_QUALITY, 50])  # Compress the image with 50% quality


# send the first photo to open ai api
# client = OpenAI(api_key="")
# response = client.chat.completions.create(
#   model="gpt-4o-mini",
#   messages=[
#     {
#       "role": "user",
#       "content": [
#         {
#           "type": "text",
#           "text": "What are in these images? Is there any difference between them?",
#         },
#         {
#           "type": "image_url",
#           "image_url": {
#             "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg",
#           },
#         },
#         {
#           "type": "image_url",
#           "image_url": {
#             "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg",
#           },
#         },
#       ],
#     }
#   ],
#   max_tokens=300,
# )
# print(response.choices[0])