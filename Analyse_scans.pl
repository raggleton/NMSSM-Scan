#!/usr/bin/perl
# use strict;
use warnings 'all';
use Archive::Tar;
use File::Basename;
use File::Path qw/make_path/;
# use Algorithm::Combinatorics qw(permutations);

########################################################
# This script analyses the output spectrum files.
#
# usage: perl Analyse_scans.pl <dir with spectrum files> <output dir for CSV files> <optional unique identifier for this set of output files>
########################################################


# ---- find PWD ---- #
my $ScriptPath = $ENV{PWD};
print "ScriptPath: ", $ScriptPath, "\n";

# dir to get spectrum files from
my $spectrDir = $ARGV[0];
print "Getting spectrum files from ${spectrDir}\n";

# get list of all spectr_* files in dir
my @spectrFiles = glob("$spectrDir/spectr_*");

# output dir
my $outDir = $ARGV[1];

# unique identifier for this output file
my $ID = "";
my $num_args = $#ARGV + 1;
if ($num_args == 3) {
  $ID = $ARGV[2];
}

# CSV file to write results to
# my $outFile = "$ScriptPath/$spectrDir/output.dat";
my $outFile = "$outDir/output$ID.dat";
my $outFileGood = "$outDir/output_good$ID.dat";
print "Writing results to $outFile and $outFileGood\n";
open(OUTPUT, ">$outFile") or die;
open(OUTPUTGOOD, ">$outFileGood") or die;

# list any results that you want to store here. will be used as column headers.
# then make sure you assign it further down.
my @columns = ("mtau", "mh1", "mh2", "mh3", "ma1", "ma2", "mhc", "mstop1", "mstop2",
              "tgbeta", "mueff", "lambda", "kappa", "alambda", "akappa",
              "h1u", "h1d", "h1b", "h1V", "h1G", "h1A",
              "h2u", "h2d", "h2b", "h2V", "h2G", "h2A",
              "Brh1gg", "Brh1tautau", "Brh1cc", "Brh1bb", "Brh1ww", "Brh1zz", "Brh1gammagamma", "Brh1zgamma", "Brh1a1a1", "Brh1a1z",
              "Brh2gg", "Brh2tautau", "Brh2bb", "Brh2ww", "Brh2zz", "Brh2gammagamma", "Brh2zgamma", "Brh2a1a1", "Brh2a1z", "Brh2h1h1",
              "Brh3gg", "Brh3tautau", "Brh3bb", "Brh3ww", "Brh3zz", "Brh3gammagamma", "Brh3zgamma", "Brh3h1h1", "Brh3h2h2", "Brh3h1h2", "Brh3a1a1", "Brh3a1z",
              "Bra1mumu", "Bra1tautau", "Bra1bb",
              "h1ggrc2", "h2ggrc2", "h1bbrc2", "h2bbrc2",
              # "S11", "S12", "S13", "S21", "S22", "S23", "S31", "S32", "S33",
              # "P11", "P12", "P13", "P21", "P22", "P23",
              "omega", "dmdiag1", "dmdiag2", "dmdiag3",
              "file", "constraints", "Del_a_mu");

# Make hash to hold results - need to do here and not in loop to ensure that
# column headers are in right order as order in @columns != order in %results
my %results = map { $_ => 0.0 } @columns;

# Print column headers to file
my $columnHeader = join(",", @columns);
$columnHeader .= "\n";
print $columnHeader;
print OUTPUT $columnHeader;
print OUTPUTGOOD $columnHeader;

my $igood = 0; # count number of points passing experimental constraints
my $iuseful = 0; # count number of points that also have acceptable ma1

my $counter = 0; my $last = 50000000; # can limit number of files run over

# Now loop over spectrum files, check if point satisfies experimental constraints
# and if so, pull BR/masses/etc from it
foreach $file (@spectrFiles) {
  # print $file, "\n";
  if ($counter > $last){
    last;
  }

  # Reset hash to null values
  %results = map { $_ => 0.0 } @columns;

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

  # remove standard first 2 lines & last line as useless
  shift(@concheck);
  shift(@concheck);
  pop(@concheck);

  my @fails = passExpCheck(@concheck);
  my $conStr = join("/", @fails);
  $results{"constraints"} = $conStr;

  # optional: can save only if passes all constraints
  # my $check = @concheck;
  # if ($check != 0) {
  #   next;
  # }


  # Get masses, parameters, etc
  open(DATASPECTR, $file) or die;
  while(<DATASPECTR>){
    # some regex goodness here to grab relevant lines
    # Note, the inline "comments" are NOT perl comments - part of matching string!
    # For future me:
    # "[E\d\.\-\+]+" matches a scientific number (so can be negative, have an exponent, decimal place)
    # " +" matches at least one space

    $results{"file"} = $file;

    # masses
    $results{"mtau"} = $1 if / +7 +([E\d\.\-\+]+) +\# MTAU/;
    $results{"mh1"} = $1 if / +25 +([E\d\.\-\+]+) +\# lightest neutral scalar/;
    $results{"mh2"} = $1 if / +35 +([E\d\.\-\+]+) +\# second neutral scalar/;
    $results{"mh3"} = $1 if / +45 +([E\d\.\-\+]+) +\# third neutral scalar/;
    $results{"ma1"} = $1 if / +36 +([E\d\.\-\+]+) +\# lightest pseudoscalar/;
    $results{"ma2"} = $1 if / +46 +([E\d\.\-\+]+) +\# second pseudoscalar/;
    $results{"mhc"} = $1 if / +37 +([E\d\.\-\+]+) +\# charged Higgs/;
    $results{"mstop1"} = $1 if /   1000006 +([E\d\.\-\+]+) +#  ~t_1/;
    $results{"mstop2"} = $1 if /   2000006 +([E\d\.\-\+]+) +#  ~t_2/;

    # parameters
    $results{"tgbeta"} = $1 if / +3 +([E\d\.\-\+]+) +\# TANBETA\(MZ\)/;
    $results{"mueff"} = $1 if / +65 +([E\d\.\-\+]+) +\# MUEFF/;
    $results{"lambda"} = $1 if / +61 +([E\d\.\-\+]+) +\# LAMBDA/;
    $results{"kappa"} = $1 if / +62 +([E\d\.\-\+]+) +\# KAPPA/;
    $results{"alambda"} = $1 if / +63 +([E\d\.\-\+]+) +\# ALAMBDA/;
    $results{"akappa"} = $1 if / +64 +([E\d\.\-\+]+) +\# AKAPPA/;

    # higgs reduced couplings
    $results{"h1u"} = $1 if / +1  1 +([E\d\.\-\+]+) +\# U\-type fermions/;
    $results{"h1d"} = $1 if / +1  2 +([E\d\.\-\+]+) +\# D\-type fermions/;
    $results{"h1b"} = $1 if / +1  3 +([E\d\.\-\+]+) +\# b\-quarks/;
    $results{"h1V"} = $1 if / +1  4 +([E\d\.\-\+]+) +\# W,Z bosons/;
    $results{"h1G"} = $1 if / +1  5 +([E\d\.\-\+]+) +\# Gluons/;
    $results{"h1A"} = $1 if / +1  6 +([E\d\.\-\+]+) +\# Photons/;

    $results{"h2u"} = $1 if / +2  1 +([E\d\.\-\+]+) +\# U\-type fermions/;
    $results{"h2d"} = $1 if / +2  2 +([E\d\.\-\+]+) +\# D\-type fermions/;
    $results{"h2b"} = $1 if / +2  3 +([E\d\.\-\+]+) +\# b\-quarks/;
    $results{"h2V"} = $1 if / +2  4 +([E\d\.\-\+]+) +\# W,Z bosons/;
    $results{"h2G"} = $1 if / +2  5 +([E\d\.\-\+]+) +\# Gluons/;
    $results{"h2A"} = $1 if / +2  6 +([E\d\.\-\+]+) +\# Photons/;

    # Higgs branching ratios
    # h1
    $results{"Brh1gg"} = $1 if / +([E\d\.\-\+]+) +2 +21 +21 +\# BR\(H_1 \-> gluon gluon\)/;
    $results{"Brh1tautau"} = $1 if / +([E\d\.\-\+]+) +2 +15 +\-15 +\# BR\(H_1 \-> tau tau\)/;
    $results{"Brh1cc"} = $1 if / +([E\d\.\-\+]+) +2 +4 +\-4 +\# BR\(H_1 \-> c cbar\)/;
    $results{"Brh1bb"} = $1 if / +([E\d\.\-\+]+) +2 +5 +\-5 +\# BR\(H_1 \-> b bbar\)/;
    $results{"Brh1ww"} = $1 if / +([E\d\.\-\+]+) +2 +24 +\-24 +\# BR\(H_1 \-> W\+ W\-\)/;
    $results{"Brh1zz"} = $1 if / +([E\d\.\-\+]+) +2 +23 +\-23 +\# BR\(H_1 \-> Z Z\)/;
    $results{"Brh1gammagamma"} = $1 if / +([E\d\.\-\+]+) +2 +22 +\-22 +\# BR\(H_1 \-> gamma gamma\)/;
    $results{"Brh1zgamma"} = $1 if / +([E\d\.\-\+]+) +2 +23 +22 +\# BR\(H_1 \-> Z gamma\)/;
    $results{"Brh1a1a1"} = $1 if / +([E\d\.\-\+]+) +2 +36 +36 +\# BR\(H_1 \-> A_1 A_1\)/;
    $results{"Brh1a1z"} = $1 if / +([E\d\.\-\+]+) +2 +23 +36 +\# BR\(H_1 \-> A_1 Z\)/;

    # h2
    $results{"Brh2gg"} = $1 if / +([E\d\.\-\+]+) +2 +21 +21 +\# BR\(H_2 \-> gluon gluon\)/;
    $results{"Brh2tautau"} = $1 if / +([E\d\.\-\+]+) +2 +15 +\-15 +\# BR\(H_2 \-> tau tau\)/;
    $results{"Brh2bb"} = $1 if / +([E\d\.\-\+]+) +2 +5 +\-5 +\# BR\(H_2 \-> b bbar\)/;
    $results{"Brh2ww"} = $1 if / +([E\d\.\-\+]+) +2 +24 +\-24 +\# BR\(H_2 \-> W\+ W\-\)/;
    $results{"Brh2zz"} = $1 if / +([E\d\.\-\+]+) +2 +23 +\-23 +\# BR\(H_2 \-> Z Z\)/;
    $results{"Brh2gammagamma"} = $1 if / +([E\d\.\-\+]+) +2 +22 +\-22 +\# BR\(H_2 \-> gamma gamma\)/;
    $results{"Brh2zgamma"} = $1 if / +([E\d\.\-\+]+) +2 +23 +22 +\# BR\(H_2 \-> Z gamma\)/;
    $results{"Brh2a1a1"} = $1 if / +([E\d\.\-\+]+) +2 +36 +36 +\# BR\(H_2 \-> A_1 A_1\)/;
    $results{"Brh2a1z"} = $1 if / +([E\d\.\-\+]+) +2 +23 +36 +\# BR\(H_2 \-> A_1 Z\)/;
    $results{"Brh2h1h1"} = $1 if / +([E\d\.\-\+]+) +2 +25 +25 +\# BR\(H_2 \-> H_1 H_1\)/;

    # h3
    $results{"Brh3gg"} = $1 if / +([E\d\.\-\+]+) +2 +21 +21 +\# BR\(H_3 \-> gluon gluon\)/;
    $results{"Brh3tautau"} = $1 if / +([E\d\.\-\+]+) +2 +15 +\-15 +\# BR\(H_3 \-> tau tau\)/;
    $results{"Brh3bb"} = $1 if / +([E\d\.\-\+]+) +2 +5 +\-5 +\# BR\(H_3 \-> b bbar\)/;
    $results{"Brh3ww"} = $1 if / +([E\d\.\-\+]+) +2 +24 +\-24 +\# BR\(H_3 \-> W\+ W\-\)/;
    $results{"Brh3zz"} = $1 if / +([E\d\.\-\+]+) +2 +23 +\-23 +\# BR\(H_3 \-> Z Z\)/;
    $results{"Brh3gammagamma"} = $1 if / +([E\d\.\-\+]+) +2 +22 +\-22 +\# BR\(H_3 \-> gamma gamma\)/;
    $results{"Brh3zgamma"} = $1 if / +([E\d\.\-\+]+) +2 +23 +22 +\# BR\(H_3 \-> Z gamma\)/;
    $results{"Brh3a1a1"} = $1 if / +([E\d\.\-\+]+) +2 +36 +36 +\# BR\(H_3 \-> A_1 A_1\)/;
    $results{"Brh3a1z"} = $1 if / +([E\d\.\-\+]+) +2 +23 +36 +\# BR\(H_3 \-> A_1 Z\)/;
    $results{"Brh3h1h1"} = $1 if / +([E\d\.\-\+]+) +2 +25 +25 +\# BR\(H_3 \-> H_1 H_1\)/;
    $results{"Brh3h2h2"} = $1 if / +([E\d\.\-\+]+) +2 +35 +35 +\# BR\(H_3 \-> H_2 H_2\)/;
    $results{"Brh3h1h2"} = $1 if / +([E\d\.\-\+]+) +2 +25 +35 +\# BR\(H_3 \-> H_1 H_2\)/;

    # a1
    $results{"Bra1mumu"} = $1 if / +([E\d\.\-\+]+) +2 +13 +\-13 +\# BR\(A_1 \-> muon muon\)/;
    $results{"Bra1tautau"} = $1 if / +([E\d\.\-\+]+) +2 +15 +\-15 +\# BR\(A_1 \-> tau tau\)/;
    $results{"Bra1bb"} = $1 if / +([E\d\.\-\+]+) +2 +5 +\-5 +\# BR\(A_1 \-> b bbar\)/;

    # Input Higgs Couplings Bosons
    $results{"h1ggrc2"} = $1 if / +([E\d\.\-\+]+) +3 +25 +21 +21 \# Higgs\(1\)-gluon-gluon reduced coupling\^2/;
    $results{"h2ggrc2"} = $1 if / +([E\d\.\-\+]+) +3 +35 +21 +21 \# Higgs\(2\)-gluon-gluon reduced coupling\^2/;
    $results{"h1bbrc2"} = $1 if / +([E\d\.\-\+]+) +[E\d\.\-\+]+ +3 +25 +5 +5 \# Higgs\(1\)-b-b red\. coupling\^2/;
    $results{"h2bbrc2"} = $1 if / +([E\d\.\-\+]+) +[E\d\.\-\+]+ +3 +35 +5 +5 \# Higgs\(2\)-b-b red\. coupling\^2/;

    # 3x3 Higgs mixing matrix
    # $results{"S11"} = $1 if /  1  1 +([E\d\.\-\+]+) +\# S_\(1,1\)/;
    # $results{"S12"} = $1 if /  1  2 +([E\d\.\-\+]+) +\# S_\(1,2\)/;
    # $results{"S13"} = $1 if /  1  3 +([E\d\.\-\+]+) +\# S_\(1,3\)/;
    # $results{"S21"} = $1 if /  2  1 +([E\d\.\-\+]+) +\# S_\(2,1\)/;
    # $results{"S22"} = $1 if /  2  2 +([E\d\.\-\+]+) +\# S_\(2,2\)/;
    # $results{"S23"} = $1 if /  2  3 +([E\d\.\-\+]+) +\# S_\(2,3\)/;
    # $results{"S31"} = $1 if /  3  1 +([E\d\.\-\+]+) +\# S_\(3,1\)/;
    # $results{"S32"} = $1 if /  3  2 +([E\d\.\-\+]+) +\# S_\(3,2\)/;
    # $results{"S33"} = $1 if /  3  3 +([E\d\.\-\+]+) +\# S_\(3,3\)/;

    # 2x3 Pseudoscalar higgs mixing matrix
    # $results{"P11"} = $1 if /  1  1 +([E\d\.\-\+]+) +\# P_\(1,1\)/;
    # $results{"P12"} = $1 if /  1  2 +([E\d\.\-\+]+) +\# P_\(1,2\)/;
    # $results{"P13"} = $1 if /  1  3 +([E\d\.\-\+]+) +\# P_\(1,3\)/;
    # $results{"P21"} = $1 if /  2  1 +([E\d\.\-\+]+) +\# P_\(2,1\)/;
    # $results{"P22"} = $1 if /  2  2 +([E\d\.\-\+]+) +\# P_\(2,2\)/;
    # $results{"P23"} = $1 if /  2  3 +([E\d\.\-\+]+) +\# P_\(2,3\)/;

    # DM relic density & 3 most common diagrams
    if (/    10 +([E\d\.\-\+]+) +\# Omega h\^2/){
      $results{"omega"} = $1;
      # skip2 comment lines in the spectrum file
      $dud = <DATASPECTR>;
      $dud = <DATASPECTR>;
      # the regex here trims whitespace from both ends of the line
      ($results{"dmdiag1"} = <DATASPECTR>) =~ s/^\s+|\s+$//g;
      ($results{"dmdiag2"} = <DATASPECTR>) =~ s/^\s+|\s+$//g;
      ($results{"dmdiag3"} = <DATASPECTR>) =~ s/^\s+|\s+$//g;
    }

    # g-2 contribution
    $results{"Del_a_mu"} = $1 if /     6 +([E\d\.\-\+]+) +\# Del_a_mu/;

  } #end while
  close(DATASPECTR);

  # Convert to number for testing
  $results{"ma1"} = $results{"ma1"}*1.0;
  $results{"Del_a_mu"} = $results{"Del_a_mu"}*1.0;

  # Write values to file if we're happy with them
  # Must do it like this - looping through @columns, otherwise order will muck up
  if($results{"ma1"} < 100 && $results{"ma1"} > 0){
    my $outStr = "";
    foreach my $col (@columns){
      $outStr .= "$results{$col},";
    }
    chop($outStr); # don't want that last , as it will screw up the ordering
    $outStr.= "\n";
    print OUTPUT $outStr;

    # Save to "good" file if passes all constraints, except for g-2,
    # where we are happy with a +ve delta a_mu, and omega, where we are happy if it's too small
    if ($results{"constraints"} eq "" || (checkExpPermutations($results{"constraints"}) && ($results{"Del_a_mu"} > 0) )){
      print OUTPUTGOOD $outStr;
      $igood++;
    }
    $iuseful++;
  }

  $counter++;
} # end loop on number of random points to scan
close(OUTPUT);
close(OUTPUTGOOD);

# printing stats
my $itotal = @spectrFiles;
my $fracGood = sprintf "%.4f", $igood / $itotal;
my $fracUseful = sprintf "%.4f", $iuseful / $itotal;
print("\n");
print("\n");
print("#########################################\n");
print("### N. input points         =   $itotal\n");
print("### N. with 0 < ma1 < 100   =   $iuseful\n");
print("### N. with 0 < ma1 < 100,\n");
print(" & passing exp. constraints = $igood\n");
print("### Fraction useful         =   $fracUseful\n");
print("### Fraction good           =   $fracGood\n");
print("#########################################\n");


sub checkExpPermutations {
  # Check if string matches one constraint, or several (in any permutation)
  # e.g. if we tested against "Chargino too light" and "Stau too light"
  # then we would return True if the input text was:
  # "Chargino too light"
  # or "Stau too light"
  # or "Chargino too light/Stau too light"
  # or "Stau too light/Chargino too light"
  # and False if e.g. "Chargino too light/Landau Pole below MGUT"

  my $conStr = $_[0];

  # constraints to test against
  my @testConstraints = (
    "Relic density too small (Planck)",
    "Muon magn. mom. more than 2 sigma away"
  );

  # eurgh would like to automate this but need Algorithms::Combinatorics, which
  # needs installing but as non-root...
  # must be in right order as in subroutine below, otherwise will go wrong
  my @permutations = (
    "Relic density too small (Planck)",
    "Muon magn. mom. more than 2 sigma away",
    "Relic density too small (Planck)/Muon magn. mom. more than 2 sigma away"
  );

  foreach $check(@permutations) {
    if ($conStr eq $check) {
      return 1;
    }
  }
  return 0;

}


sub passExpCheck {
  # Check parameter point passes various experimental limits.
  # If you don't want to test against a certain experimental constraint,
  # comment out that constraint in the array below.
  # Return list of experimental limits checks that it fails.

  # Plucked from nmhdecay.f, so need to add in new ones manually!
  # For any numerical parameters (e.g. Higgs mass) replace with "\\d+\\.?\\d*"
  # This will catch 5, 123.5, etc
  # Also note that the entries are regular expressions, so replace ( with \(, etc
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
    "Excluded by ee -> Z -> hA \\(Z width\\)",
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
    "Relic density too large \\(Planck\\)",
    "Relic density too small \\(Planck\\)",
    "Problem in micrOMEGAs",
    "Excluded by LUX",
    "b -> s gamma more than 2 sigma away",
    "Delta M_s more than 2 sigma away",
    "Delta M_d more than 2 sigma away",
    "B_s -> mu\\+ mu- more than 2 sigma away",
    "B\\+ -> tau nu_tau more than 2 sigma away",
    "Muon magn. mom. more than 2 sigma away",
    "Excluded by Upsilon\\(1S\\) -> A gamma \\(CLEO\\)",
    "\\(but A width> 10 MeV\\)",
    "Excluded etab\\(1S\\) mass difference \\(BABAR - theory\\)",
    "Excluded by BR\\(B -> X_s mu \\+mu-\\)",
    "Excluded by top -> b H\\+, H\\+ -> c s",
    "Excluded by top -> b H\\+, H\\+ -> tau nu_tau",
    "Excluded by top -> b H\\+, H\\+ -> W\\+ A1, A1 -> 2taus",
    "Excluded by t -> bH\\+ \\(LHC\\)",
    "No Higgs in the \\d+\\.?\\d*-\\d+\\.?\\d* GeV mass range",
    "chi2\\(H->gg\\) >",
    "chi2\\(H->bb\\) >",
    "chi2\\(H->ZZ\\) >",
    # "Excluded by sparticle searches at the LHC",
    # "Excluded by ggF/bb->H/A->tautau at the LHC",
    # "Excluded H_225->AA->4mu \\(CMS\\)",
    "Branching ratios of Higgs states < 1 GeV not reliable",
    "M_H1\\^2<1",
    "M_A1\\^2<1",
    "M_HC\\^2<1",
    "Negative sfermion mass squared",
    "Disallowed parameters: lambda, kappa, tan\\(beta\\) or mu=0",
    "Integration problem in RGES",
    "Integration problem in RGESOFT",
    "Convergence Problem"
  );

  my @list = @_;
  my @fails = ();

  # remove junk at start of line & check if in list - if so point failed!
  foreach $check(@list) {
    $check =~ s/^\s*\d\s*#\s//g;
    foreach $exp (@expConstraints) {
      if (grep(/$exp/, $check)) {
        $check =~ s/\n//g;
        $check =~ s/,/ /g; # as our output file is comma-separated
        push @fails, $check;
      }
    }
  }
  return @fails;
}
