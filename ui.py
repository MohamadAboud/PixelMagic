# """ Built-in Imports """
import os
import uuid
from typing import Optional
from datetime import datetime

# """ Third-Party Imports """
import torch
from PIL import Image
import streamlit as st

# """ Local Imports """
from utils import ProjectPaths
from app.base_model import BaseModel
from app import SuperResolution, RMBG


class PixelMagicApp:
    def __init__(self):
        """
        Initialize the PixelMagicApp class.
        """

        # Set the configuration
        _is_available = torch.cuda.is_available()
        device = 'cuda' if _is_available else 'cpu'
        color = 'green' if _is_available else 'red'
        st.write(f'<h1>🎨 Pixel Magic  <sup style="color: {color};"> {device}</sup></h1>', unsafe_allow_html=True)
        st.write('Welcome to Pixel Magic! This is a simple web app that allows you to upload an image and apply different image processing techniques to it. You can choose between Super Resolution and Remove Background. Choose an option and upload an image to get started.')

        # Initialize the models
        self.sr, self.rmbg = self.load_model()
        
        # Sidebar content to options [Super Resolution, Remove Background]
        st.sidebar.title('Options')
        st.sidebar.write('Choose an option to apply to your image.')
        self.option = st.sidebar.selectbox('Option', ['Remove Background', 'Super Resolution'])

        # Write a note to the user telling them that the models will take some time to process
        if device == 'cuda':
            msg = '*Note: The models will take some time to process on the first run. Subsequent runs will be faster.'
        else:
            msg = '*Note: The models will take some time to process because you are using a CPU device.'
        
        st.sidebar.write(f'<p <sup style="color: red;"> {msg}<p>', unsafe_allow_html=True)

        # File uploader
        self.uploaded_file = st.file_uploader("Choose an image...", type=['jpg', 'png', 'jpeg'])

        # Create a row for the image
        self.col1, self.col2 = st.columns(2)
        

    @st.cache(allow_output_mutation=True)
    def load_model(self):
        """
        Load Super Resolution and Remove Background models.

        Returns:
            Tuple[SuperResolution, RMBG]: Tuple containing SuperResolution and RMBG models.
        """
        return SuperResolution(), RMBG()

    def process_image(self) -> Image:
        """
        Process the image and display the result.

        Returns:
            Image: The processed image.
        """
        try:
            # Check if the image is uploaded
            if self.uploaded_file is None:
                st.warning('Please upload an image.')
                return None

            image = Image.open(self.uploaded_file)

            return image
        except Exception as e:
            st.error(f'An error occurred: {e}')
            return None

    def on_click(self, model: BaseModel):
        """
        Process the image using the specified model.

        Args:
            model (BaseModel): The model to be applied.

        Returns:
            None
        """
        img = self.process_image()

        if img:
            with self.col2:
                with st.spinner('Processing...'):
                    res = model.run(img)

                # Display the result
                st.image(res, caption='Processed Image', use_column_width=True)

                # Create a button to download the image
                # Generate a unique name for the image with the current date year-month-day_hour-minute-second
                formmated_date = datetime.now().strftime('%Y%m%d_%H%M%S')
                img_name = f"{formmated_date}.png"
                new_img = os.path.join(ProjectPaths.images_dir, img_name)
                res.save(new_img)

            with open(new_img, 'rb') as f:
                st.download_button('Download Image', f, file_name=img_name, mime='image/png')

    @property
    def history(self) -> dict:
        """
        Get the history of images uploaded by the user.
        
        Returns:
            dict: A dictionary containing the images grouped by date.
        """
        image_files = os.listdir(ProjectPaths.images_dir)

        # Assuming the date is in the file name in the format YYYYMMDD
        date_format = "%Y%m%d_%H%M%S"

        # Create a dictionary to store images grouped by creation date
        images_by_date = {}

        for image_file in image_files:
            # Extract the date from the file name
            date_str = os.path.splitext(image_file)[0]
            try:
                # Parse the date string into a datetime object
                date = datetime.strptime(date_str, date_format).date()

                # Add the image to the corresponding date in the dictionary
                if date in images_by_date:
                    images_by_date[date].append(image_file)
                else:
                    images_by_date[date] = [image_file]
            except ValueError:
                print(f"Unable to parse date from file: {image_file}")

        # Sort images within each date group
        for date, images in images_by_date.items():
            images_by_date[date] = sorted(images, reverse=True)

        return images_by_date

    def run(self):
        """
        Run the PixelMagicApp.

        Returns:
            None
        """
        # Display the image
        if self.uploaded_file is not None:
            with self.col1:
                st.image(self.uploaded_file, caption='Original Image', use_column_width=True)

        # Super Resolution
        if self.option == 'Super Resolution':
            # Apply
            if st.sidebar.button('Apply', help='Apply the Super Resolution model to the image.'):
                self.on_click(model=self.sr)

        # Remove Background
        elif self.option == 'Remove Background':
            # Apply the method
            if st.sidebar.button('Apply', help='Apply the Remove Background model to the image.'):
                self.on_click(model=self.rmbg)
        
                
        # Create a dropdown history
        with st.sidebar.expander("History"):
            st.write('View your recent activities.')
            # Get the history of images uploaded by the user
            history = self.history
            # Sorte the history by date
            keys = sorted(history.keys(), reverse=True)
            for key in keys:
                # Extract the images from the history dictionary
                images = history[key]
                st.write(f'<p style="color: gray;">{key}: </p>', unsafe_allow_html=True)
                
                for img in images:
                    img_pth = os.path.join(ProjectPaths.images_dir, img)
                    img_name = img.split('_')[1]
                    # Create a 3 column layout
                    col1, col2, col3 = st.columns([1, 2, 2])
                    # First column content a image
                    with col1:
                        img = Image.open(img_pth)
                        st.image(img, use_column_width=True)
                    # Second column content the name of the image
                    with col2:
                        st.write(img_name)
                    # Third column content a download button
                    with col3:
                        with open(img_pth, 'rb') as f:
                            st.download_button('Download', f, file_name=img_name, mime='image/png')

if __name__ == "__main__":
    app = PixelMagicApp()
    app.run()
