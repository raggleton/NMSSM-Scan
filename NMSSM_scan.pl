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
# perl NMSSM_scan.pl X
#
# where X is a unique identifier for these spectrum files
# e.g. $(process) for HTcondor jobs
#
####################################################################

# ---- find PWD ---- #
my $ScriptPath = $ENV{PWD};
print("ScriptPath: ", $ScriptPath, "\n");

# --- find NMSSM tools dir ---#
# $ENV{PWD} =~ m@^(.*)(/[^/]+){1}$@; $NMSSMtoolsPath = $1;
# print "NMSSMtoolsPath: ", $NMSSMtoolsPath, "\n";

# Unique identifier for the set of spectrum files from this script
my ${unique} = $ARGV[0];

###########################################
# select max and min range for parameters
###########################################
## EDITME
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

# imposing dependant bounds on min or max parameters
# (edit corresponding part in loop overicount)
my $userbounds=0;

###########################################
# select number of random points to generate:
###########################################

my $ninit = 1;
my $nfinal = 10; ## EDITME - number of points to scan over

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

# Read prototype input file into array so quicker
open(INPUT_PROTO, "$ScriptPath/inp_PROTO.dat") or die;
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
  
  # in case of different and dependent range, write it here
  # my scan 2
  if($userbounds==1){
    # Make sure you add any condition to the comments string!
    $kappa = rand((200*$lambda)/$mueff);
    $comments .= "kappa: rand(200 * lambda / mu_eff\n";
#    $deltaakappa=3;
#    $x0akappa=30*$lambda*$lambda-3;
#    $akappa=rand($deltaakappa)+$x0akappa;
  }
  
  # writing the input files
  my $newInput = "inp_${unique}_${icount}.dat";
  open(INPUT,	  ">$ScriptPath/$newInput") or die;

  if ($icount % 500 == 0) {
    print("Making input card $ScriptPath/$newInput\n");
  }

  foreach my $line (@proto) {
    my $newline = $line;
    $newline =~ s/SED_TGBETA/$tgbeta/g;
    $newline =~ s/SED_LAMBDA/$lambda/g;
    $newline =~ s/SED_KAPPA/$kappa/g;
    $newline =~ s/SED_ALAMBDA/$alambda/g;
    $newline =~ s/SED_AKAPPA/$akappa/g;
    $newline =~ s/SED_MUEFF/$mueff/g;
    # $_ =~ s/SED_COMMENTS/$comments/g;
    $newline .= "\n";
    print INPUT $newline;
  }
  close(INPUT);

  # run NMSSM Tools with new input file
  system("./run $newInput");

  # remove input file to save space
  unlink "$ScriptPath/$newInput";

} # end loop on number of random points to scan


# make a note of what param range we ran over
open(NOTES, ">$ScriptPath/paramRange.txt") or die;
print NOTES $comments;
close(NOTES);

# printing scan statement
print("\n");
print("\n");
print("##########################################\n");
print("### N. iterations   =   $npoints          \n");
print("##########################################\n");

exit;
