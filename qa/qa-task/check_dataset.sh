#!/bin/bash

PERIOD=LHC16m

# For merged Aod
FILEPATH="AOD/*"

# For non-merged Aod
# FILEPATH="*.*"


function dump_run()
{
    alien_find /alice/data/2016/$PERIOD/000$1/muon_calo_pass1/$FILEPATH/ -z  -name AliAOD.root
}

# Here is how we find band and/or good runs
function run_has_data()
{
    echo $1
    if (( $(dump_run $1 | wc -l) > 1 )); then
        echo $I >> good-runs-$PERIOD.log
    else
        echo "A bad run has been found: " $I
        echo $I >> bad-runs-$PERIOD.log
    fi
}


# LHC16h
# runs=(255469 255467 255466 255465 255463 255447 255442 255440 255421 255420 255419 255418 255415 255407 255402 255398 255352 255351 255350 255283 255280 255278 255276 255275 255256 255255 255253 255252 255251 255249 255248 255247 255242 255240 255211 255210 255182 255181 255180 255177 255176 255174 255173 255171 255167 255162 255159 255154 255138 255136 255135 255111 255091 255086 255085 255082 255079 255076 255075 255074 255073 255071 255070 255068 255042 255039 255011 255010 255009 255008 254984 254983 254933 254915 254914 254892 254877 254857 254854 254849 254848 254846 254766 254761 254750 254735 254706 254704 254701 254691 254673 254670 254654 254653 254652 254651 254649 254648 254646 254644 254640 254632 254630 254629 254628 254627 254621 254619 254608 254607 254606 254604 254589 254586 254581 254578 254577 254576 254568 254564 254559 254553 254530 254529 254495 254487 254479 254476 254475 254422 254419 254418 254396 254395 254394 254381 254378)

# LHC16i
#runs=(255650 255649 255648 255642 255639 255618 255617 255616 255615 255614 255592 255591 255590 255589 255587 255586 255585 255584 255583 255582 255581 255580 255579 255578 255577 255558 255543 255542 255541 255540 255539 255538 255537 255536 255535 255534 255533 255515)
# runs=(255650 255649 255648 255642 255639 255616 255615 255614 255592 255591 255582 255577 255558 255543 255542 255540 255538 255537 255535 255534 255533 255515)

# LHC16j
#runs=(256420 256419 256418 256417 256415 256373 256372 256371 256370 256368 256367 256366 256365 256364 256363 256362 256361 256357 256356 256355 256311 256309 256307 256306 256302 256299 256298 256297 256295 256294 256293 256292 256291 256290 256289 256287 256286 256285 256284 256283 256282 256281 256280 256279 256261 256231 256230 256228 256227 256226 256225 256224 256223 256222 256219 256215 256213 256212 256211 256210 256207 256204 256169 256166 256165 256162 256161 256158 256157 256156 256155 256154 256152 256151 256150 256149 256148 256147 256146 256145)

# LHC16k
# runs=(258574 258567 258560 258558 258551 258550 258549 258545 258537 258499 258498 258485 258477 258456 258455 258454 258452 258451 258424 258399 258398 258397 258395 258394 258393 258391 258390 258388 258387 258359 258357 258336 258332 258307 258306 258303 258302 258301 258299 258280 258279 258278 258277 258276 258275 258274 258273 258272 258271 258270 258266 258264 258261 258260 258259 258258 258257 258256 258255 258204 258203 258202 258198 258197 258178 258117 258114 258113 258112 258111 258110 258109 258108 258107 258063 258062 258061 258060 258059 258053 258051 258050 258049 258048 258047 258046 258045 258041 258039 258019 258016 258013 258011 258010 258008 258003 257992 257989 257988 257986 257985 257979 257971 257968 257967 257966 257965 257963 257960 257959 257958 257957 257939 257937 257936 257932 257912 257909 257908 257907 257901 257900 257899 257898 257897 257896 257895 257894 257893 257892 257855 257854 257853 257851 257850 257804 257803 257800 257799 257798 257797 257773 257765 257757 257756 257755 257754 257737 257736 257735 257734 257733 257727 257725 257724 257697 257693 257692 257691 257690 257689 257688 257687 257685 257684 257683 257682 257644 257643 257642 257636 257635 257632 257631 257630 257606 257605 257604 257601 257600 257595 257594 257592 257591 257590 257588 257587 257566 257565 257564 257563 257562 257561 257560 257541 257540 257539 257538 257537 257536 257535 257534 257533 257532 257531 257530 257491 257490 257488 257487 257433 257382 257381 257364 257358 257357 257260 257224 257209 257208 257207 257206 257205 257204 257187 257186 257145 257144 257143 257142 257141 257140 257139 257138 257137 257136 257135 257100 257099 257098 257095 257094 257093 257092 257086 257084 257083 257082 257081 257080 257079 257078 257077 257075 257074 257073 257072 257071 257028 257027 257026 257025 257024 257023 257022 257021 257012 257011 256944 256942 256941 256926 256924 256922 256921 256919 256918 256913 256912 256911 256910 256797 256782 256781 256697 256696 256695 256694 256692 256691 256681 256677 256676 256658 256657 256656 256655 256654 256653 256620 256619 256592 256591 256589 256567 256566 256565 256564 256562 256561 256560 256559 256557 256556 256514 256513 256512)

# LHC16l
# runs=(260014 260011 260010 259979 259961 259954 259915 259914 259913 259889 259888 259868 259867 259866 259865 259864 259863 259862 259861 259860 259842 259841 259822 259792 259789 259788 259781 259779 259778 259777 259756 259752 259751 259750 259748 259747 259713 259712 259711 259705 259704 259703 259702 259700 259699 259698 259697 259670 259669 259668 259650 259649 259648 259478 259477 259473 259472 259471 259470 259469 259396 259395 259394 259389 259388 259387 259386 259382 259381 259380 259379 259378 259342 259341 259340 259339 259336 259335 259334 259308 259307 259305 259303 259302 259274 259273 259272 259271 259270 259269 259268 259264 259263 259261 259260 259259 259257 259229 259228 259227 259204 259164 259162 259161 259160 259118 259117 259099 259096 259095 259091 259090 259088 259086 258964 258963 258962 258931 258926 258925 258924 258923 258921 258920 258919 258890 258889 258888 258887 258886 258885 258884 258883)

# LHC16m
runs=(260216 260217 260218 260240 260307 260308 260309 260310 260311 260312 260313 260314 260338 260339 260340 260351 260354 260355 260357 260379 260411 260429 260430 260432 260435 260436 260437 260440 260441 260447 260471 260472 260474 260475 260476 260477 260478 260479 260480 260481 260482 260486 260487 260490 260494 260495 260496 260497 260536 260537 260539 260540 260541 260542 260564 260565 260586 260610 260611 260613 260614 260615 260616 260647)

# determine good and bad runs
for I in ${runs[*]}; do
    run_has_data $I
done


# Show that bad runs have no files indeed
while read run; do
    dump_run $run
done < bad-runs-$PERIOD.log

echo -e "\x07"
