# renee_thesis

All the code for my thesis on improving speech recognition systems for children.

**Steps**:
Make sure kaldi is installed first before proceeding.
1.  Download all the required datasets
2.  In ```s5/run.sh``` modify [DATASET NAME]_ROOT to point to the main directory of the dataset
3.  ```./run.sh```  **This will build the HMM-GMM model**
4.  After completed successfully run ```local/nnet3/run_tdnn_delta.sh```  **for the TDNN model**
THe script ```s5/clean.sh``` will remove file created from s5/run.sh so that you can train the models again.

**Install Kaldi**:
Refer to: https://kaldi-asr.org/doc/tutorial_setup.html

1. ```git clone https://github.com/kaldi-asr/kaldi.git```
2. Look at the ```kaldi/INSTALL``` file and follow the instructions there
3. Download SRILM by running ```kaldi/tools/install_srilm.sh```

**Initialising katana**:

To execute the steps using the supercomputer katana.

1. In Windows PuTTY: use host name = katana1.restech.unsw.edu.au and log in using zID and password
   In Linux: ```ssh zID@katana1.restech.unsw.edu.au``` in terminal. Or, use the alias ```katana```.
2. Create a new screen using ```screen -S nameOfSession``` (the screen I'm using is called 'thesis')
3. Request an interactive GPU node using ```qsub -I -l select=1:ngpus=2:ncpus=16:mem=80gb,walltime=10:00:00```. Once the node is ready, you are now in the node. The terminal will show (zID@kxxx), where kxxx is your node. 
4. Now you are inside the screen, and inside the GPU node. Run whatever process you need. 
5. Load modules by running ```./loadmodules.sh``` or
```
module load cuda/10.1
module load python/3.6.5
module load intel/19.0.0.117
module load sox/14.4.2
```
Note: If there is an error message saying Permission Denied when running a script, use ```chmod u+x -R /path/to/directory``` to change the permissions of all the files in the directory so that you have permission to execute. 

To install any python packages not in katana, use a virtual environment: https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/
The virtual environment I am using currently is kaldi/egs/renee_thesis/thesis_env ```source thesis_env/bin/activate``` 
To list all the packages in this virtual environment use ```pip list```
Currently my environment includes num2words package.

**Leaving katana**
Asumming you are inside a screen, and inside a requested GPU node. 
1. ```CtrlA D``` to detach from the screen session.
2. ```exit``` to logout of the katana session.

**Returning to katana**
1. ```ssh zID@katana1.restech.unsw.edu.au``` in terminal. Or, use the alias ```katana```.
2. Go back to your screen ```screen -r nameOfSession``` eg. screen -r ogi

**Useful katana screen things**
- To create a new window (tab) within a screen, use ```CtrlA C```
- To go to next and previous windows, use ```CtrlA N``` and ```CtrlA P``` respectively.
- To check if you are in a screen, type the command ```echo $TERM```
- To list your screen, type command ```screen -list```
- To detach a screen remotely, find the screen name using ```screen -list``` and then ```screen -d [name of screen]```
