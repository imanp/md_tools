import re

# str = """[ molecules ]
# ; Compound        #mols
# Protein_chain_A     1
# Protein_chain_B     1
# Protein_chain_C     1
# Protein_chain_D     1
# Protein_chain_E     1
# SOL  123
# NA	      234
# CL	        234
# """
#
#
# # w= re.compile(r"(SOL|NA|CL)\s+ \d+")
# w= re.compile('(SOL\s+)\d+')
# print w.search(str)
#
# new =  w.sub("",str)
# print new


str ="""START
ATOM      1  N   VAL A   5      64.124  68.669 128.967  1.00  0.00           N
ATOM      2  H1  VAL A   5      63.345  68.938 129.534  1.00  0.00
ATOM      3  H2  VAL A   5      63.796  68.176 128.162  1.00  0.00
ATOM      4  H3  VAL A   5      64.733  68.078 129.496  1.00  0.00
ATOM      5  CA  VAL A   5      64.853  69.866 128.543  1.00  0.00           C
ATOM      6  HA  VAL A   5      65.178  70.210 129.424  1.00  0.00
ATOM      7  CB  VAL A   5      66.093  69.575 127.651  1.00  0.00           C
ATOM      8  HB  VAL A   5      66.414  70.444 127.274  1.00  0.00
ATOM      9  CG1 VAL A   5      67.240  68.992 128.466  1.00  0.00           C
ATOM     10 1HG1 VAL A   5      68.020  68.817 127.865  1.00  0.00
ATOM     11 2HG1 VAL A   5      67.507  69.642 129.178  1.00  0.00
ATOM     12 3HG1 VAL A   5      66.946  68.136 128.890  1.00  0.00
ATOM     13  CG2 VAL A   5      65.745  68.679 126.460  1.00  0.00           C
ATOM     14 1HG2 VAL A   5      66.566  68.517 125.914  1.00  0.00
ATOM     15 2HG2 VAL A   5      65.389  67.807 126.793  1.00  0.00
ATOM     16 3HG2 VAL A   5      65.052  69.129 125.896  1.00  0.00
ATOM     17  C   VAL A   5      63.945  70.931 127.933  1.00  0.00           C
ATOM     18  O   VAL A   5      62.971  70.605 127.254  1.00  0.00           O
ATOM     19  N   SER A   6      64.280  72.204 128.177  1.00  0.00           N
ATOM     20  H   SER A   6      65.090  72.370 128.739  1.00  0.00
ATOM     21  CA  SER A   6      63.548  73.369 127.684  1.00  0.00           C
ATOM     22  HA  SER A   6      62.912  73.037 126.987  1.00  0.00
ATOM     23  CB  SER A   6      62.747  74.006 128.817  1.00  0.00           C
ATOM     24  HB1 SER A   6      62.106  73.343 129.204  1.00  0.00
ATOM     25  HB2 SER A   6      62.243  74.802 128.482  1.00  0.00
ATOM     26  OG  SER A   6      63.580  74.450 129.874  1.00  0.00           O
ATOM     27  HG  SER A   6      63.018  74.859 130.592  1.00  0.00
ATOM     28  C   SER A   6      64.539  74.379 127.064  1.00  0.00           C
ATOM     29  O   SER A   6      65.732  74.301 127.370  1.00  0.00           O
ATOM     30  N   PRO A   7      64.098  75.313 126.183  1.00  0.00           N
END"""



w = re.compile("^ATOM.*",re.MULTILINE)

print "\n".join(w.findall(str))

# print m.group()


