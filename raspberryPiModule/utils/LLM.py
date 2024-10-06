# get the images and make 10 vertical line
import os

import cloudinary
import cloudinary.uploader
import cv2
from openai import OpenAI

# ------------------------------Configs-------------------------------------
cloudinary.config(
    cloud_name="djxkc3pxx",
    api_key="437248233547831",
    api_secret="P7BS5TrmZC-fW7m-ZZudlOnyXwA",  # Click 'View API Keys' above to copy your API secret
    secure=True,
)
allUrls = []
# ---------------------------------------------------------------------------


# requires the photos in the assets folder
def add_lines():
    images = ["./assets/1.jpg", "./assets/2.jpg", "./assets/3.jpg", "./assets/4.jpg"]
    # Ensure the "converted" directory exists
    os.makedirs("converted", exist_ok=True)

    # in the first image add a line in the middle vertically and then addd 3 more to the left and right all divided equall. Mark the line in the middle with 0
    image = cv2.imread(images[0])
    # rotate the image 180 degrees
    image = cv2.rotate(image, cv2.ROTATE_180)
    # Get the height and width of the image
    height, width = image.shape[:2]
    # Divide the width by 7
    step = width // 7
    # draw 7 vertical lines
    text1 = [35, 25, 15, 5, 355, 345]
    for j in range(1, 7):
        cv2.line(
            image, (j * step, 0), (j * step, height), (255,0,0), 10
        )  # Thicker and black lines
        # Add text next to each line
        cv2.putText(
            image,
            str(text1[j - 1]),
            (j * step + 5, 200),
            cv2.FONT_HERSHEY_SIMPLEX,
            2,
            (0,255,0),
            5,
            cv2.LINE_AA,
        )
        cv2.putText(
            image,
            str(text1[j - 1]),
            (j * step + 5, height - 200),
            cv2.FONT_HERSHEY_SIMPLEX,
            2,
            (0,0,225),
            5,
            cv2.LINE_AA,
        )
        # Save the image without changing the resolution
        cv2.putText(
            image,
            str(45),
            (5, 200),
            cv2.FONT_HERSHEY_SIMPLEX,
            2,
            (0,255,0),
            5,
            cv2.LINE_AA,
        )
        cv2.putText(
            image,
            str(45),
            (5, height - 200),
            cv2.FONT_HERSHEY_SIMPLEX,
            2,
            (0,0,225),
            5,
            cv2.LINE_AA,
        )
    cv2.imwrite(
        "converted/1.jpg", image, [cv2.IMWRITE_JPEG_QUALITY, 50]
    )  # Compress the image with 50% quality

    # in the first image add a line in the middle vertically and then addd 3 more to the left and right all divided equall. Mark the line in the middle with 0
    image = cv2.imread(images[1])
    # rotate the image 180 degrees
    image = cv2.rotate(image, cv2.ROTATE_180)
    # Get the height and width of the image
    height, width = image.shape[:2]
    # Divide the width by 7
    step = width // 7
    # draw 7 vertical lines
    text1 = [115, 105, 95, 85, 75, 65]
    for j in range(1, 7):
        cv2.line(
            image, (j * step, 0), (j * step, height), (255,0,0), 10
        )  # Thicker and black lines
        # Add text next to each line
        cv2.putText(
            image,
            str(text1[j - 1]),
            (j * step + 5, 200),
            cv2.FONT_HERSHEY_SIMPLEX,
            2,
            (0,225,0),
            5,
            cv2.LINE_AA,
        )
        cv2.putText(
            image,
            str(text1[j - 1]),
            (j * step + 5, height - 200),
            cv2.FONT_HERSHEY_SIMPLEX,
            2,
            (0,0,225),
            5,
            cv2.LINE_AA,
        )
        # Save the image without changing the resolution
        cv2.putText(
            image,
            str(125),
            (5, 200),
            cv2.FONT_HERSHEY_SIMPLEX,
            2,
            (0,225,0),
            5,
            cv2.LINE_AA,
        )
        cv2.putText(
            image,
            str(125),
            (5, height - 200),
            cv2.FONT_HERSHEY_SIMPLEX,
            2,
            (0,0,225),
            5,
            cv2.LINE_AA,
        )
    cv2.imwrite(
        "converted/2.jpg", image, [cv2.IMWRITE_JPEG_QUALITY, 50]
    )  # Compress the image with 50% quality

    # in the first image add a line in the middle vertically and then addd 3 more to the left and right all divided equall. Mark the line in the middle with 0
    image = cv2.imread(images[2])
    # rotate the image 180 degrees
    image = cv2.rotate(image, cv2.ROTATE_180)
    # Get the height and width of the image
    height, width = image.shape[:2]
    # Divide the width by 7
    step = width // 7
    # draw 7 vertical lines
    text1 = [205, 195, 185, 175, 165, 155]
    for j in range(1, 7):
        cv2.line(
            image, (j * step, 0), (j * step, height), (255,0,0), 10
        )  # Thicker and black lines
        # Add text next to each line
        cv2.putText(
            image,
            str(text1[j - 1]),
            (j * step + 5, 200),
            cv2.FONT_HERSHEY_SIMPLEX,
            2,
            (0,225,0),
            5,
            cv2.LINE_AA,
        )
        cv2.putText(
            image,
            str(text1[j - 1]),
            (j * step + 5, height - 200),
            cv2.FONT_HERSHEY_SIMPLEX,
            2,
            (0,0,225),
            5,
            cv2.LINE_AA,
        )
        # Save the image without changing the resolution
        cv2.putText(
            image,
            str(215),
            (5, 200),
            cv2.FONT_HERSHEY_SIMPLEX,
            2,
            (0,225,0),
            5,
            cv2.LINE_AA,
        )
        cv2.putText(
            image,
            str(215),
            (5, height - 200),
            cv2.FONT_HERSHEY_SIMPLEX,
            2,
            (0,0,225),
            5,
            cv2.LINE_AA,
        )
    cv2.imwrite(
        "converted/3.jpg", image, [cv2.IMWRITE_JPEG_QUALITY, 50]
    )  # Compress the image with 50% quality

    # in the first image add a line in the middle vertically and then addd 3 more to the left and right all divided equall. Mark the line in the middle with 0
    image = cv2.imread(images[3])
    # rotate the image 180 degrees
    image = cv2.rotate(image, cv2.ROTATE_180)
    # Get the height and width of the image
    height, width = image.shape[:2]
    # Divide the width by 7
    step = width // 7
    # draw 7 vertical lines
    text1 = [295, 285, 275, 265, 255, 245]
    for j in range(1, 7):
        cv2.line(
            image, (j * step, 0), (j * step, height), (255,0,0), 10
        )  # Thicker and black lines
        # Add text next to each line
        cv2.putText(
            image,
            str(text1[j - 1]),
            (j * step + 5, 200),
            cv2.FONT_HERSHEY_SIMPLEX,
            2,
            (0,255,0),
            5,
            cv2.LINE_AA,
        )
        cv2.putText(
            image,
            str(text1[j - 1]),
            (j * step + 5, height - 200),
            cv2.FONT_HERSHEY_SIMPLEX,
            2,
            (0,0,225),
            5,
            cv2.LINE_AA,
        )
        # Save the image without changing the resolution
        cv2.putText(
            image,
            str(305),
            (5, 200),
            cv2.FONT_HERSHEY_SIMPLEX,
            2,
            (0,255,0),
            5,
            cv2.LINE_AA,
        )
        cv2.putText(
            image,
            str(305),
            (5, height - 200),
            cv2.FONT_HERSHEY_SIMPLEX,
            2,
            (0,0,225),
            5,
            cv2.LINE_AA,
        )
    cv2.imwrite(
        "converted/4.jpg", image, [cv2.IMWRITE_JPEG_QUALITY, 50]
    )  # Compress the image with 50% quality


def upload_photos():
    for i in range(4):
        upload_result = cloudinary.uploader.upload(
            "./converted/{}.jpg".format(i + 1), public_id=i + 1
        )
        print(upload_result["secure_url"])
        allUrls.append(upload_result["secure_url"])


# requies an array of list of urls of the images - incomplete
def analyze_photos():
    # send the first photo to open ai api
    client = OpenAI(api_key="")
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Look at all the images, and find which one of the vertical lines contains a door. each line is marked by a number. find the middle of the door. if its not a line, estimate the number that was go over the middle of the door. Your answer will be used by us os just send the answer and no explaination. Wrap the final answer in {{}} brackets",
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": allUrls[0],
                        },
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": allUrls[1],
                        },
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": allUrls[2],
                        },
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": allUrls[3],
                        },
                    },
                ],
            },
        ],
        max_tokens=300,
    )
    input_string = response.choices[0].message.content
    print(input_string)
    # {{}}
    start = input_string.find("{{")
    end = input_string.find("}}")
    extracted_content = 0
    if start != -1 and end != -1:
        extracted_content = input_string[
            start + 2 : end
        ]  # +2 to exclude the curly braces
        print("Extracted content:", extracted_content)
    else:
        print("No content found inside curly braces.")
    return int(extracted_content)


def full_flow():
    print("\n--------------------------------")
    print("Sending the images for analysis...")
    print("--------------------------------\n")

    add_lines()
    upload_photos()
    return analyze_photos()
