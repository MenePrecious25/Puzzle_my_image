import streamlit as st
import cv2
from PIL import Image
import numpy as np
import random


def split_image(image, rows, cols):
    height, width = image.shape[:2]
    tile_height = height // rows
    tile_width = width // cols
    tiles = []
    for y in range(0, height, tile_height):
        for x in range(0, width, tile_width):
            tile = image[y:y+tile_height, x:x+tile_width]
            tiles.append(tile)
    return tiles

def main():
    st.title("Puzzle Your Image")

    # Upload image
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        original_image = Image.open(uploaded_file)
        # st.image(original_image, caption="Original Image", use_column_width=True)

        # Rotate the image by 180 degrees
        rotated_image = np.array(original_image)

        # Break the image into puzzle squares
        rows = st.sidebar.slider("Number of rows:", min_value=2, max_value=5, value=4)
        cols = st.sidebar.slider("Number of columns:", min_value=2, max_value=5, value=4)
        if st.button('Process'):
            puzzle_pieces = split_image(rotated_image, rows, cols)

            # Shuffle the puzzle pieces
            random.shuffle(puzzle_pieces)

            # Combine puzzle pieces to form a new image
            new_image = np.vstack([np.hstack(row) for row in np.array_split(puzzle_pieces, rows)])
            new_image_pil = Image.fromarray(new_image)
            image_with_frame = cv2.rectangle(new_image, (50, 50), (50, 50), (222, 245, 70), 20)


            st.image([original_image, new_image_pil], caption=['original', "Puzzled Image"], width = 350)


            # Save the new image
            if st.button("Save Puzzle Image"):
                new_image_pil.save("output_image.jpg")
                st.success("Puzzle image saved successfully!")

if __name__ == "__main__":
    main()
