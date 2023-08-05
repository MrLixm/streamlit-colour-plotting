# ! expected PWD is the repo root
read -p "Submit the process PID that can be found in the task manager (named python.exe):" process_pid
current_date="`date +%Y%m%d_%H%M%S`";
echo "Creating dev/profiling directory ..."
mkdir dev/profiling/
echo "Starting psrecord, use ctrl+c to stop...."
# `exec` to handle properly ctrl+c
exec psrecord $process_pid --log "dev/profiling/profiling-$current_date.txt" --plot "./dev/profiling/plot-$current_date.png"