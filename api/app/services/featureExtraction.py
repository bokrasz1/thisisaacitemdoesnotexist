import torch
import torch.nn as nn
import torch.optim as optim
import torchvision.transforms as transforms
from torchvision.datasets import ImageFolder
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt
from PIL import Image

# Transform: Convert to tensors and normalize (optional)
transform = transforms.Compose([
    # transforms.Grayscale(num_output_channels=1),  # Convert to grayscale if needed
    transforms.ToTensor(),
    # transforms.Normalize(mean=[0, 0, 0], std=[0.5, 0.5, 0.5])  # Normalizes each RGB channel
])

def pil_loader(path):
    # open path as file to avoid ResourceWarning (https://github.com/python-pillow/Pillow/issues/835)
    with open(path, 'rb') as f:
        img = Image.open(f)
        return img.convert('RGBA')

# Load dataset
dataset = ImageFolder(root="./items", transform=transform, loader=pil_loader)
dataloader = DataLoader(dataset, batch_size=16, shuffle=True)

sample_img, _ = dataset[637]

fig, axes = plt.subplots(1, 2)
axes[0].imshow(sample_img.permute(1,2,0))

# Visualize a sprite
print(len(dataset))
print(dataset)

# Calculate mean and std
def calculate_mean_std(loader):
    mean = 0.
    std = 0.
    total_images_count = 0

    for images, _ in loader:
        print("batch size:")
        print(images.size(0))
        print(images.size(1))
        print(images.size())
        print("-----------------")
        batch_size = images.size(0)  # Number of images in the batch
        images = images.view(batch_size, images.size(1), -1)  # Flatten HxW into one dimension
        mean += images.mean(2).sum(0)  # Sum mean per channel
        std += images.std(2).sum(0)  # Sum std per channel
        total_images_count += batch_size
        print("batch size:" + str(batch_size))
        print(images.size(0))
        print(images.size(1))
        print(images.size())
        # print(images.shape())
        print(images)
    mean /= total_images_count
    std /= total_images_count
    return mean, std

# Run the function
mean, std = calculate_mean_std(dataloader)
print(f"Dataset Mean: {mean}")
print(f"Dataset Std: {std}")

transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize(mean=[*mean], std=[*std])  # Normalizes each RGB channel
])

dataset = ImageFolder(root="./items", transform=transform)
dataloader = DataLoader(dataset, batch_size=16, shuffle=True)

sample_img, _ = dataset[637]
axes[1].imshow(sample_img.permute(1,2,0))
plt.show()
