""" Built-in Imports """
from pathlib import Path
from typing import Union

""" Third-Party Imports """
import numpy as np
from PIL import Image

""" Local Imports """
from .briarmbg import BriaRMBG
from app.base_model import BaseModel
from .utilities import preprocess_image, postprocess_image


class RMBG(BaseModel):
    """RMBG class to handle the session and the API calls."""
    
    def __init__(self, pretrained_model_name_or_path: Union[str, Path] = 'weights/rmbg') -> None:
        """
        Initialize the RMBG class.
        
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
    def session(self) -> BriaRMBG:
        """
        Get the current session.
        
        Returns:
            BriaRMBG: The current session.
        """
        # Check if the session is already initialized
        if self._session is None:
            # Initialize the session
            self._session = BriaRMBG.from_pretrained(self.pretrained_model_name_or_path)
            # Set the device
            self._session.to(self.device)
            
        return self._session 
    
    def _infernce(self, image: Image) -> Image:
        """
        Run the RMBG API.
        
        Args:
            image (Image): The input image.
        
        Returns:
            Image: The result image.
        """
        # Take a copy from the input image
        orig_image = image.copy()
        # Get the original image size
        orig_img_size = image.size
        # Preprocess the input image
        preprocess_img = preprocess_image(image).to(self.device)

        # Run the session 
        result = self.session(preprocess_img)

        # Postprocess the result image
        pil_im: np.ndarray = postprocess_image(result[0][0], im_size=orig_img_size)
        
        no_bg_image = Image.new("RGBA", pil_im.size, (0,0,0,0))
        no_bg_image.paste(orig_image, mask=pil_im)
        
        return no_bg_image
