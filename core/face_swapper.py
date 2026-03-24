import cv2
import numpy as np
from pathlib import Path
import pickle
import hashlib
import torch

try:
    from insightface.app import FaceAnalysis
    from insightface.model_zoo import get_model
except ImportError:
    print("InsightFace not installed")

class AdvancedFaceSwapper:
    def __init__(self, device='cuda', model_dir='models'):
        self.device = device
        self.model_dir = Path(model_dir)
        self.model_dir.mkdir(exist_ok=True)
        try:
            self.face_app = FaceAnalysis(name='buffalo_l', root=str(self.model_dir))
            ctx_id = 0 if device == 'cuda' else -1
            self.face_app.prepare(ctx_id=ctx_id, det_size=(640, 640))
            self.swapper = self.load_inswapper()
            self.face_db = {}
            self.load_face_database()
            self.gfpgan = None
        except Exception as e:
            print(f"Error: {e}")
            self.face_app = None
            self.swapper = None
    
    def load_inswapper(self):
        try:
            model_path = self.model_dir / 'inswapper_128.onnx'
            return get_model(str(model_path), download=True, download_zip=True)
        except Exception as e:
            print(f"Error loading inswapper: {e}")
            return None
    
    def swap_faces(self, source_img, target_img, enhance=True, smooth=True, **kwargs):
        if self.face_app is None or self.swapper is None:
            return target_img
        source_faces = self.face_app.get(source_img)
        target_faces = self.face_app.get(target_img)
        if len(source_faces) == 0 or len(target_faces) == 0:
            return target_img
        source_face = source_faces[0]
        areas = [(f.bbox[2] - f.bbox[0]) * (f.bbox[3] - f.bbox[1]) for f in target_faces]
        target_face = target_faces[np.argmax(areas)]
        result = self.swapper.get(target_img, target_face, source_face, paste_back=True)
        if smooth:
            result = self.poisson_blend(target_img, result, target_face.bbox)
        if enhance:
            result = self.enhance_face(result, target_face)
        return result
    
    def poisson_blend(self, original, swapped, bbox):
        x1, y1, x2, y2 = map(int, bbox)
        x1, y1 = max(0, x1 - 20), max(0, y1 - 20)
        x2, y2 = min(original.shape[1], x2 + 20), min(original.shape[0], y2 + 20)
        mask = np.zeros(original.shape[:2], dtype=np.uint8)
        mask[y1:y2, x1:x2] = 255
        center = ((x1 + x2) // 2, (y1 + y2) // 2)
        return cv2.seamlessClone(swapped, original, mask, center, cv2.NORMAL_CLONE)
    
    def enhance_face(self, image, face, method='gfpgan'):
        return image
    
    def process_video(self, source_img, video_path, output_path, **kwargs):
        cap = cv2.VideoCapture(str(video_path))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(str(output_path), fourcc, fps, (width, height))
        frame_idx = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            swapped = self.swap_faces(source_img, frame, **kwargs)
            out.write(swapped)
            frame_idx += 1
        cap.release()
        out.release()
        return output_path
    
    def save_face_database(self):
        db_path = self.model_dir / 'face_db.pkl'
        with open(db_path, 'wb') as f:
            pickle.dump(self.face_db, f)
    
    def load_face_database(self):
        db_path = self.model_dir / 'face_db.pkl'
        if db_path.exists():
            try:
                with open(db_path, 'rb') as f:
                    self.face_db = pickle.load(f)
            except:
                self.face_db = {}