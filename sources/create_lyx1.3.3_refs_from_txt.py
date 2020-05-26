#!/usr/bin/python3.6 

import re
import sys
from shutil import copyfile

class Reference:
    """
    Simple class for a reference
    """
    def __init__(self, reference_ieee_std):
        self.name, self.ref, self.tit, self.auth, self.year, self.bare_auth, self.bare_tit = clean_ref(reference_ieee_std)



# TODOs 
# - if journals not in list leave ref as is
# - check "comments"/ reply papers handling
# - complete strange letters list
# - better handle ACRONYMS
# - refactor and clean 

def print_lyx_header():
    header = "#LyX 1.3 created this file. For more info see http://www.lyx.org/\n"
    header += "\\lyxformat 221\n"
    header += "\\textclass article\n"
    header += "\\language english\n"
    header += "\\inputencoding auto\n"
    header += "\\fontscheme default\n"
    header += "\\graphics default\n"
    header += "\\paperfontsize default\n"
    header += "\\papersize Default\n"
    header += "\\paperpackage a4\n"
    header += "\\use_geometry 0\n"
    header += "\\use_amsmath 0\n"
    header += "\\use_natbib 0\n"
    header += "\\use_numerical_citations 0\n"
    header += "\\paperorientation portrait\n"
    header += "\\secnumdepth 3\n"
    header += "\\tocdepth 3\n"
    header += "\\paragraph_separation indent\n"
    header += "\\defskip medskip\n"
    header += "\\quotes_language english\n"
    header += "\\quotes_times 2\n"
    header += "\\papercolumns 1\n"
    header += "\\papersides 1\n"
    header += "\\paperpagestyle default\n"
    header += "\n"
    return header


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
    str_tmp = str_tmp.replace("ö", "\n\\begin_inset ERT\nstatus Collapsed\n\n\\layout Standard\n{\n\\backslash\n\"{o}}\n\\end_inset\n")
    str_tmp = str_tmp.replace("ù", "\n\\begin_inset ERT\nstatus Collapsed\n\n\\layout Standard\n{\n\\backslash\n\'{u}}\n\\end_inset\n")
    str_tmp = str_tmp.replace("ú", "\n\\begin_inset ERT\nstatus Collapsed\n\n\\layout Standard\n{\n\\backslash\n`{u}}\n\\end_inset\n")
    str_tmp = str_tmp.replace("ü", "\n\\begin_inset ERT\nstatus Collapsed\n\n\\layout Standard\n{\n\\backslash\n\"{u}}\n\\end_inset\n")
    str_tmp = str_tmp.replace("Ü", "\n\\begin_inset ERT\nstatus Collapsed\n\n\\layout Standard\n{\n\\backslash\n\"{U}}\n\\end_inset\n")
    str_tmp = str_tmp.replace("ğ", "\n\\begin_inset ERT\nstatus Collapsed\n\n\\layout Standard\n{\n\\backslash\nu {g}}\n\\end_inset\n")
    str_tmp = str_tmp.replace("ž", "\n\\begin_inset ERT\nstatus Collapsed\n\n\\layout Standard\n{\n\\backslash\nu {z}}\n\\end_inset\n")
    str_tmp = str_tmp.replace("š", "\n\\begin_inset ERT\nstatus Collapsed\n\n\\layout Standard\n{\n\\backslash\nu {s}}\n\\end_inset\n")
    str_tmp = str_tmp.replace("č", "\n\\begin_inset ERT\nstatus Collapsed\n\n\\layout Standard\n{\n\\backslash\nu {c}}\n\\end_inset\n")
    str_tmp = str_tmp.replace("ă", "\n\\begin_inset ERT\nstatus Collapsed\n\n\\layout Standard\n{\n\\backslash\nu {a}}\n\\end_inset\n")
    
    str_tmp = str_tmp.replace("ç", "\n\\begin_inset ERT\nstatus Collapsed\n\n\\layout Standard\n{\n\\backslash\nc {c}}\n\\end_inset\n")
    str_tmp = str_tmp.replace("Ç", "\n\\begin_inset ERT\nstatus Collapsed\n\n\\layout Standard\n{\n\\backslash\nc {C}}\n\\end_inset\n")
    str_tmp = str_tmp.replace("ı", "\n\\begin_inset ERT\nstatus Collapsed\n\n\\layout Standard\n{\n\\backslash\ni}\n\\end_inset\n")
    str_tmp = str_tmp.replace("’", "'")
    str_tmp = str_tmp.replace("×", "\n\\begin_inset Formula $\\times$\n\\end_inset\n")
    str_tmp = str_tmp.replace("°", "\n\\begin_inset Formula $^{\circ}$\n\\end_inset\n") 
    str_tmp = str_tmp.replace("ã", "\n\\begin_inset Formula $\\tilde{\\mbox{a}}$\n\\end_inset\n")
    str_tmp = str_tmp.replace("ñ", "\n\\begin_inset Formula $\\tilde{\\mbox{n}}$\n\\end_inset\n")
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
    str_tmp =    name.replace("à", "a")
    str_tmp = str_tmp.replace("á", "a")
    str_tmp = str_tmp.replace("ä", "a")
    str_tmp = str_tmp.replace("Ä", "a")
    str_tmp = str_tmp.replace("å", "a")
    str_tmp = str_tmp.replace("Å", "a") 	
    str_tmp = str_tmp.replace("ã", "a")
    str_tmp = str_tmp.replace("ă", "a")

    str_tmp = str_tmp.replace("è", "e")
    str_tmp = str_tmp.replace("é", "e")
    str_tmp = str_tmp.replace("ë", "e")
    str_tmp = str_tmp.replace("Ë", "E")

    str_tmp = str_tmp.replace("ì", "i")
    str_tmp = str_tmp.replace("í", "i") 
    str_tmp = str_tmp.replace("ï", "i")
    str_tmp = str_tmp.replace("ı", "i") 
    str_tmp = str_tmp.replace("Ï", "I")

    str_tmp = str_tmp.replace("ò", "o")
    str_tmp = str_tmp.replace("ó", "o")
    str_tmp = str_tmp.replace("ö", "o")
    str_tmp = str_tmp.replace("Ö", "O")
    str_tmp = str_tmp.replace("ø", "o")
    str_tmp = str_tmp.replace("Ø", "O")

    str_tmp = str_tmp.replace("ù", "u")
    str_tmp = str_tmp.replace("ú", "u")
    str_tmp = str_tmp.replace("ü", "u")
    str_tmp = str_tmp.replace("Ü", "u")

    str_tmp = str_tmp.replace("č", "c")
    str_tmp = str_tmp.replace("š", "s")
    str_tmp = str_tmp.replace("ž", "z")
    str_tmp = str_tmp.replace("ğ", "g")
    str_tmp = str_tmp.replace("Ÿ", "Y")
    str_tmp = str_tmp.replace("ÿ", "y")
    str_tmp = str_tmp.replace("Ç", "C")
    str_tmp = str_tmp.replace("ç", "c")
    str_tmp = str_tmp.replace("ñ", "n")

    str_tmp = str_tmp.replace(" ", "")
    str_tmp = str_tmp.replace("’", "")
    return str_tmp

def clean_ref(reference, save_refs_in_biblio=True):
    str_tmp1 = reference.split("]")[1:]  # remove number [1], [2], etc.
    new_tmp = ""
    for str_tmp in str_tmp1:
        new_tmp += str_tmp

    # if "“Reply to ‘Comments on “" in str_tmp1:
    #     flag_reply = True
    #     str_tmp2 = str_tmp1.split("“Reply to ‘Comments on “")  # divide title from rest
    #     authors = str_tmp2[0]
    #     str_tmp3 = str_tmp2[1]
    #     str_tmp4 = str_tmp3.split(",”’”")
    # else:
    flag_reply = False
    str_tmp2 = new_tmp.split("“")  # divide title from rest
    authors = str_tmp2[0]
    str_tmp3 = str_tmp2[1:]
    new_tmp = ""
    for str_tmp in str_tmp3:
        new_tmp += str_tmp
    str_tmp4 = new_tmp.split(",”")    
        
    # print(str_tmp4)
    bare_title = str_tmp4[0]
    title = bare_title.replace("–", "-").replace("—", "-")
    str_tmp8  = str_tmp4[1].split(",")
    journal = str_tmp8[0].replace("–", "-")
    rest = str_tmp4[1].replace("–", "-").replace("—", "-").replace(journal, "").split(", doi: ")[0]
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
    bare_author = ""
    finished = False
    for str_tmp in str_tmp5:
        if "." not in str_tmp and not finished:
            if bare_author == "":
                bare_author = str_tmp.split(",")[0]
            if "," in str_tmp or "and" == str_tmp:
                finished = True
            if "and" != str_tmp and 'et' != str_tmp:
                author += str_tmp.split(",")[0]

    # extract year
    year = str_tmp4[1].split(", doi: ")[0].split(" ")[-1]

    doi = str_tmp4[1].split(", doi: ")[1].upper()
    doi = doi[:-2]
    # generate naming [Surname.YEAR]
    naming = "%s.%s" %(simplify_naming(author), year)

    if naming in done_refs:
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm']
        counter = 0
        while "%s.%s" %(naming, letters[counter]) in done_refs:
            counter += 1
        # if counter == 1:
        #     done_refs[]
        naming = "%s.%s" %(naming, letters[counter])

    # if save_refs_in_biblio:
    done_refs.append(naming)
    
    # make title lower case
    str_tmp6 = title.split(" ")
    lower_tit = str_tmp6[0]
    lower_tit_divided = str_tmp6[0].split("-")
    lower_title = lower_tit_divided[0]
    for str_tmp in lower_tit_divided[1:]:
        lower = True
        file_lower_tabu = open(do_not_lower_fname, 'r')
        for line in file_lower_tabu:
            # print(line)
            if str_tmp in line:
                lower = False
        file_lower_tabu.close()
        if lower and not "$" in str_tmp:
            lower_title += "-%s" %str_tmp.lower()
        else:
            lower_title += "-%s" %str_tmp
    
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
        to_ret += "%s,\n" %fix_accent(fix_math(lower_title.replace("–", "-").replace("—", "-")))
        to_ret += "\\begin_inset Quotes erd\n"
        to_ret += "\\end_inset\n"
        to_ret += "'\n"
    else:
        to_ret += "%s,\n" %fix_accent(fix_math(lower_title.replace("–", "-").replace("—", "-")))
    
    to_ret += "\\begin_inset Quotes erd\n"
    to_ret += "\\end_inset\n"
    to_ret += "\\emph on\n"
    to_ret += " %s\n" %abbr_journal
    to_ret += "\\emph default\n"
    to_ret += "%s\n" %rest
    to_ret += " (DOI: %s).\n" %doi

    # if save_refs_in_biblio:
    years.add(int(year))
    wors_per_year[int(year)].append("[%s] %s\n" %(naming, to_ret))

    str_tmp10 = ""
    for str_tmp in bare_title.split('$'):
        if len(str_tmp) > len(str_tmp10):
            str_tmp10 = str_tmp

    return naming, to_ret, fix_accent(fix_math(lower_title.replace("–", "-").replace("—", "-"))), author, year, bare_author, str_tmp10


if __name__ == "__main__":
    # read input parameters
    input_fname = sys.argv[1]
    with open(input_fname) as file_in:
        lines = file_in.read().split("\n")
    txt_refs_fname     = lines[0]
    do_not_lower_fname = lines[1]
    abbr_fname         = lines[2]
    output_lyx_fname   = lines[3]
    rename_PDF         = lines[4] == '1'
    classif_fname      = lines[5]
    csv_export         = lines[6] == '1'
    # initialize arrays
    done_refs = []
    years = set()
    wors_per_year = {
        1950 : [],
        1951 : [],
        1952 : [],
        1953 : [],
        1954 : [],
        1955 : [],
        1956 : [],
        1957 : [],
        1958 : [],
        1959 : [],
        1960 : [],
        1961 : [],
        1962 : [],
        1963 : [],
        1964 : [],
        1965 : [],
        1966 : [],
        1967 : [],
        1968 : [],
        1969 : [],
        1970 : [],
        1971 : [],
        1972 : [],
        1973 : [],
        1974 : [],
        1975 : [],
        1976 : [],
        1977 : [],
        1978 : [],
        1979 : [],
        1980 : [],
        1980 : [],
        1980 : [],
        1980 : [],
        1980 : [],
        1980 : [],
        1980 : [],
        1980 : [],
        1981 : [],
        1982 : [],
        1983 : [],
        1984 : [],
        1985 : [],
        1986 : [],
        1987 : [],
        1988 : [],
        1989 : [],
        1990 : [],
        1991 : [],
        1992 : [],
        1993 : [],
        1994 : [],
        1995 : [],
        1996 : [],
        1997 : [],
        1998 : [],
        1999 : [],
        2000 : [],
        2001 : [],
        2002 : [],
        2003 : [],
        2004 : [],
        2005 : [],
        2006 : [],
        2007 : [],
        2008 : [],
        2009 : [],
        2010 : [],
        2011 : [],
        2012 : [],
        2013 : [],
        2014 : [],
        2015 : [],
        2016 : [],
        2017 : [],
        2018 : [],
        2019 : [],
        2020 : [],
        2021 : [],
        2022 : [],
        2023 : [],
        2024 : []}
    # PDF renaming part
    if rename_PDF:
        print("Renaming PDFs...")
        PDF_file_path = "_pdf_file_list.txt"
    else:
        print("NOT Renaming PDFs...")
    # information part
    print('Creating Biblio from:\n\t%s'          %txt_refs_fname)
    print('Keep Uppercase Word List from:\n\t%s' %do_not_lower_fname)
    print('Journal Abbreviations from:\n\t%s'    %abbr_fname)
    print('Creating Lyx file to:\n\t%s'          %output_lyx_fname)
    # file reading/writing part
    file_in = open(txt_refs_fname, 'r')
    file_out = open(output_lyx_fname, 'w')
    file_out.write(print_lyx_header())

    # start references part
    refs_for_biblio = []
    counter = 0
    for line in file_in:
        if '[' in line:
            reference = Reference(line) #name, ref, tit, auth, year, bare_auth, bare_tit = clean_ref(line)
            counter += 1
            print("[%d] %s" %(counter, reference.name))
            file_out.write("\n\\layout Itemize\n\n")
            file_out.write("[%s] %s\n" %(reference.name, reference.ref))
            refs_for_biblio.append(reference) #[name, ref, tit, auth, year, bare_auth, bare_tit])
    # end references part
    file_in.close()

    for y in sorted(years, reverse=True):
        if y:
            file_out.write("\n\\layout Subsubsection\n\n")
            file_out.write("Year %d\n" %y)
            
            for item in wors_per_year[y]:
                file_out.write("\n\\layout Itemize\n\n")
                file_out.write("%s\n" %item)

    if classif_fname != '':
        print("adding classification")
        with open(classif_fname) as file_cls:
            lines = file_cls.read().split("\n")
        for line in lines:
            if "#" in line:
                file_out.write("\n\\layout Subsection\n\n")
                file_out.write("%s\n" %line.replace("#",""))
            else:
                if '[' in line:
                    # sarch in refs_for_biblio
                    name_found=""
                    ref_found=""
                    found=False
                    for work in refs_for_biblio:
                        name =  work.name
                        title = work.bare_title
                        auth =  work.bare_auth
                        year =  work.year
                        if auth in line and year in line and title in line:
                            found = True
                            name_found = name
                            ref_found = work.ref
                    # name, ref, tit, auth, year, bare_auth, bare_tit = clean_ref(line, False)
                    # print(name)
                    if found:
                        file_out.write("\n\\layout Itemize\n\n")
                        file_out.write("[%s] %s\n" %(name_found, ref_found))
                    else:
                        print("WORK %s NOT FOUND" %line)
    else:
        print("no classification selected")

    # end document - do not modify 
    done_copy = []
    for r in refs_for_biblio:
        name =  r.name
        title = r.bare_tit
        auth =  r.bare_auth
        year =  r.year
        file_out.write("\\layout Bibliography\n\n")
        file_out.write("\\bibitem {%s}\n" %name)
        file_out.write("%s\n" %r.ref)
        # print("%s" %(title))
        # print("%s" %(r[2]))
        if rename_PDF:
            file_pdfs = open("_pdf_file_list.txt", 'r')
            found = False
            # print("Looking for PDF")
            for line in file_pdfs:
                path = line.replace(" ", " ")
                path = path[:-1]
                if title[:10] in line and auth in line and year in line:
                    found = True
                    copyfile('%s' %path, './Renamed-PDFs/%s.pdf' %name)
                    done_copy.append(name)

            file_pdfs.close()
            if not found:
                print("\tPDF file %s NOT FOUND\n" %name)
            else:
                print("\tOK! PDF file %s FOUND\n" %name)
    file_out.write("\\the_end\n")
    # end document - do not modify 

    file_out.close()
