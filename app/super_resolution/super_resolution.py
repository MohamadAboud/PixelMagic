""" Built-in Imports """
import os
from pathlib import Path
from typing import Union

""" Third-Party Imports """
from PIL import Image
from diffusers.pipelines.latent_diffusion.pipeline_latent_diffusion_superresolution import LDMSuperResolutionPipeline, UNet2DModel

""" Local Imports """
from app.base_model import BaseModel


class SuperResolution(BaseModel):
    """SuperResolution class to handle the session and the API calls."""

    def __init__(self, pretrained_model_name_or_path: Union[str, Path] = 'CompVis/ldm-super-resolution-4x-openimages') -> None:
        """
        Initialize the SuperResolution class.
        
        Args:
            pretrained_model_name_or_path (`str`, `Path`):
            - Either the `model_id` (string) of a model hosted on the Hub, e.g. `bigscience/bloom`.
            - Or a path to a `directory` containing model weights saved using
                [`~transformers.PreTrainedModel.save_pretrained`], e.g., `../path/to/my_model_directory/`.
        
        Returns:
            None
        """
        super().__init__(pretrained_model_name_or_path)

    @property
    def session(self) -> LDMSuperResolutionPipeline:
        """
        Get the current session.
        
        Returns:
            LDMSuperResolutionPipeline: The current session.
        """
        # Check if the session is already initialized
        if self._session is None:
            # Initialize the session
            self._session = LDMSuperResolutionPipeline.from_pretrained(self.pretrained_model_name_or_path)
            # Set the device
            self._session.to(self.device)
            
        return self._session 
    
    def _infernce(self, image: Image) -> Image:
        """
        Run the SuperResolution API.
        
        Args:
            image (Image): The input image.
        
        Returns:
            Image: The result image.
        """
        # Take a copy from the input image
        orig_image = image.copy()

        # Ensure the input image has 3 channels (RGB)
        low_res_img = image.convert('RGB').resize((256, 256))

        # Get the number of inference steps from system environment
        num_inference_steps: int = int(os.getenv('SUPER_RESOLUTION_STEPS', '100'))

        # Run the session (sample random noise and denoise)
        upscaled_image = self.session(low_res_img, num_inference_steps=num_inference_steps, eta=1).images[0]
        
        return upscaled_image
