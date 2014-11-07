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

$akappamax=+4000;
$akappamin=-4000;



# select number of random points to generate

$ninit=1;

$nfinal=1000000;

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
  
   $deltaakappa=3;
   $x0akappa=30*$lambda*$lambda-3;
   $akappa=rand($deltaakappa)+$x0akappa;
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
  
  $mtau=0;
  $mh1=0;
  $mh2=0;
  $mh3=0;
  $ma1=0;
  $ma2=0;
  $mhc=0;
  
  
  
  # saving informations for good points
  if($check==3){
    $errorlabel=0;
  }
  undef @error;
  if($check!=3){
    $errorlabel=1;
    open(DATASPECTR, "$ScriptPath/input/spectr.dat");
    while(<DATASPECTR>){
      if(/     2   4.1.2      \# Version number/) {
	  while (<DATASPECTR>) {
	  last if /\# Input parameters/;
	  push @error, $_;
	  }
      }             
    }#end while
    close(DATASPECTR);      
  }  
  $errordim=@error;
  
    open(DATASPECTR, "$ScriptPath/input/spectr.dat");
    while(<DATASPECTR>){
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

    
    $igood++;
    
#    system("cp $ScriptPath/input/spectr.dat $ScriptPath/output/spectr_${icount}");
#    system("cp $ScriptPath/input/decay.dat $ScriptPath/output/decay_${icount}");
    
#     if($ma1<1000){
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
      print OUTPUT "$errorlabel";
      print OUTPUT " ";
      for($ierror=0;$ierror<$errordim;$ierror++){
      
      $errorstring=@error[$ierror];
      $errorstring =~ s/\R//g;
        print OUTPUT $errorstring;
        print OUTPUT " ";
      }      
      print OUTPUT "\n";
#     }
    


  
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



