# 03. Li turns the sum into paired objects

Li replaces the analytic sum by signed objects carrying marked intersections. The first involution changes the mate along an opposite-edge cycle while leaving the second state fixed. Its fixed objects are the useful forest states. The second involution follows a different rule: reverse an unmarked D-cycle, or pair successive intersections on a ray from a white face. The remaining objects have a common sign. The picture shows a checked first-involution pair on our running triangulation. The second-involution marks below are computed by exact ray intersections on the cube. On the running triangulation the minimum D-cycle count is two, so the one-mark implementation is insufficient. The laboratory contains a multi-mark extension, but the determinant referee explicitly excluded that implementation from review. The conceptual second involution is in Li's supplied paper; the cube calculation checks the one-mark involution and every sign change.

Status: LIT: Li, Definitions 13 to 23 and Appendix B. COMPUTED: first involution here. COMPUTED cube one-mark involution and signs; multi-mark implementation has not been independently refereed.

Connects to: 2 exponential terms; 4 linear weights; 26 open doors.

Sources: papers/A-Note-On-Barnette.pdf; workings/barnette_lab/barnette_lab/li.py; fable_referee-determinants/REPORT.md.

COMPUTED figure provenance: build.py, computed.json, picture kind `li`.
