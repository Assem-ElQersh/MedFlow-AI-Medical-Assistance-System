% Read the high-resolution image
hr_image = imread('original.jpeg');  % Replace with your image file
if size(hr_image,3) == 3
    % If the image is RGB, convert to double for computations
    hr_image = im2double(hr_image);
else
    hr_image = im2double(repmat(hr_image, [1,1,3])); % Ensure 3 channels for consistency
end

% Set the scaling factor (e.g., 4x downsampling)
scale = 4;

% Get the dimensions of the HR image
[height, width, ~] = size(hr_image);

% Downsample the HR image to create the LR image using bicubic interpolation
lr_image = imresize(hr_image, [round(height/scale) round(width/scale)], 'bicubic');

% Upsample the LR image back to HR size using bicubic interpolation
upscaled_image = imresize(lr_image, [height, width], 'bicubic');

% Resize LR image back to HR dimensions using nearest neighbor interpolation
lr_resized = imresize(lr_image, [height, width], 'nearest');

% Calculate PSNR and SSIM for the LR image compared to HR
psnr_lr = psnr(lr_resized, hr_image);
ssim_lr = ssim(lr_resized, hr_image);

% Calculate PSNR and SSIM for the upscaled image compared to HR
psnr_upscaled = psnr(upscaled_image, hr_image);
ssim_upscaled = ssim(upscaled_image, hr_image);

% Print metrics
fprintf('PSNR between ground truth and LR image: %.2f dB\n', psnr_lr);
fprintf('SSIM between ground truth and LR image: %.4f\n', ssim_lr);
fprintf('PSNR between ground truth and upscaled image: %.2f dB\n', psnr_upscaled);
fprintf('SSIM between ground truth and upscaled image: %.4f\n', ssim_upscaled);

% Display the images for comparison
figure('Name','Image Comparison','NumberTitle','off','Position',[100, 100, 1200, 400]);

subplot(1, 3, 1);
imshow(hr_image);
title('Ground Truth (High-Resolution)');

subplot(1, 3, 2);
imshow(lr_resized);
title(sprintf('Low-Resolution Image\nPSNR: %.2f dB, SSIM: %.4f', psnr_lr, ssim_lr));

subplot(1, 3, 3);
imshow(upscaled_image);
title(sprintf('Upscaled Image\nPSNR: %.2f dB, SSIM: %.4f', psnr_upscaled, ssim_upscaled));
