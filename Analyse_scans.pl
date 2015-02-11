#!/usr/bin/perl
# use strict;
use warnings 'all';
use Archive::Tar;
use File::Basename;
use File::Path qw/make_path/;


########################################################
# This script analyses the output spectrum files.
#
# usage: perl Analyse_scans.pl <dir with spectrum files>
########################################################


# ---- find PWD ---- #
my $ScriptPath = $ENV{PWD};
print "ScriptPath: ", $ScriptPath, "\n";

# dir to get spectrum files from
my $spectrDir = $ARGV[0];
print "Getting spectrum files from ${spectrDir}\n";

# get list of all spectr_* files in dir
my @spectrFiles = glob("$spectrDir/spectr_*");

# file to write results to
my $outFile = "$ScriptPath/$spectrDir/output.dat";
print "Writing results to $outFile\n";
open(OUTPUT, ">$outFile") or die;
print OUTPUT "mh1 mh2 mh3 ma1 ma2 mhc Brh1a1a1 Brh2a1a1 tgbeta mueff lambda alambda akappa h1u h1d h1V h1A h2u h2d h2V h2G h2A";

# count number of good points
my $igood;

# Now loop over sctrum files, check if point satisfies experimental constraints
# and if so, pull BR/masses/etc from it
foreach $file (@spectrFiles) {

  # checking warning on exp. constraints and higgs mass
  undef @concheck;
  open(CONSTRAINT_CHECK, $file) or die;
  while(<CONSTRAINT_CHECK>){
    if(/BLOCK SPINFO/) {
      while (<CONSTRAINT_CHECK>) {
        last if /BLOCK MODSEL/;
        push @concheck, $_;
      }
    }
  }
  $check=@concheck;

  # saving informations for good points
  if($check==3){

    # Get masses, parameters, etc
    open(DATASPECTR, $file) or die;
    while(<DATASPECTR>){

      $mtau=$1 if /     7     (.\S+..)   \# MTAU/;
      $mh1=$1 if /        25     (.\S+..)   \# lightest neutral scalar/;
      $mh2=$1 if /        35     (.\S+..)   \# second neutral scalar/;
      $mh3=$1 if /        45     (.\S+..)   \# third neutral scalar/;
      $ma1=$1 if /        36     (.\S+..)   \# lightest pseudoscalar/;
      $ma2=$1 if /        46     (.\S+..)   \# second pseudoscalar/;
      $mhc=$1 if /        37     (.\S+..)   \# charged Higgs/;
      # parameters
      $tgbeta=$1 if /     3     (.\S+..)   \# TANBETA\(MZ\)/;
      $mueff=$1 if /    65     (.\S+..)   \# MUEFF/;
      $lambda=$1 if /    61     (.\S+..)   \# LAMBDA/;
      $kappa=$1 if /    62     (.\S+..)   \# KAPPA/;
      $alambda=$1 if /    63    *(.\S+..)   \# ALAMBDA/;
      $akappa=$1 if /    64   *(.\S+..)   \# AKAPPA/;

      #higgs reduced couplings
      $h1u=$1 if /  1  1     *(.\S+..)   \# U-type fermions/;
      $h1d=$1 if /  1  2     *(.\S+..)   \# D-type fermions/;
      $h1V=$1 if /  1  3     *(.\S+..)   \# W,Z bosons/;
      $h1G=$1 if /  1  4     *(.\S+..)   \# Gluons/;
      $h1A=$1 if /  1  5     *(.\S+..)   \# Photons/;

      $h2u=$1 if /  2  1     *(.\S+..)   \# U-type fermions/;
      $h2d=$1 if /  2  2     *(.\S+..)   \# D-type fermions/;
      $h2V=$1 if /  2  3     *(.\S+..)   \# W,Z bosons/;
      $h2G=$1 if /  2  4     *(.\S+..)   \# Gluons/;
      $h2A=$1 if /  2  5     *(.\S+..)   \# Photons/;

      # Higgs branching ratios
      $Brh1a1a1=$1 if /     (.*)    2          36        36   # BR\(H_1 -> A_1 A_1\)/;
      $Brh2a1a1=$1 if /     (.*)    2          36        36   # BR\(H_2 -> A_1 A_1\)/;
      $Bra1tautau=$1 if /     (.*)    2          15       -15   # BR\(A_1 -> tau tau\)/;

    } #end while
    close(DATASPECTR);

    # Convert to ???
    $mtau=$mtau*1.0;
    $mh1=$mh1*1.0;
    $mh2=$mh2*1.0;
    $mh3=$mh3*1.0;
    $ma1=$ma1*1.0;
    $ma2=$ma2*1.0;
    $mhc=$mhc*1.0;

    $tgbeta=$tgbeta*1.0;
    $mueff=$mueff*1.0;
    $lambda=$lambda*1.0;
    $kappa=$kappa*1.0;
    $alambda=$alambda*1.0;
    $akappa=$akappa*1.0;

    $h1u=$h1u*1.0;
    $h1d=$h1d*1.0;
    $h1V=$h1V*1.0;
    $h1G=$h1G*1.0;
    $h1A=$h1A*1.0;

    $h2u=$h2u*1.0;
    $h2d=$h2d*1.0;
    $h2V=$h2V*1.0;
    $h2G=$h2G*1.0;
    $h2A=$h2A*1.0;

    $Brh1a1a1=$Brh1a1a1*1.0;
    $Brh2a1a1=$Brh2a1a1*1.0;
    $Bra1tautau=$Bra1tautau*1.0;

    $igood++;

#    system("cp $ScriptPath/input/spectr.dat $ScriptPath/output/spectr_${icount}");
#    system("cp $ScriptPath/input/decay.dat $ScriptPath/output/decay_${icount}");
    if($ma1<100){
      print OUTPUT $mh1;
      print OUTPUT " ";
      print OUTPUT $mh2;
      print OUTPUT " ";
      print OUTPUT $mh3;
      print OUTPUT " ";
      print OUTPUT $ma1;
      print OUTPUT " ";
      print OUTPUT $ma2;
      print OUTPUT " ";
      print OUTPUT $mhc;
      print OUTPUT " ";
      print OUTPUT $Brh1a1a1;
      print OUTPUT " ";
      print OUTPUT $Brh2a1a1;
      print OUTPUT " ";
      print OUTPUT $Bra1tautau;
      print OUTPUT " ";
      print OUTPUT "$tgbeta";
      print OUTPUT " ";
      print OUTPUT "$mueff";
      print OUTPUT " ";
      print OUTPUT "$lambda";
      print OUTPUT " ";
      print OUTPUT "$kappa";
      print OUTPUT " ";
      print OUTPUT "$alambda";
      print OUTPUT " ";
      print OUTPUT "$akappa";
      print OUTPUT " ";
      print OUTPUT "$h1u";
      print OUTPUT " ";
      print OUTPUT "$h1d";
      print OUTPUT " ";
      print OUTPUT "$h1V";
      print OUTPUT " ";
      print OUTPUT "$h1G";
      print OUTPUT " ";
      print OUTPUT "$h1A";
      print OUTPUT " ";
      print OUTPUT "$h2u";
      print OUTPUT " ";
      print OUTPUT "$h2d";
      print OUTPUT " ";
      print OUTPUT "$h2V";
      print OUTPUT " ";
      print OUTPUT "$h2G";
      print OUTPUT " ";
      print OUTPUT "$h2A";
      print OUTPUT "\n";
    }

  } # end good points

} # end loop on number of random points to scan
close(OUTPUT);
# copy output file to main output folder
$spectrDir =~ s/\.*\///;
system("cp $ScriptPath/$spectrDir/output.dat $ScriptPath/output/output_$spectrDir.dat");

# printing stats
my $itotal = @spectrFiles;
my $fracGood = sprintf "%.4f", $igood / $itotal;
print("\n");
print("\n");
print("#########################################\n");
print("### N. input points  =   $itotal          \n");
print("### N. good points   =   $igood          \n");
print("### Fraction good    =   $fracGood       \n");
print("#########################################\n");

