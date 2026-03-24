cat > setup.sh << 'EOF'
#!/bin/bash

echo "FaceSwapPro Installation"
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

if command -v nvidia-smi &> /dev/null; then
    echo "NVIDIA GPU detected. Installing CUDA-optimized PyTorch..."
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
fi

mkdir -p models outputs temp face_db
echo "Setup complete! Run: python app.py"
EOF

chmod +x setup.sh