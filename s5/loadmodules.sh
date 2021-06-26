# Loads all the useful modules
# All the modules are found in directory /apps/
# e.g. /apps/gcc/8.4.0

# Unload current cuda module with newer version
module unload cuda/10.1
module load cuda/11.1
# Unload current gcc with newer version
module unload gcc/4.8.5
module load gcc/8.4.0
# More modules
module load python/3.6.5
module load intel/19.0.0.117
module load sox/14.4.2
