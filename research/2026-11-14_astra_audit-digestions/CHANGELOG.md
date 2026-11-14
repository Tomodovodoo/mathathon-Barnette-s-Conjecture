# Change log

Exact textual edits are in outputs/canonical-changes.patch. That patch covers all tracked canonical edits against the parent of audit commit 50a7556; the two new PNGs are listed below. Replacement-level prose ledgers are outputs/edits.json and outputs/reader-edits.json. One-time migration scripts preserve subsequent route, status and wording edits.

## Changes by purpose

- Steps 00–09 and glossary: findings A01–A11, A21, A23, A25–A27; ten reader bridges; explicit Li fixed-point data and orientation comparison.
- HOW-IT-WORKS: corrected modular-count scope, cycle signs, Li mark multiplicities, lattice status and the meaning of route labels.
- routes.py: added new manuscript, family and older-approach routes; corrected LP and matroid claims; integrated the late topology referee and provisional lattice refutation.
- build_map.py: source/shared/choice labels and proof-supplied matrix legend; regenerated every map, overview, matrix, DOT, JSON and written inventory.
- seed.py: preprint tier policy, claim-specific reviews, append-only event preservation, SOTA history and new manuscript row.
- labyrinth data, STATUS and dashboard: regenerated from canonical sources. README tier explanation corrected. Existing frontier data unchanged.
- Two new step figures: generated from the figure toolkit without editing paper/figures.

## Every changed canonical file

| File | Bytes | SHA-256 |
|---|---:|---|
| `digestions/route-map/HOW-IT-WORKS.md` | 20589 | `9557652a892e92c59de7d4e052a3d55a62fd58eae02494a44421027ad977f3d2` |
| `digestions/route-map/ROUTE-MAP.md` | 89770 | `0039b8d551b98a6d4f9d62f063dd29e85da16a6ee8089ac84f4c3e18c299453e` |
| `digestions/route-map/build_map.py` | 32616 | `f2e72e468a5f06c64569380490b084e5d15c29744d3f11136a0b0c5e8c8d77ab` |
| `digestions/route-map/route-kinds.pdf` | 45582 | `27f1d974305400092e8cff559d8098a8b530a6dd9fbc3bb9abf3fea13cddb4aa` |
| `digestions/route-map/route-kinds.png` | 216905 | `ca30e303b7a82d9cb7cf327aa927dcfb718c06015c73fe0cb9e5db51bd95149b` |
| `digestions/route-map/route-kinds.svg` | 236878 | `46a5abf0d7d3d109e9ea535460ae3b0dab10f5d096396089f4ad694908a20b94` |
| `digestions/route-map/route-map-overview.pdf` | 62092 | `a2fad5d9f7e5de4010191d1a99276416d5d3238874b7407f580c48a4208ac55e` |
| `digestions/route-map/route-map-overview.png` | 467631 | `424766fd3fedb6b7d3ab625e4f921b3461e99e2a01b51f3b2e82f9091982697c` |
| `digestions/route-map/route-map-overview.svg` | 308723 | `89b63f7746c2f7ad0a6090ede1431345ea603f3e234618ef7c78292fe26235a1` |
| `digestions/route-map/route-map.dot` | 26636 | `4231bfd0153d61a86ded7058a3df099fb502b21110313d037273ace873a525c8` |
| `digestions/route-map/route-map.pdf` | 101380 | `b889c8e714c851bd0705b01b4324f7c8cbf32727752a7c2b55c13446fd18c967` |
| `digestions/route-map/route-map.png` | 1502649 | `2fa6aac739a3af72cb5ba94044b720fda2bbee518db4c966273dbf9f412f05bb` |
| `digestions/route-map/route-map.svg` | 1099780 | `333dbf2f1fa424088aa75726852ffdb190673a5e9addecd3e71d61dd235f0a5c` |
| `digestions/route-map/routes.json` | 101690 | `94e0a85798c6f0f949e9073166082e808cc15539f3f34deb3f2a4b807cac0eec` |
| `digestions/route-map/routes.py` | 95601 | `faf83f391974e5840e433df5cb72ecda6f8acb52fb31d8ceacfe2e3f9344a805` |
| `digestions/steps/00-overview.md` | 9065 | `8b9174a637a570907822cde8ed268a5e8adeb3271534cbbd57992c69d6e53590` |
| `digestions/steps/01-degree-two-and-connectivity.md` | 8224 | `3fdfcc5b00a2d2dba6ced93893e9ae546b154aaa1b4b9869d13a2c432e5e3668` |
| `digestions/steps/02-dual-and-two-trees.md` | 13015 | `9aa5664026b26ed541cbf0d834da0909fbb772da0bc70b6e7cb5969e44ffddf0` |
| `digestions/steps/03-states-and-pairs.md` | 15335 | `66898b20b9c168873b26babb703cd5e8a3d31a3d19903d2c128ef12490d362ef` |
| `digestions/steps/04-disk-identity.md` | 11669 | `138405cabb317bbc138c585fe45ff50729ef4eea2c145a5ed1c78aacf69fa092` |
| `digestions/steps/05-cancellation.md` | 11948 | `87aec1a86f872286d807ce5dc192622c2bf6c903e82baabd1468ee9d17e07d16` |
| `digestions/steps/06-nonvanishing.md` | 23432 | `1ca512b3f3ea58ba2abc25d19dc34abcb180e5bbb5efc83387d1f1993fe0802a` |
| `digestions/steps/07-recovery.md` | 12914 | `09ecda52660f37771f14d0ca52a61620161dfc7bc35a563022902f6647e87cba` |
| `digestions/steps/08-gluing-and-hypotheses.md` | 13058 | `29cd5d1b689e06cf875861ebf2f15bfe0406337eb2e1768488b1a4b0f572c261` |
| `digestions/steps/09-what-is-still-open.md` | 17214 | `e9cea8d3cf257d4db9af364075b77282d7879dd0132e5cf57e485d6efaaf9088` |
| `digestions/steps/GLOSSARY.md` | 11815 | `14c732960def94565d31ca8a77ed2026bb5f8e312d107442a3abaf6b6e35a62a` |
| `digestions/steps/img/bad-cover-16.png` | 244124 | `f86899a2bc56ca4c57eb4282afe0571528572e1d1ec2ff98d6a715cdfb1017bc` |
| `digestions/steps/img/two-covers.png` | 223966 | `f95dce0ed055b765fba895977ddef4411e8e3bed5b806e3db6c54fef421b97ca` |
| `labyrinth/README.md` | 5600 | `0f24d30523b11b956086aa5b460b2f78dc22ddac9fb8dfa4265b84be0bc100b3` |
| `labyrinth/STATUS.md` | 23499 | `8d5adbc35b0f72a9ff6fc5223335b294e89e4f38f923a558f28ed37e40eb50fc` |
| `labyrinth/dashboard/data.json` | 403523 | `040ddc820e725de80991c52561d8fc43ddd15e4b1c6bc4ab9ba0476b2f5797a7` |
| `labyrinth/dashboard/index.html` | 461538 | `8d19f264053e24267d287150177de4228f00c080e469233bad81d1308a97b3cc` |
| `labyrinth/events.jsonl` | 15806 | `46c569863027cff944841256c4aafa507c712eccee1171b73c7a62c35851b6e9` |
| `labyrinth/knowledge.json` | 236584 | `359695f7d2feaa2d34c277367f31a6fe160cec613bcde6c1cf21ae01e07eec60` |
| `labyrinth/seed.py` | 43985 | `6e57bbace5bf7b34924b2c20595c68b7e5df364413a30e588632e13742c80096` |
| `labyrinth/sota.json` | 11923 | `082b8cb99530c183000ed4272d53337d501aafd4d28179b3041e53ce96ef79e0` |
