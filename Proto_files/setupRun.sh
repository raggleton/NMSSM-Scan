#!/bin/bash
host=`hostname`
echo "Running on $host"
echo "With parameters: $@"
# parameters are: [batch number] [batch size]
# so we run over
# inp_[batch number * batch size].dat
# to
# inp_[(batch_number+1 * batch size)-1].dat

# Setup NMSSMTools on execute machine
tar -xvzf NMSSMTOOLS.tgz
# Setup our input files
tar -xvzf input.tgz
ls
# Run over all relevant input files
START=$(($1*$2))
END=$(( (($1+1)*$2)-1 ))
for inp in $(eval echo "{$START..$END}"); do
    ./run inp_${inp}.dat
done
