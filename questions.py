"""
AI NEXUS - question bank, DSC401-6 Artificial Intelligence (Units I & II)
Main reference : Russell & Norvig, Artificial Intelligence: A Modern Approach, 3rd ed. (AIMA)
Also used      : Rich & Knight, Artificial Intelligence (production systems, problem characteristics,
                 means-end analysis) - the syllabus topic list follows this book for those items.
All worked numbers (Romania map, 8-puzzle, 8-queens, Australia map, taxi PEAS ...) are the textbook's own examples.
"""

TOPICS = [
    "Foundations & Applications", "Turing Test", "Rational Agents", "Intelligent Agents",
    "Agents & Environments", "Good Behaviour", "Nature of Environments",
    "Problems & Problem Spaces", "State Space Search", "Production Systems",
    "Problem Characteristics", "Search Design Issues", "BFS", "DFS",
    "Iterative Deepening", "Hill Climbing", "Heuristic Search", "Best First Search",
    "CSP", "Means-End Analysis",
]

ZONES = [
    ("01", "AGENT CORE", "Agents, rationality, environments",
     ["Foundations & Applications", "Turing Test", "Rational Agents", "Intelligent Agents",
      "Agents & Environments", "Good Behaviour", "Nature of Environments"]),
    ("02", "PROBLEM SPACE", "Formulation, state spaces, production systems",
     ["Problems & Problem Spaces", "State Space Search", "Production Systems",
      "Problem Characteristics", "Search Design Issues"]),
    ("03", "BLIND SEARCH", "BFS, DFS, iterative deepening",
     ["BFS", "DFS", "Iterative Deepening"]),
    ("04", "INFORMED SEARCH", "Heuristics, best-first, A*, hill climbing",
     ["Heuristic Search", "Best First Search", "Hill Climbing"]),
    ("05", "CONSTRAINT GRID", "CSP and means-end analysis",
     ["CSP", "Means-End Analysis"]),
]

TOPIC_REF = {
    "Foundations & Applications": "AIMA Ch.1 (Sec. 1.1-1.2)",
    "Turing Test": "AIMA Ch.1 (Sec. 1.1.1)",
    "Rational Agents": "AIMA Ch.2 (Sec. 2.2)",
    "Intelligent Agents": "AIMA Ch.2 (Sec. 2.4)",
    "Agents & Environments": "AIMA Ch.2 (Sec. 2.1)",
    "Good Behaviour": "AIMA Ch.2 (Sec. 2.2)",
    "Nature of Environments": "AIMA Ch.2 (Sec. 2.3)",
    "Problems & Problem Spaces": "AIMA Ch.3 (Sec. 3.1-3.2)",
    "State Space Search": "AIMA Ch.3 (Sec. 3.1-3.3)",
    "Production Systems": "Rich & Knight Ch.2 (production systems)",
    "Problem Characteristics": "Rich & Knight Ch.2 (problem characteristics)",
    "Search Design Issues": "AIMA Ch.3 (Sec. 3.3); Rich & Knight Ch.2",
    "BFS": "AIMA Ch.3 (Sec. 3.4.1)",
    "DFS": "AIMA Ch.3 (Sec. 3.4.3)",
    "Iterative Deepening": "AIMA Ch.3 (Sec. 3.4.5)",
    "Hill Climbing": "AIMA Ch.4 (Sec. 4.1.1-4.1.2)",
    "Heuristic Search": "AIMA Ch.3 (Sec. 3.5-3.6)",
    "Best First Search": "AIMA Ch.3 (Sec. 3.5.1-3.5.2)",
    "CSP": "AIMA Ch.6",
    "Means-End Analysis": "Rich & Knight Ch.3 (means-ends analysis); AIMA Ch.1 (GPS)",
}

AR_OPTS = [
    "Both A and R are true, and R is the correct explanation of A",
    "Both A and R are true, but R is NOT the correct explanation of A",
    "A is true, but R is false",
    "A is false, but R is true",
]

# dark-theme friendly Graphviz header
GV = ('bgcolor="transparent"; node [shape=circle, style=filled, fillcolor="#101a33", color="#00e5ff", '
      'fontcolor="#e6f1ff", fontname="Helvetica"]; edge [color="#6c8cff", fontcolor="#ffd166", fontname="Helvetica"]; ')

G_TREE = ("digraph G { rankdir=TB; " + GV + "S -> A; S -> B; A -> C; A -> D; B -> E; D -> G; "
          'G [shape=doublecircle, fillcolor="#0f5132", color="#7ee787"]; }')

G_ROM = ("graph R { rankdir=LR; " + GV + "node [fontsize=10]; "
         'Arad [label="Arad\\n366"]; Sibiu [label="Sibiu\\n253"]; Timisoara [label="Timisoara\\n329"]; '
         'Zerind [label="Zerind\\n374"]; Oradea [label="Oradea\\n380"]; Fagaras [label="Fagaras\\n176"]; '
         'RV [label="R.Vilcea\\n193"]; Pitesti [label="Pitesti\\n100"]; Craiova [label="Craiova\\n160"]; '
         'Bucharest [label="Bucharest\\n0", shape=doublecircle, fillcolor="#0f5132", color="#7ee787"]; '
         "Arad -- Zerind [label=75]; Arad -- Sibiu [label=140]; Arad -- Timisoara [label=118]; "
         "Zerind -- Oradea [label=71]; Oradea -- Sibiu [label=151]; Sibiu -- Fagaras [label=99]; "
         "Sibiu -- RV [label=80]; RV -- Pitesti [label=97]; RV -- Craiova [label=146]; "
         "Pitesti -- Craiova [label=138]; Pitesti -- Bucharest [label=101]; Fagaras -- Bucharest [label=211]; }")

G_AUS = ("graph A { " + GV + "WA -- NT; WA -- SA; NT -- SA; NT -- Q; SA -- Q; SA -- NSW; SA -- V; Q -- NSW; NSW -- V; TAS; }")
G_AUS_WA_NT = ("graph A { " + GV + 'WA [fillcolor="#7a1f1f"]; NT [fillcolor="#1f6b3a"]; SA [label="SA ?"]; '
               "WA -- NT; WA -- SA; NT -- SA; NT -- Q; SA -- Q; SA -- NSW; SA -- V; Q -- NSW; NSW -- V; TAS; }")
G_AUS_FC = ("graph A { " + GV + 'WA [fillcolor="#7a1f1f"]; Q [fillcolor="#1f6b3a"]; V [fillcolor="#1f3f7a"]; SA [label="SA ?"]; '
            "WA -- NT; WA -- SA; NT -- SA; NT -- Q; SA -- Q; SA -- NSW; SA -- V; Q -- NSW; NSW -- V; TAS; }")

QUESTIONS = []


def _add(topic, d):
    d.setdefault("ref", TOPIC_REF[topic])
    QUESTIONS.append(d)


def mcq(topic, diff, q, correct, wrongs, expl, hint, kind="MCQ", real=False, search=False, graph=None, ref=None):
    _add(topic, dict(topic=topic, type="mcq", kind=kind, difficulty=diff, q=q, options=[correct] + list(wrongs),
                     answer=correct, shuffle=True, explanation=expl, hint=hint, real=real, search=search,
                     graph=graph, **({"ref": ref} if ref else {})))


def tf(topic, diff, q, truth, expl, hint, real=False, search=False, ref=None):
    _add(topic, dict(topic=topic, type="tf", kind="True/False", difficulty=diff, q=q, options=["True", "False"],
                     answer="True" if truth else "False", shuffle=False, explanation=expl, hint=hint, real=real,
                     search=search, graph=None, **({"ref": ref} if ref else {})))


def ar(topic, diff, assertion, reason, code, expl, hint, ref=None):
    _add(topic, dict(topic=topic, type="ar", kind="Assertion-Reason", difficulty=diff,
                     q=f"**Assertion (A):** {assertion}\n\n**Reason (R):** {reason}", options=AR_OPTS,
                     answer=AR_OPTS[code], shuffle=False, explanation=expl, hint=hint, real=False, search=False,
                     graph=None, **({"ref": ref} if ref else {})))


def fib(topic, diff, q, accept, expl, hint, kind="Fill in the Blank", real=False, search=False, graph=None, ref=None):
    _add(topic, dict(topic=topic, type="fib", kind=kind, difficulty=diff, q=q, accept=[a.lower() for a in accept],
                     answer=accept[0], shuffle=False, explanation=expl, hint=hint, real=real, search=search,
                     graph=graph, **({"ref": ref} if ref else {})))


def match(topic, diff, q, pairs, expl, hint, real=False, ref=None):
    _add(topic, dict(topic=topic, type="match", kind="Match the Following", difficulty=diff, q=q, pairs=pairs,
                     answer="; ".join(f"{a} -> {b}" for a, b in pairs), shuffle=True, explanation=expl, hint=hint,
                     real=real, search=False, graph=None, **({"ref": ref} if ref else {})))


# =============================================================== Foundations & Applications
T = "Foundations & Applications"
match(T, "Medium", "Match each of the four approaches to AI with the idea behind it.",
      [("Acting humanly", "Turing Test approach"), ("Thinking humanly", "Cognitive modelling"),
       ("Thinking rationally", "'Laws of thought' (logic)"), ("Acting rationally", "Rational agent approach")],
      "These are the four categories in AIMA Fig. 1.1. The book itself follows the rational agent approach.",
      "Two are about behaviour, two about thought process.")
ar(T, "Hard", "The 'laws of thought' (logicist) approach alone does not give us a practical rational agent.",
   "Informal knowledge is hard to state formally, especially when it is uncertain, and solving a problem in principle is very different from solving it in practice.",
   0, "These are exactly the two obstacles AIMA lists for the logicist tradition: uncertainty and computational intractability.",
   "Think about uncertainty and computation time.")
mcq(T, "Medium", "Which field gave AI the notions of utility and decision theory?",
    "Economics", ["Linguistics", "Neuroscience", "Computer engineering"],
    "Economics formalised decision making to maximise expected utility, which AI uses for rational agents.",
    "Preferences and payoffs.", ref="AIMA Ch.1 (Sec. 1.2.3)")
mcq(T, "Hard", "AIMA says perfect rationality is not feasible in complicated environments and so studies limited rationality. Why?",
    "The computational demands of always computing the best action are too high, so the agent must act well with limited time",
    ["Performance measures cannot be defined for complex tasks", "Rational agents cannot use sensors in complex worlds",
     "Maximising expected utility is mathematically undefined"],
    "Limited rationality means acting appropriately when there is not enough time to do all the computations one would like.",
    "Think resources, not mathematics.", ref="AIMA Ch.1 (Sec. 1.1.4)")
mcq(T, "Medium", "Google Maps suggests the fastest route between two places. Which AI idea works behind it?",
    "Heuristic search over a graph of roads (A*-style)",
    ["Sorting road names alphabetically", "A fixed lookup table of every possible trip", "Random guessing until some route turns up"],
    "Roads form a graph with step costs, and A* with a straight-line-distance heuristic finds the cheapest route.",
    "Nodes, edges and a cost to minimise.", kind="Scenario", real=True)

# =============================================================== Turing Test
T = "Turing Test"
tf(T, "Easy", "The computer passes the Turing Test if a human interrogator cannot tell whether written answers come from a person or a machine.", True,
   "This is Turing's (1950) operational definition of intelligent behaviour.", "Can the judge tell the difference?")
mcq(T, "Medium", "Which pair of capabilities is added to the basic Turing Test to form the Total Turing Test?",
    "Computer vision and robotics",
    ["Machine learning and planning", "Knowledge representation and automated reasoning", "Natural language processing and speech synthesis"],
    "The Total Turing Test includes a video signal (vision) and the chance to pass physical objects (robotics).",
    "Video signal plus physical objects.")
match(T, "Medium", "Match each capability a computer needs for the Turing Test with its role.",
      [("Natural language processing", "Communicate successfully in English"),
       ("Knowledge representation", "Store what it knows or hears"),
       ("Automated reasoning", "Use stored information to answer questions and draw new conclusions"),
       ("Machine learning", "Adapt to new circumstances and detect patterns")],
      "These are the four capabilities AIMA lists for passing the (basic) Turing Test.", "Four capabilities, four jobs.")
ar(T, "Hard", "Most AI researchers devote little effort to passing the Turing Test.",
   "Studying the underlying principles of intelligence is more productive than imitating humans, just as aeronautical engineering did not aim to fool pigeons.",
   0, "AIMA uses the aeronautics analogy to explain why researchers study principles of intelligence instead of imitation.",
   "Recall the pigeon analogy.")

# =============================================================== Rational Agents
T = "Rational Agents"
mcq(T, "Medium", "Which statement matches AIMA's definition of a rational agent?",
    "For each possible percept sequence, it selects an action expected to maximise its performance measure, given the percepts and its built-in knowledge",
    ["It always selects the action that actually turns out best", "It always imitates the most successful human behaviour",
     "It selects actions that satisfy the designer's opinion of good behaviour"],
    "Rationality uses expected performance, not actual outcomes, and depends on the percept sequence and prior knowledge.",
    "Expected, not actual.")
mcq(T, "Hard", "In AIMA's street-crossing example, an agent crosses a road WITHOUT looking and gets across safely. Is the action rational?",
    "No - skipping information gathering lowers expected performance, even though the outcome was good",
    ["Yes - the outcome was successful so the action was rational", "Yes - rationality only depends on the performance measure's final value",
     "No - because rational agents must never cross roads"],
    "Looking before acting (information gathering) is part of rationality. Success by luck does not make the choice rational.",
    "Judge the decision, not the lucky outcome.", kind="Scenario", real=True)
mcq(T, "Medium", "Rationality at any given time depends on which four things?",
    "Performance measure, prior knowledge of the environment, available actions, percept sequence",
    ["CPU speed, memory size, programming language, sensor cost", "Number of rules, search depth, branching factor, heuristic value",
     "Designer's opinion, agent's mood, past luck, speed"],
    "These four ingredients appear in AIMA's definition.", "P, K, A, P.")
mcq(T, "Hard", "A simple reflex vacuum agent (Suck if dirty, else move to the other square) is rational if each clean square scores 1 point per step. Which change makes the SAME agent irrational?",
    "Charging one point for every move",
    ["Doubling the reward for each clean square", "Lengthening the episode from 1000 to 2000 steps", "Starting the agent in square B instead of A"],
    "With a movement penalty the agent wastes points by shuffling between clean squares forever. It should stop moving once everything is clean (AIMA Sec. 2.2.2).",
    "Which change makes constant shuffling costly?", kind="Scenario")

# =============================================================== Intelligent Agents
T = "Intelligent Agents"
fib(T, "Hard", "A table-driven agent has |P| = 4 possible percepts and lives for T = 3 time steps. The number of entries in its lookup table is the sum of |P|^t for t = 1..T, which is ______.",
    ["84"], "4 + 16 + 64 = 84. For chess the same formula gives about 10^150 entries, so the table approach is hopeless.",
    "4^1 + 4^2 + 4^3.", kind="Problem Solving")
match(T, "Medium", "Match each agent type with its key feature.",
      [("Simple reflex agent", "Condition-action rules on the current percept"),
       ("Model-based reflex agent", "Keeps internal state about the unseen world"),
       ("Goal-based agent", "Considers future actions to reach a goal"),
       ("Utility-based agent", "Compares how desirable outcomes are"),
       ("Learning agent", "Improves with a critic and learning element")],
      "The five agent structures from AIMA Sec. 2.4.", "Simplest to most general.")
mcq(T, "Hard", "Why does partial observability push a design from a simple reflex agent to a model-based reflex agent?",
    "The agent must keep internal state to track parts of the world it cannot currently see",
    ["Because simple reflex agents cannot execute actions", "Because model-based agents do not need sensors",
     "Because partial observability makes the performance measure undefined"],
    "Internal state is updated using knowledge of how the world evolves and how the agent's own actions affect it.",
    "What must the agent remember?")
mcq(T, "Hard", "A taxi agent chooses between three routes by weighing journey time, passenger safety and fuel cost. Which agent type is this?",
    "Utility-based agent", ["Simple reflex agent", "Table-driven agent", "Goal-based agent that treats all successful routes as equal"],
    "Several routes reach the goal, so a utility function is needed to compare how good each outcome is and to trade off conflicting objectives.",
    "Goals give yes/no, utility gives 'how good'.", kind="Scenario", real=True)
fib(T, "Medium", "In a learning agent, the component that suggests exploratory actions leading to new, informative experiences is the ______ generator.",
    ["problem"], "The other components are the critic, learning element and performance element.", "It generates new ____ to try.")

# =============================================================== Agents & Environments
T = "Agents & Environments"
tf(T, "Easy", "The percept sequence is the complete history of everything the agent has ever perceived.", True,
   "A percept is a single input; the percept sequence is the entire history.", "Percept vs. sequence.")
fib(T, "Hard", "An agent decides using only its current percept. It has 4 possible percepts and 3 possible actions. The number of distinct agent functions is ______.",
    ["81"], "Each of the 4 percepts can map to any of 3 actions, so 3^4 = 81.", "Choose an action for each percept.", kind="Problem Solving")
fib(T, "Hard", "A vacuum world has 4 squares, each clean or dirty, and the agent is in one of them. The number of states is n x 2^n = ______.",
    ["64"], "4 x 2^4 = 64. (The two-square world has 2 x 2^2 = 8 states.)", "Location x dirt patterns.", kind="Problem Solving", search=True)

# =============================================================== Good Behaviour
T = "Good Behaviour"
mcq(T, "Easy", "As a general rule, a performance measure should be designed according to:",
    "what we actually want to achieve in the environment",
    ["how we think the agent should behave", "the number of rules in the agent program", "the agent's own opinion of its success"],
    "Judge the environment states, not the agent's behaviour or self-assessment.", "Outcome in the world.")
mcq(T, "Hard", "A vacuum-cleaner agent is rewarded for the amount of dirt it picks up. What unwanted behaviour might it learn?",
    "Dump the dirt back on the floor and clean it again to earn more reward",
    ["Switch itself off to save energy", "Refuse to leave the first room", "Clean only the squares that are already clean"],
    "A better measure rewards a clean floor at each time step (AIMA Sec. 2.2.1).", "How could it get more 'dirt picked up'?",
    kind="Scenario", real=True)
mcq(T, "Medium", "Which statement correctly contrasts rationality and perfection?",
    "Rationality maximises expected performance; perfection maximises actual performance",
    ["Rationality maximises actual performance; perfection maximises expected performance", "They mean the same thing",
     "Rationality needs omniscience; perfection does not"],
    "Perfection would require knowing the outcome of actions in advance, which is impossible.", "Expected vs actual.")

# =============================================================== Nature of Environments
T = "Nature of Environments"
mcq(T, "Easy", "PEAS stands for:", "Performance measure, Environment, Actuators, Sensors",
    ["Percept, Experience, Action, State", "Problem, Environment, Agent, Solution", "Planning, Evaluation, Action, Search"],
    "PEAS describes the task environment.", "Four words, P-E-A-S.")
match(T, "Medium", "Match each PEAS element of an automated taxi with an example.",
      [("Performance measure", "Safe, fast, legal, comfortable trip"), ("Environment", "Roads, traffic, pedestrians, customers"),
       ("Actuators", "Steering, accelerator, brake, horn"), ("Sensors", "Cameras, GPS, speedometer, sonar")],
      "From AIMA Fig. 2.4.", "Actuators are what the agent can DO.", real=True)
ar(T, "Hard", "Chess played with a clock is a semidynamic environment.",
   "The environment itself does not change as time passes, but the agent's performance score does.",
   0, "This is the textbook definition of semidynamic (AIMA Sec. 2.3.2).", "Who changes with time, the board or the score?")
mcq(T, "Medium", "A system inspects each part on a conveyor belt and labels it 'defective' or 'fine'; each decision is independent of earlier ones. This task is:",
    "Episodic", ["Sequential", "Dynamic", "Continuous"],
    "Each episode does not affect later ones, so it is episodic.", "Does the earlier decision matter later?",
    kind="Scenario", real=True)
mcq(T, "Hard", "AIMA distinguishes known from unknown environments. Which statement is correct?",
    "Known/unknown is about the agent's knowledge of the environment's rules, so a known environment can still be partially observable",
    ["Known means fully observable and unknown means partially observable", "Unknown environments are always stochastic",
     "Known environments are always single-agent"],
    "A card game is known (you know the rules) but partially observable; a new video game can be fully observable yet unknown.",
    "Rules versus what you can see.")
match(T, "Hard", "Match each task environment (AIMA Fig. 2.6) with its distinguishing property.",
      [("Crossword puzzle", "Deterministic and static"), ("Poker", "Partially observable, stochastic, multiagent"),
       ("Chess with a clock", "Semidynamic"), ("Image analysis", "Episodic")],
      "Crossword: fully observable, deterministic, sequential, static, discrete, single-agent. Image analysis is episodic.",
      "Recall the table in the textbook.")

# =============================================================== Problems & Problem Spaces
T = "Problems & Problem Spaces"
mcq(T, "Easy", "Which of these is NOT part of the formal definition of a search problem?", "A random seed",
    ["Initial state", "Goal test", "Path cost function"],
    "A problem is defined by initial state, actions, transition model, goal test and path cost.", "Which one sounds unrelated?")
mcq(T, "Medium", "In the Romania problem, the transition model gives RESULT(In(Arad), Go(Sibiu)) = ?",
    "In(Sibiu)", ["In(Arad)", "In(Bucharest)", "Go(Sibiu)"],
    "The transition model returns the state reached by taking an action in a state.", "Where are you after driving to Sibiu?",
    search=True)
mcq(T, "Hard", "A random 8-puzzle instance has average solution cost about 22 and branching factor about 3. About how many nodes does an exhaustive tree search to depth 22 examine?",
    "About 3.1 x 10^10", ["About 3.1 x 10^6", "About 6.6 x 10^22", "About 22 x 3 = 66"],
    "3^22 is about 3.1 x 10^10. Graph search cuts this to 181,440 distinct states (AIMA Sec. 3.2.1).",
    "Compute 3^22.", kind="Problem Solving", search=True)
mcq(T, "Hard", "AIMA's improved incremental formulation of the 8-queens problem (place a queen in the leftmost empty column so it is not attacked) reduces the state space from about 1.8 x 10^14 to:",
    "2,057 states", ["8! = 40,320 states", "64 x 63 = 4,032 states", "8^8 = 16,777,216 states"],
    "A good formulation prunes the state space drastically (AIMA Sec. 3.2.2).", "A very small number.", search=True)
mcq(T, "Medium", "For a route-finding app, which is a sensible path cost?",
    "Total distance or travel time of the roads used",
    ["Number of cities in the country", "Number of road signs passed", "Alphabetical order of city names"],
    "Path cost should reflect what the user wants minimised.", "What does a traveller care about?", kind="Scenario", real=True)

# =============================================================== State Space Search
T = "State Space Search"
tf(T, "Easy", "The state space is the set of all states reachable from the initial state by any sequence of actions.", True,
   "It forms a graph: nodes are states, links are actions.", "States + actions = graph.", search=True)
mcq(T, "Hard", "Only half of all arrangements of the 8-puzzle are reachable from a given start. How many states are reachable?",
    "181,440", ["362,880", "40,320", "90,720"], "9!/2 = 181,440; the other half cannot be reached because of parity.",
    "9! = 362,880.", kind="Problem Solving", search=True)
mcq(T, "Medium", "Water-jug problem with a 4 L and a 3 L jug, state = (litres in 4 L jug, litres in 3 L jug). Which state can be reached from (0,0) in exactly one move?",
    "(4,0)", ["(1,3)", "(4,3)", "(2,0)"], "One move from (0,0) can only fill a jug: (4,0) or (0,3).",
    "Only fill, empty or pour.", kind="Problem Solving", search=True, ref="Rich & Knight Ch.2 (water-jug problem)")
fib(T, "Hard", "Water-jug problem (4 L and 3 L jugs, start (0,0)): the minimum number of moves needed to get exactly 2 L in the 3 L jug is ______.",
    ["4"], "(0,0) -> (0,3) -> (3,0) -> (3,3) -> (4,2). No shorter route exists.", "Fill 3L, pour into 4L, fill 3L again...",
    kind="Problem Solving", search=True, ref="Rich & Knight Ch.2 (water-jug problem)")

# =============================================================== Production Systems
T = "Production Systems"
mcq(T, "Medium", "A production system consists of:", "A set of rules, a global database and a control strategy",
    ["Only a set of rules", "A neural network and a loss function", "Sensors, actuators and a performance measure"],
    "Rules (condition-action), a database describing the current state, and a control strategy to choose which rule fires.", "Three parts.")
match(T, "Medium", "Match each production-system term with its meaning.",
      [("Rule", "Condition-action pair"), ("Global database", "Description of the current state"),
       ("Control strategy", "Decides which applicable rule to fire"), ("Conflict resolution", "Picks one rule when several match")],
      "Building blocks of any production system.", "Think of an IF-THEN expert system.")
tf(T, "Hard", "A commutative production system is one that is both monotonic and partially commutative.", True,
   "Monotonic: applying a rule never blocks a rule that was applicable earlier. Partially commutative: any allowable reordering of a rule sequence gives the same state.",
   "Combine the two properties.")
mcq(T, "Medium", "A medical expert system has IF-THEN rules. Two rules match the same symptoms. The mechanism that decides which one fires is:",
    "Conflict resolution", ["Constraint propagation", "Hill climbing", "Backtracking"],
    "The control strategy applies conflict resolution to pick one rule from the conflict set.", "Two rules, one winner.",
    kind="Scenario", real=True)
match(T, "Hard", "Match each problem with its production-system class.",
      [("Theorem proving", "Monotonic, partially commutative"), ("Robot navigation", "Nonmonotonic, partially commutative"),
       ("Chemical synthesis", "Monotonic, not partially commutative"), ("Playing bridge", "Nonmonotonic, not partially commutative")],
      "Rich & Knight's classification of production systems by monotonicity and partial commutativity.",
      "Can steps be undone? Can order be changed?")

# =============================================================== Problem Characteristics
T = "Problem Characteristics"
mcq(T, "Medium", "Which of the following problems is decomposable?",
    "Symbolic integration of a sum of independent terms", ["Playing chess", "The 8-puzzle", "Planning a robot's route through a cluttered room"],
    "The integral of a sum splits into independent sub-integrals; the others have interacting sub-problems.",
    "Can it be split into independent parts?")
mcq(T, "Medium", "Chess moves cannot be undone, so mistakes may be permanent. Chess is an example of an ______ problem.",
    "irrecoverable", ["ignorable", "recoverable", "decomposable"],
    "Ignorable (theorem proving), recoverable (8-puzzle), irrecoverable (chess).", "Can a bad move be taken back?", kind="Scenario")
tf(T, "Hard", "The 8-puzzle is a recoverable problem because a wrong move can be reversed by moving the tile back.", True,
   "Steps can be undone, so it is recoverable (but not ignorable, since we must still undo them).", "Moving a tile back undoes it.")
ar(T, "Hard", "In the water-jug problem the final state alone is not a sufficient answer.",
   "The problem asks for the sequence of operations that reaches the goal, i.e. the solution is a path.",
   0, "Solution is a path here, unlike natural-language understanding where the solution is a state (an interpretation).", "State or path?")
fib(T, "Hard", "Theorem proving, where a wrong step can simply be ignored, belongs to the ______ class (ignorable / recoverable / irrecoverable).",
    ["ignorable"], "An unneeded lemma is just not used, so nothing needs to be undone.", "Starts with 'i'.")
mcq(T, "Hard", "Which statement about the universe being predictable is correct?",
    "In the 8-puzzle outcomes are certain so a full plan can be made in advance; in bridge outcomes are uncertain so planning must allow revision",
    ["The 8-puzzle has uncertain outcomes while bridge has certain outcomes", "Both have certain outcomes",
     "Outcome certainty does not affect how we solve a problem"],
    "Certain-outcome problems allow open-loop plans; uncertain-outcome problems need plan revision or feedback.",
    "Can you predict the result of a move?")

# =============================================================== Search Design Issues
T = "Search Design Issues"
mcq(T, "Medium", "Searching from the goal back towards the initial state is called:",
    "Backward reasoning", ["Forward reasoning", "Random restart", "Generate-and-test"],
    "The direction of search is a key design issue.", "Reverse direction.")
tf(T, "Medium", "Tree search may re-expand states reached through different paths; keeping an explored set (graph search) avoids this.", True,
   "Graph search with an explored set prevents repeated states and loops.", "Remember visited states.", search=True)
tf(T, "Hard", "Even though the Romania map has only 20 cities, tree search without repeated-state checking can generate an infinite number of nodes.", True,
   "A loopy path such as Arad - Sibiu - Arad - Sibiu ... keeps producing new nodes for the same states.",
   "Is Arad -> Sibiu -> Arad allowed?", search=True)
mcq(T, "Medium", "A search algorithm that is guaranteed to find a solution whenever one exists is called:",
    "Complete", ["Optimal", "Admissible", "Monotonic"],
    "Completeness, optimality, time complexity and space complexity are the four evaluation criteria.", "Not the same as optimal.")

# =============================================================== BFS
T = "BFS"
mcq(T, "Easy", "Breadth-first search stores its frontier in which data structure?", "FIFO queue",
    ["LIFO stack", "Priority queue ordered by h(n)", "Hash table only"],
    "BFS expands the shallowest node first, so a queue is needed.", "First in, first out.", search=True)
fib(T, "Hard", "b = 10, shallowest goal at depth d = 3. BFS tests for the goal when a node is EXPANDED, so in the worst case it generates b + b^2 + b^3 + (b^4 - b) = ______ nodes.",
    ["11100", "11,100"], "10 + 100 + 1000 + 9990 = 11,100. Testing at generation instead would save the last b^(d+1) - b nodes.",
    "Add the four terms.", kind="Problem Solving", search=True)
mcq(T, "Medium", "Using BFS (children left to right) on the tree shown, in which order are nodes expanded until the goal G is reached?",
    "S, A, B, C, D, E, G", ["S, A, C, D, G", "S, B, E, A, D, G", "S, A, B, E, C, D, G"],
    "BFS goes level by level: S | A B | C D E | G.", "Go level by level.", kind="Problem Solving", search=True, graph=G_TREE)
mcq(T, "Medium", "A social network wants the fewest-hops connection between two users. Which uninformed search fits best?",
    "Breadth-first search", ["Depth-first search", "Hill climbing", "Depth-limited search with limit 1"],
    "BFS finds the shallowest path, i.e. the fewest edges.", "Fewest hops = shallowest.", kind="Scenario", real=True, search=True)
mcq(T, "Hard", "b = 10, goal at depth 8, about 1000 bytes per node. Roughly how much memory does BFS need to hold its frontier?",
    "About 100 GB", ["About 100 MB", "About 1 GB", "About 10 TB"],
    "10^8 nodes x 10^3 bytes = 10^11 bytes = 100 GB. AIMA's lesson: memory is a bigger problem for BFS than time.",
    "10^8 x 1000.", kind="Problem Solving", search=True)

# =============================================================== DFS
T = "DFS"
mcq(T, "Easy", "Depth-first search uses which data structure for its frontier?", "LIFO stack",
    ["FIFO queue", "Priority queue", "Circular buffer"], "The deepest (most recent) node is expanded first.", "Last in, first out.", search=True)
tf(T, "Medium", "DFS (tree-search version) is complete even in infinite state spaces.", False,
   "DFS can follow an infinite path forever. It is complete only in finite spaces with repeated-state checking.",
   "What if one branch never ends?", search=True)
fib(T, "Hard", "b = 10 and maximum depth m = 16. DFS needs to store only b*m + 1 = ______ nodes (AIMA compares this with 10 exabytes for BFS).",
    ["161"], "10 x 16 + 1 = 161 nodes, about 156 KB at 1000 bytes per node, versus about 10 exabytes for BFS at depth 16.",
    "Multiply and add 1.", kind="Problem Solving", search=True)
mcq(T, "Medium", "Using DFS (children left to right) on the tree shown, which path to G does it return?",
    "S - A - D - G", ["S - B - E - G", "S - A - C - D - G", "S - A - B - D - G"],
    "DFS goes S, A, C (dead end), backtracks to A, then D, then G.", "Go as deep as possible first.",
    kind="Problem Solving", search=True, graph=G_TREE)
mcq(T, "Medium", "A maze-solving robot has very little memory. Which search suits it best?",
    "Depth-first search with backtracking", ["Breadth-first search", "Search that stores the whole maze graph", "Bidirectional search"],
    "DFS stores only the current path plus unexpanded siblings.", "Memory is limited.", kind="Scenario", real=True, search=True)

# =============================================================== Iterative Deepening
T = "Iterative Deepening"
mcq(T, "Medium", "Iterative deepening search combines the advantages of:",
    "DFS's low memory and BFS's completeness / optimality (unit step cost)",
    ["Hill climbing and CSP", "Greedy search and A*", "Minimax and alpha-beta"],
    "It repeats depth-limited DFS with increasing limits.", "Two basic uninformed strategies.", search=True)
tf(T, "Medium", "Iterative deepening is asymptotically much slower than BFS because it regenerates the upper levels again and again.", False,
   "Most nodes lie at the deepest level, so the repeated work is small; both take O(b^d) time.", "Where are most nodes in a tree?", search=True)
fib(T, "Hard", "b = 10, d = 5. Iterative deepening generates 50 + 400 + 3,000 + 20,000 + 100,000 = ______ nodes.",
    ["123450", "123,450"], "N(IDS) = d*b + (d-1)*b^2 + ... + 1*b^d = 123,450 (AIMA Sec. 3.4.5).", "Just add them.",
    kind="Problem Solving", search=True)
fib(T, "Hard", "For the same b = 10, d = 5, BFS that tests the goal on expansion generates b + b^2 + ... + b^5 + (b^6 - b) = ______ nodes, about 9 times more than IDS.",
    ["1111100", "1,111,100"], "111,110 + 999,990 = 1,111,100, compared with 123,450 for IDS. Repeating upper levels costs only about 11%.",
    "Add the five terms, then add b^6 - b.", kind="Problem Solving", search=True)
mcq(T, "Medium", "A rescue robot explores a collapsed building: the depth of the exit is unknown and memory is limited. The best uninformed strategy is:",
    "Iterative deepening search", ["Breadth-first search", "Pure depth-first search", "Greedy best-first search"],
    "AIMA: iterative deepening is the preferred uninformed method when the search space is large and the solution depth is unknown.",
    "Unknown depth + little memory.", kind="Scenario", real=True, search=True)

# =============================================================== Hill Climbing
T = "Hill Climbing"
mcq(T, "Medium", "A flat area of the landscape where all neighbours have the same value as the current state is called a:",
    "Plateau", ["Ridge", "Global maximum", "Peak"], "Hill climbing may wander or stop on a plateau.", "Think of flat ground.")
match(T, "Medium", "Match each hill-climbing variant with its idea.",
      [("Steepest-ascent", "Picks the best of all neighbours"), ("Stochastic", "Chooses randomly among uphill moves"),
       ("First-choice", "Generates successors until a better one appears"), ("Random-restart", "Repeats climbs from random start states"),
       ("Simulated annealing", "Occasionally accepts downhill moves")],
      "AIMA Sec. 4.1.1-4.1.2.", "Which one uses random start states?")
tf(T, "Medium", "Steepest-ascent hill climbing always finds the global maximum.", False,
   "It can get stuck at local maxima, ridges or plateaus.", "Greedy methods can be trapped.", search=True)
ar(T, "Hard", "Simulated annealing can escape local maxima.",
   "It sometimes accepts downhill moves, with probability that falls as the temperature is lowered.", 0,
   "Bad moves let it leave a local maximum; cooling makes it settle later.", "Why accept a worse move?")
mcq(T, "Hard", "In simulated annealing a move worsens the value by 2 (Delta E = -2) at temperature T = 2. The probability that it is accepted is e^(Delta E / T), about:",
    "0.37", ["0.14", "0.50", "0.86"], "e^(-2/2) = e^(-1) = 0.368.", "Compute e^(-1).", kind="Problem Solving")
fib(T, "Hard", "In the 8-queens complete-state formulation (one queen per column, move a queen within its column), each state has ______ successors.",
    ["56"], "8 queens x 7 alternative rows = 56 successors (AIMA Sec. 4.1.1).", "8 x 7.", kind="Problem Solving", search=True)
mcq(T, "Hard", "Steepest-ascent hill climbing solves only 14% of random 8-queens instances. Allowing up to 100 consecutive sideways moves raises this to about:",
    "94%", ["24%", "50%", "100%"], "Sideways moves let the search cross shoulders (flat regions) instead of stopping, at the price of more steps per run.",
    "A big jump.", search=True)
fib(T, "Hard", "Steepest-ascent solves 14% of 8-queens instances, taking about 4 steps when it succeeds and 3 when it gets stuck. With random restarts (about 7 runs: 6 failures + 1 success) the expected total steps is about ______.",
    ["22"], "6 x 3 + 4 = 22 steps (AIMA Sec. 4.1.1).", "6 x 3 + 4.", kind="Problem Solving", search=True)
mcq(T, "Hard", "A hill-climbing 8-queens solver stops at a state with h = 1 attacking pair where every neighbour has h >= 1. What has happened?",
    "It is stuck at a local minimum of the cost h (a local optimum)",
    ["It has found the global optimum", "It has reached a goal state", "It is on a plateau of goal states"],
    "A goal needs h = 0. All neighbours are no better, so the search is trapped; random restarts help.", "Is h = 1 a goal?",
    kind="Scenario", real=True, search=True)

# =============================================================== Heuristic Search
T = "Heuristic Search"
mcq(T, "Medium", "A heuristic h(n) is admissible if it:",
    "never overestimates the true cost to reach the goal", ["always overestimates the true cost", "equals g(n) at every node", "is always zero"],
    "Admissible means optimistic. A* tree search with an admissible heuristic is optimal.", "Optimistic.")
puz = "```\nStart      Goal\n7 2 4      _ 1 2\n5 _ 6      3 4 5\n8 3 1      6 7 8\n```"
fib(T, "Medium", f"8-puzzle (AIMA Fig. 3.28): the number of misplaced tiles h1 for the start state (blank not counted) is ______.\n\n{puz}",
    ["8"], "All 8 tiles are out of place.", "Compare tile by tile.", kind="Problem Solving", search=True)
fib(T, "Hard", f"For the same start and goal, the sum of Manhattan distances h2 is ______.\n\n{puz}",
    ["18"], "Distances: 7:3, 2:1, 4:2, 5:2, 6:3, 8:2, 3:2, 1:3 -> total 18.", "Rows plus columns away from goal position.",
    kind="Problem Solving", search=True)
mcq(T, "Hard", "AIMA shows h1 (misplaced tiles) and h2 (Manhattan distance) are the exact costs of relaxed versions of the 8-puzzle. Which relaxations?",
    "h1: a tile can move to any square; h2: a tile can move to any adjacent square, even if occupied",
    ["h1: a tile can move to any adjacent square; h2: a tile can move anywhere", "Both: the blank can jump anywhere",
     "h1: tiles may be removed; h2: tiles may be swapped freely"],
    "The cost of an optimal solution to a relaxed problem is an admissible heuristic for the original (AIMA Sec. 3.6.2).",
    "Weaker rules, easier problem.", search=True)
mcq(T, "Hard", "A* finds a solution at depth 5 after generating N = 52 nodes. The effective branching factor b* solves N + 1 = 1 + b* + b*^2 + ... + b*^5. It is about:",
    "1.92", ["1.52", "2.41", "3.10"], "b* = 1.92 (AIMA Sec. 3.6.1). A good heuristic has b* close to 1.", "Between 1 and 2.",
    kind="Problem Solving", search=True)
tf(T, "Hard", "Every consistent heuristic is admissible, but not every admissible heuristic is consistent.", True,
   "Consistency (h(n) <= c(n,a,n') + h(n')) is the triangle inequality and implies admissibility; the reverse can fail.",
   "Triangle inequality.", search=True)
mcq(T, "Medium", "A delivery app uses straight-line distance as the heuristic for road distance. Why is it admissible?",
    "No road can be shorter than the straight line between two points",
    ["Roads are always straight", "It equals the actual cost at every city", "It is always larger than the road distance"],
    "A straight line is the shortest possible path, so it never overestimates.", "Can a road beat a straight line?",
    kind="Scenario", real=True, search=True)

# =============================================================== Best First Search
T = "Best First Search"
mcq(T, "Easy", "Greedy best-first search evaluates nodes using:", "f(n) = h(n)", ["f(n) = g(n)", "f(n) = g(n) + h(n)", "f(n) = depth(n)"],
    "Greedy picks the node that looks closest to the goal; A* uses f(n) = g(n) + h(n).", "Only the heuristic.", search=True)
tf(T, "Medium", "Greedy best-first search is always optimal.", False,
   "It ignores g(n), so it can pick a longer path that merely looks promising.", "It ignores the cost so far.", search=True)
mcq(T, "Hard", "Straight-line distances to Bucharest (inside the nodes) and road costs (on the edges) are shown. Greedy best-first search from Arad to Bucharest returns:",
    "Arad - Sibiu - Fagaras - Bucharest, cost 450",
    ["Arad - Sibiu - Rimnicu Vilcea - Pitesti - Bucharest, cost 418", "Arad - Timisoara - Bucharest, cost 329",
     "Arad - Zerind - Oradea - Sibiu - Fagaras - Bucharest, cost 647"],
    "Greedy picks Sibiu (253), then Fagaras (176 < 193), then Bucharest: 140 + 99 + 211 = 450.",
    "Always pick the smallest h.", kind="Problem Solving", search=True, graph=G_ROM)
mcq(T, "Hard", "For the same map, in what order does A* (graph search) EXPAND nodes from Arad until it expands Bucharest?",
    "Arad, Sibiu, Rimnicu Vilcea, Fagaras, Pitesti, Bucharest",
    ["Arad, Sibiu, Fagaras, Bucharest", "Arad, Sibiu, Rimnicu Vilcea, Pitesti, Bucharest", "Arad, Timisoara, Zerind, Sibiu, Fagaras, Bucharest"],
    "f(Sibiu)=393, then f(RV)=413, f(Fagaras)=415, f(Pitesti)=417, f(Bucharest via Pitesti)=418 beats 450 via Fagaras.",
    "Use f = g + h and always expand the smallest f.", kind="Problem Solving", search=True, graph=G_ROM)
fib(T, "Hard", "On the same map, the greedy path (cost 450) is longer than the optimal path found by A* by ______.",
    ["32"], "A* returns Arad - Sibiu - Rimnicu Vilcea - Pitesti - Bucharest with cost 140 + 80 + 97 + 101 = 418, so 450 - 418 = 32.",
    "Compute the optimal cost first.", kind="Problem Solving", search=True, graph=G_ROM)
tf(T, "Hard", "Greedy best-first TREE search is incomplete even in a finite state space.", True,
   "It can oscillate between promising-looking states or dead ends (AIMA's Iasi to Fagaras example). The graph-search version is complete in finite spaces.",
   "Think of repeated states.", search=True)
mcq(T, "Hard", "A* graph search is guaranteed to return an optimal solution if the heuristic is:",
    "Consistent", ["Always zero", "Greater than the true cost", "Equal to g(n)"],
    "Tree search needs admissibility; graph search needs consistency so the first path found to a node is optimal.",
    "Triangle inequality.", search=True)

# =============================================================== CSP
T = "CSP"
mcq(T, "Easy", "A constraint satisfaction problem is defined by:", "Variables, domains and constraints",
    ["States, actions and path costs", "Percepts, actions and goals", "Rules, facts and a control strategy"],
    "Assign each variable a value from its domain without violating constraints.", "V, D, C.")
mcq(T, "Medium", "In exam timetabling, what are the variables of the CSP?",
    "The exams (each to be assigned a time slot)", ["The time slots", "The students", "The invigilators' salaries"],
    "Variables = exams, domains = slots, constraints = exams sharing students cannot share a slot.", "What needs a value?",
    kind="Scenario", real=True, search=True)
mcq(T, "Medium", "Map colouring (AIMA's Australia) with {red, green, blue}: if WA = red and NT = green, which colour must SA take?",
    "Blue", ["Red", "Green", "Any colour"], "SA is adjacent to both WA and NT, so red and green are ruled out.",
    "Remove the neighbours' colours.", kind="Problem Solving", search=True, graph=G_AUS_WA_NT)
mcq(T, "Medium", "The Minimum Remaining Values (MRV) heuristic chooses the next variable that:",
    "has the fewest legal values left", ["has the most legal values left", "appears first alphabetically", "is involved in the fewest constraints"],
    "'Fail-first': pick the most constrained variable.", "Most constrained.", search=True)
mcq(T, "Hard", "At the start of the Australia map-colouring problem, the degree heuristic picks which variable first?",
    "SA", ["WA", "TAS", "NSW"], "SA touches 5 other regions (WA, NT, Q, NSW, V), more than any other. TAS has none.",
    "Count the neighbours.", kind="Problem Solving", search=True, graph=G_AUS)
mcq(T, "Hard", "With forward checking, WA = red, Q = green and V = blue have been assigned. What does forward checking detect?",
    "SA's domain becomes empty, so the search backtracks immediately",
    ["NT's domain becomes empty", "A solution has been found", "Nothing: all domains are still non-empty"],
    "SA is adjacent to WA (red), Q (green) and V (blue), so no colour is left (AIMA Fig. 6.7).",
    "Which region touches all three coloured ones?", kind="Problem Solving", search=True, graph=G_AUS_FC)
mcq(T, "Hard", "X and Y both have domain {1,2,3} with constraint X < Y. After making the arc X -> Y consistent, the domain of X becomes:",
    "{1, 2}", ["{1, 2, 3}", "{2, 3}", "{3}"], "X = 3 has no Y greater than 3, so it is removed.",
    "Does every X value have a supporting Y?", kind="Problem Solving", search=True)
mcq(T, "Medium", "The least-constraining-value heuristic prefers the value that:",
    "rules out the fewest choices for neighbouring variables", ["rules out the most choices for neighbours", "is numerically smallest", "was used most recently"],
    "It keeps the most flexibility for the remaining variables.", "Least constraining.", search=True)

# =============================================================== Means-End Analysis
T = "Means-End Analysis"
mcq(T, "Easy", "Means-end analysis works by repeatedly:", "reducing the difference between the current state and the goal state",
    ["trying random moves", "expanding all nodes level by level", "colouring graph nodes"],
    "It picks an operator that reduces the most significant difference.", "Difference reduction.")
mcq(T, "Medium", "Which early AI program famously used means-end analysis?", "General Problem Solver (GPS) by Newell and Simon",
    ["MYCIN", "Deep Blue", "ELIZA"], "GPS (1957) used means-end analysis.", "Newell and Simon.", ref="AIMA Ch.1 (Sec. 1.3); Rich & Knight Ch.3")
mcq(T, "Medium", "A robot must move a box from Room A to Room B but is standing in Room C. PUSH needs the robot beside the box. What does means-end analysis do next?",
    "Sets up a sub-goal to get the robot to the box (WALK to Room A)", ["Gives up because PUSH is not applicable", "Applies PUSH anyway", "Restarts from a random state"],
    "When the chosen operator's preconditions are not met, MEA creates a sub-goal to satisfy them.", "Satisfy the precondition first.",
    kind="Scenario", real=True)
tf(T, "Hard", "Means-end analysis can be seen as mixing forward and backward reasoning: it reduces differences from the current state and sets sub-goals from operator preconditions.", True,
   "Operators are chosen by relevance to the difference, then the problem splits into reaching the operator's preconditions and continuing from its result.",
   "Look at both ends of the operator.")
mcq(T, "Hard", "In Rich & Knight's household-robot example, which operators are listed for reducing the difference 'move object'?",
    "PUSH and CARRY", ["WALK and PICKUP", "PLACE and PUTDOWN", "PICKUP only"],
    "The difference table maps: move object -> PUSH, CARRY; move robot -> WALK; clear object -> PICKUP; and so on.",
    "Which operators change an object's location?", real=True)

# ---- extra conceptual fill-in-the-blank questions
fib("Turing Test", "Easy", "The Turing Test was proposed by ______ in 1950.", ["alan turing", "turing", "a. m. turing"],
    "Alan Turing proposed it in 'Computing Machinery and Intelligence' (1950).", "He is also known for breaking the Enigma code.")
fib("Hill Climbing", "Medium", "In simulated annealing, the probability of accepting a bad move decreases as the ______ decreases.",
    ["temperature"], "A cooling schedule: high T accepts many bad moves, low T almost none.", "Metallurgy word.")
fib("Problems & Problem Spaces", "Medium", "A sequence of actions leading from the initial state to a goal state is called a ______.",
    ["solution", "solution path"], "An optimal solution has the lowest path cost among all solutions.", "What does the search return?")
fib("Nature of Environments", "Medium", "An environment in which the current decision can affect all future decisions is called ______.",
    ["sequential"], "Chess and taxi driving are sequential; classifying one image is episodic.", "Opposite of episodic.")

for _i, _q in enumerate(QUESTIONS, 1):
    _q["id"] = _i
    if _q["type"] in ("mcq", "tf", "ar"):
        assert _q["answer"] in _q["options"], _i
    assert _q["topic"] in TOPICS, _q["topic"]
