import Projection
import numpy as np

class SimpleTerm(Projection.ProjectionPP):
    
    def runDecrements(self):
        self.polsIF_bop = np.ones(self.RunConfig.proj_term)
