
Setup Environment - Shell/Terminal
  python -m venv env
 .\env\Scripts\activate
 pip install -r requirements.txt
 pip install pybind11>=2.12
 pip install --upgrade matplotlib pandas pybind11
 pip install "numpy<2.0"

Run steamlit app
 streamlit run D:/dashboard2/dashboard2.py
