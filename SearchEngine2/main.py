# Storing all word that have to be ignored in a set
def IgnoreWord():
    f = open("english.txt",encoding="utf8")
    read = f.readlines()
    temp_list = []
    for line in read:
        temp_list.append(line.strip())
    f.close()

    ignored_word_set = set()

    for x in temp_list:
        if x not in ignored_word_set:
            ignored_word_set.add(x)
    return ignored_word_set

# removepuc will remove all the punctuation from the word and also lower case it
def RemovePunc(word):
    new_word = ""
    word = word.lower()
    for letter in word:
        if letter.isalnum():
            new_word += letter
    return new_word

# now we will loop through all article and it will store article name as key and a dict as value 
# in that inside dict individual word will be stored as key and a list of its all indexes as value
# like main_dict = {"k1" : {"katrina" : [1,3,4],"salmon":[2]}}
# in the nested dict there is a "article-title" key which will store all the title word of that particular article
# like main_dict = {"k1" : {"katrina" : [1,3,4],"salmon":[2],"article-title":["katrina","kaif"]}}
def PreProcessing():
    main_dict = {}
    for x in range(1,51):
        current_article = "k" + str(x)
        f = open("news_k50/"+current_article+".txt",encoding="utf-8")
        i = 0
        word_index = 1
        read = f.readlines()
        for line in read:
            for word in line.split():
                word = RemovePunc(word)
                if word not in ignored_word_set: 
                    if current_article not in main_dict:
                        main_dict[current_article] = {word : [word_index]}
                    else:
                        if word in main_dict[current_article]:
                            main_dict[current_article][word] += [word_index]
                        else:
                            main_dict[current_article][word] = [word_index]
                    # i is use to check if the word is in title or not
                    if i == 0:
                        if "article-title" not in main_dict[current_article]:
                            main_dict[current_article]["article-title"] = [word]
                        else:
                            main_dict[current_article]["article-title"] += [word]
                word_index += 1
            i += 1
        f.close()
    return main_dict
    # ranking rules that this program follows is
    # more query word matches in the article and after that it follows
    # second rule the more queryword matched in the title
    # and third rule which is the sum of all frequecy of query words
    # fourth rule is word that occur in starting of the document(article)
def main():
    main_dict = PreProcessing()
    while True:
        user_input = input("Enter your word:- ")
        user_input = user_input.split()
        inputed_word_list = []
        # removing all the word that has to be ignored and also punctuations
        for word in user_input:
            if word not in ignored_word_set:
                inputed_word_list.append(RemovePunc(word))
        temp_dict = {}
        # queryword means the no. of words that matches with inputed words and words in a particular article
        # title means the no. of inputed words thats in the title of an article
        # freq means the frequecy of all inputed words in a particular article
        # first_occ means the sum of all indexes of all inputed words in a particular article

        for current_article in main_dict:
            temp_dict[current_article] = [0,0,0,float("inf")]
                                       # [queryword,title,freq,first_occ]
            for word in inputed_word_list:
                if word in main_dict[current_article]:
                    # queryword
                    temp_dict[current_article][0] += 1
                    # title
                    if word in main_dict[current_article]["article-title"]:
                        temp_dict[current_article][1] += 1
                    # freq
                    temp_dict[current_article][2] += len(main_dict[current_article][word])
                    # occurr
                    if temp_dict[current_article][3] == float("inf"):
                        temp_dict[current_article][3] = main_dict[current_article][word][0]
                    else:
                        temp_dict[current_article][3] += main_dict[current_article][word][0]
            if temp_dict[current_article] == [0,0,0,float("inf")]:
                del temp_dict[current_article]

        #sorting queryword,title, freq in decreasing order and first_occ by increasing order
        temp_list = sorted(temp_dict.keys(),key=lambda x: (temp_dict[x][0],temp_dict[x][1],temp_dict[x][2],-temp_dict[x][3]), reverse=True)

        #removing the k part and printing only the no. of articles
        final_list = []
        for x in temp_list[:5]:
            final_list.append(x[1:])
    
        print("Articles related to your query are:- ")
        print(final_list)
        print()
        
ignored_word_set = IgnoreWord()
main()