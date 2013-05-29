<?php

function templ($tmp)
 {
   // $file_t = file("./sub/".$tmp);
 $file_t = file($tmp);
 $count_t = count($file_t);
 $test1 = 0;
 $test2 = 0;
 for ($te=0; $te<$count_t; $te++) { echo $file_t[$te];}
 };

templ("prodDef1.html");
templ("prodDef2.html");
$dir    = './';
$files = array();
$dh  = opendir($dir);
while (false !== ($filename = readdir($dh))) {
   $files[] = $filename;
}
closedir($dh);

rsort($files);
$m = count($files);

$totalDP = array();
$totalDM = array();
$totalDB = array();
$totalDT = array();
$totalDA = array();
$totalDR = array();
$link = array();
$mMod = array(); 

for ($num=1; $num<$m; $num++) {


  $al = array();
  $ma = array();
  $ba = array();
  $tr = array();
  $ad = array();
  $d = array();
  $mo = array();
  $nr = array();
  $test = array();

  if($files[$num]{0}=="M" &&  ( $files[$num]{3}>="3" || $files[$num]{2}>="1"))
  { 
      
    $subs = array();
    $sh  = opendir($files[$num]);
    while (false !== ($subname = readdir($sh))) {
      $subs[] = $subname;
    }
    closedir($sh);

    rsort($subs);
    $s = count($subs);

    for($mum=0; $mum<$s; $mum++) {

      $col = -1;
      if($subs[$mum]=="T-10a") { $col = 0; $mMod[0]++; }
      if($subs[$mum]=="T-10b") { $col = 1; $mMod[1]++; }
      if($subs[$mum]=="T+17a") { $col = 2; $mMod[2]++; }
      if($col == -1) { continue; }

      $path = $files[$num]."/".$subs[$mum];
      $ft = date("d.m.y",fileatime($path."/summaryTest.txt"));
      $handle = fopen($path."/summaryTest.txt", "r");
      $li = 0;
      while ($userinfo = fscanf($handle, "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n"))
      {
        $li = $li +1;

        if($li==1)  {

	  $nr[$col]='M0'.$userinfo[1]{2}.$userinfo[1]{3}.$userinfo[1]{4};
	}

        if($li==2)  {

	  $mo[$col]=$userinfo[2].'/'. $userinfo[3];
          $link[$col]= $userinfo[2].$userinfo[3].'.html';
          $test[$col]=$userinfo[3]; 
        }

        if($li==3) {
	  $al[$col]=$userinfo[0];
	  $ma[$col]=$userinfo[1];
	  $ba[$col]=$userinfo[2];
	  $tr[$col]=$userinfo[3];
	  $ad[$col]=$userinfo[4];
        }
        if($li==4){$d[$col]=$userinfo[5];}

      }

      fclose($handle);

      $totalDP[$col] += $al[$col];
      $totalDM[$col] += $ma[$col];
      $totalDB[$col] += $ba[$col];
      $totalDT[$col] += $tr[$col];
      $totalDA[$col] += $ad[$col];
      $totalDR[$col] += $d[$col];

    }



  echo "	<TBODY>";
  echo "		<TR>";
  echo "			<TD ALIGN=CENTER><FONT FACE=\"Bitstream Vera Serif\">$nr[0]</FONT></TD>";
  echo "			<TD ALIGN=LEFT><FONT FACE=\"Bitstream Vera Serif\"><a href=\"$mo[0]/$link[0]\">$test[0]</a> <a href=\"$mo[1]/$link[1]\"> $test[1]</a> <a href=\"$mo[2]/$link[2]\"> $test[2]</a></FONT></TD>";
  echo "			<TD ALIGN=CENTER><FONT FACE=\"Bitstream Vera Serif\">$al[0]</FONT></TD>";
  echo "			<TD ALIGN=CENTER><FONT FACE=\"Bitstream Vera Serif\">$al[1]</FONT></TD>";
  echo "			<TD ALIGN=CENTER><FONT FACE=\"Bitstream Vera Serif\">$al[2]</FONT></TD>";
  echo "			<TD ALIGN=CENTER><FONT FACE=\"Bitstream Vera Serif\">$ma[0]</FONT></TD>";
  echo "			<TD ALIGN=CENTER><FONT FACE=\"Bitstream Vera Serif\">$ma[1]</FONT></TD>";
  echo "			<TD ALIGN=CENTER><FONT FACE=\"Bitstream Vera Serif\">$ma[2]</FONT></TD>";
  echo "			<TD ALIGN=CENTER><FONT FACE=\"Bitstream Vera Serif\">$ba[0]</FONT></TD>";
  echo "			<TD ALIGN=CENTER><FONT FACE=\"Bitstream Vera Serif\">$ba[1]</FONT></TD>";
  echo "			<TD ALIGN=CENTER><FONT FACE=\"Bitstream Vera Serif\">$ba[2]</FONT></TD>";
  echo "			<TD ALIGN=CENTER><FONT FACE=\"Bitstream Vera Serif\">$tr[0]</FONT></TD>";
  echo "			<TD ALIGN=CENTER><FONT FACE=\"Bitstream Vera Serif\">$tr[1]</FONT></TD>";
  echo "			<TD ALIGN=CENTER><FONT FACE=\"Bitstream Vera Serif\">$tr[2]</FONT></TD>";
  echo "			<TD ALIGN=CENTER><FONT FACE=\"Bitstream Vera Serif\">$ad[0]</FONT></TD>";
  echo "			<TD ALIGN=CENTER><FONT FACE=\"Bitstream Vera Serif\">$ad[1]</FONT></TD>";
  echo "			<TD ALIGN=CENTER><FONT FACE=\"Bitstream Vera Serif\">$ad[2]</FONT></TD>";
  echo "			<TD ALIGN=CENTER><FONT FACE=\"Bitstream Vera Serif\">$d[0]</FONT></TD>";
  echo "			<TD ALIGN=CENTER><FONT FACE=\"Bitstream Vera Serif\">$d[1]</FONT></TD>";
  echo "			<TD ALIGN=CENTER><FONT FACE=\"Bitstream Vera Serif\">$d[2]</FONT></TD>";
  echo "		</TR>";
  echo "	</TBODY>";

  }

}


for ($lum=0; $lum<3; $lum++){

  $totalDP[$lum] /= $mMod[$lum];
  $totalDM[$lum] /= $mMod[$lum];
  $totalDB[$lum] /= $mMod[$lum];
  $totalDT[$lum] /= $mMod[$lum];
  $totalDA[$lum] /= $mMod[$lum];
  $totalDR[$lum] /= $mMod[$lum];
  $totalDP[$lum] = number_format($totalDP[$lum],2);
  $totalDM[$lum] = number_format($totalDM[$lum],2);
  $totalDB[$lum] = number_format($totalDB[$lum],2);
  $totalDT[$lum] = number_format($totalDT[$lum],2);
  $totalDA[$lum] = number_format($totalDA[$lum],2);
  $totalDR[$lum] = number_format($totalDR[$lum],2);

  }


echo "	<TBODY>";
echo "		<TR>";
echo "			<TD ALIGN=LEFT><FONT FACE=\"Bitstream Vera Serif\">Average Defect </FONT></TD>";
echo "			<TD ALIGN=LEFT><FONT FACE=\"Bitstream Vera Serif\">/ Module</FONT></TD>";
echo "			<TD ALIGN=CENTER><FONT FACE=\"Bitstream Vera Serif\">$totalDP[0]</FONT></TD>";
echo "			<TD ALIGN=CENTER><FONT FACE=\"Bitstream Vera Serif\">$totalDP[1]</FONT></TD>";
echo "			<TD ALIGN=CENTER><FONT FACE=\"Bitstream Vera Serif\">$totalDP[2]</FONT></TD>";
echo "			<TD ALIGN=CENTER><FONT FACE=\"Bitstream Vera Serif\">$totalDM[0]</FONT></TD>";
echo "			<TD ALIGN=CENTER><FONT FACE=\"Bitstream Vera Serif\">$totalDM[1]</FONT></TD>";
echo "			<TD ALIGN=CENTER><FONT FACE=\"Bitstream Vera Serif\">$totalDM[2]</FONT></TD>";
echo "			<TD ALIGN=CENTER><FONT FACE=\"Bitstream Vera Serif\">$totalDB[0]</FONT></TD>";
echo "			<TD ALIGN=CENTER><FONT FACE=\"Bitstream Vera Serif\">$totalDB[1]</FONT></TD>";
echo "			<TD ALIGN=CENTER><FONT FACE=\"Bitstream Vera Serif\">$totalDB[2]</FONT></TD>";
echo "			<TD ALIGN=CENTER><FONT FACE=\"Bitstream Vera Serif\">$totalDT[0]</FONT></TD>";
echo "			<TD ALIGN=CENTER><FONT FACE=\"Bitstream Vera Serif\">$totalDT[1]</FONT></TD>";
echo "			<TD ALIGN=CENTER><FONT FACE=\"Bitstream Vera Serif\">$totalDT[2]</FONT></TD>";
echo "			<TD ALIGN=CENTER><FONT FACE=\"Bitstream Vera Serif\">$totalDA[0]</FONT></TD>";
echo "			<TD ALIGN=CENTER><FONT FACE=\"Bitstream Vera Serif\">$totalDA[1]</FONT></TD>";
echo "			<TD ALIGN=CENTER><FONT FACE=\"Bitstream Vera Serif\">$totalDA[2]</FONT></TD>";
echo "			<TD ALIGN=CENTER><FONT FACE=\"Bitstream Vera Serif\">$totalDR[0]</FONT></TD>";
echo "			<TD ALIGN=CENTER><FONT FACE=\"Bitstream Vera Serif\">$totalDR[1]</FONT></TD>";
echo "			<TD ALIGN=CENTER><FONT FACE=\"Bitstream Vera Serif\">$totalDR[2]</FONT></TD>";
echo "		</TR>";
echo "	</TBODY>";

 templ("footer.html");
?>
