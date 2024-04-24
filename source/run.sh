
module purge;
module load anaconda3;
module load singularityce;
module load /home/fisher_research/Module/fishermodulefile;
export PYTHONPATH=$(pwd):$PYTHONPATH
python -c "
from Crontab import run; print(run); run();
"
