#!/usr/bin/python3.6 

import re
import sys
from shutil import copyfile

# TODOs 
# - check multiple namings
# - rename files flag

input_fname = sys.argv[1]
with open(input_fname) as file_in:
    lines = file_in.read().split("\n")
txt_refs_fname     = lines[0]
do_not_lower_fname = lines[1]
abbr_fname         = lines[2]
output_lyx_fname   = lines[3]

rename_PDF = lines[4] == '1'

done_refs = []

if rename_PDF:
    print("Renaming PDFs...")
    PDF_file_path = "_pdf_file_list.txt"
else:
    print("NOT Renaming PDFs...")

print('Creating Biblio from:\n\t%s'          %txt_refs_fname)
print('Keep Uppercase Word List from:\n\t%s' %do_not_lower_fname)
print('Journal Abbreviations from:\n\t%s'    %abbr_fname)
print('Creating Lyx file to:\n\t%s'          %output_lyx_fname)

# function definition
def abbreviate(journal, abbr_file):
    file_abbr = open(abbr_file, 'r')
    for line in file_abbr:
        tmp = line.split(" | ")
        extended_name = tmp[0].replace(" ", "")
        abbr_name = tmp[1]
        # print(journal, extended_name, abbr_name)
        if journal.replace(" ", "") == extended_name:
            file_abbr.close()
            return abbr_name

def fix_accent(name):
    str_tmp = name.replace("à", "\n\\begin_inset ERT\nstatus Collapsed\n\n\\layout Standard\n{\n\\backslash\n\'{a}}\n\\end_inset\n")
    str_tmp = name.replace("á", "\n\\begin_inset ERT\nstatus Collapsed\n\n\\layout Standard\n{\n\\backslash\n`{a}}\n\\end_inset\n")
    str_tmp = str_tmp.replace("è", "\n\\begin_inset ERT\nstatus Collapsed\n\n\\layout Standard\n{\n\\backslash\n`{e}}\n\\end_inset\n")
    str_tmp = str_tmp.replace("é", "\n\\begin_inset ERT\nstatus Collapsed\n\n\\layout Standard\n{\n\\backslash\n\'{e}}\n\\end_inset\n")
    str_tmp = str_tmp.replace("ì", "\n\\begin_inset ERT\nstatus Collapsed\n\n\\layout Standard\n{\n\\backslash\n\'{i}}\n\\end_inset\n")
    str_tmp = str_tmp.replace("í", "\n\\begin_inset ERT\nstatus Collapsed\n\n\\layout Standard\n{\n\\backslash\n`{i}}\n\\end_inset\n")
    str_tmp = str_tmp.replace("ò", "\n\\begin_inset ERT\nstatus Collapsed\n\n\\layout Standard\n{\n\\backslash\n\'{o}}\n\\end_inset\n")
    str_tmp = str_tmp.replace("ó", "\n\\begin_inset ERT\nstatus Collapsed\n\n\\layout Standard\n{\n\\backslash\n`{o}}\n\\end_inset\n")
    str_tmp = str_tmp.replace("ù", "\n\\begin_inset ERT\nstatus Collapsed\n\n\\layout Standard\n{\n\\backslash\n\'{u}}\n\\end_inset\n")
    str_tmp = str_tmp.replace("ú", "\n\\begin_inset ERT\nstatus Collapsed\n\n\\layout Standard\n{\n\\backslash\n`{u}}\n\\end_inset\n")
    str_tmp = str_tmp.replace("ü", "\n\\begin_inset ERT\nstatus Collapsed\n\n\\layout Standard\n{\n\\backslash\n\"{u}}\n\\end_inset\n")
    str_tmp = str_tmp.replace("Ü", "\n\\begin_inset ERT\nstatus Collapsed\n\n\\layout Standard\n{\n\\backslash\n\"{U}}\n\\end_inset\n")
    str_tmp = str_tmp.replace("ğ", "\n\\begin_inset ERT\nstatus Collapsed\n\n\\layout Standard\n{\n\\backslash\nu {g}}\n\\end_inset\n")
    str_tmp = str_tmp.replace("ı", "\n\\begin_inset ERT\nstatus Collapsed\n\n\\layout Standard\n{\n\\backslash\ni}\n\\end_inset\n")
    str_tmp = str_tmp.replace("’", "'")
    str_tmp = str_tmp.replace("×", "\n\\begin_inset Formula $\\times$\n\\end_inset\n")
    str_tmp = str_tmp.replace("°", "\n\\begin_inset Formula $^{\circ}$\n\\end_inset\n") 
    return str_tmp

def fix_math(name):
    if "$" in name:
        content = re.search(r"\$.*\$", name).group(0).replace("$","")
        str_tmp = re.sub(r"\$.*\$", '__PLACEHOLDER__', name)
        str_tmp = str_tmp.replace("__PLACEHOLDER__", "\n\\begin_inset Formula\n$%s$\n\\end_inset\n" %content)
        return str_tmp
    else:
        return name

def simplify_naming(name):
    str_tmp = name.replace("à", "a")
    str_tmp = str_tmp.replace("á", "a")
    str_tmp = str_tmp.replace("è", "e")
    str_tmp = str_tmp.replace("é", "e")
    str_tmp = str_tmp.replace("ì", "i")
    str_tmp = str_tmp.replace("í", "i") 
    str_tmp = str_tmp.replace("ı", "i") 
    str_tmp = str_tmp.replace("ò", "o")
    str_tmp = str_tmp.replace("ó", "o")
    str_tmp = str_tmp.replace("ù", "u")
    str_tmp = str_tmp.replace("ú", "u")
    str_tmp = str_tmp.replace("ü", "u")
    str_tmp = str_tmp.replace("Ü", "u")
    str_tmp = str_tmp.replace("ğ", "g")
    
    str_tmp = str_tmp.replace(" ", "")
    str_tmp = str_tmp.replace("’", "")
    return str_tmp

def clean_ref(reference):
    str_tmp1 = reference.split("]")[1]  # remove number [1], [2], etc.

    if "“Reply to ‘Comments on “" in str_tmp1:
        flag_reply = True
        str_tmp2 = str_tmp1.split("“Reply to ‘Comments on “")  # divide title from rest
        authors = str_tmp2[0]
        str_tmp3 = str_tmp2[1]
        str_tmp4 = str_tmp3.split(",”’”")
    else:
        flag_reply = False
        str_tmp2 = str_tmp1.split("“")  # divide title from rest
        authors = str_tmp2[0]
        str_tmp3 = str_tmp2[1]
        str_tmp4 = str_tmp3.split(",”")  
        
    bare_title = str_tmp4[0]
    title = bare_title.replace("–", "-")
    str_tmp8  = str_tmp4[1].split(",")
    journal = str_tmp8[0]
    rest = str_tmp4[1].replace(journal, "").split(", doi: ")[0]
    abbr_journal = abbreviate(journal, abbr_fname)
   
    # print(reference)
    # print("\tautors: ", authors)
    # print("\ttitle: ", title)
    # print("\tjournal: ", journal)
    # print("\tabbr journal: ", abbr_journal)
    # print("\trest: ", rest)

    # extract first author's surname
    str_tmp5 = authors.split(" ")
    author = ""
    for str_tmp in str_tmp5:
        if "." not in str_tmp and author == "":
            author = str_tmp.split(",")[0]

    # Dec. 2018, doi: 10.1109/TAP.2018.2871752.

    # extract year
    year = str_tmp4[1].split(", doi: ")[0].split(" ")[-1]
    doi = str_tmp4[1].split(", doi: ")[1].upper()
    doi = doi[:-2]
    # generate naming [Surname.YEAR]
    naming = "%s.%s" %(simplify_naming(author), year)

    if naming in done_refs:
        letters = ['b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm']
        counter = 0
        while "%s.%s" %(naming, letters[counter]) in done_refs:
            counter += 1
        naming = "%s.%s" %(naming, letters[counter])

    done_refs.append(naming)
    
    # make title lower case
    str_tmp6 = title.split(" ")
    lower_title = str_tmp6[0]
    
    for str_tmp in str_tmp6[1:]:
        lower = True
        file_lower_tabu = open(do_not_lower_fname, 'r')
        for line in file_lower_tabu:
            # print(line)
            if str_tmp in line:
                lower = False
        file_lower_tabu.close()
        if lower and not "$" in str_tmp:
            lower_title += " %s" %str_tmp.lower()
        else:
            lower_title += " %s" %str_tmp

    to_ret  = "%s\n" %fix_accent(authors)
    to_ret += "\\begin_inset Quotes eld\n"
    to_ret += "\\end_inset\n"

    if flag_reply:
        to_ret += "Reply to 'Comments on \n"
        to_ret += "\\begin_inset Quotes eld\n"
        to_ret += "\\end_inset\n"
        to_ret += "%s,\n" %fix_accent(fix_math(lower_title))
        to_ret += "\\begin_inset Quotes erd\n"
        to_ret += "\\end_inset\n"
        to_ret += "'\n"
    else:
        to_ret += "%s,\n" %fix_accent(fix_math(lower_title))
    
    to_ret += "\\begin_inset Quotes erd\n"
    to_ret += "\\end_inset\n"
    to_ret += "\\emph on\n"
    to_ret += " %s\n" %abbr_journal
    to_ret += "\\emph default\n"
    to_ret += "%s\n" %rest
    to_ret += " (DOI: %s).\n" %doi
    return naming, to_ret, title, author, year

# processing part
file_in = open(txt_refs_fname, 'r')
file_out = open(output_lyx_fname, 'w')

# start header - do not modify
file_out.write("#LyX 1.3 created this file. For more info see http://www.lyx.org/\n")
file_out.write("\\lyxformat 221\n")
file_out.write("\\textclass article\n")
file_out.write("\\language english\n")
file_out.write("\\inputencoding auto\n")
file_out.write("\\fontscheme default\n")
file_out.write("\\graphics default\n")
file_out.write("\\paperfontsize default\n")
file_out.write("\\papersize Default\n")
file_out.write("\\paperpackage a4\n")
file_out.write("\\use_geometry 0\n")
file_out.write("\\use_amsmath 0\n")
file_out.write("\\use_natbib 0\n")
file_out.write("\\use_numerical_citations 0\n")
file_out.write("\\paperorientation portrait\n")
file_out.write("\\secnumdepth 3\n")
file_out.write("\\tocdepth 3\n")
file_out.write("\\paragraph_separation indent\n")
file_out.write("\\defskip medskip\n")
file_out.write("\\quotes_language english\n")
file_out.write("\\quotes_times 2\n")
file_out.write("\\papercolumns 1\n")
file_out.write("\\papersides 1\n")
file_out.write("\\paperpagestyle default\n")
file_out.write("\n")
# end header - do not modify

# start references part
refs_for_biblio = []
for line in file_in:
    if '[' in line:
        name, ref, tit, auth, year = clean_ref(line)
        print(name)
        file_out.write("\n\\layout Itemize\n\n")
        file_out.write("[%s] %s\n" %(name, ref))
        refs_for_biblio.append([name, ref, tit, auth, year])
# end references part

file_in.close()

# end document - do not modify 
done_copy = []
for r in refs_for_biblio:
    name = r[0]
    title = r[2]
    auth = r[3]
    year = r[4]
    file_out.write("\\layout Bibliography\n\n")
    file_out.write("\\bibitem {%s}\n" %name)
    file_out.write("%s\n" %r[1])
    if rename_PDF:
        file_pdfs = open("_pdf_file_list.txt", 'r')
        found = False
        for line in file_pdfs:
            path = line.replace(" ", " ")
            path = path[:-1]
            print(line)
            print(title)
            if title[:10] in line and auth in line and year in line:
                found = True
                copyfile('%s' %path, './Renamed-PDFs/%s.pdf' %name)
                done_copy.append(name)

        file_pdfs.close()
        print("File %s NOT FOUND" %name)
file_out.write("\\the_end\n")
# end document - do not modify 

file_out.close()
