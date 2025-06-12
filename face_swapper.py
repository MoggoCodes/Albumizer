import os
import cv2
import torch
import numpy as np
from PIL import Image
from insightface.app import FaceAnalysis
import insightface
import argparse
from pathlib import Path

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
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            result_pil.save(output_path)
        return result_pil

def main():
    parser = argparse.ArgumentParser(description='Face swapping for album covers')
    parser.add_argument('source', help='Name of the source image file (from Photos/People/)')
    parser.add_argument('target', help='Name of the target album cover (from Photos/Albums/)')
    parser.add_argument('--output', '-o', help='Name for the output file (will be saved in Photos/Swapped/)')
    
    args = parser.parse_args()
    
    # Construct full paths
    source_path = os.path.join('Photos', 'People', args.source)
    target_path = os.path.join('Photos', 'Albums', args.target)
    
    # If no output name specified, construct one from source and target names
    if not args.output:
        source_name = Path(args.source).stem
        target_name = Path(args.target).stem
        output_name = f"{source_name}_on_{target_name}.png"
    else:
        output_name = args.output if args.output.endswith(('.png', '.jpg', '.jpeg')) else f"{args.output}.png"
    
    output_path = os.path.join('Photos', 'Swapped', output_name)
    
    # Verify input files exist
    if not os.path.exists(source_path):
        raise FileNotFoundError(f"Source image not found: {source_path}")
    if not os.path.exists(target_path):
        raise FileNotFoundError(f"Target album cover not found: {target_path}")
    
    try:
        swapper = FaceSwapper()
        result = swapper.swap_face(
            source_image_path=source_path,
            target_image_path=target_path,
            output_path=output_path
        )
        print(f"Face swapped image saved to {output_path}")
        
    except Exception as e:
        print(f"Error during face swapping: {e}")

if __name__ == "__main__":
    main() 