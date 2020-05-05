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

# PATHS
# ====================================================
SOURCE_PATH=$HOME'/Utilities/ieeestyle-happy/sources/'

# PARAMETERS
# ====================================================
FILENAME_INPUT_FROM_ZOTERO='zotero_refs.txt'
FILENAME_INPUT_NON_LOWERCASE='non_lowercase_words.txt'
FILENAME_INPUT_ABBREVIATIONS='journal_abbreviations.txt'
FILENAME_OUTPUT='output.lyx'

# Optional (Rename PDF files correctly)
#-----------------------------------------------------
ENABLE_PDF_RENAMING=1  # 1:ON, 0:OFF
ZOTERO_EXPORT_FOLDER_NAME="ExportedItems"

if [ $ENABLE_PDF_RENAMING -eq 1 ]; then
    echo "Renaming PDFs"
    find $ZOTERO_EXPORT_FOLDER_NAME"/" -type f -name "*.pdf" > _pdf_file_list.txt
fi

# EXE
# =======================================
cp $SOURCE_PATH"/create_lyx1.3.3_refs_from_txt.py" create_lyx.py

# EXECUTION 
# =======================================
echo $FILENAME_INPUT_FROM_ZOTERO    >  in.create_lyx
echo $FILENAME_INPUT_NON_LOWERCASE  >> in.create_lyx
echo $FILENAME_INPUT_ABBREVIATIONS  >> in.create_lyx
echo $FILENAME_OUTPUT               >> in.create_lyx

./create_lyx.py in.create_lyx > out.create_lyx
exit
# CLEAN
# =======================================
rm create_lyx.py 
rm in.create_lyx 
# rm out.create_lyx 
