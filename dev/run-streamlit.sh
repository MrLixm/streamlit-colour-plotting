export PYTHONPATH=$PWD/streamlit_colourplotting:$PWD/streamlit_colourplotting/ui:$PWD/streamlit_colourplotting/core
# python logging level expected
export APP_LOG_LEVEL=DEBUG
echo $PYTHONPATH
python -m streamlit run src/app.py --server.headless true