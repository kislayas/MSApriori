#Authors: Kislaya Kumar Singh and Chinmay Gangal
# Email: ksingh38@uic.edu and cganga2@uic.edu

from __future__ import division

import itertools
import re
from collections import OrderedDict
from operator import itemgetter


def msApriori(infile, paramfile, outfile):
    #take input_file and parameter file and write frequent itemsets to output file
    transactions = dict()
    #list of lists of transactions
    T = list()
    with open("input/"+infile, "r") as i_file:
        for t in i_file:
            T.append([x for x in re.sub('[{}\n\r ]','',t).split(",")])
    num_of_trans = len(T)
    itemset=[]
    for item in T:
        itemset+=item
    itemset = [x for x in list(set(itemset))]
    #gather MIS values and other parameter values
    mis = dict()
    not_together = list()
    must_together = list()
    with open("parameter/"+paramfile, "r") as p_file:
        for line in p_file:
            line = re.sub('[ \r\n]','',line)
            if line[0:3]=="MIS":
                key = re.match(r"^.*\((.*)\).*$",line.split("=")[0]).group(1)
                if key in itemset:
                    value = float(line.split("=")[1])
                    mis[key] = value
                else:
                    #ignore if item does not exist in itemset
                    continue
            elif line[0:3]=="SDC":
                #sdc constant from input file
                sdc = float(line.split("=")[1])
            elif line.split(":")[0]=="cannot_be_together":
                is_can_not_have = True
                temp = re.sub('[{}]','',line.split(":")[1].replace("},{","#")).split("#")
                for t in temp:
                    not_together.append([x for x in t.split(",")])
            elif line.split(":")[0]=="must-have":
                must_together = [x for x in line.split(":")[1].split("or")]
            else:
                continue
    import operator
    
    #sort dictionary with mis values according to key
    M = OrderedDict(sorted(mis.items(), key=operator.itemgetter(1)))
    if sorted(itemset)!=sorted(M.keys()):
        return
    #to store item support
    item_sup = {}
    #to store item frequency/count
    item_freq = {}
    #finding L by pruning items with MIS less than minimum MIS
    #Also finding frequency of each item in T
    L, item_freq = init_pass(M, T, num_of_trans)
    import copy
    item_sup = copy.deepcopy(item_freq)
    item_sup.update((k, round(v * (1/int(num_of_trans)),4)) for k,v in item_sup.items())
    #start writing to output file
    with open("output/"+outfile, "w") as o_file:
        F = dict()
        #find,store and write o output file : F1 
        F[1] = list()
        o_file.write("Frequent 1-itemsets\n\n")
        #counter to count items satisfying constraints
        count_F1=0
        for item in M.keys():
            if item_sup[item]>=mis[item]:
                    temp_list = list()
                    temp_list.append(item)
                    F[1].append(temp_list)
                    #writing to output_file after pruning according to can_not_have and must_have
                    #if item in must_together: 
                    if not must_together or item in must_together:
                        count_F1+=1
                        o_file.write("\t"+str(item_freq[item])+" : {"+str(item)+"}\n")
        o_file.write("\n\tTotal number of frequent 1-itemsets = " + str(count_F1)+"\n\n\n")
        if F[1]==[]:
            return
        k = 2
        #store candidate in C
        C = dict()
        #loop till empty frequent itemset generates
        while True:
            C[k]=list()
            if k==2:
                #generate candidate for k=2
                C[k] = level2_candidate_gen(L, sdc, mis, item_sup) 
            else:
                #generate candidate for k>2
                C[k] = MScandidate_gen(F[k-1], mis, item_sup, sdc)
            if C[k]==[]:
                break

            #find and store count and tailcount of each element in candidate
            cand_count = dict()
            for c in C[k]:
                cand_count[hash(str(c))] = {}
                cand_count[hash(str(c))]["count"] = 0
                cand_count[hash(str(c))]["tailCount"] = 0
            for t in T:
                for c in C[k]:
                    #making the last twoelements of c as its count and tailcount respectively
                    if set(c).issubset(set(t)):
                        cand_count[hash(str(c))]["count"]+=1
                    if set(c[1:]).issubset(set(t)):
                        cand_count[hash(str(c))]["tailCount"]+=1
            F[k] = list()
            strPrint = ""
            strPrint = strPrint + "\nFrequent "+str(k)+"-itemsets\n"
            #o_file.write("\nFrequent "+str(k)+"-itemsets\n")
            #o_file.write(strPrint)
            count = 0
            for c in C[k]:
                if (cand_count[hash(str(c))]["count"]/num_of_trans)>=mis[c[0]]:
                    F[k].append(c)
                    if checkMustHave(must_together,c) and checkCantHave(not_together,c):
                        count+=1
                        strPrint = strPrint + "\n\t"+str(cand_count[hash(str(c))]["count"]) + " : {"+", ".join(map(str,c))+"}"
                        strPrint = strPrint + "\nTailcount = " + str(cand_count[hash(str(c))]["tailCount"])
            strPrint = strPrint + "\n\n\tTotal number of frequent " + str(k) + "-itemsets = " + str(count) + "\n\n"
            if count!=0:
                o_file.write(strPrint)
            if F[k]==[]:
                break
            k+=1
        o_file.write("....\n")

#to check must-have constraint
def checkMustHave(mustHaveList, candidate):
    if not mustHaveList:
        return True
    for m in mustHaveList:
        if m in candidate:
            return True
    return False

#to check cannot-be-together comstraint
def checkCantHave(cantHaveList, candidate):
    for ch in cantHaveList:
        if set(ch).issubset(candidate):
            return False
    return True

#Ck candidate generation for k>2
def MScandidate_gen(Fk,MIS,supps,sdc):
    #we sort each itemset-element of Fk for easy comparison while pruning
    import copy
    Ck = []
    combos = []
    combos.extend(itertools.combinations(Fk,2))
    for f1,f2 in combos:
        if f1[:-1]==f2[:-1]:
            c = []
            if abs(supps[f1[-1]] - supps[f2[-1]])<=sdc:
                c = f1[:-1]
                c.extend((f1[-1],f2[-1])) if f1[-1]<f2[-1] else c.extend((f2[-1],f1[-1]))
                Ck.append(c)
                for s in itertools.combinations(c,len(c)-1):
                    if (c[0] in s) or (MIS[c[1]]==MIS[c[0]]):
                        #convert tuple() s to list[]
                        #check if s is there in fk
                        if list(s) not in Fk: 
                            Ck.remove(c)
                            break #to avoid removing same c again
    return Ck            


#to generate candidate when k=2
def level2_candidate_gen(L,sdc,MIS,supps):
        C2 = []
        for el in L:
            if supps[el]>=MIS[el]:
                hIndex = L.index(el) +1
                while hIndex<len(L):
                    h = L[hIndex]
                    hIndex +=1
                    if supps[h]>=MIS[el] and abs(supps[h] - supps[el])<=sdc:
                        newEl = [el,h]
                        C2.append(newEl)
        return C2


#initial pass to generate L in algorithm and calcu;ate individual item-counts
def init_pass(M, T, n):
    item_freq = OrderedDict()
    min_mis = min(M.values())
    L = list()
    for item in M.keys():
        item_freq[item] = 0
        for t in T:
            if item in t:
                item_freq[item]+=1
    for item,count in item_freq.items():
        if count/n>=min_mis:
            L.append(item)
    return L, item_freq


#input
inFileName = raw_input("Please enter name of the input file (with .txt extension):\t")
paramFileName = raw_input("Please enter name of the parameter file (with .txt extension):\t")
outFileName = raw_input("Please enter name of output file to be generated (with .txt extension):\t")
msApriori(inFileName, paramFileName, outFileName)
