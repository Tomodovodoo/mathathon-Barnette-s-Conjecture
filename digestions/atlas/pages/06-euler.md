# 06. The disk identity as a census

The long directed cycle in the running pair encloses five black triangles, six white triangles, and three strictly interior vertices. It has seven boundary edges, two with the black triangle on the inside. These are actual counts produced by cutting the dual adjacency graph at the cycle. The state bijection accounts for the five interior black faces by three interior choices and two inward boundary choices. Thus B equals I plus l. Euler's disk formula gives B plus W equals twice I plus h minus two. Counting signed triangle sides gives three times B minus W equals twice l minus h. Combining the equations forces the signed boundary sum to have magnitude three. The shaded region is the disk away from the root face. Moving the roots into that disk would invalidate the matching count.

Status: LIT: OpenAI Lemma 4.1. COMPUTED: B=5, W=6, I=3, h=7, l=2; all D and directed Q cycles of all pairs also checked.

Connects to: 7 white surplus; 8 turning angles; 21 hypotheses.

Sources: papers/OpenAI-Barnette.pdf, Lemma 4.1; paper/figures/model.py, disk; build.py.

COMPUTED figure provenance: build.py, computed.json, picture kind `count`.
