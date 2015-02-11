#!/usr/bin/perl
use strict;
use warnings 'all';
use Archive::Tar;
use File::Basename;
use File::Path qw/make_path/;

##################################################
# This script makes lots of input files, and sets up
# for batch running on HTCondor system at Bristol
##################################################

# ---- find PWD ---- #
my $ScriptPath = $ENV{PWD};
print "ScriptPath: ", $ScriptPath, "\n";

# --- find NMSSM tools dir ---#
# $ENV{PWD} =~ m@^(.*)(/[^/]+){1}$@; $NMSSMtoolsPath = $1;
# print "NMSSMtoolsPath: ", $NMSSMtoolsPath, "\n";

###########################################
# select max and min range for parameters
###########################################

my $tgbetamax=50;
my $tgbetamin=1.5;

my $mueffmax=300;
my $mueffmin=100;
  
my $lambdamax=1;
my $lambdamin=0;
  
my $kappamax=1;
my $kappamin=0;

my $alambdamax=+4000;
my $alambdamin=-4000;

my $akappamax=+10;
my $akappamin=-30;

###########################################
# select number of random points to generate:
###########################################

# $ninit=SED_NINIT;
my $ninit = 1;

# $nfinal=SED_NFINAL;
my $nfinal = 500000;

my $npoints = $nfinal - $ninit + 1;
print "Running over $npoints points\n";

###########################################
# determine how many points / batch job, and how many batch jobs
###########################################
my $batchsize = 10000;
my $nbatch = $npoints / $batchsize;
if ($npoints % $batchsize != 0) {
  $nbatch += 1;
}
print "Doing points in $nbatch batches of $batchsize\n";

# imposing derivate bounds on min or max parameters (edit corresponding part)

my $userbounds=1;


######################################################
#####         SCRIPT STARTING                   ######
######################################################

# Get date and time for unique folder name
my @months = qw( Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec );
my ($sec,$min,$hour,$mday,$mon,$year,$wday,$yday,$isdst) = localtime();
$year -= 100;
$mon = $months[$mon];
my $date = "${mday}_${mon}_${year}";
# Fix bug in localtime - if 0 minutes past the hour, localtime returns 0, not 00
if ($min == "0") {
  $min = "00";
}
my $time = "$hour$min";

# Optional description for this set of jobs (to remind you in 6 months time :D)
my $desc = "first";

# make directory to hold input and output
my $job_dir = "jobs_${desc}_${date}_${time}";
print "Input files going into: ", $job_dir, "\n";

unless (make_path($job_dir)) {
  die "Cannot create directory $job_dir - already exists?";
}

# removing old outputs
# system("rm $ScriptPath/output/*");

# computing range for random generator
my $deltatgbeta=($tgbetamax-$tgbetamin);
my $x0tgbeta=$tgbetamin;

my $deltalambda=($lambdamax-$lambdamin);
my $x0lambda=$lambdamin;

my $deltakappa=($kappamax-$kappamin);
my $x0kappa=$kappamin;

my $deltaalambda=($alambdamax-$alambdamin);
my $x0alambda=$alambdamin;

my $deltaakappa=($akappamax-$akappamin);
my $x0akappa=$akappamin;

my $deltamueff=($mueffmax-$mueffmin);
my $x0mueff=$mueffmin;

# keep a list of all input files
# my @inp_filelist = ();

for(my $icount = $ninit; $icount <= $nfinal; $icount++){

  # generating random points within the range
  my $tgbeta=rand($deltatgbeta)+$x0tgbeta;
  my $lambda=rand($deltalambda)+$x0lambda;
  my $kappa=rand($deltakappa)+$x0kappa;
  my $alambda=rand($deltaalambda)+$x0alambda;
  my $akappa=rand($deltaakappa)+$x0akappa;
  my $mueff=rand($deltamueff)+$x0mueff;
  
  # in case of different and dependent range, write it here
  # my scan 2
  if($userbounds==1){
  
    $kappa=rand((200*$lambda)/$mueff);
  
#    $deltaakappa=3;
#    $x0akappa=30*$lambda*$lambda-3;
#    $akappa=rand($deltaakappa)+$x0akappa;
  }
  
  
  # writing the input files to job folder
  open(INPUT_PROTO, "$ScriptPath/Proto_files/inp_PROTO.dat") or die;
  my $new_input = "$job_dir/inp_$icount.dat";
  open(INPUT,	  ">$ScriptPath/${new_input}") or die;
    if ($icount % 500 == 0 || $icount == $nfinal) {
      print "Making input card $ScriptPath/${new_input}\n";
    }
    while(<INPUT_PROTO>) {
      $_ =~ s/SED_TGBETA/$tgbeta/g;
      $_ =~ s/SED_LAMBDA/$lambda/g;
      $_ =~ s/SED_KAPPA/$kappa/g;
      $_ =~ s/SED_ALAMBDA/$alambda/g;
      $_ =~ s/SED_AKAPPA/$akappa/g;
      $_ =~ s/SED_MUEFF/$mueff/g;
      print(INPUT);
    }
    # push(@inp_filelist, $new_input);
  close(INPUT_PROTO);
  close(INPUT);

} # end loop on number of random points to scan

# tar up input files for easy transport
# my $tar = Archive::Tar->new();
# $tar->add_files(@inp_filelist);
# $tar->write("$job_dir/input.tgz", "COMPRESSION_GZIP");
system("cd $job_dir && tar -cvzf input.tgz inp_*.dat && cd ../..");

# make HTCondor job file
open(JOB_PROTO, "$ScriptPath/Proto_files/runScan.condor") or die;
open(JOB, ">$ScriptPath/$job_dir/runScan.condor") or die;
  print "Making HTCondor job description $ScriptPath/$job_dir/runScan.condor\n";
  while(<JOB_PROTO>) {
    $_ =~ s/SED_INPUT/$ScriptPath\/$job_dir\/input.tgz/g;
    $_ =~ s/SED_ARG/\$(process) $batchsize/g;
    $_ =~ s/SED_INITIAL/$ScriptPath\/$job_dir/g;
    $_ =~ s/SED_JOB/queue $nbatch/g;
    print(JOB);
  }
close(JOB_PROTO);
close(JOB);

# make shell script to setup run
open(SETUP_SCRIPT_PROTO, "$ScriptPath/Proto_files/setupRun.sh") or die;
open(SETUP_SCRIPT, ">$ScriptPath/$job_dir/setupRun.sh") or die;
  print "Making run setup script $ScriptPath/$job_dir/setupRun.sh\n";
  while(<SETUP_SCRIPT_PROTO>) {
    # $_ =~ s///g;
    print(SETUP_SCRIPT);
  }
close(SETUP_SCRIPT_PROTO);
close(SETUP_SCRIPT);

print "Can now run jobs with\ncondor_submit $job_dir/runScan.condor\n";

# printing scan statement
print("\n");
print("\n");
print("##########################################\n");
print("### N. iterations   =   $npoints          \n");
print("##########################################\n");

exit;



