
# anaconda(또는 miniconda)가 존재하지 않을 경우 설치해주세요!
## TODO
if ! command -v conda &> /dev/null
then
    echo "[INFO] Conda가 없습니다. 설치를 시작합니다..."
    curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.sh
    bash Miniconda3-latest-MacOSX-arm64.sh -b -p $HOME/miniconda
    source "$HOME/miniconda/etc/profile.d/conda.sh"
else
    echo "[INFO] Conda가 이미 설치되어 있습니다."
fi

# Conda 환셩 생성 및 활성화
## TODO
source $(conda info --base)/etc/profile.d/conda.sh
conda create -n myenv python=3.10 -y
conda activate myenv

## 건드리지 마세요! ##
python_env=$(python -c "import sys; print(sys.prefix)")
if [[ "$python_env" == *"/envs/myenv"* ]]; then
    echo "[INFO] 가상환경 활성화: 성공"
else
    echo "[INFO] 가상환경 활성화: 실패"
    exit 1 
fi

# 필요한 패키지 설치
## TODO
pip install mypy

# Submission 폴더 파일 실행
cd submission || { echo "[INFO] submission 디렉토리로 이동 실패"; exit 1; }

for file in *.py; do
    ## TODO
    filename=$(basename "$file" .py)
    real_name=${filename#*_}
    python3 "$file" < "../input/${real_name}_input" > "../output/${filename}_output"
done

# mypy 테스트 실행 및 mypy_log.txt 저장
## TODO
cd ..
mypy submission/ > mypy_log.txt

# conda.yml 파일 생성
## TODO
conda env export > conda.yml

# 가상환경 비활성화
## TODO
conda deactivate