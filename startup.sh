# startup.sh
# About: To be run when you go into a new screen session
#        Run in current directory './startup.sh'
#        Loads modules
#        Activates virtual environment 'thesis_env'

echo "Loading modules..."
module load cuda/10.1
module load python/3.6.5
module load intel/19.0.0.117
module load sox/14.4.2

echo "Activating thesis_env virtual environment..."
source thesis_env/bin/activate
