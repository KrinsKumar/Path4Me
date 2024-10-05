# get the images and make 10 vertical line
import cv2
import os
from openai import OpenAI
import subprocess
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url

# ------------------------------Configs-------------------------------------
cloudinary.config( 
    cloud_name = "djxkc3pxx", 
    api_key = "437248233547831", 
    api_secret = "P7BS5TrmZC-fW7m-ZZudlOnyXwA", # Click 'View API Keys' above to copy your API secret
    secure=True
)
allUrls = ["https://res.cloudinary.com/djxkc3pxx/image/upload/v1728102994/1.jpg",
          "https://res.cloudinary.com/djxkc3pxx/image/upload/v1728102995/2.jpg",
          "https://res.cloudinary.com/djxkc3pxx/image/upload/v1728102996/3.jpg",
          "https://res.cloudinary.com/djxkc3pxx/image/upload/v1728102997/4.jpg]",]
# ---------------------------------------------------------------------------

# requires the photos in the assets folder
def add_lines():
  images = ["./assets/1.jpg", "./assets/2.jpg", "./assets/3.jpg", "./assets/4.jpg"]
  # Ensure the "converted" directory exists
  os.makedirs("converted", exist_ok=True)

  line_number = 10  # Start with the first line number as 10
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
      cv2.putText(image, str(line_number), (j * step + 5, height // 2), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 5, cv2.LINE_AA)
      line_number += 10  # Increment the line number by 10 for the next line
    # Ensure the next image starts with the correct line number
    line_number += 10  # Skip 10 to start from 110 after 90
    # Save the image without changing the resolution
    cv2.imwrite(f"converted/{i + 1}.jpg", image)  # Compress the image with 50% quality
    # cv2.imwrite(f"converted/{i + 1}.jpg", image, [cv2.IMWRITE_JPEG_QUALITY, 50])  # Compress the image with 50% quality

def upload_photos():
  for i in range(4):
    upload_result = cloudinary.uploader.upload("./converted/{}.jpg".format(i + 1),
                                              public_id=i + 1)
    print(upload_result["secure_url"])
    allUrls.append(upload_result["secure_url"])

# requies an array of list of urls of the images - incomplete
def analyze_photos():
  # send the first photo to open ai api
  client = OpenAI(api_key="")
  response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
      {
        "role": "system",
        "content": "You are a helpful assistant."
      },
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": "Look at all the images, and find which one of the vertical lines contains a door. each line is marked by a number. find the middle of the door. if its not a line, estimate the number that was go over the middle of the door",
          },
          {
            "type": "image_url",
            "image_url": {
              "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg",
            },
          },
          {
            "type": "image_url",
            "image_url": {
              "url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg",
            },
          },
        ],
      }
    ],
    max_tokens=300,
  )
  print(response.choices[0])

def full_flow():
  add_lines()
  upload_photos()
  # analyze_photos()

def main():
  full_flow()

if __name__ == "__main__":
  main()