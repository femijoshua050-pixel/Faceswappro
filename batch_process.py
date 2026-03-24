cat > batch_process.py << 'EOF'
#!/usr/bin/env python3
import os
import sys
from pathlib import Path
import cv2
import argparse
from tqdm import tqdm

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from core.face_swapper import AdvancedFaceSwapper

def batch_process(source_path, target_folder, output_folder, **kwargs):
    print("Initializing FaceSwapPro Batch Processor...")
    swapper = AdvancedFaceSwapper(device='cuda')
    source_img = cv2.imread(source_path)
    if source_img is None:
        print(f"Error loading source image: {source_path}")
        return
    print(f"Source image loaded: {source_path}")
    
    target_paths = (list(Path(target_folder).glob("*.jpg")) + 
                   list(Path(target_folder).glob("*.png")) +
                   list(Path(target_folder).glob("*.jpeg")))
    
    if len(target_paths) == 0:
        print(f"No images found in {target_folder}")
        return
    
    print(f"Found {len(target_paths)} target images")
    processed_count = 0
    
    for target_path in tqdm(target_paths, desc="Processing images"):
        target_img = cv2.imread(str(target_path))
        if target_img is None:
            continue
        try:
            result = swapper.swap_faces(source_img, target_img, **kwargs)
            output_path = Path(output_folder) / f"swapped_{target_path.name}"
            cv2.imwrite(str(output_path), result)
            processed_count += 1
        except Exception as e:
            print(f"Error processing {target_path.name}: {e}")
    
    print(f"Batch processing complete! Processed {processed_count}/{len(target_paths)} images")
    print(f"Output saved to: {output_folder}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Batch process images with FaceSwapPro")
    parser.add_argument("source", help="Path to source image")
    parser.add_argument("target", help="Path to target folder")
    parser.add_argument("output", help="Path to output folder")
    parser.add_argument("--enhance", action="store_true", help="Enable face enhancement")
    parser.add_argument("--smooth", action="store_true", help="Enable smooth blending")
    
    args = parser.parse_args()
    Path(args.output).mkdir(exist_ok=True, parents=True)
    batch_process(args.source, args.target, args.output, enhance=args.enhance, smooth=args.smooth)
EOF

chmod +x batch_process.py