import json, random, sys, os

f = open('index.json')
pdic = json.load(f)
f.close()

num_words = len(pdic.keys())

# create a list of words in the cmudic
def create_words():
  words = open('words','w')
  for i in pdic:
    words.write(i + "\n")

# lookup the word in the cmudic
# assume word exists
def lookup(word):
  try:
    return pdic[word]
  except:
    print("Error: word in not in dict")
    sys.exit(0)

# get the pronuciation vector 
def get_phonetic_list(word):
  return lookup(word).split(" ")

# find n unique indicies from the range of words
def get_sample(n = 100):
  return random.sample(range(0,num_words),n)

# convert from list of indicies to list of words
def get_words(n):
  keys = list(pdic.keys())
  return [keys[i] for i in n]

# find n unique random pronuciation vectors
def generate_words(n = 100):
  if isinstance(n,list):
    return [get_phonetic_list(i) for i in n] 
  else:
    indices = get_sample(n) 
    return [get_phonetic_list(i) for i in get_words(indices)]

# the sound hueristic
def get_score(word1,word2,tar_len):
  count = 0;
  score = 0
  same_count = 0
  a = []
  for i,j in zip(word1,word2):
    #if sounds are exactly the same then max score
    if i == j:
      score = score + 2
      count = count + 1
      same_count = same_count + 1
    #if the sounds are basically the same, then half score
    #stress marks on vowels for are basically the same for simplicity
    elif i[0:2] == j[0:2]:
      score = score + 1
      count = count + 1
    #if the sounds are slantly the same, then quarter score
    a.append(same_count)
  final_score = score * (count * (1.0/tar_len))
  #final_score = score * (float(count)/float(len(word1)))
  #final_score = final_score * 100
  #final_score = float(final_score) * ((1.0 + 1.0/len(word1)))
  return score*count,count
  return int(final_score),count

'''
make a similarity score. Based on how alike two words sound like. 
return the score and meta data like where its most similar 
in a word: a bad tattoo is a ca-TAT-strophe, 
starting sounds: puns through pun-etics
ending sounds: a mad pirate is p-irate
also consider spelling verse pronuciantion
'''
def similar(word1, word2):
  #get target length
  tar_len = len(word1)
  # make word 2 the shorter of the two
  # just to make it simpler
  if len(word2) >= len(word1):
    word1,word2 = word2,word1

  scores = []
  max_score = 0
  sum_scores = 0
  # overlap the smaller one over the larger one
  word1_len = len(word1)
  word2_len = len(word2)
  proposed = []
  for pos in range(0,word1_len + word2_len - 1): 
    #find starting and ending indicies of each overlap
    start = 0 if pos - word2_len < 0 else pos - word2_len + 1
    end = pos+1 if pos - word1_len < 0 else word1_len
    start2 = word2_len - (pos + 1) if word2_len - (pos + 1) > 0 else 0
    end2 = word2_len - (pos - end + 1)
    score,count = get_score(word1[start:end],word2[start2:end2],tar_len)
    sum_scores += score
    if score > max_score:
      max_score == score
      if start2 > 0:
        proposed = word2 + word1[end2-start2:]
      elif end == word1_len:
        proposed = word1[:start]+word2
      else:
        if count < 0.5 * tar_len:
          score = int(score * 0.8)
        proposed = word1[:start] + word2 + word1[end:]
    if len(proposed) <= (word1_len * 1.5):
      scores.append((score,proposed))

  # hueristic for geting score is max scores of all subsets
  return sum_scores,proposed

def generate(target):
  phonetic_target = get_phonetic_list(target)
  try:
    words = get_words(get_sample(int(argv[1])))
  except:
    words = get_words(get_sample(num_words))
  scores = {}
  for i in words:
    if target not in i:
      score,proposed = similar(phonetic_target,get_phonetic_list(i))
      if score in scores:
        scores[score].append((i,proposed)) 
      else:
        scores[score] = [(i,proposed)]

  max_score = (list(scores.keys()))
  max_score.sort()
  max_score = max_score[-3:]
  max_score = max_score[::-1]
  words = []
  puns = []
  for ms in max_score:
    for tup in scores[ms]:
      words.append(tup[0])
      puns.append(tup[1])
  for word,pun in zip(words,puns):
    #print(word + "\t\t" + str(pun))
    #print(word)
    #print(str(pun))
    print(word + "\t" + str(pun))

def main(argv):
  if len(argv) > 0:
    if argv[0] in ('-t', 'test'):
      a = input("word: ")
      print(get_phonetic_list(a))
      b = input("index: ")
      print(generate_words(int(b)))
    elif argv[0] in ('-l','lookup'):
      for i in argv[1:]:
        print(get_phonetic_list(i))
      while(True):
        a = input("word: ")
        print(get_phonetic_list(a))
    elif argv[0] in ('-g','generate'):
      target = input("target: ")
      generate(target)
    elif argv[0] in ('-r','random'):
      word = get_words(get_sample(1))[0]
      print("target: " + word)
      generate(word)
  else:
    a = input("target: ")
    b = input("word: ")
    print(similar(get_phonetic_list(a),get_phonetic_list(b)))

if __name__ == "__main__":
  main(sys.argv[1:])
