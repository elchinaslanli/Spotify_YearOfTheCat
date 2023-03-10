"""Year of the Cat spotify playlist's backend. Link to the playlist: https://open.spotify.com/playlist/5SeRSnMKdrkDX0Gi60fI9z?si=136ec6ea697f457b

Author: Elchin Aslanli
Date: March 12, 2023
"""


# Importing the PIL library for image editing
from PIL import Image, ImageFont, ImageDraw, ImageEnhance
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
# Importing other utilities
import cv2
import requests
from datetime import date
import config
import base64


def refresh_the_token():

    auth_client = config.my_client_id + ":" + config.my_client_secret
    auth_encode = 'Basic ' + base64.b64encode(auth_client.encode()).decode()

    headers = {
        'Authorization': auth_encode,
    }

    data = {
        'grant_type': 'refresh_token',
        'refresh_token': config.refresh_token
    }

    response = requests.post('https://accounts.spotify.com/api/token',
                             data=data, headers=headers)  # sends request off to spotify

    if (response.status_code == 200):  # checks if request was valid
        print("Spotify token refreshed")
        response_json = response.json()
        new_expire = response_json['expires_in']
        print("The duration of new token " +
              str(new_expire / 60) + "min")  # refreshed token has 60 minutes duration
        return response_json["access_token"]
    else:
        print("ERROR! The response of request is: " + str(response))


def draw_vertical_progress_bar(d, x, y, h, w, colour):

    shape = [(x, y), (w, h)]

    d.rectangle(shape, fill=colour)
    return d


def add_text_to_image(draw, txt_left_limit, txt_height_init, text, txt_anchor, font, colour_text, stroke, stroke_fill):
    draw.text((txt_left_limit, txt_height_init), text, anchor=txt_anchor,
              font=font, fill=colour_text, stroke_width=stroke, stroke_fill=stroke_fill)


def main():

    try:
        # Initialization
        year_start = date(2023, 1, 1)
        current_date = date.today()

        if current_date > date(2023, 12, 31):
            print("The year is over")
            return

        days_passed = (current_date - year_start).days + 1
        months_text = f"{current_date.month} months"
        weeks_text = f"{days_passed // 7} weeks"
        days_text = f"{days_passed} days"

        # Refresh token and set headers
        access_token = refresh_the_token()
        config.custom_auth = f"Bearer {access_token}"
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': config.custom_auth,
        }

        # API request to get stats
        response = requests.get(config.playlist_url, headers=headers)
        response.raise_for_status()
        json_total = response.json().get('total')
        tracks_text = f"{json_total} tracks"

        # Image editing
        with Image.open('rorys_original_image.jpeg') as img:
            draw = ImageDraw.Draw(img)
            font = ImageFont.truetype('circular-std-medium-500.ttf', 180)
            text_color = 'white'
            stroke = 4
            # Draw progress bar
            progress_ratio = days_passed / 365
            progress_colour = 'green' if days_passed == json_total else 'red'
            # draw_vertical_progress_bar(draw, 2050, 2923, 2921, progress_colour, progress_ratio)
            # draw = draw_vertical_progress_bar(draw, 2050, 2923, 29, 2923 - (2923 * progress_ratio), progress_colour)
            draw = draw_vertical_progress_bar(
                draw, 2050, 2923, 2923-(2923*progress_ratio), 2921, progress_colour)
            # d=draw_vertical_progress_bar(d, 2050, 2923, 2923-(2923*progress_ratio), 2921, progress_colour)
            # Define positions for text
            height_init = 2300
            height_step = 180
            txt_left_limit = 2065
            # Add stats as text
            add_text_to_image(draw, txt_left_limit, height_init,
                              months_text, "ls", font, text_color, stroke, "black")
            add_text_to_image(draw, txt_left_limit, height_init+height_step,
                              weeks_text, "ls", font, text_color, stroke, "black")
            add_text_to_image(draw, txt_left_limit, height_init+2*height_step,
                              days_text, "ls", font, text_color, stroke, "black")
            add_text_to_image(draw, txt_left_limit, height_init+3*height_step,
                              tracks_text, "ls", font, text_color, stroke, "black")

            # Save the image
            image_dir = "generated_images//edited_rorys_image"
            image_format = ".jpeg"
            resized_image_path = f"{image_dir}resized{image_format}"
            img.save(f"{image_dir}{image_format}")
            img.resize((1000, 1000)).save(resized_image_path)

            # Encode and upload the image
            with open(resized_image_path, "rb") as img_file:
                encoded_image = base64.b64encode(img_file.read())

            print("Putting the image")
            response_put = requests.put(
                config.playlist_image_url, headers=headers, data=encoded_image)
            response_put.raise_for_status()

    except requests.RequestException as e:
        print(f"Network error: {e}")
    except IOError as e:
        print(f"I/O error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
