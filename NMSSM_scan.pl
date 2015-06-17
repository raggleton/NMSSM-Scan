#!/usr/bin/perl
use strict;
use warnings 'all';
use Archive::Tar;
use File::Basename;
use File::Path qw/make_path/;

###################################################################
# This script runs NMSSMTools over many parameter points.
# The output "spectr_X_Y.dat" files are produced in $PWD
#
# Usage:
# perl NMSSM_scan.pl <input/output dir> X
#
# where <input/output dir> is the job directory name
# where X is a unique identifier for these spectrum files
# e.g. $(process) for HTcondor jobs
#
####################################################################

# ---- find PWD ---- #
my $ScriptPath = $ENV{PWD};
print("ScriptPath: ", $ScriptPath, "\n");

my $outDir = $ARGV[0];
print("Output dir: ", $outDir, "\n");

# --- find NMSSM tools dir ---#
# $ENV{PWD} =~ m@^(.*)(/[^/]+){1}$@; $NMSSMtoolsPath = $1;
# print "NMSSMtoolsPath: ", $NMSSMtoolsPath, "\n";

# Unique identifier for the set of spectrum files from this script
my ${unique} = $ARGV[1];

###########################################
# select max and min range for parameters
###########################################
## EDIT ME
my $tgbetamax=50;
my $tgbetamin=1.5;

my $mueffmax=300;
my $mueffmin=100;
  
my $lambdamax=0.7;
my $lambdamin=0;
  
my $kappamax=0.7;
my $kappamin=0;

my $alambdamax=+4000;
my $alambdamin=-1000;

my $akappamax=2.5;
my $akappamin=-30;

my $m3min=500;
my $m3max=2000;

my $mq3min=500;
my $mq3max=2500;

my $mu3min=500;
my $mu3max=2500;

my $md3min=500;
my $md3max=2500;

my $au3min=500;
my $au3max=3000;

my $ad3min=500;
my $ad3max=3000;

# For Nils-Erik's card (inp_NE_PROTO.dat)
my $m0max=1200;
my $m0min=800;

my $m12max=1200;
my $m12min=800;

my $a0max=-800;
my $a0min=-1200;

$tgbetamax=6;
$tgbetamin=1.5;

$mueffmax=120;
$mueffmin=100;

$lambdamax=0.6;
$lambdamin=0.4;

$kappamax=0.3;
$kappamin=0.2;

$alambdamax=-200;
$alambdamin=-250;

$akappamax=-100;
$akappamin=-120;

# imposing dependant bounds on min or max parameters
# (edit corresponding part in loop overicount)
my $userbounds=0;

###########################################
# select number of random points to generate:
###########################################

my $ninit = 1;
my $nfinal = 5000; ## EDITME - number of points to scan over

my $npoints = $nfinal - $ninit + 1;
print("Running over $npoints points\n");

######################################################
#####         SCRIPT STARTING                   ######
######################################################

# Make note of what range was run over
my $comments = "# Scanning range:\n";
$comments .= "# tan(beta): $tgbetamin -> $tgbetamax\n";
$comments .= "# mu_eff: $mueffmin -> $mueffmax\n";
$comments .= "# lambda: $lambdamin -> $lambdamax\n";
$comments .= "# kappa: $kappamin -> $kappamax\n";
$comments .= "# A_lambda: $alambdamin -> $alambdamax\n";
$comments .= "# A_kappa: $akappamin -> $akappamax\n";
$comments .= "# M3: $m3min -> $m3max\n";
$comments .= "# MQ3: $mq3min -> $mq3max\n";
$comments .= "# MU3: $mu3min -> $mu3max\n";
$comments .= "# MD3: $md3min -> $md3max\n";
$comments .= "# AU3: $au3min -> $au3max\n";
$comments .= "# AD3: $ad3min -> $ad3max\n";

# computing range for random generator
my $deltatgbeta = ($tgbetamax - $tgbetamin);
my $x0tgbeta = $tgbetamin;

my $deltalambda = ($lambdamax - $lambdamin);
my $x0lambda = $lambdamin;

my $deltakappa = ($kappamax - $kappamin);
my $x0kappa = $kappamin;

my $deltaalambda = ($alambdamax - $alambdamin);
my $x0alambda = $alambdamin;

my $deltaakappa = ($akappamax - $akappamin);
my $x0akappa = $akappamin;

my $deltamueff = ($mueffmax - $mueffmin);
my $x0mueff = $mueffmin;

my $deltam3 = ($m3max - $m3min);
my $x0m3 = $m3min;

my $deltamq3 = ($mq3max - $mq3min);
my $x0mq3 = $mq3min;

my $deltamu3 = ($mu3max - $mu3min);
my $x0mu3 = $mu3min;

my $deltamd3 = ($md3max - $md3min);
my $x0md3 = $md3min;

my $deltaau3 = ($au3max - $au3min);
my $x0au3 = $au3min;

my $deltaad3 = ($ad3max - $ad3min);
my $x0ad3 = $ad3min;

my $deltam0 = ($m0max - $m0min);
my $x0m0 = $m0min;

my $deltam12 = ($m12max - $m12min);
my $x0m12 = $m12min;

my $deltaa0 = ($a0max - $a0min);
my $x0a0 = $a0min;

# Read prototype input file into array so quicker
# open(INPUT_PROTO, "$ScriptPath/inp_PROTO.dat") or die;
open(INPUT_PROTO, "$ScriptPath/inp_NE_PROTO.dat") or die;
chomp (my @proto = (<INPUT_PROTO>));
close(INPUT_PROTO);

# Run parameter points - make an input file, run it, delete it
for(my $icount = 0; $icount < $nfinal; $icount++){

  # generating random points within the range
  my $tgbeta = rand($deltatgbeta) + $x0tgbeta;
  my $lambda = rand($deltalambda) + $x0lambda;
  my $kappa = rand($deltakappa) + $x0kappa;
  my $alambda = rand($deltaalambda) + $x0alambda;
  my $akappa = rand($deltaakappa) + $x0akappa;
  my $mueff = rand($deltamueff) + $x0mueff;
  my $m3 = rand($deltam3) + $x0m3;
  my $mq3 = rand($deltamq3) + $x0mq3;
  my $mu3 = rand($deltamu3) + $x0mu3;
  my $md3 = rand($deltamd3) + $x0md3;
  my $au3 = rand($deltaau3) + $x0au3;
  my $ad3 = rand($deltaad3) + $x0ad3;
  my $m0 = rand($deltam0) + $x0m0;
  my $m12 = rand($deltam12) + $x0m12;
  my $a0 = rand($deltaa0) + $x0a0;
  
  # in case of different and dependent range, write it here

  if($userbounds==1){
    # Make sure you add any condition to the comments string!
    $kappa = rand((200*$lambda)/$mueff);
    $comments .= "kappa: rand(200 * lambda / mu_eff)\n";
#    $deltaakappa=3;
#    $x0akappa=30*$lambda*$lambda-3;
#    $akappa=rand($deltaakappa)+$x0akappa;
  }
  
  # writing the input files
  my $newInput = "inp_${unique}_${icount}.dat";
  my $inputCard = "${outDir}/${newInput}";
  open(INPUT,   ">$inputCard") or die;

  if ($icount % 500 == 0) {
    print("Making input card $inputCard\n");
  }

  foreach my $line (@proto) {
    my $newline = $line;
    $newline =~ s/SED_TGBETA/$tgbeta/g;
    $newline =~ s/SED_LAMBDA/$lambda/g;
    $newline =~ s/SED_KAPPA/$kappa/g;
    $newline =~ s/SED_ALAMBDA/$alambda/g;
    $newline =~ s/SED_AKAPPA/$akappa/g;
    $newline =~ s/SED_MUEFF/$mueff/g;
    $newline =~ s/SED_COMMENTS/$comments/g;
    $newline =~ s/SED_M3/$m3/g;
    $newline =~ s/SED_MQ3/$mq3/g;
    $newline =~ s/SED_MU3/$mu3/g;
    $newline =~ s/SED_MD3/$md3/g;
    $newline =~ s/SED_AU3/$au3/g;
    $newline =~ s/SED_AD3/$ad3/g;
    $newline =~ s/SED_M0/$m0/g;
    $newline =~ s/SED_A0/$a0/g;
    $newline =~ s/SED_M12/$m12/g;

    $newline .= "\n";
    print INPUT $newline;
  }
  close(INPUT);

  # run NMSSM Tools with new input file
  system("cd NMSSMTools_?.?.?/ && ./run $inputCard && cd ..");

  # remove input file to save space
  unlink "$inputCard";

  #
  # Do NMSSMCALC input file
  #
  # Read prototype NMSSMCALC input file into array so quicker
  # open(INPUT_PROTO, "$ScriptPath/inp_nmssmcalc_PROTO.dat") or die;
  # chomp(my @protoNMSSMCALC = (<INPUT_PROTO>));
  # close(INPUT_PROTO);

  # my $newInputNMSSMCALC = "inp_nmssmcalc_${unique}_${icount}.dat";
  # my $inputCardNMSSMCALC = "${outDir}/${newInputNMSSMCALC}";
  # open(INPUT,   ">$inputCardNMSSMCALC") or die;
  # if ($icount % 500 == 0) {
  #   print("Making input card $inputCardNMSSMCALC\n");
  # }

  # foreach my $line (@protoNMSSMCALC) {
  #   my $newline = $line;
  #   $newline =~ s/SED_TGBETA/$tgbeta/g;
  #   $newline =~ s/SED_LAMBDA/$lambda/g;
  #   $newline =~ s/SED_KAPPA/$kappa/g;
  #   $newline =~ s/SED_ALAMBDA/$alambda/g;
  #   $newline =~ s/SED_AKAPPA/$akappa/g;
  #   $newline =~ s/SED_MUEFF/$mueff/g;
  #   $newline =~ s/SED_COMMENTS/$comments/g;
  #   $newline =~ s/SED_M3/$m3/g;
  #   $newline =~ s/SED_MQ3/$mq3/g;
  #   $newline =~ s/SED_MU3/$mu3/g;
  #   $newline =~ s/SED_MD3/$md3/g;
  #   $newline =~ s/SED_AU3/$au3/g;
  #   $newline =~ s/SED_AD3/$ad3/g;

  #   $newline .= "\n";
  #   print INPUT $newline;
  # }
  # close(INPUT);

  # # run NMSSMCALC with new input file
  # # because the FORTRAN inquire function only take RELATIVE not ABSOLUTE paths
  # # we have to convert out absolute path to a relative one.
  # # easiest way to do this is via python
  # # so we make a temp bash var that has the relpath
  # # Yes, this is ridiculous. Should prob just convert to using relpaths throughout?
  # my $outputNMSSMCALC = "${outDir}/nmssmcalc_${unique}_${icount}.dat";
  # my $relpathCalcIn = `cd nmssmcalc && python -c "import os.path; print os.path.relpath('$inputCardNMSSMCALC')"`;
  # chomp $relpathCalcIn; # important to strip off newlines, otherwise ./run fails
  # my $relpathCalcOut = `cd nmssmcalc && python -c "import os.path; print os.path.relpath('$outputNMSSMCALC')"`;
  # chomp $relpathCalcOut;
  # print("$relpathCalcIn\n");
  # print("$relpathCalcOut\n");
  # system("cd nmssmcalc && ./run $relpathCalcIn slha.in $relpathCalcOut && cd ..");

  # # remove input file
  # unlink "$inputCardNMSSMCALC";


} # end loop on number of random points to scan


# make a note of what param range we ran over
open(NOTES, ">$outDir/paramRange.txt") or die;
print NOTES $comments;
close(NOTES);

# printing scan statement
print("\n");
print("\n");
print("##########################################\n");
print("### N. iterations   =   $npoints          \n");
print("##########################################\n");

exit;
