#!/usr/bin/perl
# perl lsvm2arff.pl inputLibSVMData.lsvm outputWeka.arff
$attNum=`head -n1 $ARGV[0] | wc -w`;
$attNum=$attNum-1;

$cmd_str="cat $ARGV[0] | perl -lane 'print \$F[0]' | sort | uniq | sort -n";
chomp($IDs=`$cmd_str`);
@classIDs=split(' ',$IDs);
#print "IDS=@classIDs, $classIDs[0]\n";
print "In this convertion code, your original class 'label' will be converted into 'class_label'; \nFor example, if class IDs are:\t1,\t\t2; \nthey will be converted into:\tclass_1,\tclass_2\n";


open(OUT, ">$ARGV[1]") || die "$!";
print OUT "\@relation libSVM2ARFF_DATA\n";
print OUT "\n";

for($i=1;$i<=$attNum;$i++){
print OUT "\@attribute attribute_${i} real\n";
}
$tmp_str="";
for($j=0;$j<@classIDs-1;$j++){
 $ID=$classIDs[$j];
 $tmp_str=$tmp_str."class_$ID,";
}
print OUT "\@attribute class {${tmp_str}class_$classIDs[-1]}\n";

print OUT "\n";

print OUT "\@data\n";

#print "$cmd_str\n";
#$cmd_str="cat ~/Dropbox/tmp/tst_data_D50.lsvm |  perl -lane 's|\d+:||g; print \$_' | perl -lane '\$str="";for(\$i=1;\$i<\@F;\$i++){\$str=\$str."\$F[\$i],"};print "${str}class$F[0]"'"
$cmd_str="cat $ARGV[0] |  perl -lane 's|\\d+:||g; print \$_' | perl -lane '\$len=\@F; \$str=\"\";for(\$i=1;\$i<\$len;\$i++){\$str=\$str.\"\$F[\$i],\"};print \"\${str}class_\$F[0]\"'";
#print "$cmd_str\n";
#`echo $cmd_str`;
chomp(@data=`$cmd_str`);

foreach(@data){
print OUT "$_\n";
}
