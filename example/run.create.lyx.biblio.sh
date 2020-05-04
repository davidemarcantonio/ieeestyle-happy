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

set -ue
export LC_NUMERIC=en_US.utf8
export LC_ALL=C

# PATHS
# ====================================================
SOURCE_PATH=$HOME'/Utilities/ieeestyle-happy/sources/'

# PARAMETERS
# ====================================================
FILENAME_INPUT_FROM_ZOTERO='zotero_refs.txt'
FILENAME_INPUT_NON_LOWERCASE='non_lowercase_words.txt'
FILENAME_INPUT_ABBREVIATIONS='journal_abbreviations.txt'
FILENAME_OUTPUT='output.lyx'

# EXE
# =======================================
cp $SOURCE_PATH"/create_lyx1.3.3_refs_from_txt.py" create_lyx.exe

# EXECUTION 
# =======================================
echo $FILENAME_INPUT_FROM_ZOTERO    >  in.create_lyx
echo $FILENAME_INPUT_NON_LOWERCASE  >> in.create_lyx
echo $FILENAME_INPUT_ABBREVIATIONS  >> in.create_lyx
echo $FILENAME_OUTPUT               >> in.create_lyx

time ./create_lyx.exe in.create_lyx > out.create_lyx

# CLEAN
# =======================================
# rm create_lyx.exe 
# rm in.create_lyx 
# rm out.create_lyx 
