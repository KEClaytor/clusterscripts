# Download script for the Duke cluster (DSCR)
# Adapt as you see fit.
# Provided "as is" with no support.
# 2012-06-25 Kevin Claytor

# The file extensions we wish to download
ftypes[0]=.m
ftypes[1]=.mat
ftypes[2]=.log
ftypes[3]=.err
ftypes[4]=.txt
ftypes[5]=.q
ftypes[6]=.jpg
nftypes=7;

# Find which folder the user wants to download to
echo "User Deteccted as $USER"
echo "NMR Folder (1) or Laser Folder (2)"
read fldr
if test $fldr = 1; then
	folder=/xtmp/kec30/repos/WarrenLab/NMRLungDiffusion/Simulation_Code/
elif test $fldr = 2; then
	folder=/xtmp/kec30/repos/WarrenLab/ScatteringAndEpiImaging/Simulation_Code/
else
	echo "Okay smarty-pants, put in your own folder."
	read folder
	echo "You sure you want to put it in $folder? (Y/n)"
	read dm
	if test $dm != Y
	then
		echo "One more chance..."
		read folder
		echo "This had better be right; $folder"
	fi
fi

# Loop over the file types we specified above
for ((i = 0; i < nftypes; i++))
do
	# Ask if the user wants to download that file type
	echo "Download ${ftypes[$i]} files? (Y/n/q)"
	read dm
	if test $dm = Y
	then
		# Copy all files of that type from the remote directory to the specified folder
		scp $USER@dscr-login-01.oit.duke.edu:*${ftypes[$i]} $folder
	elif test $dm = q
	then
		# Break out by setting i = ntftypes
		i=nftypes
	fi
done

