# Local research map

This map belongs only to the dimer-route agent. It does not update the coordinator's canonical findings. All four theorem nodes are T2 unreviewed. Sampled numerical evidence is T4.

Run from this folder's parent:

    python -B code/map.py
    python -X utf8 -B labyrinth/lab.py check
    python -X utf8 -B labyrinth/lab.py build

Dashboard: dashboard/index.html. It stays local. The frontier's zero value means no disjoint pair; positive values are minimum D-cycle counts observed on stored rooted examples. Unobserved values remain unknown. events.jsonl here is generated from the agent's append-only event log one directory above.
