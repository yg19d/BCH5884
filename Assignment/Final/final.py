#!/usr/bin/python3
#https://github.com/yg19d/BCH5884/tree/master/Assignment/Final

import matplotlib
import pylab
import numpy as np
from Bio import SeqIO
from Bio import AlignIO
from Bio import Phylo
from Bio.Align.Applications import ClustalwCommandline

#The program first plots the quality scores of two fastq file, mutant_01 and mutant_02. 
#In the second part, the file MSA.fasta is read by the program and gives the multiple sequence alignment of the sequences present in that file. It will be saved as a clustal file at the end.
#It then forms a substituion matrix with the help of the alignment. It comes an an output on the terminal only.
#The alignment is also being used to draw a phylogenetic tree here.
#In the third part, a dot plot between the parent and one mutant has been plotted by the program.
#The last part consists of the code for html output. The images will be shown there. But in order to access the alignment, you would need to open the clustal file with notepad/word.


##### Plotting the quality scores of two mutant sequencing data #####
def quality_score(filename,limit=60):
    fastq_parser=SeqIO.parse(filename,"fastq")
    res=[]
    c=0
    for record in fastq_parser:
        score=record.letter_annotations["phred_quality"]
        res.append(score)
        c+=1
        if c>limit:
            break
        pylab.plot(score)

f1=quality_score("mutant_01.fastq")
f2=quality_score("mutant_02.fastq")
pylab.ylim(0, 65)
pylab.ylabel("PHRED quality score",color='purple')
pylab.xlabel("Position",color='salmon')
pylab.savefig("Quality Score.png")
pylab.close()

##### Multiple Sequence Alignment of the parent SirC and its mutants #####
cline=ClustalwCommandline("clustalw2.exe",infile="MSA.fasta")   #accesses the clustalw2 commandline and creates a .dnd file that is used while making a phylogenetic tree
stdout, stderr=cline()  #creates .aln clustal file which is the final product and can't be saved as an image.
align=AlignIO.read("MSA.aln","clustal") #Aligns the .aln clustal multiple sequence alignment


##### Calculating a substitution matrix from MSA #####
observed_frequencies=align.substitutions    #sustituions property of the alignment stores the number of times different residues substitute for each other
observed_frequencies=observed_frequencies.select("DEHKR")   #only polar side chains
observed_frequencies/=np.sum(observed_frequencies)   #normalizing the matrix
residue_frequencies=np.sum(observed_frequencies,0)   #summing over rows/columns to give the relative frequency of occurence of each residue
expected_frequencies=np.dot(residue_frequencies[:,None],residue_frequencies[None,:]) #expected frequencies of residue pairs
matrix=format(expected_frequencies,"%.3f")
#matrix=np.log2(observed_frequencies/expected_frequencies)    #calculating the log-odds matrix
print(matrix)


##### Make the phylogenetic tree #####
#The Evolution.dnd file that ClustalW has created is a standard Newick tree file that Bio.Phylo can parse
#draw function from matplotlib creates a graphic 
tree=Phylo.read("MSA.dnd","newick")
tree.rooted=True
tree.root.color="blue"
tree.clade[0].color="purple"
tree.clade[1].color="salmon"
tree.clade[2].color="green"
Phylo.draw(tree,branch_labels=lambda c:c.branch_length)



##### Making a dot plot of SirC and one of the mutants #####
with open("dot_plot.fasta") as in_handle:
    record_iterator=SeqIO.parse(in_handle,"fasta")
    SirC=next(record_iterator)
    mutant=next(record_iterator)
#create dictionaries which map the window-sized sub-sequences to locations
window = 7
dict_SirC = {}
dict_mutant = {}
for (seq, section_dict) in [
    (str(SirC.seq).upper(), dict_SirC),
    (str(mutant.seq).upper(), dict_mutant),
]:
    for i in range(len(seq) - window):
        section = seq[i : i + window]
        try:
            section_dict[section].append(i)
        except KeyError:
            section_dict[section] = [i]
# Now find any sub-sequences found in both sequences
matches = set(dict_SirC).intersection(dict_mutant)
print("%i unique matches found in the two sequences for the dot plot" % len(matches))
# Create lists of x and y co-ordinates for scatter plot
x = []
y = []
for section in matches:
    for i in dict_SirC[section]:
        for j in dict_mutant[section]:
            x.append(i)
            y.append(j)

pylab.cla()  # clear any prior graph
pylab.gray()
pylab.scatter(x, y)
pylab.xlim(0, len(SirC) - window)
pylab.ylim(0, len(mutant) - window)
pylab.xlabel("%s (length %i bp)" % (SirC.id, len(SirC)))
pylab.ylabel("%s (length %i bp)" % (mutant.id, len(mutant)))
pylab.title("Dot plot using window size %i\n(allowing no mis-matches)" % window)
pylab.savefig("dot plot.png")
pylab.close()

#### HTML output ####

def openHTML(f,title):
    f.write("""<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml">
    """)
    f.write("<head>\n")
    f.write("<title>%s</title>\n" % title)
    f.write("</head>\n")
    f.write("<body>\n")
    
def writeHTMLImage(f,title,imgpath):
    f.write('<p class="SeqAnalysis">%s</p>\n' % title)
    f.write('<img src="%s" />\n' % imgpath)

def closeHTML(f):
    f.write("</body>\n")
    f.write("</html>\n")
    f.close()

f=open("output.html",'w')
openHTML(f,"DNA and Protein Sequence Analysis")
writeHTMLImage(f,"Quality Score data of two mutants","Quality Score.png")
writeHTMLImage(f,"The Multiple Sequence Alignment file has been saved as a 'clustal' file by the name MSA.aln. Kindly open it with notepad/word to see the alignment. The phylo module of Biopython doesn't let the phylogenetic tree to be saved automatically as an image. The user has to save it manually and that is why a pre-saved image of the tree has been added here for the reader to know how it looks.","Tree.png")
writeHTMLImage(f,"Dot plot of a mutant with parent SirC","dot plot.png")
closeHTML(f)

