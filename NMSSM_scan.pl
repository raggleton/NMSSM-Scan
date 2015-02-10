#!/usr/bin/perl
use strict;
use warnings 'all';
use Archive::Tar;
use File::Basename;
use File::Path qw/make_path/;


# ---- find Script ---- #
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
my $nfinal = 5000;

my $npoints = $nfinal - $ninit + 1;
print "Running over $npoints points\n";

###########################################
# determine how many points / batch job, and how many batch jobs
###########################################
my $batchsize = 1000;
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


# counter for good points
my $igood=0;

# open(OUTPUT,">>$ScriptPath/output/output.dat");

# keep a list of all input files
# my @inp_filelist = ();

for(my $icount = $ninit; $icount <= $nfinal; $icount++){

  # initializing BR to zero (e.g. if the decay is kinematically forbidden)
  # $Brh1a1a1=0;
  # $Brh2a1a1=0;
  # $Bra1tautau=0;


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


  # running NMSSM decay
  #WIP. Have to set the directory by hand. If I put $ScriptPath does not work
  # system("cd $NMSSMtoolsPath && ./run Daniele_scan/input/inp.dat");
  # system("cd $NMSSMtoolsPath && ./run NMSSM-Scan/input/inp_$icount.dat");

  
#   # checking warning on exp. constraints and higgs mass
#   undef @concheck;
#   open(CONSTRAINT_CHECK, "$ScriptPath/input/spectr.dat");
#   while(<CONSTRAINT_CHECK>){
#       if(/BLOCK SPINFO/) {
# 	  while (<CONSTRAINT_CHECK>) {
# 	  last if /BLOCK MODSEL/;
# 	  push @concheck, $_;
# 	  }
#       }
#   }
#   $check=@concheck;
  
#   # saving informations for good points
#   if($check==3){
  
#     open(DATASPECTR, "$ScriptPath/input/spectr.dat");
#     while(<DATASPECTR>){
#       $mtau=$1 if /     7     (.\S+..)   \# MTAU/;
#       $mh1=$1 if /        25     (.\S+..)   \# lightest neutral scalar/;
#       $mh2=$1 if /        35     (.\S+..)   \# second neutral scalar/;
#       $mh3=$1 if /        45     (.\S+..)   \# third neutral scalar/;
#       $ma1=$1 if /        36     (.\S+..)   \# lightest pseudoscalar/;
#       $ma2=$1 if /        46     (.\S+..)   \# second pseudoscalar/;
#       $mhc=$1 if /        37     (.\S+..)   \# charged Higgs/;
#       # parameters
#       $tgbeta=$1 if /     3     (.\S+..)   \# TANBETA\(MZ\)/;
#       $mueff=$1 if /    65     (.\S+..)   \# MUEFF/;
#       $lambda=$1 if /    61     (.\S+..)   \# LAMBDA/;
#       $kappa=$1 if /    62     (.\S+..)   \# KAPPA/;
#       $alambda=$1 if /    63    *(.\S+..)   \# ALAMBDA/;
#       $akappa=$1 if /    64   *(.\S+..)   \# AKAPPA/;
      
#       #higgs reduced couplings
#       $h1u=$1 if /  1  1     *(.\S+..)   \# U-type fermions/;
#       $h1d=$1 if /  1  2     *(.\S+..)   \# D-type fermions/;
#       $h1V=$1 if /  1  3     *(.\S+..)   \# W,Z bosons/;
#       $h1G=$1 if /  1  4     *(.\S+..)   \# Gluons/;
#       $h1A=$1 if /  1  5     *(.\S+..)   \# Photons/;
                              
#       $h2u=$1 if /  2  1     *(.\S+..)   \# U-type fermions/;
#       $h2d=$1 if /  2  2     *(.\S+..)   \# D-type fermions/;
#       $h2V=$1 if /  2  3     *(.\S+..)   \# W,Z bosons/;
#       $h2G=$1 if /  2  4     *(.\S+..)   \# Gluons/;
#       $h2A=$1 if /  2  5     *(.\S+..)   \# Photons/;
      
#     }#end while
#     close(DATASPECTR);
#     $mtau=$mtau*1.0;
#     $mh1=$mh1*1.0;
#     $mh2=$mh2*1.0;
#     $mh3=$mh3*1.0;
#     $ma1=$ma1*1.0;
#     $ma2=$ma2*1.0;
#     $mhc=$mhc*1.0;
    
#     $tgbeta=$tgbeta*1.0;
#     $mueff=$mueff*1.0;
#     $lambda=$lambda*1.0;
#     $kappa=$kappa*1.0;
#     $alambda=$alambda*1.0;
#     $akappa=$akappa*1.0;
    
#     $h1u=$h1u*1.0;
#     $h1d=$h1d*1.0;
#     $h1V=$h1V*1.0;
#     $h1G=$h1G*1.0;
#     $h1A=$h1A*1.0;
    
#     $h2u=$h2u*1.0;
#     $h2d=$h2d*1.0;
#     $h2V=$h2V*1.0;
#     $h2G=$h2G*1.0;
#     $h2A=$h2A*1.0;
    

    
#     open(DATADECAY, "$ScriptPath/input/decay.dat");
#     while(<DATADECAY>){
#         $Brh1a1a1=$1 if /     (.*)    2          36        36   # BR\(H_1 -> A_1 A_1\)/;
#         $Brh2a1a1=$1 if /     (.*)    2          36        36   # BR\(H_2 -> A_1 A_1\)/;
#         $Bra1tautau=$1 if /     (.*)    2          15       -15   # BR\(A_1 -> tau tau\)/;
#     }
#     close(DATADECAY);
    
#     $Brh1a1a1=$Brh1a1a1*1.0;
#     $Brh2a1a1=$Brh2a1a1*1.0;
#     $Bra1tautau=$Bra1tautau*1.0;
    
#     $igood++;
    
# #    system("cp $ScriptPath/input/spectr.dat $ScriptPath/output/spectr_${icount}");
# #    system("cp $ScriptPath/input/decay.dat $ScriptPath/output/decay_${icount}");
#     print OUTPUT "mh1 mh2 mh3 ma1 ma2 mhc Brh1a1a1 Brh2a1a1 tgbeta mueff lambda alambda akappa h1u h1d h1V h1A h2u h2d h2V h2G h2A"
#     if($ma1<100){
#       print OUTPUT $mh1;
#       print OUTPUT " ";
#       print OUTPUT $mh2;
#       print OUTPUT " ";
#       print OUTPUT $mh3;
#       print OUTPUT " ";
#       print OUTPUT $ma1;
#       print OUTPUT " ";
#       print OUTPUT $ma2;
#       print OUTPUT " ";
#       print OUTPUT $mhc;
#       print OUTPUT " ";
#       print OUTPUT $Brh1a1a1;
#       print OUTPUT " ";
#       print OUTPUT $Brh2a1a1;
#       print OUTPUT " ";
#       print OUTPUT $Bra1tautau;
#       print OUTPUT " ";
#       print OUTPUT "$tgbeta";
#       print OUTPUT " ";
#       print OUTPUT "$mueff";
#       print OUTPUT " ";
#       print OUTPUT "$lambda";
#       print OUTPUT " ";
#       print OUTPUT "$kappa";
#       print OUTPUT " ";
#       print OUTPUT "$alambda";
#       print OUTPUT " ";
#       print OUTPUT "$akappa";
#       print OUTPUT " ";
#       print OUTPUT "$h1u";
#       print OUTPUT " ";
#       print OUTPUT "$h1d";
#       print OUTPUT " ";
#       print OUTPUT "$h1V";
#       print OUTPUT " ";
#       print OUTPUT "$h1G";
#       print OUTPUT " ";
#       print OUTPUT "$h1A";
#       print OUTPUT " ";
#       print OUTPUT "$h2u";
#       print OUTPUT " ";
#       print OUTPUT "$h2d";
#       print OUTPUT " ";
#       print OUTPUT "$h2V";
#       print OUTPUT " ";
#       print OUTPUT "$h2G";
#       print OUTPUT " ";
#       print OUTPUT "$h2A";
#       print OUTPUT "\n";
#     }

#   }# end good points


  
} # end loop on number of random points to scan

# close(OUTPUT);

# system("rm $ScriptPath/input/*");

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
# print("### N. points found =   $igood            \n");
print("##########################################\n");

exit;



