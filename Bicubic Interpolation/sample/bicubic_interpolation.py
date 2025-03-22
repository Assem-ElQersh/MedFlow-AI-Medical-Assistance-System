import cv2
import matplotlib.pyplot as plt
import numpy as np
from skimage.metrics import peak_signal_noise_ratio as psnr
from skimage.metrics import structural_similarity as ssim

# Read the high-resolution image
hr_image = cv2.imread('original.jpeg')  # Replace with your image file
hr_image = cv2.cvtColor(hr_image, cv2.COLOR_BGR2RGB)  # Convert from BGR to RGB

# Set the scaling factor (e.g., 4x downsampling)
scale = 4

# Get the dimensions of the HR image
height, width, _ = hr_image.shape

# Downsample the HR image (create LR image)
lr_image = cv2.resize(hr_image, (width // scale, height // scale), interpolation=cv2.INTER_CUBIC)

# Upsample the LR image back to HR size using bicubic interpolation
upscaled_image = cv2.resize(lr_image, (width, height), interpolation=cv2.INTER_CUBIC)

# Resize LR image back to HR dimensions for comparison
lr_resized = cv2.resize(lr_image, (width, height), interpolation=cv2.INTER_NEAREST)

# Calculate PSNR and SSIM for the LR image compared to HR
psnr_lr = psnr(hr_image, lr_resized)
ssim_lr = np.mean([ssim(hr_image[:,:,i], lr_resized[:,:,i], data_range=hr_image[:,:,i].max() - hr_image[:,:,i].min()) for i in range(3)])

# Calculate PSNR and SSIM for the upscaled image compared to HR
psnr_upscaled = psnr(hr_image, upscaled_image)
ssim_upscaled = np.mean([ssim(hr_image[:,:,i], upscaled_image[:,:,i], data_range=hr_image[:,:,i].max() - hr_image[:,:,i].min()) for i in range(3)])

# Print metrics
print(f'PSNR between ground truth and LR image: {psnr_lr:.2f} dB')
print(f'SSIM between ground truth and LR image: {ssim_lr:.4f}')
print(f'PSNR between ground truth and upscaled image: {psnr_upscaled:.2f} dB')
print(f'SSIM between ground truth and upscaled image: {ssim_upscaled:.4f}')

# Display the images for comparison
plt.figure(figsize=(15, 5))
plt.subplot(1, 3, 1)
plt.imshow(hr_image)
plt.title('Ground Truth (High-Resolution)')
plt.axis('off')

plt.subplot(1, 3, 2)
plt.imshow(lr_resized)
plt.title(f'Low-Resolution Image\nPSNR: {psnr_lr:.2f} dB, SSIM: {ssim_lr:.4f}')
plt.axis('off')

plt.subplot(1, 3, 3)
plt.imshow(upscaled_image)
plt.title(f'Upscaled Image\nPSNR: {psnr_upscaled:.2f} dB, SSIM: {ssim_upscaled:.4f}')
plt.axis('off')

plt.show()
