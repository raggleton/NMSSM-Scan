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

# print OUTPUT "mh1 mh2 mh3 ma1 ma2 mhc Brh1a1a1 Brh2a1a1 Bra1tautau tgbeta mueff lambda kappa alambda akappa h1u h1d h1V h1G h1A h2u h2d h2V h2G h2A\n";

# store results in hash to auto do column titles
my @header = ("mh1", 0.0, "mh2", 0.0, "mh3", 0.0, "ma1", 0.0, "ma2", 0.0,
              "mhc", 0.0, "Brh1a1a1", 0.0, "Brh2a1a1", 0.0, "Bra1tautau", 0.0,
              "tgbeta", 0.0, "mueff", 0.0, "lambda", 0.0, "kappa", 0.0,
              "alambda", 0.0, "akappa", 0.0, "h1u", 0.0, "h1d", 0.0,
              "h1V", 0.0, "h1G", 0.0, "h1A", 0.0, "h2u", 0.0, "h2d", 0.0,
              "h2V", 0.0, "h2G", 0.0, "h2A", 0.0);
my %results = @header;
my $columnHeader = join(" ", keys %results);
$columnHeader .= "\n";
print $columnHeader;
print OUTPUT $columnHeader;

# count number of points passing constraints
my $igood;
# count number of points with acceptable ma1
my $iuseful;

# Now loop over sctrum files, check if point satisfies experimental constraints
# and if so, pull BR/masses/etc from it
foreach $file (@spectrFiles) {

  # checking warning on exp. constraints and higgs mass
  # keep any failures and store
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
  # remove standard first 2 lines (boring)
  unshift(@concheck);
  unshift(@concheck);
  $check=@concheck;

  # saving informations for good points
  if(passExpCheck(@concheck)){
    # reset values
    # important otherwise get repeated points
    my $mtau = 0.0;
    my $mh1 = 0.0;
    my $mh2 = 0.0;
    my $mh3 = 0.0;
    my $ma1 = 0.0;
    my $ma2 = 0.0;
    my $mhc = 0.0;
    my $tgbeta = 0.0;
    my $mueff = 0.0;
    my $lambda = 0.0;
    my $kappa = 0.0;
    my $alambda = 0.0;
    my $akappa = 0.0;
    my $h1u = 0.0;
    my $h1d = 0.0;
    my $h1V = 0.0;
    my $h1G = 0.0;
    my $h1A = 0.0;
    my $h2u = 0.0;
    my $h2d = 0.0;
    my $h2V = 0.0;
    my $h2G = 0.0;
    my $h2A = 0.0;
    my $Brh1a1a1 = 0.0;
    my $Brh2a1a1 = 0.0;
    my $Bra1tautau = 0.0;

    # Get masses, parameters, etc
    # Note, the inline "comments" are NOT perl comments - part of matching string!
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
      $Bra1bb=$1 if /     (.*)    2          5       -5   # BR\(A_1 -> b bbar\)/;

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
    if($ma1 < 100 && $ma1 > 0){
      $results{"mh1"} = $mh1;
      $results{"mh2"} = $mh2;
      $results{"mh3"} = $mh3;
      $results{"ma1"} = $ma1;
      $results{"ma2"} = $ma2;
      $results{"mhc"} = $mhc;
      $results{"Brh1a1a1"} = $Brh1a1a1;
      $results{"Brh2a1a1"} = $Brh2a1a1;
      $results{"Bra1tautau"} = $Bra1tautau;
      $results{"tgbeta"} = $tgbeta;
      $results{"mueff"} = $mueff;
      $results{"lambda"} = $lambda;
      $results{"kappa"} = $kappa;
      $results{"kappa"} = $kappa;
      $results{"alambda"} = $alambda;
      $results{"akappa"} = $akappa;
      $results{"h1u"} = $h1u;
      $results{"h1d"} = $h1d;
      $results{"h1V"} = $h1V;
      $results{"h1G"} = $h1G;
      $results{"h1A"} = $h1A;
      $results{"h2u"} = $h2u;
      $results{"h2d"} = $h2d;
      $results{"h2V"} = $h2V;
      $results{"h2G"} = $h2G;
      $results{"h2A"} = $h2A;

      my @nums = values % results;
      my $numStr = join(" ", @nums);
      $numStr .= "\n";
      print OUTPUT $numStr;
      $iuseful++;

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
my $fracUseful = sprintf "%.4f", $iuseful / $itotal;
print("\n");
print("\n");
print("#########################################\n");
print("### N. input points  =   $itotal          \n");
print("### N. good points   =   $igood          \n");
print("### N. useful points =   $iuseful        \n");
print("### Fraction good    =   $fracGood       \n");
print("### Fraction useful  =   $fracUseful       \n");
print("#########################################\n");


sub passExpCheck {
  # Check parameter point passes various experimental limits.
  # If you don't want to test against a certain experimental constraint,
  # comment out that constraint in the array below.
  # Plucked from nmhdecay.f, so need to add in new ones manually!
  # For any numerical parameters (e.g. Higgs mass) replace with "\\d+\\.?\\d*"
  # This will catch 5, 123.5, etc
  my @expConstraints = (
    "Chargino too light",
    "Neutralinos too light",
    "Charged Higgs too light",
    "Excluded by ee -> hZ, ind. of h decay",
    "Excluded by ee -> hZ, h -> bb",
    "Excluded by ee -> hZ, h -> tautau",
    "Excluded by ee -> hZ, h -> invisible",
    "Excluded by ee -> hZ, h -> 2jets",
    "Excluded by ee -> hZ, h -> 2photons",
    "Excluded by ee -> hZ, h -> AA -> 4bs",
    "Excluded by ee -> hZ, h -> AA -> 4taus",
    "Excluded by ee -> hZ, h -> AA -> 2bs 2taus",
    "Excluded by ee -> hZ, h -> AA,A -> light pair",
    "Excluded by ee -> Z -> hA (Z width)",
    "Excluded by ee -> hA -> 4bs",
    "Excluded by ee -> hA -> 4taus",
    "Excluded by ee -> hA -> 2bs 2taus",
    "Excluded by ee -> hA -> AAA -> 6bs",
    "Excluded by ee -> hA -> AAA -> 6taus",
    "Excluded by stop -> b l sneutrino",
    "Excluded by stop -> neutralino c",
    "Excluded by sbottom -> neutralino b",
    "Squark/gluino too light",
    "Selectron/smuon too light",
    "Stau too light",
    "Lightest neutralino is not the LSP",
    "Mass of the lightest neutralino < 511 keV",
    "Landau Pole below MGUT",
    "Unphysical global minimum",
    "Higgs soft masses >> Msusy",
    "Relic density too large (Planck)",
    "Relic density too small (Planck)",
    "Problem in micrOMEGAs",
    "Excluded by LUX",
    "b -> s gamma more than 2 sigma away",
    "Delta M_s more than 2 sigma away",
    "Delta M_d more than 2 sigma away",
    "B_s -> mu+ mu- more than 2 sigma away",
    "B+ -> tau nu_tau more than 2 sigma away",
    "Muon magn. mom. more than 2 sigma away",
    "Excluded by Upsilon(1S) -> A gamma (CLEO)",
    "(but A width> 10 MeV)",
    "Excluded etab(1S) mass difference (BABAR - theory)",
    "Excluded by BR(B -> X_s mu +mu-)",
    "Excluded by top -> b H+, H+ -> c s",
    "Excluded by top -> b H+, H+ -> tau nu_tau",
    "Excluded by top -> b H+, H+ -> W+ A1, A1 -> 2taus",
    "Excluded by t -> bH+ (LHC)",
    "No Higgs in the \\d+\\.?\\d*-\\d+\\.?\\d* GeV mass range",
    "chi2(H->gg) > \\d+\\.?\\d*",
    "chi2(H->bb) > \\d+\\.?\\d*",
    "chi2(H->ZZ) > \\d+\\.?\\d*",
    # "Excluded by sparticle searches at the LHC",
    # "Excluded by ggF/bb->H/A->tautau at the LHC",
    # "Excluded H_125->AA->4mu (CMS)",
    "Branching ratios of Higgs states < 1 GeV not reliable",
    "M_H1\\^2<1",
    "M_A1\\^2<1",
    "M_HC\\^2<1",
    "Negative sfermion mass squared",
    "Disallowed parameters: lambda, kappa, tan(beta) or mu=0",
    "Integration problem in RGES",
    "Integration problem in RGESOFT",
    "Convergence Problem"
  );

  my @list = @_;

  # remove junk at start of line & check if in list - if so point failed!
  foreach $check(@list) {
    $check =~ s/^\s*\d\s*#\s//g;
    foreach $exp (@expConstraints) {
      if (grep(/$exp/, $check)) {
        return 0;
      }
    }
  }
  return 1;

}
