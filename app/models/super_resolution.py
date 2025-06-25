import cv2
import numpy as np
from PIL import Image
import io

def lanczos_interpolation(img, scale_factor):
    h, w = img.shape[:2]
    new_h, new_w = int(h * scale_factor), int(w * scale_factor)
    return cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_LANCZOS4)

def bilinear_interpolation(img, scale_factor):
    h, w = img.shape[:2]
    new_h, new_w = int(h * scale_factor), int(w * scale_factor)
    return cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_LINEAR)

def bicubic_interpolation(img, scale_factor):
    h, w = img.shape[:2]
    new_h, new_w = int(h * scale_factor), int(w * scale_factor)
    return cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_CUBIC)

def edsr_super_resolution(img, scale_factor):
    try:
        sr = cv2.dnn_superres.DnnSuperResImpl_create()
        sr.readModel('app/models/EDSR_x4.pb')
        sr.setModel("edsr", 4)
        return sr.upsample(img)
    except:
        return bicubic_interpolation(img, scale_factor)

def apply_detail_enhancement(img):
    try:
        return cv2.detailEnhance(img, sigma_s=10, sigma_r=0.15)
    except:
        return img

def apply_unsharp_mask(img, strength=1.5, gaussian_sigma=3.0):
    gaussian = cv2.GaussianBlur(img, (0, 0), gaussian_sigma)
    return cv2.addWeighted(img, strength, gaussian, -(strength-1), 0)

def adaptive_bilateral_filter(img):
    try:
        return cv2.bilateralFilter(img, 9, 75, 75)
    except:
        return img

def adjust_brightness_contrast(img, brightness=0, contrast=0):
    if brightness == 0 and contrast == 0:
        return img
    img_float = img.astype(np.float32) / 255.0
    if brightness != 0:
        brightness_factor = 1.0 + (brightness / 100.0)
        img_float = img_float * brightness_factor
    if contrast != 0:
        contrast_factor = 1.0 + (contrast / 100.0)
        mean = np.mean(img_float)
        img_float = (img_float - mean) * contrast_factor + mean
    img_float = np.clip(img_float * 255.0, 0, 255).astype(np.uint8)
    return img_float

def adjust_saturation(img, saturation=0):
    if saturation == 0:
        return img
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    saturation_factor = 1.0 + (saturation / 100.0)
    hsv[:,:,1] = np.clip(hsv[:,:,1] * saturation_factor, 0, 255).astype(np.uint8)
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

def apply_custom_sharpness(img, amount=0):
    if amount == 0:
        return img
    strength = amount / 100.0
    kernel = np.array([[0, -1, 0],
                       [-1, 4 + strength, -1],
                       [0, -1, 0]]) / (strength + 1)
    sharpened = cv2.filter2D(img, -1, kernel)
    if strength > 1.0:
        blend_factor = min(2.0, strength) - 1.0
        result = cv2.addWeighted(img, 1.0 - blend_factor, sharpened, blend_factor, 0)
        return result
    else:
        return sharpened

def process_image_for_upscaling(img, x, y, zoom_level, brightness=0, contrast=0, sharpness=0, saturation=0):
    h, w = img.shape[:2]
    x = max(0, min(x, w-1))
    y = max(0, min(y, h-1))
    region_size = int(min(h, w) / zoom_level)
    half_size = region_size // 2
    left = max(0, x - half_size)
    top = max(0, y - half_size)
    right = min(w, x + half_size)
    bottom = min(h, y + half_size)
    roi = img[top:bottom, left:right]
    if roi.size == 0:
        return img
    roi = adaptive_bilateral_filter(roi)
    if zoom_level <= 2.0:
        enhanced = bicubic_interpolation(roi, 2.0)
    elif zoom_level <= 5.0:
        enhanced = lanczos_interpolation(roi, 2.0)
    elif zoom_level <= 10.0:
        try:
            enhanced = edsr_super_resolution(roi, 2.0)
        except:
            enhanced = lanczos_interpolation(roi, 2.0)
    else:
        first_pass = lanczos_interpolation(roi, 1.5)
        enhanced_details = apply_detail_enhancement(first_pass)
        enhanced = lanczos_interpolation(enhanced_details, 1.33)
    if brightness != 0 or contrast != 0:
        enhanced = adjust_brightness_contrast(enhanced, brightness, contrast)
    if saturation != 0:
        enhanced = adjust_saturation(enhanced, saturation)
    if sharpness < 50:
        enhanced = apply_detail_enhancement(enhanced)
    if sharpness > 0:
        enhanced = apply_custom_sharpness(enhanced, sharpness)
    else:
        unsharp_strength = min(1.5 + (zoom_level / 10.0), 2.2)
        enhanced = apply_unsharp_mask(enhanced, strength=unsharp_strength)
    return enhanced 