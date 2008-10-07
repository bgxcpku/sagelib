"""
Functorial composition species
"""
#*****************************************************************************
#       Copyright (C) 2008 Mike Hansen <mhansen@gmail.com>, 
#
#  Distributed under the terms of the GNU General Public License (GPL)
#
#    This code is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#    General Public License for more details.
#
#  The full text of the GPL is available at:
#
#                  http://www.gnu.org/licenses/
#*****************************************************************************
from species import GenericCombinatorialSpecies
from structure import GenericSpeciesStructure
from sage.misc.cachefunc import cached_function

class FunctorialCompositionStructure(GenericSpeciesStructure):
    pass

@cached_function
def FunctorialCompositionSpecies(*args, **kwds):
    """
    Returns the functorial composition of two species.

    EXAMPLES:
        sage: E = species.SetSpecies()
        sage: E2 = species.SetSpecies(size=2)
        sage: WP = species.SubsetSpecies()
        sage: P2 = E2*E
        sage: G = WP.functorial_composition(P2)
        sage: G.isotype_generating_series().coefficients(5)
        [1, 1, 2, 4, 11]

    """
    return FunctorialCompositionSpecies_class(*args, **kwds)

class FunctorialCompositionSpecies_class(GenericCombinatorialSpecies):
    def __init__(self, F, G, min=None, max=None, weight=None):
        """
        EXAMPLES:
            sage: G = species.SimpleGraphSpecies()
            sage: c = G.generating_series().coefficients(2)
            sage: type(G)
            <class 'sage.combinat.species.functorial_composition_species.FunctorialCompositionSpecies_class'>
            sage: G == loads(dumps(G))
            True
            sage: G._check() #False due to isomorphism types not being implemented
            False

        """
        self._F = F
        self._G = G
        self._state_info = [F, G]
        self._name = "Functorial composition of (%s) and (%s)"%(F, G)
        GenericCombinatorialSpecies.__init__(self, min=None, max=None, weight=None)

    _default_structure_class = FunctorialCompositionStructure

    _cached_constructor = staticmethod(FunctorialCompositionSpecies)

    def _structures(self, structure_class, s):
        """
        EXAMPLES:
            sage: G = species.SimpleGraphSpecies()
            sage: G.structures([1,2,3]).list()
            [{},
             {{1, 2}*{3}},
             {{1, 3}*{2}},
             {{2, 3}*{1}},
             {{1, 2}*{3}, {1, 3}*{2}},
             {{1, 2}*{3}, {2, 3}*{1}},
             {{1, 3}*{2}, {2, 3}*{1}},
             {{1, 2}*{3}, {1, 3}*{2}, {2, 3}*{1}}]
        """
        gs = self._G.structures(s).list()
        for f in self._F.structures(gs):
            yield f
        
    def _isotypes(self, structure_class, s):
        """
        There is no known algorithm for efficiently generating the isomorphism types
        of the functorial composition of two species.

        EXAMPLES:
            sage: G = species.SimpleGraphSpecies()
            sage: G.isotypes([1,2,3]).list()
            Traceback (most recent call last):
            ...
            NotImplementedError
        """
        raise NotImplementedError

    
    def _gs(self, series_ring, base_ring):
        """
        EXAMPLES:
            sage: G = species.SimpleGraphSpecies()
            sage: G.generating_series().coefficients(5)
            [1, 1, 1, 4/3, 8/3]

        """
        return self._F.generating_series(base_ring).functorial_composition(self._G.generating_series(base_ring))

    def _itgs(self, series_ring, base_ring):
        """
        EXAMPLES:
            sage: G = species.SimpleGraphSpecies()
            sage: G.isotype_generating_series().coefficients(5)
            [1, 1, 2, 4, 11]
        """
        return self.cycle_index_series(base_ring).isotype_generating_series()
    
    def _cis(self, series_ring, base_ring):
        """
        EXAMPLES:
            sage: G = species.SimpleGraphSpecies()
            sage: G.cycle_index_series().coefficients(5)
            [p[],
             p[1],
             p[1, 1] + p[2],
             4/3*p[1, 1, 1] + 2*p[2, 1] + 2/3*p[3],
             8/3*p[1, 1, 1, 1] + 4*p[2, 1, 1] + 2*p[2, 2] + 4/3*p[3, 1] + p[4]]
        """
        return  self._F.cycle_index_series(base_ring).functorial_composition(self._G.cycle_index_series(base_ring))
    
    def weight_ring(self):
        """
        Returns the weight ring for this species.  This is determined by asking
        Sage's coercion model what the result is when you multiply (and add)
        lements of the weight rings for each of the operands.

        EXAMPLES:
            sage: G = species.SimpleGraphSpecies()
            sage: G.weight_ring()
            Rational Field
        """
        from sage.structure.element import get_coercion_model
        cm = get_coercion_model()

        f_weights = self._F.weight_ring()
        g_weights = self._G.weight_ring()
        
        return cm.explain(f_weights, g_weights, verbosity=0)
