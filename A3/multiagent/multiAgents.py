# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        Capsule = successorGameState.getCapsules()
        score = successorGameState.getScore()
                
        if successorGameState.isWin():
            return float("inf")
        if successorGameState.isLose():
            return float("-inf")
        
        # the distance of the nearest capsule
        if len(Capsule) > 0:
            capsuleDistance = util.manhattanDistance(newPos,Capsule[0])
            for (x,y) in Capsule:
                if util.manhattanDistance(newPos,(x,y)) < capsuleDistance:
                    capsuleDistance =  util.manhattanDistance(newPos,(x,y))
            score += 5.0/capsuleDistance**2
      
        # the distance of the nearest food
        newFood = newFood.asList()
        if len(newFood) > 0:
            foodDistance = util.manhattanDistance(newPos,newFood[0])
            for (x,y) in newFood:
                if util.manhattanDistance(newPos,(x,y)) < foodDistance:
                    foodDistance =  util.manhattanDistance(newPos,(x,y))                
            score += 10.0/foodDistance

        # the distance of the nearest ghost      
        if len(newGhostStates)>0 and not newGhostStates[0].scaredTimer:
            ghostDistance = util.manhattanDistance(newPos,newGhostStates[0].getPosition())
            for ghost in newGhostStates:
                if not ghost.scaredTimer:
                    ghostDistance = util.manhattanDistance(newPos,ghost.getPosition())
            
            if ghostDistance == 1:
                return float("-inf")
            else:
                score -= 10.0/ghostDistance

        return score

    
        

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"

        return self.MinMax(gameState, self.index, self.depth)[1]
        
    def MinMax(self, state, agent, d):
        if state.isLose() or state.isWin() or d == 0:
            return (self.evaluationFunction(state), None)
        
        legalActions = state.getLegalActions(agent)
        
        if agent == 0:
            if len(legalActions) == 0:
                return (self.evaluationFunction(state),None)

            maxScore, nextAct = self.MinMax(state.generateSuccessor(0, legalActions[0]), 1, d)
            maxAction = legalActions[0]
            if len(legalActions) > 1:
                for i in range(1,len(legalActions)):
                    score, nextAct = self.MinMax(state.generateSuccessor(0, legalActions[i]), 1, d)
                    if score > maxScore:
                        maxScore = score
                        maxAction = legalActions[i]
            return (maxScore,maxAction)

        else:
            if len(legalActions) == 0:
                return (self.evaluationFunction(state),None)

            if agent+1 >= state.getNumAgents():
                nextAgent = 0
                dNew = d - 1
            else:
                nextAgent = agent + 1
                dNew = d

            minScore, nextAct = self.MinMax(state.generateSuccessor(agent, legalActions[0]), nextAgent, dNew)
            minAction = legalActions[0]
            if len(legalActions) >1:
                for i in range(1,len(legalActions)):
                    score, nextAct = self.MinMax(state.generateSuccessor(agent, legalActions[i]), nextAgent, dNew)
                    if score < minScore:
                        minScore = score
                        minAction = legalActions[i]
            return (minScore,minAction)
 
    
    
    

    

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        a = float("-inf")
        b = float("inf")
        return self.AlphaBeta(gameState, self.index, self.depth,a,b)[1]
        
    
        
    def AlphaBeta(self, state, agent, d, a, b):
        if state.isLose() or state.isWin() or d == 0:
            return (self.evaluationFunction(state),None)
        
        legalActions = state.getLegalActions(agent)
        
        if agent == 0:
            maxScore = float("-inf")
            maxAction = legalActions[0]
            for i in range(len(legalActions)):
                score, nextAct = self.AlphaBeta(state.generateSuccessor(0, legalActions[i]), 1, d, a, b)
                if score > maxScore:
                    maxScore = score
                    maxAction = legalActions[i]
                if maxScore>=b:
                    break
                a = max(maxScore,a)
                
            return (maxScore,maxAction)

        else:
            if agent+1 >= state.getNumAgents():
                nextAgent = 0
                dNew = d - 1
            else:
                nextAgent = agent + 1
                dNew = d

            minScore = float("inf")
            minAction = legalActions[0]
            for i in range(len(legalActions)):
                score, nextAct = self.AlphaBeta(state.generateSuccessor(agent, legalActions[i]), nextAgent, dNew, a, b)
                if score < minScore:
                    minScore = score
                    minAction = legalActions[i]
                if a >= minScore:
                    break
                b = min(minScore,b)
                
            return (minScore,minAction)

        

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"

        return self.ExpMax(gameState, self.index, self.depth)[1]
        
    def ExpMax(self, state, agent, d):
        if state.isLose() or state.isWin() or d == 0:
            return (self.evaluationFunction(state),None)
        
        legalActions = state.getLegalActions(agent)
    
        if agent == 0:
            maxScore = float("-inf")
            maxAction = legalActions[0]
            for i in range(len(legalActions)):
                score, nextAct = self.ExpMax(state.generateSuccessor(0, legalActions[i]), 1, d)
                if score > maxScore:
                    maxScore = score
                    maxAction = legalActions[i]
            return (maxScore,maxAction)
        else:
            if agent+1 >= state.getNumAgents():
                nextAgent = 0
                dNew = d - 1
            else:
                nextAgent = agent + 1
                dNew = d
            
            scoreSum = 0
            for i in range(len(legalActions)):
                score, nextAct = self.ExpMax(state.generateSuccessor(agent, legalActions[i]), nextAgent, dNew)
                scoreSum += score
            scoreSum = scoreSum /len(legalActions)
            return (scoreSum,None)
        
        
   

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
      1. Find the nearest capsule and score it as 1/(the shortest distance)
      2. Find the nearest capsule and score it as 10/(the shortest distance)
      3. Find the nearest capsule and score it as -14/(the shortest distance)
         when the shortest distance is larger than 3. 
         And score it as -20/(the shortest distance) when the shortest distance
         is smaller or equal to 3
      4. Sum up all these scores with the original score obtained by
         currentGameState.getScore()
         
    """
    "*** YOUR CODE HERE ***"

    Pos = currentGameState.getPacmanPosition()
    Food = currentGameState.getFood()
    GhostStates = currentGameState.getGhostStates()
    Capsule = currentGameState.getCapsules()
    ScaredTimes = [ghostState.scaredTimer for ghostState in GhostStates]
    score = currentGameState.getScore()
            
    if currentGameState.isWin():
        return float("inf")
    if currentGameState.isLose():
        return float("-inf")
    
    # the distance of the nearest capsule
    if len(Capsule) > 0:
        capsuleDistance = util.manhattanDistance(Pos,Capsule[0])
        for (x,y) in Capsule:
            if util.manhattanDistance(Pos,(x,y)) < capsuleDistance:
                capsuleDistance =  util.manhattanDistance(Pos,(x,y))
        score += 1.0/capsuleDistance
  
    # the distance of the nearest food
    Food = Food.asList()
    if len(Food) > 0:
        foodDistance = util.manhattanDistance(Pos,Food[0])
        for (x,y) in Food:
            if util.manhattanDistance(Pos,(x,y)) < foodDistance:
                foodDistance =  util.manhattanDistance(Pos,(x,y))                
        score += 10.0/foodDistance

    # the distance of the nearest ghost      
    if len(GhostStates)>0 and not GhostStates[0].scaredTimer:
        ghostDistance = util.manhattanDistance(Pos,GhostStates[0].getPosition())
        for ghost in GhostStates:
            if not ghost.scaredTimer:
                ghostDistance = util.manhattanDistance(Pos,ghost.getPosition())
        
        if ghostDistance <= 3:
            score -= 20.0/ghostDistance
        else:
            score -= 14.0/ghostDistance
            
    return score


# Abbreviation
better = betterEvaluationFunction

