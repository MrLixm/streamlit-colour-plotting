export PYTHONPATH=$PWD/streamlit_colourplotting:$PWD/streamlit_colourplotting/ui:$PWD/streamlit_colourplotting/core
echo $PYTHONPATH
python -m streamlit run src/app.py --server.headless true