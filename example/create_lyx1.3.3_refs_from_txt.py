#!/usr/bin/python3.6 

import re
import sys

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
    str_tmp = str_tmp.replace("è", "\n\\begin_inset ERT\nstatus Collapsed\n\n\\layout Standard\n{\n\\backslash\n`{e}}\n\\end_inset\n")
    str_tmp = str_tmp.replace("é", "\n\\begin_inset ERT\nstatus Collapsed\n\n\\layout Standard\n{\n\\backslash\n\'{e}}\n\\end_inset\n")
    str_tmp = str_tmp.replace("ì", "\n\\begin_inset ERT\nstatus Collapsed\n\n\\layout Standard\n{\n\\backslash\n\'{i}}\n\\end_inset\n")
    str_tmp = str_tmp.replace("í", "\n\\begin_inset ERT\nstatus Collapsed\n\n\\layout Standard\n{\n\\backslash\n`{i}}\n\\end_inset\n")
    str_tmp = str_tmp.replace("ò", "\n\\begin_inset ERT\nstatus Collapsed\n\n\\layout Standard\n{\n\\backslash\n\'{o}}\n\\end_inset\n")
    str_tmp = str_tmp.replace("ù", "\n\\begin_inset ERT\nstatus Collapsed\n\n\\layout Standard\n{\n\\backslash\n\'{u}}\n\\end_inset\n")
    #°
    return str_tmp

def simplify_naming(name):
    str_tmp = name.replace("à", "a")
    str_tmp = str_tmp.replace("è", "e")
    str_tmp = str_tmp.replace("é", "e")
    str_tmp = str_tmp.replace("ì", "i")
    str_tmp = str_tmp.replace("í", "i") 
    str_tmp = str_tmp.replace("ò", "o")
    str_tmp = str_tmp.replace("ù", "u")
    str_tmp = str_tmp.replace(" ", "")
    return str_tmp

def clean_ref(reference):
    str_tmp = reference.replace("–", "-")
    str_tmp1 = str_tmp.split("]")[1]  # remove number [1], [2], etc.
    str_tmp2 = str_tmp1.split("“")  # divide title from rest
    authors = str_tmp2[0]
    str_tmp3 = str_tmp2[1]
    str_tmp4 = str_tmp3.split("”")
    title = str_tmp4[0]
    str_tmp8  = str_tmp4[1].split(",")
    journal = str_tmp8[0]
    rest = str_tmp4[1].replace(journal, "")
    abbr_journal = abbreviate(journal, abbr_fname)
   
    # print("autors: ", authors)
    # print("title: ", title)
    # print("journal: ", journal)
    # print("abbr journal: ", abbr_journal)
    # print("rest: ", rest)

    # extract first author's surname
    str_tmp5 = authors.split(" ")
    author = ""
    for str_tmp in str_tmp5:
        if "." not in str_tmp and author == "":
            author = str_tmp.split(",")[0]
    # extract year
    year = str_tmp4[1].split(".")[-2].split(" ")[-1]
    # generate naming [Surname.YEAR]
    naming = "%s.%s" %(author, year)
    
    # make title lower case
    str_tmp6 = title.split(" ")
    lower_title = str_tmp6[0]
    
    for str_tmp in str_tmp6[1:-1]:
        lower = True
        file_lower_tabu = open(do_not_lower_fname, 'r')
        for line in file_lower_tabu:
            # print(line)
            if str_tmp in line:
                lower = False
        file_lower_tabu.close()
        if lower:
            lower_title += " %s" %str_tmp.lower()
        else:
            lower_title += " %s" %str_tmp

    to_ret  = "%s\n" %fix_accent(authors)
    to_ret += "\\begin_inset Quotes eld\n"
    to_ret += "\\end_inset\n"
    to_ret += "%s,\n" %fix_accent(lower_title)
    to_ret += "\\begin_inset Quotes erd\n"
    to_ret += "\\end_inset\n"
    to_ret += "\\emph on\n"
    to_ret += " %s\n" %abbr_journal
    to_ret += "\\emph default\n"
    to_ret += "%s\n" %rest
    return simplify_naming(naming), to_ret

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
        name, ref = clean_ref(line)
        print(name)
        file_out.write("\n\\layout Itemize\n\n")
        file_out.write("[%s] %s\n" %(name, ref))
        refs_for_biblio.append([name, ref])
# end references part

file_in.close()

# end document - do not modify 
for r in refs_for_biblio:
    name = r[0]
    file_out.write("\\layout Bibliography\n\n")
    file_out.write("\\bibitem {%s}\n" %name)
    file_out.write("%s\n" %r[1])
file_out.write("\\the_end\n")
# end document - do not modify 

file_out.close()
