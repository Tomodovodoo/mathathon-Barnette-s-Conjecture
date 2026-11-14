/* bar.c -- lattice extremes, tree pairs, c_min and #TM for rooted Eulerian triangulations.

   Input (stdin): plantri planar code (default; neighbours clockwise, 1-based)
                  or with -t a text format, one graph per line:
                  V  d_0 n n n ...  d_1 n n ...   (neighbours counterclockwise, 0-based)
   Every face is tried as root t0 (coloured black), unless -r k (k random roots per graph).

   Modes:
     -m ext   : compute both lattice extremes exactly, count tree pairs in each   (C2)
     -m full  : additionally enumerate the whole lattice of 2-factors: c_min, #TM,
                which elements carry tree pairs                                    (C1, C2 refined)
   Conventions (see CONJECTURES.md, section 1):
     rotation ccw, faces traced with interior on the left.
     H_0 faces = white faces, the three white faces at t0 merged into node 0 (outer).
     alpha-orientations <-> integer potentials phi on H_0-faces, phi(outer)=0, with
        phi(R_e) - phi(L_e) in {-1,0} for each spoke e (L,R w.r.t. reference direction),
        value -1 iff e is reversed relative to the reference orientation.
     phi-maximal element = FMIN (Felsner minimum: no counterclockwise directed cycle),
     phi-minimal element = FMAX (no clockwise directed cycle).  Checked in check_conv().
*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAXV 600
#define MAXF (2*MAXV)
#define MAXD 128

static int nv, nf, deg[MAXV], adj[MAXV][MAXD], rev_[MAXV][MAXD];
static int fd[MAXV][MAXD];          /* face left of dart (v,k) */
static int fv[MAXF][3];             /* face vertices in ccw order */
static int across[MAXF][3];         /* face across edge fv[i]->fv[i+1] */
static int col[MAXF];

static long long g_count = 0;

/* ---------- reading ---------- */
static int read_planar(FILE *f) {
    static int header = 0;
    if (!header) {
        char h[16];
        if (fread(h, 1, 15, f) != 15) return 0;
        header = 1;
    }
    int c = fgetc(f);
    if (c == EOF) return 0;
    int n = c, two = 0;
    if (n == 0) { two = 1; int a = fgetc(f), b = fgetc(f); n = a | (b << 8); }
    nv = n;
    for (int v = 0; v < n; v++) {
        int tmp[MAXD], d = 0;
        for (;;) {
            int x;
            if (two) { int a = fgetc(f), b = fgetc(f); x = a | (b << 8); }
            else x = fgetc(f);
            if (x == 0) break;
            tmp[d++] = x - 1;
        }
        deg[v] = d;
        for (int k = 0; k < d; k++) adj[v][k] = tmp[d - 1 - k];   /* cw -> ccw */
    }
    return 1;
}
static int printu = 0;
static FILE *ufile = NULL;
static int given_root[3], use_given_root = 0;
static int read_text(FILE *f) {
    if (fscanf(f, "%d", &nv) != 1) return 0;
    for (int v = 0; v < nv; v++) {
        if (fscanf(f, "%d", &deg[v]) != 1) return 0;
        for (int k = 0; k < deg[v]; k++) if (fscanf(f, "%d", &adj[v][k]) != 1) return 0;
    }
    if (use_given_root) for (int i = 0; i < 3; i++) if (fscanf(f, "%d", &given_root[i]) != 1) return 0;
    return 1;
}

static void build_faces(void) {
    for (int v = 0; v < nv; v++)
        for (int k = 0; k < deg[v]; k++) {
            int w = adj[v][k], j;
            for (j = 0; j < deg[w]; j++) if (adj[w][j] == v) break;
            if (j == deg[w]) { fprintf(stderr, "bad rotation\n"); exit(1); }
            rev_[v][k] = j;
            fd[v][k] = -1;
        }
    nf = 0;
    for (int v = 0; v < nv; v++)
        for (int k = 0; k < deg[v]; k++) {
            if (fd[v][k] >= 0) continue;
            int a = v, ka = k, len = 0;
            while (fd[a][ka] < 0) {
                fd[a][ka] = nf;
                if (len >= 3) { fprintf(stderr, "non-triangular face\n"); exit(1); }
                fv[nf][len++] = a;
                int b = adj[a][ka], j = rev_[a][ka];
                int kb = (j - 1 + deg[b]) % deg[b];   /* predecessor of a around b */
                a = b; ka = kb;
            }
            if (len != 3) { fprintf(stderr, "face len %d\n", len); exit(1); }
            nf++;
        }
    if (nf != 2 * nv - 4) { fprintf(stderr, "Euler fail nf=%d nv=%d\n", nf, nv); exit(1); }
    for (int f = 0; f < nf; f++)
        for (int i = 0; i < 3; i++) {
            int a = fv[f][i], b = fv[f][(i + 1) % 3], k;
            for (k = 0; k < deg[b]; k++) if (adj[b][k] == a) break;
            across[f][i] = fd[b][k];
        }
    /* 2-colouring */
    for (int f = 0; f < nf; f++) col[f] = -1;
    int q[MAXF], qh = 0, qt = 0;
    col[0] = 0; q[qt++] = 0;
    while (qh < qt) {
        int f = q[qh++];
        for (int i = 0; i < 3; i++) {
            int g = across[f][i];
            if (col[g] < 0) { col[g] = 1 - col[f]; q[qt++] = g; }
            else if (col[g] == col[f]) { fprintf(stderr, "not Eulerian\n"); exit(1); }
        }
    }
}

/* ---------- rooted instance ---------- */
static int f0, n, isroot[MAXV], nA, Af[MAXV], aidx[MAXF];
static int wnode[MAXF], nW;             /* white face -> H0 face node (0 = outer) */
static int spL[MAXV][3], spR[MAXV][3];  /* spoke (t,i) directed t->corner: left/right node */
static int u0[MAXV];                    /* reference deleted corner (corner index 0..2) */
static int hasroot[MAXV];

static int is_black(int f) { return col[f] == col[f0]; }

/* b-matching: free faces choose u among corners, capacity b_x-2 at nonroot x */
static int capx[MAXV], load[MAXV], vis[MAXV];
/* simpler correct version: standard Kuhn with explicit visited on vertices */
static int owner_cnt[MAXV];
static int kuhn(int t) {
    for (int i = 0; i < 3; i++) {
        int x = fv[Af[t]][i];
        if (vis[x]) continue;
        vis[x] = 1;
        if (load[x] < capx[x]) { load[x]++; u0[t] = i; return 1; }
        for (int s = 0; s < nA; s++) {
            if (hasroot[s] || s == t || u0[s] < 0 || fv[Af[s]][u0[s]] != x) continue;
            int old = u0[s];
            u0[s] = -1; load[x]--;
            if (kuhn(s)) { load[x]++; u0[t] = i; return 1; }
            u0[s] = old; load[x]++;
        }
    }
    return 0;
}

static int setup_root(int froot) {
    f0 = froot;
    memset(isroot, 0, sizeof(int) * nv);
    for (int i = 0; i < 3; i++) isroot[fv[f0][i]] = 1;
    n = nv - 3;
    nA = 0;
    for (int f = 0; f < nf; f++) {
        aidx[f] = -1;
        if (is_black(f) && f != f0) { aidx[f] = nA; Af[nA++] = f; }
    }
    if (nA != n) { fprintf(stderr, "nA != n\n"); exit(1); }
    /* white nodes */
    nW = 1;
    for (int f = 0; f < nf; f++) {
        if (is_black(f)) { wnode[f] = -1; continue; }
        int outer = 0;
        for (int i = 0; i < 3; i++) if (across[f][i] == f0) outer = 1;
        wnode[f] = outer ? 0 : nW++;
    }
    for (int t = 0; t < nA; t++) {
        int f = Af[t];
        hasroot[t] = -1;
        for (int i = 0; i < 3; i++) {
            spL[t][i] = wnode[across[f][i]];
            spR[t][i] = wnode[across[f][(i + 2) % 3]];
            if (isroot[fv[f][i]]) hasroot[t] = i;
        }
    }
    for (int v = 0; v < nv; v++) { capx[v] = isroot[v] ? 0 : deg[v] / 2 - 2; load[v] = 0; }
    for (int t = 0; t < nA; t++) {
        if (hasroot[t] >= 0) { u0[t] = hasroot[t]; hasroot[t] = 1; } else { u0[t] = -1; hasroot[t] = 0; }
    }
    for (int t = 0; t < nA; t++) {
        if (hasroot[t]) continue;
        memset(vis, 0, sizeof(int) * nv);
        if (!kuhn(t)) return 0;
    }
    return 1;
}

/* ---------- potentials ---------- */
static int phi_lo[MAXF], phi_hi[MAXF];
/* constraint per spoke e=(t,i): Lr, Rr w.r.t. reference direction */
static int cL[MAXV][3], cR[MAXV][3];
static void ref_constraints(void) {
    for (int t = 0; t < nA; t++)
        for (int i = 0; i < 3; i++) {
            if (u0[t] == i) { cL[t][i] = spR[t][i]; cR[t][i] = spL[t][i]; }   /* corner -> t */
            else { cL[t][i] = spL[t][i]; cR[t][i] = spR[t][i]; }
        }
}
/* arcs: L->R weight 0, R->L weight 1. dist from 0 = phi_hi.  dist to 0 = -phi_lo */
static int arc_to[6 * MAXV], arc_w[6 * MAXV], arc_next[6 * MAXV], head1[MAXF], head2[MAXF], narc;
static void add_arc(int *head, int a, int b, int w) {
    arc_to[narc] = b; arc_w[narc] = w; arc_next[narc] = head[a]; head[a] = narc++;
}
static void zero_one_bfs(int *head, int *dist) {
    static int dq[4 * MAXF];
    for (int i = 0; i < nW; i++) dist[i] = 1 << 29;
    int h = 2 * MAXF, tl = 2 * MAXF;
    dist[0] = 0; dq[tl++] = 0;
    while (h < tl) {
        int a = dq[h++];
        for (int e = head[a]; e >= 0; e = arc_next[e]) {
            int b = arc_to[e], w = arc_w[e];
            if (dist[a] + w < dist[b]) {
                dist[b] = dist[a] + w;
                if (w == 0) dq[--h] = b; else dq[tl++] = b;
            }
        }
    }
}
static void extremes(void) {
    ref_constraints();
    narc = 0;
    for (int i = 0; i < nW; i++) head1[i] = head2[i] = -1;
    for (int t = 0; t < nA; t++)
        for (int i = 0; i < 3; i++) {
            int L = cL[t][i], R = cR[t][i];
            if (L == R) continue;
            add_arc(head1, L, R, 0); add_arc(head1, R, L, 1);
            add_arc(head2, R, L, 0); add_arc(head2, L, R, 1);   /* reversed graph */
        }
    int d2[MAXF];
    zero_one_bfs(head1, phi_hi);
    zero_one_bfs(head2, d2);
    for (int i = 0; i < nW; i++) phi_lo[i] = -d2[i];
}
/* u from potential */
static void u_from_phi(const int *phi, int *u) {
    for (int t = 0; t < nA; t++) {
        int cnt = 0;
        u[t] = -1;
        for (int i = 0; i < 3; i++) {
            int d = phi[cR[t][i]] - phi[cL[t][i]];
            if (d != 0 && d != -1) { fprintf(stderr, "bad potential\n"); exit(1); }
            int into = (u0[t] == i) ^ (d == -1);
            if (into) { u[t] = i; cnt++; }
        }
        if (cnt != 1) { fprintf(stderr, "bad u: cnt=%d\n", cnt); exit(1); }
    }
}
static void check_u(const int *u) {
    int cnt[MAXV];
    memset(cnt, 0, sizeof(int) * nv);
    for (int t = 0; t < nA; t++) cnt[fv[Af[t]][u[t]]]++;
    for (int v = 0; v < nv; v++) {
        int want = isroot[v] ? deg[v] / 2 - 1 : deg[v] / 2 - 2;
        if (cnt[v] != want) { fprintf(stderr, "u count fail at %d: %d vs %d\n", v, cnt[v], want); exit(1); }
    }
}

/* ---------- cycles and tree pairs ---------- */
static int ncyc, cycstart[MAXV + 1], cyc_t[MAXV], cyc_x[MAXV], cyc_y[MAXV], cyc_u[MAXV];
static int cycles_of(const int *u) {
    /* D-edge in t joins the two corners != u(t); each nonroot has degree 2 */
    int e1[MAXV], e2[MAXV], et1[MAXV], et2[MAXV];
    for (int v = 0; v < nv; v++) e1[v] = e2[v] = -1;
    for (int t = 0; t < nA; t++) {
        int f = Af[t], a = fv[f][(u[t] + 1) % 3], b = fv[f][(u[t] + 2) % 3];
        if (e1[a] < 0) { e1[a] = b; et1[a] = t; } else { e2[a] = b; et2[a] = t; }
        if (e1[b] < 0) { e1[b] = a; et1[b] = t; } else { e2[b] = a; et2[b] = t; }
    }
    static int seen[MAXV];
    memset(seen, 0, sizeof(int) * nv);
    ncyc = 0;
    int m = 0;
    for (int v = 0; v < nv; v++) {
        if (isroot[v] || seen[v]) continue;
        if (e2[v] < 0) { fprintf(stderr, "deg fail in D\n"); exit(1); }
        cycstart[ncyc] = m;
        int x = v, prevt = -1;
        do {
            seen[x] = 1;
            int y, t;
            if (et1[x] != prevt) { y = e1[x]; t = et1[x]; } else { y = e2[x]; t = et2[x]; }
            cyc_t[m] = t; cyc_x[m] = x; cyc_y[m] = y; cyc_u[m] = fv[Af[t]][u[t]]; m++;
            prevt = t; x = y;
        } while (x != v);
        ncyc++;
    }
    cycstart[ncyc] = m;
    if (m != n) { fprintf(stderr, "cycle cover size %d != %d\n", m, n); exit(1); }
    return ncyc;
}
/* union-find with rollback */
static int ufp[MAXV], ufr[MAXV], stk[2 * MAXV], sp;
static int uf_find(int x) { while (ufp[x] != x) x = ufp[x]; return x; }
static int uf_union(int a, int b) {
    a = uf_find(a); b = uf_find(b);
    if (a == b) return 0;
    if (ufr[a] > ufr[b]) { int t = a; a = b; b = t; }
    ufp[a] = b; stk[sp++] = a;
    if (ufr[a] == ufr[b]) { ufr[b]++; stk[sp++] = -1 - b; } else stk[sp++] = MAXV + 5;
    return 1;
}
static void uf_rollback(int to) {
    while (sp > to) {
        int r = stk[--sp], a = stk[--sp];
        if (r < 0) ufr[-1 - r]--;
        ufp[a] = a;
    }
}
static long long tp_count, tp_cap;
static int tp_first_mask[MAXV], cur_mask[MAXV];
static int cyc_order[MAXV];
static void tp_rec(int k) {
    if (tp_count >= tp_cap) return;
    if (k == ncyc) {
        if (tp_count == 0) memcpy(tp_first_mask, cur_mask, sizeof(int) * ncyc);
        tp_count++;
        return;
    }
    int c = cyc_order[k];
    for (int b = 0; b < 2; b++) {
        int save = sp, ok = 1;
        for (int j = cycstart[c]; j < cycstart[c + 1]; j++) {
            int tail = b == 0 ? cyc_x[j] : cyc_y[j];      /* r(t); Q edge = {r(t), u(t)} */
            if (!uf_union(tail, cyc_u[j])) { ok = 0; break; }
        }
        if (ok) { cur_mask[c] = b; tp_rec(k + 1); }
        uf_rollback(save);
        if (tp_count >= tp_cap) return;
    }
}
static long long tree_pairs(const int *u, long long cap) {
    cycles_of(u);
    for (int v = 0; v < nv; v++) { ufp[v] = v; ufr[v] = 0; }
    sp = 0;
    /* order: shorter cycles last (long ones constrain most) */
    for (int i = 0; i < ncyc; i++) cyc_order[i] = i;
    for (int i = 0; i < ncyc; i++)
        for (int j = i + 1; j < ncyc; j++) {
            int li = cycstart[cyc_order[i] + 1] - cycstart[cyc_order[i]];
            int lj = cycstart[cyc_order[j] + 1] - cycstart[cyc_order[j]];
            if (lj > li) { int t = cyc_order[i]; cyc_order[i] = cyc_order[j]; cyc_order[j] = t; }
        }
    tp_count = 0; tp_cap = cap;
    tp_rec(0);
    return tp_count;
}

/* ---------- full lattice enumeration ---------- */
static int ord[MAXF], nodeinc_cnt[MAXF], nodeinc[MAXF][3 * MAXD];
static int phi_cur[MAXF], assigned[MAXF];
static long long L_size, L_cap, L_tm, L_with_tp, L_pairs;
static int L_cmin, L_cmin_count, L_overflow;
static int L_fmin_cyc, L_fmax_cyc;
static int setup_enum(void) {
    for (int i = 0; i < nW; i++) nodeinc_cnt[i] = 0;
    for (int t = 0; t < nA; t++)
        for (int i = 0; i < 3; i++) {
            int L = cL[t][i], R = cR[t][i];
            if (L == R) continue;
            nodeinc[L][nodeinc_cnt[L]++] = t * 3 + i;
            nodeinc[R][nodeinc_cnt[R]++] = t * 3 + i;
        }
    /* BFS order from 0 over adjacency */
    int seen[MAXF];
    memset(seen, 0, sizeof(int) * nW);
    int qh = 0, qt = 0;
    ord[qt++] = 0; seen[0] = 1;
    while (qh < qt) {
        int a = ord[qh++];
        for (int k = 0; k < nodeinc_cnt[a]; k++) {
            int e = nodeinc[a][k], t = e / 3, i = e % 3;
            int b = cL[t][i] == a ? cR[t][i] : cL[t][i];
            if (!seen[b]) { seen[b] = 1; ord[qt++] = b; }
        }
    }
    return qt;
}
static void visit_element(void) {
    int u[MAXV];
    u_from_phi(phi_cur, u);
    long long tp = tree_pairs(u, 1LL << 40);
    int c = ncyc;
    L_size++;
    L_pairs += 1LL << c;
    L_tm += tp;
    if (tp) L_with_tp++;
    if (c < L_cmin) { L_cmin = c; L_cmin_count = 1; } else if (c == L_cmin) L_cmin_count++;
}
static void enum_rec(int k) {
    if (L_size >= L_cap) { L_overflow = 1; return; }
    if (k == nW) { visit_element(); return; }
    int a = ord[k];
    for (int val = phi_lo[a]; val <= phi_hi[a]; val++) {
        int ok = 1;
        for (int j = 0; j < nodeinc_cnt[a] && ok; j++) {
            int e = nodeinc[a][j], t = e / 3, i = e % 3;
            int L = cL[t][i], R = cR[t][i];
            int b = L == a ? R : L;
            if (!assigned[b]) continue;
            int pl = L == a ? val : phi_cur[L], pr = R == a ? val : phi_cur[R];
            int d = pr - pl;
            if (d != 0 && d != -1) ok = 0;
        }
        if (!ok) continue;
        phi_cur[a] = val; assigned[a] = 1;
        enum_rec(k + 1);
        assigned[a] = 0;
        if (L_overflow) return;
    }
}

/* potential of a given deleted-corner map relative to u0 (BFS); returns 0 if inconsistent */
static int phi_of_u(const int *u, int *phi) {
    int done[MAXF];
    for (int i = 0; i < nW; i++) done[i] = 0;
    phi[0] = 0; done[0] = 1;
    int changed = 1;
    while (changed) {
        changed = 0;
        for (int t = 0; t < nA; t++) for (int i = 0; i < 3; i++) {
            int L = cL[t][i], R = cR[t][i];
            if (L == R) continue;
            int rev = (u[t] == i) != (u0[t] == i);
            int d = rev ? -1 : 0;
            if (done[L] && !done[R]) { phi[R] = phi[L] + d; done[R] = 1; changed = 1; }
            else if (done[R] && !done[L]) { phi[L] = phi[R] - d; done[L] = 1; changed = 1; }
            else if (done[L] && done[R] && phi[R] - phi[L] != d) return 0;
        }
    }
    return 1;
}
/* can single node a be moved by delta (+1/-1)? */
static int node_movable(const int *phi, int a, int delta) {
    for (int t = 0; t < nA; t++) for (int i = 0; i < 3; i++) {
        int L = cL[t][i], R = cR[t][i];
        if (L == R || (L != a && R != a)) continue;
        int pl = phi[L] + (L == a ? delta : 0), pr = phi[R] + (R == a ? delta : 0);
        if (pr - pl != 0 && pr - pl != -1) return 0;
    }
    return 1;
}
/* directed facial hexagons of u: ccw (u(t_ab)=a along the ccw order of white face y) and cw */
static long long sense_tot[4];
static void facial_senses(const int *u, int *ccw, int *cw) {
    *ccw = *cw = 0;
    for (int y = 0; y < nf; y++) {
        if (is_black(y)) continue;
        int k0 = 1, k1 = 1;
        for (int i = 0; i < 3; i++) {
            int a = fv[y][i], b = fv[y][(i + 1) % 3];
            int t = aidx[across[y][i]];
            if (t < 0) { k0 = k1 = 0; break; }
            int x = fv[Af[t]][u[t]];
            if (x != a) k0 = 0;
            if (x != b) k1 = 0;
        }
        *ccw += k0; *cw += k1;
    }
}
/* ---------- output helpers ---------- */
static void dump_instance(FILE *out, const char *tag, int froot) {
    fprintf(out, "%s %d %d", tag, nv, froot);
    for (int v = 0; v < nv; v++) {
        fprintf(out, " %d", deg[v]);
        for (int k = 0; k < deg[v]; k++) fprintf(out, " %d", adj[v][k]);
    }
    fprintf(out, " | t0 %d %d %d\n", fv[froot][0], fv[froot][1], fv[froot][2]);
}

int main(int argc, char **argv) {
    int text = 0, full = 0, rroots = 0;
    unsigned seed = 1;
    long long cap = 2000000;
    const char *dumpfile = NULL;
    for (int i = 1; i < argc; i++) {
        if (!strcmp(argv[i], "-t")) text = 1;
        else if (!strcmp(argv[i], "-m")) full = !strcmp(argv[++i], "full");
        else if (!strcmp(argv[i], "-r")) rroots = atoi(argv[++i]);
        else if (!strcmp(argv[i], "-s")) seed = (unsigned)atoi(argv[++i]);
        else if (!strcmp(argv[i], "-cap")) cap = atoll(argv[++i]);
        else if (!strcmp(argv[i], "-d")) dumpfile = argv[++i];
        else if (!strcmp(argv[i], "-U")) printu = 1;
        else if (!strcmp(argv[i], "-u")) ufile = fopen(argv[++i], "r");
        else if (!strcmp(argv[i], "-T")) { text = 1; use_given_root = 1; }
    }
    srand(seed);
    FILE *dump = dumpfile ? fopen(dumpfile, "w") : NULL;
    long long graphs = 0, rooted = 0, withpair = 0;
    long long fail_min = 0, fail_max = 0, fail_both = 0, same_ext = 0;
    long long c1_viol = 0, c1_eq = 0, c1_tested = 0, overflow = 0;
    long long hist[64][8];   /* hist[c_min][min(#TM/2^cmin,7)] */
    memset(hist, 0, sizeof hist);
    long long maxlat = 0;
    while (text ? read_text(stdin) : read_planar(stdin)) {
        graphs++;
        build_faces();
        int roots[MAXF], nr = 0;
        if (use_given_root) {
            for (int f = 0; f < nf; f++) {
                int m = 0;
                for (int i = 0; i < 3; i++) for (int j = 0; j < 3; j++) m += fv[f][i] == given_root[j];
                if (m == 3) roots[nr++] = f;
            }
        } else if (rroots > 0) { for (int k = 0; k < rroots; k++) roots[nr++] = rand() % nf; }
        else for (int f = 0; f < nf; f++) roots[nr++] = f;
        for (int k = 0; k < nr; k++) {
            int froot = roots[k];
            rooted++;
            if (!setup_root(froot)) continue;
            withpair++;
            check_u(u0);
            extremes();
            int ulo[MAXV], uhi[MAXV];
            u_from_phi(phi_lo, uhi);   /* FMIN = phi-minimal element (no ccw directed facial hexagon, checked) */
            u_from_phi(phi_hi, ulo);   /* FMAX = phi-maximal element */
            {
                int a1, b1, a2, b2;
                facial_senses(uhi, &a1, &b1); facial_senses(ulo, &a2, &b2);
                sense_tot[0] += a1; sense_tot[1] += b1; sense_tot[2] += a2; sense_tot[3] += b2;
            }
            check_u(uhi); check_u(ulo);
            if (printu) {
                printf("UMIN");
                for (int t = 0; t < nA; t++) printf(" %d,%d,%d:%d", fv[Af[t]][0], fv[Af[t]][1], fv[Af[t]][2], fv[Af[t]][uhi[t]]);
                printf("\nUMAX");
                for (int t = 0; t < nA; t++) printf(" %d,%d,%d:%d", fv[Af[t]][0], fv[Af[t]][1], fv[Af[t]][2], fv[Af[t]][ulo[t]]);
                printf("\n");
            }
            if (ufile) {
                int ug[MAXV], ph[MAXF], a, b, c, x;
                for (int t = 0; t < nA; t++) ug[t] = -1;
                while (fscanf(ufile, "%d %d %d %d", &a, &b, &c, &x) == 4) {
                    for (int t = 0; t < nA; t++) {
                        int f = Af[t], m = 0;
                        for (int i = 0; i < 3; i++) m += fv[f][i] == a || fv[f][i] == b || fv[f][i] == c;
                        if (m == 3) for (int i = 0; i < 3; i++) if (fv[f][i] == x) ug[t] = i;
                    }
                }
                check_u(ug);
                ref_constraints();
                if (!phi_of_u(ug, ph)) printf("given u: inconsistent potential"  "\n");
                int eqlo = 1, eqhi = 1, up = 0, down = 0;
                for (int i = 0; i < nW; i++) { eqlo &= ph[i] == phi_lo[i]; eqhi &= ph[i] == phi_hi[i]; }
                for (int i = 1; i < nW; i++) { up += node_movable(ph, i, 1); down += node_movable(ph, i, -1); }
                printf("given u: equals phi_lo %d, equals phi_hi %d, single-face moves up %d down %d, tree pairs %lld" "\n",
                       eqlo, eqhi, up, down, tree_pairs(ug, 1000000));
            }
            long long tmin = tree_pairs(uhi, 1);
            int cmn = ncyc;
            long long tmax = tree_pairs(ulo, 1);
            int cmx = ncyc;
            int same = 1;
            for (int i = 0; i < nW; i++) if (phi_lo[i] != phi_hi[i]) same = 0;
            same_ext += same;
            if (!tmin) fail_min++;
            if (!tmax) fail_max++;
            if (!tmin && !tmax) {
                fail_both++;
                if (dump) dump_instance(dump, "BOTH", froot);
            } else if ((!tmin || !tmax) && dump) dump_instance(dump, !tmin ? "LOFAIL" : "HIFAIL", froot);
            if (full) {
                setup_enum();
                L_size = 0; L_cap = cap; L_tm = 0; L_with_tp = 0; L_pairs = 0;
                L_cmin = 1 << 20; L_cmin_count = 0; L_overflow = 0;
                memset(assigned, 0, sizeof(int) * nW);
                assigned[0] = 1; phi_cur[0] = 0;
                enum_rec(1);
                if (L_overflow) { overflow++; continue; }
                if (L_size > maxlat) maxlat = L_size;
                c1_tested++;
                long long p2 = 1LL << L_cmin;
                if (L_tm < p2) { c1_viol++; if (dump) dump_instance(dump, "C1VIOL", froot); }
                if (L_tm == p2) c1_eq++;
                long long ratio = L_tm / p2; if (ratio > 7) ratio = 7;
                if (L_cmin < 64) hist[L_cmin][ratio]++;
                printf("R %lld %d cmin=%d ncmin=%d TM=%lld L=%lld Ltp=%lld pairs=%lld lo(c=%d,tp=%lld) hi(c=%d,tp=%lld)\n",
                       graphs, froot, L_cmin, L_cmin_count, L_tm, L_size, L_with_tp, L_pairs, cmn, tmin, cmx, tmax);
            }
        }
    }
    printf("SENSES directed facial hexagons: E_lo ccw=%lld cw=%lld ; E_hi ccw=%lld cw=%lld\n", sense_tot[0], sense_tot[1], sense_tot[2], sense_tot[3]);
    printf("SUMMARY graphs=%lld rooted=%lld withpair=%lld fail_lo=%lld fail_hi=%lld fail_both=%lld extremes_equal=%lld\n",
           graphs, rooted, withpair, fail_min, fail_max, fail_both, same_ext);
    if (full) {
        printf("C1 tested=%lld violations=%lld equality=%lld overflow=%lld maxlattice=%lld\n", c1_tested, c1_viol, c1_eq, overflow, maxlat);
        for (int c = 0; c < 64; c++) {
            long long s = 0;
            for (int j = 0; j < 8; j++) s += hist[c][j];
            if (!s) continue;
            printf("cmin=%d:", c);
            for (int j = 0; j < 8; j++) printf(" %lld", hist[c][j]);
            printf("   (#TM/2^cmin floor = 0..7+)\n");
        }
    }
    if (dump) fclose(dump);
    return 0;
}
