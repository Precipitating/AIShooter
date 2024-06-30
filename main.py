import os
import pickle
from shooterenv import *


local_dir = os.path.dirname(__file__)
config_path = os.path.join(local_dir, "config2.txt")

config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     config_path)


def eval_genomes(genomes, config):
    for i, (genome_id1, genome1) in enumerate(genomes):
        genome1.fitness = 0
        game = Game()
        game.train_ai(genome1, config)


def run_neat(config):
   # p = neat.Checkpointer.restore_checkpoint('finished')
    p = neat.Population(config)
    p.config.inputs = 8
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1))
    winner = p.run(eval_genomes, 200)
    with open("best.pickle", "wb") as f:
        pickle.dump(winner, f)

def test_ai(config):
    with open("best.pickle", "rb") as f:
        pickle.load(f)
    game = Game()


run_neat(config)







