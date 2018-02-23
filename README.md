------------------------------------------------------------
Project Title
------------------------------------------------------------
MSApriori Algorithm Implementation to find frequent itemsets
This is generalization of famous Apriori algorithm. 
It is implemented when items have different Minimum Item Support(MIS)
It generates all frequent itemsets by making multiple passes over the data.

------------------------------------------------------------
Prerequisites
------------------------------------------------------------
1. Python 2.7

------------------------------------------------------------
Steps to run:
------------------------------------------------------------
1. run python file using 'msapriori.py'
2. it will ask for input file name. Give input file name and press enter
3. it will ask for parameter file name. Give parameter file name and press enter
4. it will ask for output file name. Give output file name and press enter
4. check the output in the output file


-----------------------------------------------------------
Locations
-----------------------------------------------------------
Input File Location: input/.
Parameter File Location: parameter/.
Output File Location: output/
-----------------------------------------------------------
-----------------------------------------------------------


------------------------------------------------------------
For example: 
------------------------------------------------------------
input file is- i3.txt,
i1.txt
------
{20, 30, 80, 70, 50, 90}
{20, 10, 80, 70}
{10, 20, 80}
{20, 30, 80}
{20, 80}
{20, 30, 80, 70, 50, 90, 100, 120, 140}

parameter file is - p3.txt
MIS(10) = 0.43
MIS(20) = 0.30
MIS(30) = 0.30
MIS(40) = 0.40
MIS(50) = 0.40
MIS(60) = 0.30
MIS(70) = 0.20
MIS(80) = 0.20
MIS(90) = 0.20
MIS(100) = 0.10
MIS(120) = 0.20
MIS(140) = 0.15
SDC = 0.1
cannot_be_together: {20, 40}, {70, 80}
must-have: 20 or 40 or 50

-----------------------------------------------
python msapriori.py 
Please enter name of the input file:i1.txt
Please enter name of the parameter file:p1.txt
-----------------------------------------------

open output file (output-patterns.txt) and check the output
output-patterns.txt
-------------------
Frequent 1-itemsets

    6 : {20}

    Total number of frequent 1-itemsets = 1



Frequent 2-itemsets

    6 : {80, 20}
Tailcount = 6
    2 : {90, 50}
Tailcount = 2

    Total number of frequent 2-itemsets = 2

....
------------------------------------------------------------
------------------------------------------------------------


------------------------------------------------------------
Authors
------------------------------------------------------------
1. Kislaya Kumar Singh - ksingh38@uic.edu
2. Chinmay Gangal - cganga2@uic.edu


------------------------------------------------------------
License
------------------------------------------------------------
Copyright: Kislaya and Chinmay 


------------------------------------------------------------
Course details
------------------------------------------------------------
This project is implemented as part of Course CS-583- Data Mining by Prof Bing Liu
