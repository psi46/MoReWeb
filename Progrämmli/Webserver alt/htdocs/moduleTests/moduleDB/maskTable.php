<?php


function templ($tmp)
 {
 $file_t = file($tmp);
 $count_t = count($file_t);
 $tests = 0;
 for ($te=0; $te<$count_t; $te++) { echo $file_t[$te];}
 };

if ( isset($HTTP_GET_VARS['Serie']) ) {

  $serie = $HTTP_GET_VARS['Serie'];
}
else {

  $serie = "all";
}

$modSel = 0;
if ( isset($HTTP_GET_VARS['modul']) ) {

  $modSel = 1;
  $myMod= $HTTP_GET_VARS['modul'];
}

templ("prodHeader.html");

$dir    = './';
$files = array();
$dh  = opendir($dir);
while (false !== ($filename = readdir($dh))) {
   $files[] = $filename;
}
closedir($dh);
rsort($files);
$m = count($files);
$monthN = array("01","02","03","04","05","06","07","08","09","10","11","12");
$monthS = array("Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec");

$list = 1;

 for($num=0; $num<$m; $num++) {

  $take = 0;
  if ( $modSel ) { 

    if ( $files[$num]{0}==$myMod{0} && $files[$num]{1}==$myMod{1}  && $files[$num]{2}==$myMod{2} && 
	 $files[$num]{3}==$myMod{3} && $files[$num]{4}==$myMod{4} ) { $take = 1; }
  }
  else if ( !strcmp($serie, "all") ) { 
 
    if ( $files[$num]{0}=="M" && ( $files[$num]{3}>="3" || $files[$num]{2}>="1") ) { $take = 1; }
  }
  else if ( $serie == 0 ) { 
 
    if ( $files[$num]{0}=="M" && ( $files[$num]{3}>="3" && $files[$num]{2}=="0") ) { $take = 1; }
  }
  else {
 
    if ($files[$num]{0}=="M" && 
	$files[$num]{1}==substr($serie, 0, 1) && 
	$files[$num]{2}==substr($serie, 1, 2) )  { $take = 1; }
  }

  if ( !$modSel && !strcmp($serie, "all") && $num>1000 ) { exit; }

  if ( $take ) {

    $subs = array();
    $sh  = opendir($files[$num]);
    while (false !== ($subname = readdir($sh))) {
      $subs[] = $subname;
    }
    closedir($sh);

    rsort($subs);
    $s = count($subs);

    for($mum=0; $mum<$s; $mum++) {

      if($subs[$mum]{0}=="T" && $subs[$mum]{5} == "" ) {

	$moduleTemp = '';
	$module = '';
        $pi=0; $ma=0; $bu=0; $tr=0; $ad=0;
	$rocs=0; $root=0;
	$date=''; $datr=''; $daca='';
	$c=''; $t=''; $n='';
	$temp=0; $sollTemp=0;$cycl=''; $cy='';
	$i=0; $ivVar=0; $ivDP=0; $slope=0;
	$tbm1=1; $tbm2=1;
	$iv150 = ''; $iv150_2 = '';
	$grade = '';
	$overallGrade = '';
	$finalGrade = '';
	$com=' ';
	$mis=' ';
	$tempWarning=' ';
	$noiB=0; $noiC=0; $trmB=0; $trmC=0;
	$gainB=0; $gainC=0; $pedB=0; $pedC=0;

        $path = $files[$num]."/".$subs[$mum];
        #echo "$path\n";
        $ft = date("d.m.y",fileatime($path."/summaryTest.txt"));
        $handle = fopen($path."/summaryTest.txt", "r");
        $li = 0;
        while ($userinfo = fscanf($handle, "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n"))  {

          $li = $li +1;

	  // if($li==1)  { ------------------------------------------------------------------
          if( !strcmp($userinfo[0],"Directory") )  {
	
	    $moduleTemp = 'M'.$userinfo[1]{1}.$userinfo[1]{2}.$userinfo[1]{3}.$userinfo[1]{4};
	    $moduleNr   = $userinfo[1]{2}.$userinfo[1]{3}.$userinfo[1]{4};
	    
	    $day   = $userinfo[1]{10}.$userinfo[1]{11};
	    $month = $userinfo[1]{8}.$userinfo[1]{9};
	    
	    for ( $i=0; $i<12;$i++ ) {
	      if (!strcmp($month, $monthN[$i]) ) {
		
		$date = $monthS[$i].' '.$day;
	      }
	    }
	  }
	  
	  // if($li==2)  { ------------------------------------------------------------------
          if( !strcmp($userinfo[0],"ModuleNr") ) {
	    
            $testNr  = $userinfo[3]; 
	    $testDir = $userinfo[2].'/'. $userinfo[3];
            $link    = $userinfo[2].$userinfo[3];
          }
	  
          if($li==3)  { //------------------------------------------------------------------
	    // if( !strcmp($userinfo[0],"Defects") ) {
	    
            $pi=$userinfo[1];
            $ma=$userinfo[2];
            $bu=$userinfo[3];
            $tr=$userinfo[4];
            $ad=$userinfo[5];
          }
	  
	  if ( $ma > 0 ) { $list = 1; } else { $list = 0; }
	  // if($li==4) {  ------------------------------------------------------------------
          if( !strcmp($userinfo[0],"ROCS") ) {
	    
	    $rocs = $userinfo[5];
	    $defB = $userinfo[6];
	    $defC = $userinfo[7];

	    if ( $defC > 0 ) { 
	      $rocs   = $rocs.'<FONT COLOR=#cc0000> ('.$defC.'C)</FONT>'; 
	    }
	    
	  }
	  
	  // if($li==6)  {  ------------------------------------------------------------------
          if( !strcmp($userinfo[0],"Tested") && $moduleNr < 50 ) {

            $date=$userinfo[4].' '.$userinfo[5];
	  }
	  
	  // if($li==7)  {  ------------------------------------------------------------------
          if( !strcmp($userinfo[0],"Trimming") ) {

           $t=$userinfo[1];
	  }
	  
	  // if($li==8)  {  ------------------------------------------------------------------
          if( !strcmp($userinfo[0],"phCalibration") ) {

           $c=$userinfo[1];
	  }

	  // if($li==9){  ------------------------------------------------------------------
          if( !strcmp($userinfo[0],"Temp") ) {

	    if ( $userinfo[2] != -100 ) {
	      $temp=sprintf("%01.2f+-%01.2f", $userinfo[1],$userinfo[2]);
	      $sollTemp=$userinfo[4];
	    }
	    else {
	      $temp=$userinfo[4];
	      $sollTemp=$userinfo[4];
	    }
	    if ( abs($temp - $sollTemp) > 1 ) {
	      $temp = '<FONT COLOR=#cc0000><B>'.$temp.'</B></FONT>';
	      $tempWarning='<FONT COLOR=#cc0000><B>T not '.$sollTemp.'!</B></FONT>';
	    }
	  }

	  // if($li==10){  ------------------------------------------------------------------
          if( !strcmp($userinfo[0],"Thermal") ) {

	    if (!strcmp($userinfo[2],"yes"))  {
	      $cy= $userinfo[2];
	      if( $userinfo[4] != -100 ) {
		$cycl=sprintf("(%01.1f+-%01.1f)", $userinfo[3], $userinfo[4]);
	      }
	    }
	    else {
	      $cy = $userinfo[2];
	    }
	  }

	  // if($li==17)  {  ------------------------------------------------------------------
          if( !strcmp($userinfo[0],"TBM1") ) {
	    
            $tbm1=$userinfo[1];
            if ( $tbm1 != 0 )   {
	      
	      $com=' '.$com.' TBM1: <a
href="http://kamor.ethz.ch/moduleTests/moduleDB/tbmDefects.html"> Err '.$tbm1.'</a>.';
	    }
	  }
	  
	  // if($li==18)  {  ------------------------------------------------------------------
          if( !strcmp($userinfo[0],"TBM2") ) {
	    
            $tbm2=$userinfo[1];
            if ( $tbm2 != 0 )   {
	      
	      $com=' '.$com.' TBM2: <a
href="http://kamor.ethz.ch/moduleTests/moduleDB/tbmDefects.html"> Err '.$tbm2.'</a>.';
	      
	    }
	  }

	  // if($li==19)  {  ------------------------------------------------------------------
          if( !strcmp($userinfo[0],"I") ) {

	    $i=$userinfo[2];
	    
	    if($i==0 || $i=='') { $iv150=''; }
	    else {
	      
	      $iv150=sprintf("%01.2f muA",$i);
	      
	      if ( $sollTemp < 0 ) { 
		
		$i10   = sprintf("%01.2f muA", $i/12.10188635);
		$iv150_2 = '('.$i10.')';
		
		if ( $i > 15 ) { 
		  $iv150   = '<FONT COLOR=#cc0000>'.$iv150.'</FONT>'; 
		  $iv150_2 = '<FONT COLOR=#cc0000>'.$iv150_2.'</FONT>';
		}

		else if ( $i > 3 ) {
		  $iv150   = '<FONT COLOR=#ff3300>'.$iv150.'</FONT>'; 
		  $iv150_2 = '<FONT COLOR=#ff3300>'.$iv150_2.'</FONT>'; 
		}
	      }
	      
	      if ( $sollTemp > 0 ) { 
		
		$iv150_2 = '';

		if ( $i > 10 ) { 
		  $iv150   = '<FONT COLOR=#cc0000>'.$iv150.'</FONT>';  
		}

		else if ( $i > 2 ) { 
		  $iv150   = '<FONT COLOR=#ff3300>'.$iv150.'</FONT>';
		}
	      }
	    }
	  }

	  // if($li==20){  ------------------------------------------------------------------
          if( !strcmp($userinfo[0],"I150/I100") ) {
	    
	    $ivVar=$userinfo[1];
	    if ( $ivVar > 0 ) { 
	      $slope=sprintf("%01.2f",$ivVar);
	    }
	    else {
	      $slope = '';
	    }

	    if ( $ivVar > 2 ) { 
	      $slope='<FONT COLOR=#ff3300> '.$slope.' </FONT>'; }
	  }

	  // if($li==21){  ------------------------------------------------------------------
          if( !strcmp($userinfo[0],"iv") ) {

	    $ivDP=$userinfo[2];
	    if ( $ivDP < 10 &&  $ivDP != 0 ) {$com=$com.' incompl. iv-data: '.$iDP.' meas.';}
	  }

	  // if($li==22){  ------------------------------------------------------------------
          if( !strcmp($userinfo[0],"Grade") ) {

	    $grade=$userinfo[1];
	  }

	  // if($li==28){  ------------------------------------------------------------------
          if( !strcmp($userinfo[0],"Noise") ) {

	    $noiB=$userinfo[1];
	    $noiC=$userinfo[2];

	    if ( $noiB == 0 && $noiC == 0 ) {

		$n = 'ok';
	    }
	    else if ( $noiB > 0 && $noiC == 0 ) {
	      $n = $noiB.'B';
	    }
	    else if ( $noiB > 0 && $noiC > 0) {
	      $n = $noiB.'B/<FONT COLOR=#cc0000>'.$noiC.'C</FONT>';
	    }
	    else if ( $noiC > 0 && $noiB == 0 ) {
	      $n = '<FONT COLOR=#cc0000>'.$noiC.'C</FONT>';
	    }
	  }

	  // if($li==29){  ------------------------------------------------------------------
          if( !strcmp($userinfo[0],"VcalThrWidth") ) {

	    $trmB=$userinfo[1];
	    $trmC=$userinfo[2];

	    if ( $trmB == 0 && $trmC == 0 ) {
	      if ( strcmp($t, "no") ) {
		$t = 'ok';
	      }
	    }
	    else if ( $trmB > 0 && $trmC == 0 ) {
	      $t = $trmB.'B';
	    }
	    else if ( $trmB > 0 && $trmC > 0 ) {
	      $t = $trmB.'B/<FONT COLOR=#cc0000>'.$trmC.'C</FONT>';
	    }
	    else if ( $trmC > 0 && $trmB == 0 ) {
	      $t = '<FONT COLOR=#cc0000>'.$trmC.'C</FONT>';
	    }
	  }

	  // if($li==30){  ------------------------------------------------------------------
          if( !strcmp($userinfo[0],"RelGainWidth") ) {

	    $gainB=$userinfo[1];
	    $gainC=$userinfo[2];
	    
	    if (  $gainB == 0 && $gainC == 0 ) {
	      
	      if ( !strcmp($c, "yes") ) {
		$c = '';
	      }
	    }
	    else if ( $gainB > 0 && $gainC == 0 ) {
	      $c = $gainB.'B Gain';
	    }
	    else if ( $gainB > 0 && $gainC > 0 ) {
	      $c = $gainB.'B/<FONT COLOR=#cc0000>'.$gainC.'C</FONT> Gain';
	    }
	    else if ( $gainC > 0 && $gainB == 0 ) {
	      $c = '<FONT COLOR=#cc0000>'.$gainC.'C</FONT> Gain';
	    }
	  }

	  // if($li==31){  ------------------------------------------------------------------
          if( !strcmp($userinfo[0],"PedSpread") ) {

	    $pedB=$userinfo[1];
	    $pedC=$userinfo[2];

	    if (  $gainB == 0 && $gainC == 0 &&
		  $pedB  == 0 && $pedC  == 0 ) {
	      
	      if ( strcmp($c, "no") ) {
		$c = 'ok';
	      }
	    }
	    else if ( $pedB > 0 && $pedC == 0 ) {
	      $c = $c.'  '.$pedB.'B Ped';
	    }
	    else if ( $pedB > 0 && $pedC > 0 ) {
	      $c = $c.'  '.$pedB.'B/<FONT COLOR=#cc0000>'.$pedC.'C</FONT>  Ped';
	    }
	    else if ( $pedC > 0 && $pedB == 0 ) {
	      $c = $c.'  <FONT COLOR=#cc0000>'.$pedC.'C</FONT> Ped';
	    }
	  }

	  // if($li==34){  ------------------------------------------------------------------
          if( !strcmp($userinfo[0],"RATIO") ) {

	    if ( $userinfo[1] > 5 ) { 
	      $com=$com.'current conversion factor > 5.'; 
	    }
	  }

	  // if($li==35){  ------------------------------------------------------------------
          if( !strcmp($userinfo[0],"OVERALL") ) {

	    if (!strcmp($userinfo[2], "A") ) { $overallGrade =  '<FONT COLOR=#009c66> '.$userinfo[2].' </FONT>'; }
	    if (!strcmp($userinfo[2], "B") ) { $overallGrade =  '<FONT COLOR=#3366ff> '.$userinfo[2].' </FONT>'; }
	    if (!strcmp($userinfo[2], "C") ) { $overallGrade =  '<FONT COLOR=#cc0000> '.$userinfo[2].' </FONT>'; }
	  }

	  // if($li==36){  ------------------------------------------------------------------
          if( !strcmp($userinfo[0],"FINAL") ) {

	    if ( $ma > 0 ) { $finalGrade =  $userinfo[2].'*'; } 
	    else           { $finalGrade =  $userinfo[2]; }

	    if (!strcmp($userinfo[2], "A") ) { 
	      $finalGrade =  '<FONT COLOR=#009c66> '.$finalGrade.' </FONT>'; 
	      $module     =  '<FONT COLOR=#009c66> '.$moduleTemp.' </FONT>'; 
	    }	 
	    else if (!strcmp($userinfo[2], "B") ) { 
	      $finalGrade =  '<FONT COLOR=#3366ff> '.$finalGrade.' </FONT>'; 
	      $module     =  '<FONT COLOR=#3366ff> '.$moduleTemp.' </FONT>'; 
	    }
	    else if (!strcmp($userinfo[2], "C") ) { 
	      $finalGrade =  '<FONT COLOR=#cc0000> '.$finalGrade.' </FONT>'; 
	      $module     =  '<FONT COLOR=#cc0000> '.$moduleTemp.' </FONT>'; 
	    }
	    else {
	      $finalGrade =  $finalGrade; 
	      $module     =  $moduleTemp; 
	    }
	  }
	  
	  if (!strcmp($module, "") ) { $module = $moduleTemp; }
	  
	  // commments:
	  // if($li==15 || $li==16 || $li==17 ||$li==18 || $li==37 ) {
	  if (!strcmp($userinfo[2],"Vcal") ||
 	      !strcmp($userinfo[2],"SCurve") ||
 	      !strcmp($userinfo[2],"Gain") ||
 	      !strcmp($userinfo[2],"Ped") ) {
	    
	    $com=$com.' ';
	    $ar = count($userinfo);
	    if($ar>1) {
	      
	      for($en=0; $en<$ar+10; $en++) {
		
		$com=$com.' '.$userinfo[$en];
	      }
	    }
	  }

	  if( !strcmp($userinfo[0],"Regrading:") ) {
	    
	    $com=$com.' ';
	    $ar = count($userinfo);
	    
	    $com=$com.'<FONT COLOR=#cc0000>';
	    
	    for($en=1; $en<$ar+10; $en++) {
	      
	      $com=$com.' '.$userinfo[$en];
	    }

	    $com=$com.'</FONT>';
	  }

	  if( !strcmp($userinfo[0],"Missing:") ) {
	    
	    $tmp_mis = ''; $files_mis=0;

	    $mis=$mis.' <FONT COLOR=#ff3300><I><small> MISSING: ';
	    $ar = count($userinfo);
	    
	    for($en=1; $en<$ar+10; $en++) {

	      if ( $files_mis == 1 ) { $mis= $mis.''.$tmp_mis; $files_mis = 0; }

	      if( !strcmp($userinfo[$en],"Files:") ) {

		$tmp_mis = " FILES:";
		$files_mis = 1;
		continue;
	      }
	      
	      $mis=$mis.' '.$userinfo[$en];
	    }

	    $mis=$mis.'</I></small></FONT>';
	  }

	  if( !strcmp($userinfo[0],"Comment:") ) {
 	     	    	      
	    $com=$com.' ';
	    $ar = count($userinfo);
	    
	    for($en=1; $en<$ar+10; $en++) {
	      
	      $com=$com.' '.$userinfo[$en];
	    }
	  }

	  if( !strcmp($userinfo[0],"Half-Module") ) {
	    
	    $module='H-'.$module;
	  }
	}
		
	fclose($handle);
	if ( $list ) {
	  echo "	<TBODY>";
	  echo "		<TR>";
	  echo "			<TD HEIGHT=17 SIZE=4><b>$module</b></FONT></TD>";
	  echo "			<TD ><a href=\"$testDir/$link.html\">$testNr</a></FONT></TD>";
	  echo "			<TD >$date</FONT></TD>";
	  echo "			<TD ><a href=\"$testDir/$link.gif\">$grade</a></FONT></TD>";
	  echo "			<TD ><b>$overallGrade</b></FONT></TD>";
	  echo "			<TD ><b>$finalGrade</b></FONT></TD>";
	  echo "			<TD >$pi/$ma/$bu/$tr/$ad</FONT></TD>";
	  echo " ";
	  echo "			<TD >$rocs</FONT></TD>";
	  echo "			<TD >$n </FONT></TD>";
	  echo "			<TD >$t </FONT></TD>";
	  echo "			<TD >$c </FONT></TD>";
	  echo "			<TD >$iv150 $iv150_2</FONT></TD>";
	  echo "			<TD >$slope</FONT></TD>";
	  echo "			<TD >$temp</a></FONT></TD>";
	  if ( $cycl ){ 
	    echo "			<TD ><a href=\"$testDir/../tProfile.gif\">$cy</a>   $cycl</FONT></TD>";
	  }
	  else { 
	    echo "			<TD >$cy</FONT></TD>";
	  }
	  echo " ";
	  echo "			<TD ALIGN=LEFT>$tempWarning $com $mis</FONT></TD>";
	  echo "		</TR>";
	  echo "	</TBODY>";
	}
	
      }
    }    
  }
}

templ("footer.html");

?>
