Phrase conclusion: dernière phrase
 we can say with confidence: safe, functional destination passing is not an
oxymoron—it exists!

En effet, on en avait l'intuition avec le début des travaux pratiques.

Mais on a identifié des dangers, qu'on a contrecarré avec des limitations

On s'est donc libéré des contraintes d'implem, et avons cherché à a formaliser, et on a obtenu la preuve formelle qu'on peut baser un système de langage fonctionnel que sur du destination-passing

Articulation: l'objectif est d'avoir une implémentation, on redescend au niveau implem.
Ce système s'exporte plus ou moins bien vers des langages concrets en fonction de la richesse du système de type. Avec des types linéaires seulement, on peut retrouver +/- de ce qu'on a dans le système théorique en fonction du curseur qu'on place sur la complexité de l'API visée.

Marquer rupture contributions/perspectives

__________________

At the end of this long journey, we can say with confidence: safe, functional destination passing is not an
oxymoron---it exists!

Initial experiments with destination-passing style programming in Haskell---that actually actually predate the theoretical development of \destcalculus{}---gave us the intuition that linear types were, in effect, a powerful way to tame the impure nature of destinations and make it compatible with a pure language[...]

However scope escape was discovered not long after. If we were able to immediately avoid scope escape by imposing harsher restrictions on the use of destinations, this made us aware that having a proper formalization of functional destination passing would help us to evolve towards a system that we are confident is safe.

So we freed ourselves from the implementation details, and started fresh with a calculus based on destinations at its heart, even bypassing the need for usual functional data constructors. We obtained the formal proof that this calculi is sound. To permit this, the calculus has a few notable features:
- linear
- age system in addition because [...]
- operational semantics based on linear substitutions on the evaluation context (as a light form of state update)

With this in hand, we were able to circle back to one of our initial goals: practical destination passing in a functional language. We chose Haskell as a target[...], which has a rich type system, with support for linear types. But it doesn't support age or any form of scope control.

So there is a balance to be found between the simplicity of the destination passing API, and the expressiveness we obtain. In destcalculus we could have both, at the expense of a tailored type system featuring ages.

Consequently, we iterate over various concrete destination-passing APIs [...]. Notably, we recover, at the end, a practical system in which the motivating examples of destcalculus can all be implemented, with no adaptations further than mere translation of a syntax to another.

Another core contribution of our practical work is that the destination-passing API leverages, but also extends what can be done with Compact regions in Haskell. [...]

[INSERT POSSIBLE IMPROVEMENTS]