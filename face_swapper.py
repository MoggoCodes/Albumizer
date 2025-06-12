import os
import cv2
import torch
import numpy as np
from PIL import Image
from insightface.app import FaceAnalysis
import insightface
from safetensors.torch import load_file

class FaceSwapper:
    def __init__(self):
        # Initialize face detection
        self.face_analyzer = FaceAnalysis(name="buffalo_l", providers=['CPUExecutionProvider'])
        self.face_analyzer.prepare(ctx_id=0, det_size=(640, 640))
        
        # Initialize face swapper
        model_path = "models/insightface/inswapper_128.onnx"
        self.face_swapper = insightface.model_zoo.get_model(model_path)

    def detect_faces(self, image_path):
        """Detect faces in an image using InsightFace"""
        # Read image
        if isinstance(image_path, str):
            img = cv2.imread(image_path)
        else:
            img = cv2.cvtColor(np.array(image_path), cv2.COLOR_RGB2BGR)
            
        # Detect faces
        faces = self.face_analyzer.get(img)
        return faces, img

    def swap_face(self, source_image_path, target_image_path, output_path=None):
        """Swap faces between source and target images"""
        # Detect faces in both images
        source_faces, source_img = self.detect_faces(source_image_path)
        target_faces, target_img = self.detect_faces(target_image_path)
        
        if not source_faces or not target_faces:
            raise ValueError("No faces detected in one or both images")
        
        # Swap faces
        result = target_img.copy()
        for target_face in target_faces:
            result = self.face_swapper.get(result, target_face, source_faces[0], paste_back=True)
        
        # Convert to PIL Image
        result_pil = Image.fromarray(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
        
        # Save or return the result
        if output_path:
            result_pil.save(output_path)
        return result_pil

def main():
    swapper = FaceSwapper()
    
    # Replace these paths with your actual paths
    source_image = "Headshot.JPG"  # Image containing the face you want to use
    target_image = "jam.jpg"  # Album cover
    output_path = "face_swapped_album.png"
    
    try:
        result = swapper.swap_face(
            source_image_path=source_image,
            target_image_path=target_image,
            output_path=output_path
        )
        print(f"Face swapped image saved to {output_path}")
        
    except Exception as e:
        print(f"Error during face swapping: {e}")

if __name__ == "__main__":
    main() 