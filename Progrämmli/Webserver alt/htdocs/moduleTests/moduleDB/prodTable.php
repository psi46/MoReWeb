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

 for($num=0; $num<$m; $num++) {

  $take = 0;
  if ( $modSel ) { 

    if ( $files[$num]{0}==$myMod{0} && $files[$num]{1}==$myMod{1}  && $files[$num]{2}==$myMod{2} && 
	 $files[$num]{3}==$myMod{3} && $files[$num]{4}==$myMod{4} ) { $take = 1; }
  }
  else if ( !strcmp($serie, "all") ) { 
 
    if ( $files[$num]{0}=="M" ) { $take = 1; }
  }
  else {
 
    if ($files[$num]{0}=="M" && 
	$files[$num]{1}==substr($serie, 0, 1) && 
	$files[$num]{2}==substr($serie, 1, 2) )  { $take = 1; }
  }

  if ( !$modSel && !strcmp($serie, "all") && $num>100 ) { exit; }

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
        $no=0; $th=0; $ga=0; $pe=0; $pa=0;
	$rocs=0; $root=0;
	$date=''; $datr=''; $daca='';
	$c=''; $t=''; $n='';
	$temp=0; $sollTemp=0;$cycl=''; $cy='';
	$i=0; $ivVar=0; $ivDP=0; $slope=0;
	$tbm1=1; $tbm2=1;
	$iv150 = ''; $iv150_2 = '';
	$grade = '';
	$mount = '';
	$finalGrade = '';
	$fullGrade = '';
	$shortGrade = '';
	$reGrade = '';
	$com=' ';
	$mis=' ';
	$tempWarning=' ';
	$noiB=0; $noiC=0; $trmB=0; $trmC=0;
	$gainB=0; $gainC=0; $pedB=0; $pedC=0;
	$highCur = 0;
	$perfDef = 0;
	$half = 0;
	$regraded = 0;
	$star = 0;

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
	    $year = $userinfo[1]{6}.$userinfo[1]{7};
	    
	    for ( $i=0; $i<12;$i++ ) {
	      if (!strcmp($month, $monthN[$i]) ) {
		
		$date = $monthS[$i].' '.$day.' 20'.$year;
	      }
	    }
	  }
	  
	  // if($li==2)  { ------------------------------------------------------------------
          if( !strcmp($userinfo[0],"ModuleNr") ) {
	    
            $testNr  = $userinfo[3]; 
	    $testDir = $userinfo[2].'/'. $userinfo[3];
            $link    = $userinfo[2].$userinfo[3];
          }
	  
	  $alvl = "";
	  if (file_exists($path."/alvl_$link.gif")) {
	    $alvl = "fits";
	  }
          //if($li==3)  { //------------------------------------------------------------------
	  if( !strcmp($userinfo[0],"Defects") ) {
	    
            $pi=$userinfo[1];
            $ma=$userinfo[2];
	    if ( $ma > 0 ) { 
	      $star = 1;
	      $ma='<FONT COLOR=#cc0000>'.$ma.'</FONT>'; 
	    }
            $bu=$userinfo[3];
            $tr=$userinfo[4];
            $ad=$userinfo[5];
          }

          //if($li==3)  { //------------------------------------------------------------------
	  if( !strcmp($userinfo[0],"PerfDefects") ) {
	    
            $no=$userinfo[1];
            $th=$userinfo[2];
            $ga=$userinfo[3];
            $pe=$userinfo[4];
            $pa=$userinfo[5];
	    $perfDef=1;
          }
	  
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
//           if( !strcmp($userinfo[0],"Tested") && $moduleNr < 50 ) {

//             $date=$userinfo[4].' '.$userinfo[5];
// 	  }
	  
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
href="http://cmspixel.phys.ethz.ch/moduleTests/moduleDB/tbmDefects.html"> Err '.$tbm1.'</a>.';
	    }
	  }
	  
	  // if($li==18)  {  ------------------------------------------------------------------
          if( !strcmp($userinfo[0],"TBM2") ) {
	    
            $tbm2=$userinfo[1];
            if ( $tbm2 != 0 )   {
	      
	      $com=' '.$com.' TBM2: <a
href="http://cmspixel.phys.ethz.ch/moduleTests/moduleDB/tbmDefects.html"> Err '.$tbm2.'</a>.';
	      
	    }
	  }

	  // if($li==19)  {  ------------------------------------------------------------------
          if( !strcmp($userinfo[0],"I") ) {

	    $i=$userinfo[2];
	    
	    if($i==0 || $i=='') { $iv150=''; }
	    else {
	      
	      $iv150=sprintf("%01.2f uA",$i);
	      
	      if ( $sollTemp < 0 ) { 
		
		$i10   = sprintf("%01.2f uA", $i/12.10188635);
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


	  // if($li==19)  {  ------------------------------------------------------------------
          if( !strcmp($userinfo[0],"SwitchOn") ) {

	    $i=$userinfo[1];
	    
	    if($i==0 || $i=='') { $switchOn ='-'; }
	    else {
	      
	      $switchOn=sprintf("%01.2f uA",$i);
	    }
	  
	  }
	  
	  // if($li==19)  {  ------------------------------------------------------------------
          if( !strcmp($userinfo[0],"Current") ) {

	    $i=$userinfo[1];
	    
	    if($i==0 || $i=='') { $current='-'; }
	    else {
	      
	      $current=sprintf("%01.2f uA",$i);

	      if ( $sollTemp < 0 ) { 
		
		$i17   = sprintf("%01.2f uA", $i*12.10188635);
		$current_2 = $i17;
		$current = '('.$current.')';
		
		if ( $i17 > 15 ) { 
		  $highCur   = 1;
		  $current   = '<FONT COLOR=#cc0000>'.$current.'</FONT>'; 
		  $current_2 = '<FONT COLOR=#cc0000>'.$current_2.'</FONT>';
		}

		else if ( $i > 3 ) {
		  $current   = '<FONT COLOR=#ff3300>'.$current.'</FONT>'; 
		  $current_2 = '<FONT COLOR=#ff3300>'.$current_2.'</FONT>'; 
		}
	      }
	      
	      if ( $sollTemp > 0 ) { 
		
		$current_2 = '';

		if ( $i > 10 ) { 
		  $highCur   = 1;
		  $current   = '<FONT COLOR=#cc0000>'.$current.'</FONT>';  
		}

		else if ( $i > 2 ) { 
		  $current   = '<FONT COLOR=#ff3300>'.$current.'</FONT>';
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


	  // if($li==22){  ------------------------------------------------------------------
          if( !strcmp($userinfo[0],"position") ) {

	    $mount=$userinfo[1];
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
	    } else {
	      $n = '-';
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
	      
	      if ( strcmp($c, "yes") ) {
		$c = '';
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


	  // if($li==31){  ------------------------------------------------------------------
          if( !strcmp($userinfo[0],"MeanParameter1") ) {

	    $par1B=$userinfo[1];
	    $par1C=$userinfo[2];

	    if (  $gainB == 0 && $gainC == 0 &&
		  $pedB  == 0 && $pedC  == 0 &&
		  $par1B  == 0 && $par1C  == 0 ) {
	      
	      if ( strcmp($c, "no") ) {
		$c = 'ok';
	      }
	    }
	    else if ( $par1B > 0 && $par1C == 0 ) {
	      $c = $c.'  '.$par1B.'B Par1';
	    }
	    else if ( $par1B > 0 && $par1C > 0 ) {
	      $c = $c.'  '.$par1B.'B/<FONT COLOR=#cc0000>'.$par1C.'C</FONT>  Par1';
	    }
	    else if ( $par1C > 0 && $par1B == 0 ) {
	      $c = $c.'  <FONT COLOR=#cc0000>'.$par1C.'C</FONT> Ped';
	    }
	  }

	  // if($li==34){  ------------------------------------------------------------------
          if( !strcmp($userinfo[0],"RATIO") ) {

	    if ( $userinfo[1] > 5 ) { 
	      $com=$com.' I_recalc > 5 x I_meas'; 
	    }
	  }



	  // if($li==36){  ------------------------------------------------------------------
          if( !strcmp($userinfo[0],"FINAL") ) {

	    $finalGrade = $userinfo[2];

	    if (!strcmp($userinfo[2], "A") ) { 
	      $finalGrade =  '<FONT COLOR=#009c66> '.$finalGrade.' </FONT>';  
	    }	 
	    else if (!strcmp($userinfo[2], "B") ) { 
	      $finalGrade =  '<FONT COLOR=#3366ff> '.$finalGrade.' </FONT>'; 
	    }
	    else if (!strcmp($userinfo[2], "C") ) { 
	      $finalGrade =  '<FONT COLOR=#cc0000> '.$finalGrade.' </FONT>';  
	    }
	    else {
	      $finalGrade =  $finalGrade; 
	    }
	  }

	  // if($li==35){  ------------------------------------------------------------------
          if( !strcmp($userinfo[0],"shortTest") ) {

	    $shortGrade =  $userinfo[2];
	    if (!strcmp($userinfo[2], "A") ) { $shortGrade =  '<FONT COLOR=#009c66> a </FONT>'; }
	    if (!strcmp($userinfo[2], "B") ) { $shortGrade =  '<FONT COLOR=#3366ff> b </FONT>'; }
	    if (!strcmp($userinfo[2], "C") ) { $shortGrade =  '<FONT COLOR=#cc0000> c </FONT>'; }
	  }

	  // if($li==36){  ------------------------------------------------------------------
          if( !strcmp($userinfo[0],"fullTest")  ) {

	    if ( $star ) { $fullGrade =  $userinfo[2].'*'; } 
	    else         { $fullGrade =  $userinfo[2]; }

	    if (!strcmp($userinfo[2], "A") ) { 
	      $fullGrade =  '<FONT COLOR=#009c66> '.$fullGrade.' </FONT>'; 
	      $module     =  '<FONT COLOR=#009c66> '.$moduleTemp.' </FONT>'; 
	    }	 
	    else if (!strcmp($userinfo[2], "B") ) { 
	      $fullGrade =  '<FONT COLOR=#3366ff> '.$fullGrade.' </FONT>'; 
	      $module     =  '<FONT COLOR=#3366ff> '.$moduleTemp.' </FONT>'; 
	    }
	    else if (!strcmp($userinfo[2], "C") ) { 
	      $fullGrade =  '<FONT COLOR=#cc0000> '.$fullGrade.' </FONT>'; 
	      $module     =  '<FONT COLOR=#cc0000> '.$moduleTemp.' </FONT>'; 
	    }
	    else {
	      $fullGrade =  $fullGrade; 
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
	    
	    $regraded=1;
	    $ar = count($userinfo);
	    
	    $reGrade=$reGrade.'<FONT COLOR=#cc0000>*';
	    
	    for($en=1; $en<$ar+10; $en++) {
	      
	      $reGrade=$reGrade.' '.$userinfo[$en];
	    }

	    $reGrade=$reGrade.'</FONT>';
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
	    $half = 1;
	  }
	}
	
	if ( $highCur ){
	  $com =  $com.' <FONT COLOR=#006600><I>switch-on: '.$switchOn.'</I></FONT> ';
	}

	$pdef   = '';
	if ( $perfDef ) {
		  $pdef   = '<BR><FONT COLOR=#424242>'.$no.'/'.$th.'/'.$ga.'/'.$pe.'/'.$pa.'</FONT>'; 
	}

	if ( $regraded ) {
	  $com = $reGrade.'<br>'.$com;
	  $finalGrade = $finalGrade.'<FONT COLOR=#cc0000>*</FONT>';
	}

	if ( $half ) {
	  $module='H-'.$module;
	}
	fclose($handle);
	
	echo "	<TBODY>";
	echo "		<TR>";
	echo "			<TD ><b>$finalGrade</b></FONT></TD>";
	echo "			<TD HEIGHT=17 SIZE=4><b>$module</b></FONT></TD>";
	echo "			<TD ><a href=\"$testDir/$link.html\">$testNr</a></FONT></TD>";
	echo "			<TD >$date</FONT></TD>";
	echo "			<TD ><a href=\"$testDir/$link.gif\">$grade</a></FONT></TD>";
	echo "			<TD ><b>$fullGrade</b></FONT></TD>";
	echo "			<TD ><a href=\"http://cmspixel.phys.ethz.ch/moduleTests/moduleDB/shortTests/prodTable.php?modul=$moduleTemp\">$shortGrade</a></FONT></TD>";
	echo "			<TD>$pi/$ma/$bu/$tr/$ad    $pdef</FONT></TD>";
	echo " ";
	echo "			<TD >$rocs</FONT></TD>";
	echo "			<TD >$n </FONT></TD>";
	echo "			<TD >$t </FONT></TD>";
	echo "			<TD >$c </FONT></TD>";
	echo "			<TD ><a href=\"$testDir/alvl_$link.gif\">$alvl</a></FONT></TD>";
	echo "			<TD >$current_2 $current</FONT></TD>";
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
	echo "			<TD> $mount </FONT></TD>";
	echo "			<TD ALIGN=LEFT>$tempWarning $com $mis</FONT></TD>";
	echo "		</TR>";
	echo "	</TBODY>";
	
      }
    }    
  }
}

templ("footer.html");

?>
