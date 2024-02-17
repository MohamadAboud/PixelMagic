""" Third-Party Imports """
import torch
import numpy as np
from PIL import Image
import torch.nn.functional as F
from torchvision.transforms.functional import normalize


def preprocess_image(im: Image, model_input_size: list = [1024, 1024]) -> torch.Tensor:
    """
    Preprocess the input image.
    
    Args:
        im (Image): The input image.
        model_input_size (list): The model input size. default: [1024, 1024]
    
    Returns:
        torch.Tensor: The preprocessed image.
    """
    # Convert the image to a numpy array
    im = np.array(im)
    if len(im.shape) < 3:
        im = im[:, :, np.newaxis]
    # orig_im_size=im.shape[0:2]
    im_tensor = torch.tensor(im, dtype=torch.float32).permute(2,0,1)
    im_tensor = F.interpolate(torch.unsqueeze(im_tensor,0), size=model_input_size, mode='bilinear').type(torch.uint8)
    image = torch.divide(im_tensor,255.0)
    image = normalize(image,[0.5,0.5,0.5],[1.0,1.0,1.0])
    return image


def postprocess_image(result: torch.Tensor, im_size: list)-> Image:
    """
    Postprocess the result image.
    
    Args:
        result (torch.Tensor): The result image.
        im_size (list): The image size.
    
    Returns:
        Image: The postprocessed image.
    """
    result = torch.squeeze(F.interpolate(result, size=im_size, mode='bilinear') ,0)
    ma = torch.max(result)
    mi = torch.min(result)
    result = (result-mi)/(ma-mi)
    im_array = (result*255).permute(1,2,0).cpu().data.numpy().astype(np.uint8)
    im_array = np.squeeze(im_array)
    
    im = Image.fromarray(im_array).resize(im_size)
    return im
    