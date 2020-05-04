#!/bin/bash
# ====================================================
#
# CREATE A LYX DOCUMENT (V.1.3.3) WITH A LIST OF 
# REFERENCE IN THE STANDARD FORMAT OF IEEE-TAP
#
# ====================================================
#
# INPUTs:
# - .txt file exported from ZOTERO in IEEE-TAP std 
# - .txt file of words NOT to put lowercase in title
# - .txt of journal abbreviations
#
# OUTPUTs:
# - .lyx file with a list (itemize) of reference and
#   consistent bibliography 
#
# ====================================================
#
# Creation:        04/05/2020
# Updates:         04/05/2020 - added Test 1D
#
# ====================================================

#
# PATHS
# ====================================================
SOURCE_PATH=$HOME'/Utilities/ieee-stylehappy'

#
# PARAMETERS
# ====================================================
FILENAME_INPUT_FROM_ZOTERO='zotero_refs.txt'
FILENAME_INPUT_NON_LOWERCASE='non_lowercase_words.txt'
FILENAME_INPUT_ABBREVIATIONS='journal_abbreviations.txt'
FILENAME_OUTPUT='output.lyx'

#
# EXE
# =======================================
cp $SOURCE_PATH'/create_lyx1.3.3_refs_from_txt.py' .

#
# EXECUTION 
# =======================================
echo $FILENAME_INPUT_FROM_ZOTERO    >  in.Compute.Benchmark
echo $FILENAME_INPUT_NON_LOWERCASE  >> in.Compute.Benchmark
echo $FILENAME_INPUT_ABBREVIATIONS  >> in.Compute.Benchmark
echo $FILENAME_OUTPUT               >> in.Compute.Benchmark

time ./create_lyx_refs_from_txt.py < in.create_lyx > out.create_lyx

#
# CLEAN
# =======================================
rm create_lyx_refs_from_txt.py 
rm in.create_lyx 
rm out.create_lyx 
