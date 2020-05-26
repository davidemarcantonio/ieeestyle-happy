#!/bin/bash
# ====================================================
#
# CREATE A LYX (V.1.3.3) DOCUMENT WITH A LIST OF 
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

# Optional
#-----------------------------------------------------
#  (Rename PDF files correctly)
ENABLE_PDF_RENAMING=0  # 1:ON, 0:OFF
ZOTERO_EXPORT_FOLDER_NAME="../pdfs/"
#  (Add subsections of list for classification)
# usage ->    '':OFF, 'filename.txt':ON
SUB_LIST_FROM_ZOTERO=''

if [ $ENABLE_PDF_RENAMING -eq 1 ]; then
    find $ZOTERO_EXPORT_FOLDER_NAME -type f -name "*.pdf" > _pdf_file_list.txt
    mkdir -p "Renamed-PDFs"
fi

CSV_LIST_EXPORT=1  # 1:ON, 0:OFF

# EXE
# =======================================
cp $SOURCE_PATH"/create_lyx1.3.3_refs_from_txt.py" create_lyx.py

# EXECUTION 
# =======================================
echo $FILENAME_INPUT_FROM_ZOTERO    >  in.create_lyx
echo $FILENAME_INPUT_NON_LOWERCASE  >> in.create_lyx
echo $FILENAME_INPUT_ABBREVIATIONS  >> in.create_lyx
echo $FILENAME_OUTPUT               >> in.create_lyx
echo $ENABLE_PDF_RENAMING           >> in.create_lyx
echo $SUB_LIST_FROM_ZOTERO          >> in.create_lyx
echo $CSV_LIST_EXPORT               >> in.create_lyx

./create_lyx.py in.create_lyx > out.create_lyx
rm in.create_lyx 
# rm out.create_lyx 

# CLEAN
# =======================================
rm create_lyx.py 
rm -f _pdf_file_list.txt
