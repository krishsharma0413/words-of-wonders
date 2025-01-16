from itertools import permutations

class Brain:
    def __init__(self, words:str = "./data/brain.txt"):
        self.words = set()
        with open(f"{words}", "r") as file:
            for lines in file.readlines():
                self.words.add(lines.strip())

   
    def predict(self, letters, limit=None):
        permute = []
        if limit == None:
            for x in range(3, len(letters)+1):
                permute.extend(list(permutations(letters, x)))
        else:
            permute.extend(list(permutations(letters, limit)))
        permute = list(map(lambda x: "".join(x), permute))
        permute = set(permute)
        result = permute.intersection(self.words)
        result = list(result)
        return result
    
    def newbrain(self):
        awords = []
        for x in self.words:
            if len(x) > 2 and "-" not in x and "'" not in x and " " not in x:
                awords.append(x)
                
        with open("./data/brain.txt", "w") as file:
            for x in awords:
                file.write(f"{x}\n")
    