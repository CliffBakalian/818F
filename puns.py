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
def get_score(word1,word2):
  count = 0;
  score = 0
  for i,j in zip(word1,word2):
    #if sounds are exactly the same then max score
    if i == j:
      score = score + 2
      count = count + 1
    #if the sounds are basically the same, then half score
    #stress marks on vowels for are basically the same for simplicity
    elif i[0:2] == j[0:2]:
      score = score + 1
      count = count + 1
    #if the sounds are slantly the same, then quarter score

  return score * count

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
  if len(word2) > len(word1):
    word1,word2 = word2,word1

  scores = []

  # overlap the smaller one over the larger one
  word1_len = len(word1)
  word2_len = len(word2)
  for pos in range(0,word1_len + word2_len - 1): 
    #find starting and ending indicies of each overlap
    start = 0 if pos - word2_len < 0 else pos - word2_len + 1
    end = pos+1 if pos - word1_len < 0 else word1_len
    start2 = word2_len - (pos + 1) if word2_len - (pos + 1) > 0 else 0
    end2 = word2_len - (pos - end + 1)
    score = get_score(word1[start:end],word2[start2:])
    scores.append(score);

  # hueristic for geting score is max scores of all subsets
  return sum(scores)

def filter_set():
  '''
  using the simlarity score along with other metadata like word length, 
  percentage of overlap sounds, etc, 
  try to figure out to choose good puns from sets
  '''
  return 1

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
      phonetic_target = get_phonetic_list(target)
      try:
        words = get_words(get_sample(int(argv[1])))
      except:
        words = get_words(get_sample(num_words))
      out = open('generate.txt','w')
      scores = {}
      for i in words:
        out.write(i + '\n')
        score = similar(phonetic_target,get_phonetic_list(i))
        if score in scores:
          scores[score].append(i) 
        else:
          scores[score] = [i]
      out.close()

      max_score = (list(scores.keys()))
      max_score.sort()
      max_score = max_score[-7:]
      max_score = max_score[::-1]
      words = []
      for ms in max_score:
        words = words + scores[ms]
      for word in words:
        print(word)
  else:
    a = input("target: ")
    b = input("word: ")
    print(similar(get_phonetic_list(a),get_phonetic_list(b)))

if __name__ == "__main__":
  main(sys.argv[1:])
