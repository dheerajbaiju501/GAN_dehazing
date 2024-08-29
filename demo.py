import argparse
from model import Generator
from PIL import Image
from torch.autograd import Variable
from utils import *
import torch
import os
import gc  # Import garbage collection

parser = argparse.ArgumentParser(description='image-dehazing')

parser.add_argument('--model', required=True, help='training directory')
parser.add_argument('--images', nargs='+', type=str, default='inputs', help='path to hazy folder')
parser.add_argument('--outdir', default='outputs', help='data save directory')

args = parser.parse_args()

def test(args):
    my_model = Generator()
    my_model.load_state_dict(torch.load(args.model, map_location=torch.device('cpu')))
    my_model.eval()

    output_dir = args.outdir
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    img_paths = args.images

    for img_path in img_paths:
        image = Image.open(img_path).convert('RGB')
        width, height = image.size
        scale = 32
        image = image.resize((width // scale * scale, height // scale * scale))
        with torch.no_grad():
            image = rgb_to_tensor(image)
            image = image.unsqueeze(0)
            image = Variable(image)  # No need to move to GPU
            output = my_model(image)
            del image  # Clear the image variable
            torch.cuda.empty_cache()  # Clear the cache after processing each image
        output = tensor_to_rgb(output)
        out = Image.fromarray(np.uint8(output), mode='RGB')
        out = out.resize((width, height), resample=Image.BICUBIC)
        output_path = os.path.join(output_dir, os.path.basename(img_path))
        out.save(output_path)
        print('One image saved at ' + output_path)
        del output, out  # Clear the output variables
        gc.collect()  # Invoke garbage collector

if __name__ == '__main__':
    test(args)
