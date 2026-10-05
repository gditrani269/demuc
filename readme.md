python3 -m venv .venv
source .venv/bin/activate


ffmpeg -version
si no esa instalado: (siendo root ejecutar)
apt update
apt install ffmpeg

instalamos demucs
python -m pip install -U pip
python -m pip install demucs

verifica con:
demucs --help
y
python -c "import demucs; print('Demucs OK')"
Demucs OK  (esta OK)

si es necesario instalar numpy:
python -m pip install numpy

una comprobacion mas haciendo:
python -c "import torch; print('PyTorch:', torch.__version__); print('CPU disponible:', torch.cuda.is_available())"
PyTorch: 2.14.1+cu130
CPU disponible: False

como usarlo:
en la carpeta "canciones" ponemos nuestra cancion
en la carpeta "pistas" tendremos las pistas resultantes.
Ejecutamos el comando:
demucs -o pistas canciones/mi_cancion.mp3
y obtenemos:
pistas/
└── htdemucs/
    └── mi_cancion/
        ├── bass.wav
        ├── drums.wav
        ├── other.wav
        └── vocals.wav

y para usar el modelo experimental de 6 pistas que discrimina guitarra (entre 6 pistas):
demucs -n htdemucs_6s -o pistas canciones/mi_cancion.mp3
y obtenemos
pistas/
└── htdemucs_6s/
    └── mi_cancion/
        ├── bass.wav
        ├── drums.wav
        ├── guitar.wav
        ├── piano.wav
        ├── other.wav
        └── vocals.wav

Para deteccion de notas usaremos  librosa + pYIN.
Asi que instalaremos:
python -m pip install librosa soundfile
comprobamos con:
python -c "import librosa; print('Librosa:', librosa.__version__)"

seguramente en elgun momento sera necesario instalartambien:
pip install matplotlib

python -c "import matplotlib; print('Matplotlib:', matplotlib.__version__)"