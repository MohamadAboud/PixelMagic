""" Built-in Imports """
from abc import ABC, abstractmethod, abstractproperty
from pathlib import Path
from typing import Any, Optional, Union

""" Third-Party Imports """
import torch
from PIL import Image


class BaseModel(ABC):
    """
    BaseModel class to handle the session and the API calls.
    """
    
    _session: Optional[Any] = None
    
    def __init__(self, pretrained_model_name_or_path: Union[str, Path]) -> None:
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
        self.pretrained_model_name_or_path = pretrained_model_name_or_path

    @property
    def device(self) -> torch.device:
        """
        Get the current device.
        
        Returns:
            torch.device: The current device.
        """
        return torch.device("cuda" if torch.cuda.is_available() else "cpu")

    @abstractproperty
    def session(self) -> Any:
        """
        Get the current session.
        
        Returns:
            Any: The current session.
        """
        pass
    
    @abstractmethod
    def _infernce(self, *args, **kwargs) -> Image:
        """
        Run the model inference.
        
        Args:
            *args: The input arguments.
            **kwargs: The input keyword arguments.
        
        Returns:
            Image: The result image.
        """
        pass
    
    def run(self, image: Image) -> Image:
        """
        Run the RMBG API.
        
        Args:
            image (Image): The input image.
        
        Returns:
            Image: The result image.
        """
        res = self._infernce(image)
        
        return res

    def __call__(self, image: Image) -> Image:
        """
        Call the RMBG API.
        
        Args:
            image (Image): The input image.
        
        Returns:
            Image: The result image.
        """
        return self.run(image)
