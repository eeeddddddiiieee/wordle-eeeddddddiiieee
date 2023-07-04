#!/usr/bin/env python3
from matplotlib import pyplot as plt

from wordle import *
from random import randint
from information import *


class Solver(Player):
    """
    The Solver Class Defines the Wordle Solver.
    Your task is to fill in this class to automatically play the game.
    """

    def __init__(self):
        """Initialize the solver.

        At the very least, your solver should maintain the number of guesses for
        cooperation with the evaluation script

        """
        self.num_guesses = 0
        self.wordlist=WordList()
        self.guess2="salty"


    def make_guess(self):
        """the make_guess function makes a guess.

        Currently, it always guesses "salty". Write code here to improve your solver.

        For compatibility with the benchmarking script please ensure that you
        always increment the number of guesses when you make a guess

        """
        wl=WordList()

        if self.num_guesses==0:
            self.num_guesses += 1
            guess="raise"
            self.wordlist.remove("raise")
        else:
            self.num_guesses += 1
            guess=self.new_guess()
            self.wordlist.remove(guess)
        return guess
        '''
        elif self.num_guesses==1:
            self.num_guesses+=1
            guessPair=self.double_guess()
            guess=guessPair[0]
            self.guess2=guessPair[1]
            self.wordlist.remove(guess)
        elif self.num_guesses==2:
            self.num_guesses+=1
            guess=self.guess2
            self.wordlist.remove(guess)
        '''


    def update_knowledge(self, info):
        """update_knowledge updates the solver's knowledge with an `info` object
        Use this method to update your search state.
        """
        self.wordlist.refine(info)
        pass


    def double_guess(self):

        ##list of 2d lists
        listOfLengths=[]
        ##2d list of averages for every possible guess pair
        listOfAverages=[]
        ##2d list of stdev for every possible guess pair

        b=100000
        si=0
        sj=0
        ##copy of originalWordList
        originalWordList=WordList(given_words=self.wordlist.words)
        for i in range(len(self.wordlist.words)):
            #for every possible answer in the wordlist
            possible_answer=self.wordlist.words[i]

            ##list of lengths of possible refined wordlists after two guesses
            ##for a set goal word
            list1=[]

            indexOfBestWord=0
            lengthOfBestWord=1000000
            ##goes through every possible word the true answer could be
            for j in range(len(self.wordlist.words)):
                ##makes a copy of the wordlist and goes through it
                tempWordList=WordList(given_words=self.wordlist.words)
                test_guess=self.wordlist.words[j]
                ##if the above given word was the answer, it refines the temp wordlist and finds the length of it

                tempWordList.refine(Information(possible_answer,test_guess))

                ##list of possible refined wordlists after the second guess after a set first guess
                list2=[]
                print(len(tempWordList))
                if len(tempWordList)>0:
                    for t in range(len(tempWordList.words)):
                        test_guess2=tempWordList.words[t]
                        tempWordList.refine(Information(possible_answer,test_guess2))
                        list2.append(len(tempWordList))
                else:
                    list2.append(0)

                ##print(len(tempWordList))
                list1.append(list2)
            listOfLengths.append(list1)


        ##listOfLengths[goalword][guess1][guess2]
        for ii in range(len(listOfLengths[0])):
            firstGuessAverages=[]
            for jj in range(len(listofLengths[0][0])):
                sum=0
                for kk in range(len(listOfLengths)):
                    sum+=listOfLengths[kk][ii][jj]
                sum=(sum/len(listOfLengths))
                if (sum<b and ii!=jj):
                    si=ii
                    sj=jj
                firstGuessAverages.append(sum)
            listOfAverages.append(firstGuessAverages)
        return(self.wordlist.words[si],self.wordlist.words[sj])



            ##adds ordered pair of
            ##pair=(sigma,avgEnt)

            #umcomment this later
            ##print("sigma:"+str(sigma)+" AvListSize:"+str(avgEnt)+" Index:"+str(i))
            ##listOfAverages.append((sigma,avgEnt))
        '''
        for i in range(len(listOfAverages)):
            plt.plot(listOfAverages[i][0],listOfAverages[i][1],"bo")

        plt.xlabel("Standard Deviation")
        plt.ylabel("Average Refined List Length")
        plt.title("Guess:"+str(self.num_guesses))

        plt.show()
        plt.close()

        print(listOfAverages[s])
        print(str(s))
        return self.wordlist.words[s]
        '''
    def new_guess(self):
        ##list of tuples
        listOfAverages=[]
        b=100000
        s=0
        originalWordList=WordList(given_words=self.wordlist.words)
        for i in range(len(self.wordlist.words)):
            ##test guess
            test_guess=self.wordlist.words[i]
            ##list of lengths of possible refined wordlists
            list1=[]
            indexOfBestWord=0
            lengthOfBestWord=1000000
            ##goes through every possible word the true answer could be
            for j in range(len(self.wordlist)):
                ##makes a copy of the wordlist and goes through it
                tempWordList=WordList(given_words=self.wordlist.words)
                possible_answer=self.wordlist.words[j]
                ##if the above given word was the answer, it refines the temp wordlist and finds the length of it
                tempWordList.refine(Information(possible_answer,test_guess))

                ##print(len(tempWordList))
                list1.append(len(tempWordList))

            list1sum=0

            #sum of every element in the list
            for p in range(len(list1)):
                list1sum+=list1[p]
            avgEnt=list1sum/(len(list1))



            ##standard deviation
            sigma=0
            for u in range(len(list1)):
                ##variance
                sigma+=((list1[u]-avgEnt)**2)
            sigma=((sigma/(len(list1)))**.5)

            if (avgEnt)<b:
                b=avgEnt
                s=i

            ##adds ordered pair of
            ##pair=(sigma,avgEnt)

            #umcomment this later
            ##print("sigma:"+str(sigma)+" AvListSize:"+str(avgEnt)+" Index:"+str(i))
            listOfAverages.append((sigma,avgEnt))
        
        for i in range(len(listOfAverages)):
            plt.plot(listOfAverages[i][0],listOfAverages[i][1],"bo")

        plt.xlabel("Standard Deviation")
        plt.ylabel("Average Refined List Length")
        plt.title("Guess:"+str(self.num_guesses))

        plt.show()
        plt.close()

        print(listOfAverages[s])
        print(str(s))

        return self.wordlist.words[s]

class AllLetters(Player):
    def __init__(self): pass
    def make_guess(self): pass
    def update_knowledge(self,info): pass

def main():
    '''
    solver=Solver()
    goal_word=WordList().get_random_word()
    solver.wordlist.refine(Information(goal_word,"raise"))
    next_guess=solver.new_guess()
    print(next_guess)


    '''
    for i in range(5):
        solver  = Solver()
        manager = GameManager(solver)
        n_guess = manager.play_game()
        print("you found the word in", n_guess, "guesses")


if __name__ == "__main__": main()
