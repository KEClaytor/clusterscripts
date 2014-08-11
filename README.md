clusterscripts
==============

Collection of scripts I've written that I've used for the DSCR cluster.

ssjob.py
--------
Submit MATLAB file to run on the cluster. Allow specification of <path> to add to the MATLAB path, and version of MATLAB to use.
Download and make executable: chmod 775 ssjob.py
Run help to view all options: ./ssjob.py -h

upload.sh/download.sh
---------------------
Batch upload / download files by extension. Useful if you're on a linux box, not so much if you have filezilla.
You will likely want to edit download / upload folders and the login node.
Download and make executable: chmod 775 upload.sh
Run: ./upload.sh
