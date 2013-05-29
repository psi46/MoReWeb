<?php


function templ($tmp)
 {
 $file_t = file($tmp);
 $count_t = count($file_t);
 $tests = 0;
 for ($te=0; $te<$count_t; $te++) { echo $file_t[$te];}
 };

templ("radHeader.html");
$dir    = './';
$files = array();
$dh  = opendir($dir);
while (false !== ($filename = readdir($dh))) {
   $files[] = $filename;
}

rsort($files);
$m = count($files);

for ($num=0; $num<$m; $num++) {

  if($files[$num]{0}=="R" && $files[$num]{5}=="M")
  {
    $subs = array();
    $sh  = opendir($files[$num]);
    while (false !== ($subname = readdir($sh))) {
      $subs[] = $subname;
    }

    rsort($subs);
    $s = count($subs);

  }

  for ($mum=0; $mum<$s; $mum++) {

  if($files[$num]{0}=="R" && $files[$num]{5}=="M")  {

    $subs = array();
    $sh  = opendir($files[$num]);
    while (false !== ($subname = readdir($sh))) {
      $subs[] = $subname;
    }
    closedir($sh);

    rsort($subs);
    $s = count($subs);

    for($mum=0; $mum<$s; $mum++) {

      if($subs[$mum]{0}=="T") {

        $pi=0; $ma=0; $bu=0; $tr=0; $ad=0;
	$rocs=0; $root=0;
	$date=''; $datr=''; $daca='';
	$temp=0; $cycl=0;
	$i=0; $ivVar=0; $ivDP=0;
	$com=' ';

        $path = $files[$num]."/".$subs[$mum];
        #echo "$path\n";
        $ft = date("d.m.y",fileatime($path."/summaryTest.txt"));
        $handle = fopen($path."/summaryTest.txt", "r");
        $li = 0;
        while ($userinfo = fscanf($handle, "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n"))  {

          $li = $li +1;

          if($li==2)  {
	    $testDir=$userinfo[2]."/".$userinfo[3];
	    $module='M'.$userinfo[2]{6}.$userinfo[2]{7};
	    $testNr=$userinfo[3]; 
            if ($userinfo[1]{3}!="0") { 
              $rad=$userinfo[2]{3}.$userinfo[2]{4};
            }
	    else { $rad=$userinfo[2]{4};}
            $link= $userinfo[2].$userinfo[3].'.html';
          }
          if($li==3)  {
            $pi=$userinfo[0];
            $ma=$userinfo[1];
            $bu=$userinfo[2];
            $tr=$userinfo[3];
            $ad=$userinfo[4];
          }
          if($li==4)  {$rocs=$userinfo[5];}
          if($li==5)  {
            $root=$userinfo[2];
            if ( $root > 0 )   {$com=$com.'  <FONT COLOR=#cc0000> DATA MISSING: '.$root.' hist. not found in FullTest.root </FONT>';}
            }
          if($li==6)  {$date=$userinfo[4].' '.$userinfo[5];}
          if($li==7)  {
            $t=$userinfo[1];
            $datr=', '.$userinfo[4].' '.$userinfo[5];
          }
         if($li==8)  {
           $c=$userinfo[1];
           $daca=', '.$userinfo[4].' '.$userinfo[5];
         }
         if($li==9){$temp=$userinfo[1];}
         if($li==10){$cycl=$userinfo[2];}
         if($li==19)  {
           $i=$userinfo[2];
           if($i==0 || $i=='') { $iv150='no'; }
           else {
             $iv150=sprintf("I(150) =     %01.2f muA",$i);
             if ( $i > 2 ) { $com=$com.'leakage current to high!'; }
           }
         }
         if($li==20){
           $ivVar=$userinfo[1];
           $ivVar = number_format($ivVar,1);
           if ( $ivVar > 2 ) { $com=$com.'high variation of leakage current I(150)/I(100) = '.$ivVar.'!'; }
           }
         if($li==21){
           $ivDP=$userinfo[2];
           if ( $ivDP < 10 &&  $ivDP != 0 ) {$com=$com.' incompl. iv-data: '.$ivDP.' meas.';}
           }

         # commments:
         if($li==15 || $li==16 || $li==17 ||$li==18 ) {
           if (strcmp($userinfo[1],"good"))  {
             $com=$com.' ';
             $ar = count($userinfo);
             if($ar>1)
             {
               for($en=0; $en<$ar+10; $en++)
               {
                 $com=$com.' '.$userinfo[$en];
               }
             }
           }
         }
       }

       fclose($handle);

       echo "	<TBODY>";
       echo "		<TR>";
       echo "			<TD HEIGHT=17 ALIGN=CENTER><FONT FACE=\"Bitstream Vera Serif\">$rad</FONT></TD>";
       echo "			<TD HEIGHT=17 ALIGN=CENTER><FONT FACE=\"Bitstream Vera Serif\">$module</FONT></TD>";
       echo "			<TD ALIGN=CENTER><FONT FACE=\"Bitstream Vera Serif\"><a href=\"$testDir/$link\">$testNr</a></FONT></TD>";
       echo "			<TD ALIGN=CENTER><FONT FACE=\"Bitstream Vera Serif\">$date</FONT></TD>";
       echo "			<TD ALIGN=CENTER><FONT FACE=\"Bitstream Vera Serif\">$pi/$ma/$bu/$tr/$ad</FONT></TD>";
       echo " ";
       echo "			<TD ALIGN=CENTER><FONT FACE=\"Bitstream Vera Serif\">$t$datr</FONT></TD>";
       echo "			<TD ALIGN=CENTER><FONT FACE=\"Bitstream Vera Serif\">$c$daca</FONT></TD>";
       echo "			<TD ALIGN=CENTER><FONT FACE=\"Bitstream Vera Serif\">$rocs</FONT></TD>";
       echo "			<TD ALIGN=CENTER><FONT FACE=\"Bitstream Vera Serif\">$cycl</FONT></TD>";
       echo "			<TD ALIGN=CENTER><FONT FACE=\"Bitstream Vera Serif\">$iv150</FONT></TD>";
       echo "			<TD ALIGN=CENTER><FONT FACE=\"Bitstream Vera Serif\">$temp C</FONT></TD>";
       echo " ";
       echo "			<TD ALIGN=LEFT><FONT FACE=\"Bitstream Vera Serif\">$com</FONT></TD>";
       echo "		</TR>";
       echo "	</TBODY>";

      }
    }
  }
  }
}

 templ("footer.html");
?>
