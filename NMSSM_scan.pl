#!/usr/bin/perl

# ---- find Script ---- #
$ScriptPath = $ENV{PWD};

# --- find NMSSM tools dir ---#
$ENV{PWD} =~ m@^(.*)(/[^/]+){1}$@; $NMSSMtoolsPath = $1;

# select max and min range for parameters


$tgbetamax=50;
$tgbetamin=1.5;

$mueffmax=300;
$mueffmin=100;
  
$lambdamax=1;
$lambdamin=0;
  
$kappamax=1;
$kappamin=0;

$alambdamax=+4000;
$alambdamin=-4000;

$akappamax=+10;
$akappamin=-30;



# select number of random points to generate

$ninit=SED_NINIT;

$nfinal=SED_NFINAL;

$npoints=$nfinal-$ninit+1;


# imposing derivate bounds on min or max parameters (edit corresponding part)

$userbounds=1;


######################################################
#####         SCRIPT STARTING                   ######
######################################################

# removing old outputs
system("rm $ScriptPath/output/*");

# computing range for random generator
$deltatgbeta=($tgbetamax-$tgbetamin);
$x0tgbeta=$tgbetamin;

$deltalambda=($lambdamax-$lambdamin);
$x0lambda=$lambdamin;

$deltakappa=($kappamax-$kappamin);
$x0kappa=$kappamin;

$deltaalambda=($alambdamax-$alambdamin);
$x0alambda=$alambdamin;

$deltaakappa=($akappamax-$akappamin);
$x0akappa=$akappamin;

$deltamueff=($mueffmax-$mueffmin);
$x0mueff=$mueffmin;


#counter for good points
$igood=0;

open(OUTPUT,">>$ScriptPath/output/output.dat");

for($icount=$ninit;$icount<=$nfinal;$icount++){

  # initializing BR to zero (e.g. if the decay is kinematically forbidden)
  $Brh1a1a1=0;
  $Brh2a1a1=0;
  $Bra1tautau=0;


  # generating random points within the range
  $tgbeta=rand($deltatgbeta)+$x0tgbeta;
  $lambda=rand($deltalambda)+$x0lambda;
  $kappa=rand($deltakappa)+$x0kappa;
  $alambda=rand($deltaalambda)+$x0alambda;
  $akappa=rand($deltaakappa)+$x0akappa;
  $mueff=rand($deltamueff)+$x0mueff;
  

  
  # in case of different and dependent range, write it here
  # my scan 2
  if($userbounds==1){
  
    $kappa=rand((200*$lambda)/$mueff);
  
#    $deltaakappa=3;
#    $x0akappa=30*$lambda*$lambda-3;
#    $akappa=rand($deltaakappa)+$x0akappa;
  }
  
  
  # writing the input file
  open(INPUT_PROTO, "$ScriptPath/Proto_files/inp_PROTO.dat");
  open(INPUT,	  ">$ScriptPath/input/inp.dat");
    while(<INPUT_PROTO>) {
      $_ =~ s/SED_TGBETA/$tgbeta/g;
      $_ =~ s/SED_LAMBDA/$lambda/g;
      $_ =~ s/SED_KAPPA/$kappa/g;
      $_ =~ s/SED_ALAMBDA/$alambda/g;
      $_ =~ s/SED_AKAPPA/$akappa/g;
      $_ =~ s/SED_MUEFF/$mueff/g;
      print(INPUT);
    }
  close(INPUT_PROTO);
  close(INPUT);

  # running NMSSM decay
  #WIP. Have to set the directory by hand. If I put $ScriptPath does not work
  system("cd $NMSSMtoolsPath && ./run Daniele_scan/input/inp.dat");

  
  # checking warning on exp. constraints and higgs mass
  undef @concheck;
  open(CONSTRAINT_CHECK, "$ScriptPath/input/spectr.dat");
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
  
    open(DATASPECTR, "$ScriptPath/input/spectr.dat");
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
      
    }#end while
    close(DATASPECTR);
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
    

    
    open(DATADECAY, "$ScriptPath/input/decay.dat");
    while(<DATADECAY>){
        $Brh1a1a1=$1 if /     (.*)    2          36        36   # BR\(H_1 -> A_1 A_1\)/;
        $Brh2a1a1=$1 if /     (.*)    2          36        36   # BR\(H_2 -> A_1 A_1\)/;        
        $Bra1tautau=$1 if /     (.*)    2          15       -15   # BR\(A_1 -> tau tau\)/;
    }
    close(DATADECAY);
    
    $Brh1a1a1=$Brh1a1a1*1.0;
    $Brh2a1a1=$Brh2a1a1*1.0;
    $Bra1tautau=$Bra1tautau*1.0;
    
    $igood++;
    
#    system("cp $ScriptPath/input/spectr.dat $ScriptPath/output/spectr_${icount}");
#    system("cp $ScriptPath/input/decay.dat $ScriptPath/output/decay_${icount}");
    
    if($ma1<10){
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
    
  }# end good points


  
} # end loop on number of random points to scan

close(OUTPUT);

system("rm $ScriptPath/input/*");

# printing scan statement
print("\n");
print("\n");
print("##########################################\n");
print("### N. iterations   =   $npoints          \n");
print("### N. points found =   $igood            \n");
print("##########################################\n");

exit;



