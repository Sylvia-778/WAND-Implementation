from collections import defaultdict


def getMax(inverted_index):
    w = 0
    for i in inverted_index:
        if i[1] > w:
            w = i[1]
    return w


def nextPosting(num, term, docid, posting_dict, inverted_index):
    posting = set()
    for i in inverted_index[term]:
        if i[0] > docid:
            posting = i
            break
    if posting:
        posting_dict[num] = posting
    else:
        posting_dict.pop(num)
    return posting_dict


def delete_smallest(Ans):
    Ans = sorted(Ans, key=lambda x: x[0], reverse=True)
    # print(Ans)
    score_min = Ans[-1][0]
    docid = 0     # find the maximum docid with smallest score
    index_pop = -1
    for (index, ans) in enumerate(Ans):
        if ans[0] == score_min and ans[1] > docid:
            docid = ans[1]
            index_pop = index
    if index_pop != -1:
        Ans.pop(index_pop)
    threshold = Ans[-1][0]
    return Ans, threshold


def seek_to_document(num, term, docid, posting_dict, inverted_index):
    posting = set()
    for i in inverted_index[term]:
        if i[0] >= docid:
            posting = i
            break
    if posting:
        posting_dict[num] = posting
    else:
        posting_dict.pop(num)
    return posting_dict


def WAND_Algo(query_terms, top_k, inverted_index):
    U = defaultdict(int)
    posting_dict = defaultdict(set)
    for t in range(len(query_terms)):
        U[t] = getMax(inverted_index[query_terms[t]])
        posting_dict[t] = inverted_index[query_terms[t]][0]
    # print(U)
    # print(first_posting)
    # current threshold
    threshold = 0
    # k-set of (d, s) values
    Ans = []
    count = 0
    while posting_dict:
        permuted_posting_list = sorted(posting_dict.items(), key=lambda x:x[1][0])
        permuted_t = [i[0] for i in permuted_posting_list]
        candidates = [i[1] for i in permuted_posting_list]
        score_limit = 0
        pivot = 0
        while pivot < len(candidates):
            tmp_score_limit = score_limit + U[permuted_t[pivot]]
            if tmp_score_limit > threshold:
                break
            score_limit = tmp_score_limit
            pivot += 1
        if pivot == len(candidates):
            break
        if candidates[0][0] == candidates[pivot][0]:
            count += 1
            s = 0
            t = 0
            while t < len(candidates) and candidates[t][0] == candidates[pivot][0]:
                s += candidates[t][1]
                posting_dict = nextPosting(permuted_t[t], query_terms[permuted_t[t]], candidates[t][0], posting_dict, inverted_index)
                # print(posting_dict)
                t += 1
            # print(posting_dict)
            # print(s)
            if s > threshold:
                Ans.append((s, candidates[pivot][0]))
                if len(Ans) > top_k:
                    Ans, threshold = delete_smallest(Ans)
        else:
            for t in range(0, pivot):
                posting_dict = seek_to_document(permuted_t[t], query_terms[permuted_t[t]], candidates[pivot][0], posting_dict, inverted_index)
        Ans = sorted(Ans, key=lambda x: x[1])
        Ans = sorted(Ans, key=lambda x: x[0], reverse=True)
    return Ans, count
