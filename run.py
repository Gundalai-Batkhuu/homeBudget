from src.controller.desktop_controller import run_desktop_app
from src.controller.streamlit_controller import run_streamlit_app
import sys

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "web":
        run_streamlit_app()
    else:
        run_desktop_app()

