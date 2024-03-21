from fim_resources import *


# task 1
# A function to compute the support count of an itemset
def support_count(dataset, itemset):
    count = 0
    for transaction in dataset:
        if itemset.issubset(transaction):
            count += 1
    return count


# Task 2
# A function which takes the candidates and returns the frequent and non-frequent  based on their support count
def get_frequent(dataset, candidates, threshold):
    non_frequent = []
    frequent = []
    for itemset in candidates:
        if (support_count(dataset, itemset) < threshold):
            non_frequent.append(itemset)
        else:
            frequent.append(itemset)

    return frequent, non_frequent


# This function returns the list of the items we need to start our enumeration(The first level of our enumeration)
def get_items(dataset):
    # We initialize the list to return
    result = []
    for transaction in dataset:
        for item in transaction:
            if (item not in result):
                result.append(item)
    # We sort our list
    result.sort()
    # We transform each item in a set of one item
    i = 0
    for item in result:
        result[i] = {item}
        i += 1
    return result

def generate_next_level(frequent, items):
    candidate_list = []
    for itemset in frequent:
        # this line allows me to go through the item and can possibly add to the itemset
        if ({(sorted(list(itemset)))[-1]} != items[-1]):
            for i in range(items.index({(sorted(list(itemset)))[-1]}) + 1, len(list(items))):
                candidate_list.append(itemset.union(items[i]))
    return candidate_list

def level_wise_enumeration(dataset, threshold):
    items = get_items(dataset)
    # A list of frequent itemset of the current level
    frequent, non_frequent = get_frequent(dataset, items, threshold)
    # A list of our levels
    frequent_itemset=frequent
    # print(items)
    while (len(frequent) != 0):
        candidate_list=generate_next_level(frequent,items)
        # We pruned candidates with downward closure
        pruned = []
        for candidate in candidate_list:
            for nf in non_frequent:
                if (nf.issubset(candidate)):
                    pruned.append(candidate)
                    break
        for itemset in pruned:
            candidate_list.remove(itemset)

        # Now we count the support
        frequent, non_frequent = get_frequent(dataset, candidate_list, threshold)
        non_frequent.extend(pruned)
        frequent_itemset.extend(frequent)
        #print(frequent_itemset_count)
    return frequent_itemset

# task 4
# I define a class for association rules
class Rule:
    def __init__(self, antecedent, consequent):
        self.antecedent = antecedent
        self.consequent = consequent

    # method to calculate the confidence of the rule
    def confidence(self, dataset):
        union=self.antecedent.union(self.consequent)
        confidence = support_count(dataset,union)/support_count(dataset,self.antecedent)
        return confidence

    # method to check if our rule is a strong association rule
    def is_strong(self, dataset, threshold):
        return self.confidence(dataset) >= threshold

    def toString(self,U):
        antecedant_list=list(self.antecedent)
        consequent_list=list(self.consequent)
        return f'({[U[i] for i in antecedant_list]})==>({[U[i] for i in consequent_list]})'

# A function which return all non-empty subsets of a given itemset
def non_empty_itemset(frequent):
    items = []
    non_empty_itemset = []
    for item in sorted(list(frequent)):
        items.append(set([item]))
    non_empty_itemset.extend(items)
    frequent = items
    while True:
        next_level = generate_next_level(frequent, items)
        if (len(non_empty_itemset[-1]) == len(items) - 1):
            break
        non_empty_itemset.extend(next_level)
        frequent = next_level
    return non_empty_itemset


# A function to generate the rules
def generate_rules(frequent):
    # for each non empty subset of this frequent itemset
    rules = []
    for subset in non_empty_itemset(frequent):
        # antecendent=subset , consequent =frequent-subset
        rule = Rule(subset,frequent - subset)
        rules.append(rule)
    return rules


def association_rules(dataset, frequent_itemset, conf_threshold):
    association_rules=[]
    for itemset in frequent_itemset:
        #We get all the rules with our function generate_rules()
        rules=[]
        if(len(itemset)>1):
            rules=generate_rules(itemset)
        #Now for each rule , we check if it is a strong association or not
        for rule in rules:
            if(rule.is_strong(dataset,conf_threshold)):
                association_rules.append(rule)
    return association_rules

# A function to run the tests
def run_test(dataset,threshold):
    which= dataset
    if which not in DATASETS:
        print("Unknown setup (%s)!" % which)
        exit()
    try:
        method_load =  eval("load_%s" % DATASETS[which]["format"])
    except AttributeError:
        raise Exception('No known method to load this data type (%)!' % DATASETS[which]["format"])
    tracts, U = method_load(DATASETS[which]["in_file"], **DATASETS[which].get("params", {}))
    tic = datetime.datetime.now()
    FI=level_wise_enumeration(tracts,threshold)
    tac = datetime.datetime.now()
    print("threshold= %d" %threshold)
    print("Found %d itemsets" %len(FI))
    print("Function running time: %s" % (tac-tic))
    print("The function took %s seconds to complete" % (tac-tic).total_seconds())
    print("*******************************************")
    return tracts,U,FI
# Task3 , test on Dataset
if __name__=="__main__":
    
    #Test on abalone dataset
    
    #With threshold = 500
    run_test("abalone",500)
    
    #With threshold = 250
    run_test("abalone",250)

    # Test on pizzas dataset 
    
    #threshold = 145
    run_test("pizzas",145)

    #threshold = 289
    run_test('pizzas',289)

    #Test on house dataset
    
    # With threshold=500
    run_test('house',260)

    #with threshold=200
    run_test('house',200)

    #Test on covtype dataset
    
    # With threshold=50
    run_test('plants',1500)

    #with threshold=200
    run_test('plants',2000)

    #Test of the association rule function 
    tracts,U,FI=run_test("pizzas",289)
    #print(FI)
    #print(tracts)
    #print(U)
    #Association rules for pizzas dataset 
    X=association_rules(tracts,FI,0.8)
    for rule in X:
        print(rule.toString(U))
    print("******************************")
    Y=association_rules(tracts,FI,0.5)
    for rule in Y:
        print(rule.toString(U))
    print("******************************")
    Z=association_rules(tracts,FI,0.7)
    for rule in Z:
        print(rule.toString(U))
    print("******************************")
    #Association rules for abalone dataset

    
    

    