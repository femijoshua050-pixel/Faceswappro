import torch
from gfpgan import GFPGANer

class FaceEnhancer:
    def __init__(self, model_path='weights/gfpgan.pth'):
        self.gfpganer = GFPGANer(model_path=model_path)

    def enhance(self, input_image):
        
        # Assuming input_image is a tensor or a valid path to an image file, modify as necessary
        if isinstance(input_image, str):  # If input_image is a path to an image file
            img = self.load_image(input_image)
        else:
            img = input_image

        _, _, restored_img = self.gfpganer.enhance(img)
        return restored_img

    def load_image(self, image_path):
        # Load the image from the given path
        from PIL import Image
        import torchvision.transforms as transforms
        img = Image.open(image_path).convert('RGB')
        transform = transforms.ToTensor()
        return transform(img).unsqueeze(0)  # Add batch dimension
        

