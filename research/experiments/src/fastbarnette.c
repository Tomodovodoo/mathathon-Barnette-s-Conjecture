/* fastbarnette.c -- a fast implementation of the objects of the paper and of
   proofs/algorithm/algorithm.md, for the experiment in research/experiments.

   It follows workings/barnette (the reference implementation) convention by
   convention, so that on the same labelled triangulation it visits the same
   partial choices in the same order, starts the exchange walk from the same
   tokens, and cuts along the same separating triangles.  crosscheck.py
   compares the two on every small instance.

   A triangulation is passed as nf triples of vertex labels (flat array F of
   length 3*nf), all listed counterclockwise, and the index t0 of a face.
   Labels lie in 0..nv-1; not every label need occur (pieces of a cut keep the
   labels of the whole).  The faces of A are the black faces other than t0, in
   increasing index; "A-index" below is the position in this list.  A state is
   an array s[0..n-1] of vertex labels, s[i] a corner of the face A[i].

   Build:  gcc -O2 -shared -o fastbarnette.dll fastbarnette.c                */

#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#ifdef _WIN32
#define BX_API __declspec(dllexport)
#else
#define BX_API
#endif

typedef long long i64;
typedef unsigned long long u64;

/* ------------------------------------------------------------------ */
/* The triangulation                                                    */
/* ------------------------------------------------------------------ */

typedef struct {
    int nf, nv, n, t0;
    int *F;                 /* 3*nf corners                                   */
    int *nb;                /* 3*nf: the face across side k = (F[k], F[k+1])  */
    unsigned char *black;   /* nf                                             */
    int *A, *aidx;          /* n faces; face -> A-index or -1                 */
    int root[3];
    unsigned char *isroot;  /* nv                                             */
    unsigned char *present; /* nv                                             */
    int *hc;                /* 3*n: corner of A[i] in slot k, or -1 if a root */
    int *vfs, *vf, *vslot;  /* vertex -> its A-faces (A-index, slot), by index */
    /* darts sorted by (tail, head) */
    int *dv, *dw, *df, *dk, *vstart;
} BX;

static void bx_free(BX *b)
{
    free(b->F); free(b->nb); free(b->black); free(b->A); free(b->aidx);
    free(b->isroot); free(b->present); free(b->hc); free(b->vfs); free(b->vf);
    free(b->vslot); free(b->dv); free(b->dw); free(b->df); free(b->dk);
    free(b->vstart);
    memset(b, 0, sizeof *b);
}

static int dart_find(const BX *b, int v, int w)
{
    int lo = b->vstart[v], hi = b->vstart[v + 1] - 1;
    while (lo <= hi) {
        int mid = (lo + hi) >> 1;
        if (b->dw[mid] == w) return mid;
        if (b->dw[mid] < w) lo = mid + 1; else hi = mid - 1;
    }
    return -1;
}

/* Errors: -1 inconsistent orientation or an edge with one face, -2 not two-
   colourable or not connected, -3 not a sphere / odd degree, -4 bad input.  */
static int bx_setup(BX *b, const int *F, int nf, int nv, int t0)
{
    int i, k, f, nd = 3 * nf;
    memset(b, 0, sizeof *b);
    if (nf < 8 || (nf & 1) || t0 < 0 || t0 >= nf) return -4;
    b->nf = nf; b->nv = nv; b->t0 = t0; b->n = nf / 2 - 1;
    b->F = malloc(sizeof(int) * nd);
    memcpy(b->F, F, sizeof(int) * nd);
    for (i = 0; i < nd; i++) if (F[i] < 0 || F[i] >= nv) { bx_free(b); return -4; }
    b->nb = malloc(sizeof(int) * nd);
    b->black = calloc(nf, 1);
    b->aidx = malloc(sizeof(int) * nf);
    b->A = malloc(sizeof(int) * (b->n + 1));
    b->isroot = calloc(nv, 1);
    b->present = calloc(nv, 1);
    b->hc = malloc(sizeof(int) * 3 * (b->n + 1));
    b->vfs = calloc(nv + 2, sizeof(int));
    b->dv = malloc(sizeof(int) * nd); b->dw = malloc(sizeof(int) * nd);
    b->df = malloc(sizeof(int) * nd); b->dk = malloc(sizeof(int) * nd);
    b->vstart = calloc(nv + 2, sizeof(int));
    b->vf = malloc(sizeof(int) * nd); b->vslot = malloc(sizeof(int) * nd);

    /* counting sort of the darts by tail, then insertion sort by head */
    for (i = 0; i < nd; i++) { b->vstart[F[i] + 1]++; b->present[F[i]] = 1; }
    for (i = 0; i < nv; i++) b->vstart[i + 1] += b->vstart[i];
    {
        int *pos = malloc(sizeof(int) * (nv + 1));
        memcpy(pos, b->vstart, sizeof(int) * (nv + 1));
        for (f = 0; f < nf; f++) for (k = 0; k < 3; k++) {
            int v = F[3 * f + k], w = F[3 * f + (k + 1) % 3], p = pos[v]++;
            b->dv[p] = v; b->dw[p] = w; b->df[p] = f; b->dk[p] = k;
        }
        free(pos);
    }
    for (i = 0; i < nv; i++) {
        int lo = b->vstart[i], hi = b->vstart[i + 1], p, q;
        if ((hi - lo) & 1) { bx_free(b); return -3; }
        for (p = lo + 1; p < hi; p++) {
            int w = b->dw[p], ff = b->df[p], kk = b->dk[p];
            for (q = p - 1; q >= lo && b->dw[q] > w; q--) {
                b->dw[q + 1] = b->dw[q]; b->df[q + 1] = b->df[q]; b->dk[q + 1] = b->dk[q];
            }
            b->dw[q + 1] = w; b->df[q + 1] = ff; b->dk[q + 1] = kk;
        }
        for (p = lo + 1; p < hi; p++) if (b->dw[p] == b->dw[p - 1]) { bx_free(b); return -1; }
    }
    for (f = 0; f < nf; f++) for (k = 0; k < 3; k++) {
        int v = F[3 * f + k], w = F[3 * f + (k + 1) % 3];
        int d = dart_find(b, w, v);
        if (d < 0) { bx_free(b); return -1; }
        b->nb[3 * f + k] = b->df[d];
    }
    {   /* Euler's formula and the two-colouring from t0 */
        int nvp = 0, *queue = malloc(sizeof(int) * nf), qh = 0, qt = 0;
        signed char *col = malloc(nf);
        for (i = 0; i < nv; i++) nvp += b->present[i];
        if (nvp - nd / 2 + nf != 2 || nvp < 4) { free(queue); free(col); bx_free(b); return -3; }
        memset(col, -1, nf);
        col[t0] = 1; queue[qt++] = t0;
        while (qh < qt) {
            f = queue[qh++];
            for (k = 0; k < 3; k++) {
                int y = b->nb[3 * f + k];
                if (col[y] < 0) { col[y] = 1 - col[f]; queue[qt++] = y; }
                else if (col[y] == col[f]) { free(queue); free(col); bx_free(b); return -2; }
            }
        }
        if (qt != nf) { free(queue); free(col); bx_free(b); return -2; }
        for (f = 0; f < nf; f++) b->black[f] = (unsigned char)col[f];
        free(queue); free(col);
    }
    for (k = 0; k < 3; k++) { b->root[k] = F[3 * t0 + k]; b->isroot[b->root[k]] = 1; }
    {
        int na = 0;
        for (f = 0; f < nf; f++) {
            b->aidx[f] = -1;
            if (b->black[f] && f != t0) {
                if (na >= b->n) { bx_free(b); return -2; }
                b->aidx[f] = na; b->A[na] = f;
                for (k = 0; k < 3; k++) {
                    int v = F[3 * f + k];
                    b->hc[3 * na + k] = b->isroot[v] ? -1 : v;
                }
                na++;
            }
        }
        if (na != b->n) { bx_free(b); return -2; }
    }
    for (i = 0; i < b->n; i++) for (k = 0; k < 3; k++)
        if (b->hc[3 * i + k] >= 0) b->vfs[b->hc[3 * i + k] + 1]++;
    for (i = 0; i < nv; i++) b->vfs[i + 1] += b->vfs[i];
    {
        int *pos = malloc(sizeof(int) * (nv + 1));
        memcpy(pos, b->vfs, sizeof(int) * (nv + 1));
        for (i = 0; i < b->n; i++) for (k = 0; k < 3; k++) {
            int v = b->hc[3 * i + k];
            if (v >= 0) { b->vf[pos[v]] = i; b->vslot[pos[v]] = k; pos[v]++; }
        }
        free(pos);
    }
    return 0;
}

/* ------------------------------------------------------------------ */
/* Enumeration of states (Algorithm E)                                  */
/* ------------------------------------------------------------------ */

typedef struct WS {
    const BX *b;
    int *mf, *mv;           /* a perfect matching of the faces not yet fixed */
    unsigned char *used;
    int *s, *ci;
    int *par, *sz, *ustack; int usp;
    unsigned char *did;
    int bad;                /* number of chosen sides that closed a cycle    */
    int *logf, *logv, *mark; int logn, logcap;
    int *queue, *pv, *stamp; int st;
    const int *avoid;
} WS;

static void ws_init(WS *w, const BX *b)
{
    int n = b->n, nv = b->nv, i;
    w->b = b;
    w->mf = malloc(sizeof(int) * (n + 1)); w->mv = malloc(sizeof(int) * (nv + 1));
    w->used = calloc(nv + 1, 1);
    w->s = malloc(sizeof(int) * (n + 1)); w->ci = malloc(sizeof(int) * (n + 2));
    w->par = malloc(sizeof(int) * (nv + 1)); w->sz = malloc(sizeof(int) * (nv + 1));
    w->ustack = malloc(sizeof(int) * (n + 1)); w->did = calloc(n + 1, 1);
    w->logcap = 4 * n + 64;
    w->logf = malloc(sizeof(int) * w->logcap); w->logv = malloc(sizeof(int) * w->logcap);
    w->mark = malloc(sizeof(int) * (n + 1));
    w->queue = malloc(sizeof(int) * (n + 1)); w->pv = malloc(sizeof(int) * (nv + 1));
    w->stamp = calloc(nv + 1, sizeof(int)); w->st = 0;
    w->avoid = NULL;
    for (i = 0; i < n; i++) w->mf[i] = -1;
    for (i = 0; i < nv; i++) w->mv[i] = -1;
}

static void ws_free(WS *w)
{
    free(w->mf); free(w->mv); free(w->used); free(w->s); free(w->ci); free(w->par);
    free(w->sz); free(w->ustack); free(w->did); free(w->logf); free(w->logv);
    free(w->mark); free(w->queue); free(w->pv); free(w->stamp);
}

static void ws_log(WS *w, int f, int v)
{
    if (w->logn == w->logcap) {
        w->logcap *= 2;
        w->logf = realloc(w->logf, sizeof(int) * w->logcap);
        w->logv = realloc(w->logv, sizeof(int) * w->logcap);
    }
    w->logf[w->logn] = f; w->logv[w->logn] = v; w->logn++;
}

static void ws_restore(WS *w, int mark)
{
    while (w->logn > mark) {
        int f, v;
        w->logn--;
        f = w->logf[w->logn]; v = w->logv[w->logn];
        w->mf[f] = v;
        if (v >= 0) w->mv[v] = f;
    }
}

static int uf_find(const int *par, int v)
{
    while (par[v] != v) v = par[v];
    return v;
}

/* An augmenting path from the unmatched face f0 to an unmatched vertex. */
static int ws_augment(WS *w, int f0)
{
    const BX *b = w->b;
    int qh = 0, qt = 0, k;
    w->st++;
    w->queue[qt++] = f0;
    while (qh < qt) {
        int f = w->queue[qh++];
        for (k = 0; k < 3; k++) {
            int x = b->hc[3 * f + k];
            if (x < 0 || w->used[x] || w->stamp[x] == w->st) continue;
            if (w->avoid && w->avoid[f] == x) continue;
            w->stamp[x] = w->st; w->pv[x] = f;
            if (w->mv[x] < 0) {
                for (;;) {
                    int g = w->pv[x], old = w->mf[g];
                    ws_log(w, g, old);
                    w->mf[g] = x; w->mv[x] = g;
                    if (g == f0) return 1;
                    x = old;
                }
            }
            w->queue[qt++] = w->mv[x];
        }
    }
    return 0;
}

typedef int (*leaf_cb)(WS *w, void *ctx);

/* Depth-first search through the partial choices that extend to a state
   (test 1) and, if prune is set, whose opposite sides are acyclic after the
   roots are identified (test 2).  Returns 0 when the search is complete,
   1 when the callback stopped it, 2 when the node budget ran out, and 3 if
   there is no state at all.
   nodes  partial choices kept (with at least one face),
   cands  corners examined,  tests  matching tests carried out.            */
static int enumerate(WS *w, int prune, i64 budget, i64 *nodes, i64 *cands, i64 *tests,
                     leaf_cb cb, void *ctx)
{
    const BX *b = w->b;
    int n = b->n, nv = b->nv, i, lvl = 0;
    for (i = 0; i < n; i++) w->mf[i] = -1;
    for (i = 0; i < nv; i++) { w->mv[i] = -1; w->used[i] = 0; w->par[i] = i; w->sz[i] = 1; }
    w->par[b->root[1]] = b->root[0]; w->par[b->root[2]] = b->root[0]; w->sz[b->root[0]] = 3;
    w->usp = 0; w->bad = 0; w->logn = 0;
    for (i = 0; i < n; i++) if (!ws_augment(w, i)) return 3;
    w->logn = 0;
    w->ci[0] = 0;
    for (;;) {
        int v, f, k, ra, rb, a, c;
        if (lvl == n) {
            if (cb(w, ctx)) return 1;
            goto up;
        }
        if (w->ci[lvl] >= 3) {
        up:
            if (lvl == 0) return 0;
            lvl--;
            v = w->s[lvl];
            w->used[v] = 0;
            ws_restore(w, w->mark[lvl]);
            if (w->did[lvl] == 1) {
                int r = w->ustack[--w->usp];
                w->sz[w->par[r]] -= w->sz[r]; w->par[r] = r;
            } else if (w->did[lvl] == 2) w->bad--;
            continue;
        }
        k = w->ci[lvl]++;
        v = b->hc[3 * lvl + k];
        if (v < 0 || w->used[v]) continue;
        if (w->avoid && w->avoid[lvl] == v) continue;
        (*cands)++;
        f = b->A[lvl];
        a = b->F[3 * f + (k + 1) % 3]; c = b->F[3 * f + (k + 2) % 3];
        ra = uf_find(w->par, a); rb = uf_find(w->par, c);
        if (ra == rb && prune) continue;
        w->mark[lvl] = w->logn;
        (*tests)++;
        if (w->mf[lvl] != v) {
            int v2 = w->mf[lvl], j = w->mv[v];
            ws_log(w, lvl, v2); ws_log(w, j, v);
            w->mf[lvl] = v; w->mv[v] = lvl; w->mf[j] = -1; w->mv[v2] = -1;
            w->used[v] = 1;
            if (!ws_augment(w, j)) {
                w->used[v] = 0;
                ws_restore(w, w->mark[lvl]);
                continue;
            }
        }
        w->used[v] = 1; w->s[lvl] = v;
        if (ra != rb) {
            if (w->sz[ra] > w->sz[rb]) { int t = ra; ra = rb; rb = t; }
            w->par[ra] = rb; w->sz[rb] += w->sz[ra];
            w->ustack[w->usp++] = ra; w->did[lvl] = 1;
        } else { w->did[lvl] = 2; w->bad++; }
        (*nodes)++;
        lvl++;
        w->ci[lvl] = 0;
        if (*nodes > budget) return 2;
    }
}

typedef struct { i64 count, good; int *first; int stop_first; } CountCtx;

static int count_cb(WS *w, void *ctx)
{
    CountCtx *c = ctx;
    c->count++;
    if (w->bad == 0) {
        c->good++;
        if (c->first && c->good == 1) memcpy(c->first, w->s, sizeof(int) * w->b->n);
        if (c->stop_first) return 1;
    }
    return 0;
}

/* mode 0: all states; out = [status, states, good states, nodes, cands, tests]
   mode 1: good states only (pruned search); out[1] = out[2] = their number
   mode 2: pruned search, stopped at the first good state, which is copied
           to first[0..n-1].
   status is the return value of enumerate().                              */
BX_API int bx_enumerate(const int *F, int nf, int nv, int t0, int mode, i64 budget,
                        i64 *out, int *first)
{
    BX b; WS w; CountCtx c = {0, 0, first, mode == 2};
    i64 nodes = 0, cands = 0, tests = 0;
    int rc = bx_setup(&b, F, nf, nv, t0), st;
    if (rc) return rc;
    ws_init(&w, &b);
    st = enumerate(&w, mode != 0, budget, &nodes, &cands, &tests, count_cb, &c);
    out[0] = st; out[1] = c.count; out[2] = c.good; out[3] = nodes; out[4] = cands; out[5] = tests;
    ws_free(&w); bx_free(&b);
    return 0;
}

/* ------------------------------------------------------------------ */
/* The number of states as a determinant (algorithm.md, Lemma 1)        */
/* ------------------------------------------------------------------ */

/* |det K| by fraction-free elimination; exact while the minors fit in 63
   bits, which Hadamard's bound guarantees for n <= 79.  Returns -1 if n is
   larger than that.                                                       */
BX_API i64 bx_states_det(const int *F, int nf, int nv, int t0)
{
    BX b; i64 *a, prev = 1, det; int n, i, j, k, *xi, nx = 0, sign = 1;
    if (bx_setup(&b, F, nf, nv, t0)) return -2;
    n = b.n;
    if (n > 79) { bx_free(&b); return -1; }
    xi = malloc(sizeof(int) * nv);
    for (i = 0; i < nv; i++) xi[i] = (b.present[i] && !b.isroot[i]) ? nx++ : -1;
    a = calloc((size_t)n * n, sizeof(i64));
    for (i = 0; i < n; i++) for (k = 0; k < 3; k++)
        if (b.hc[3 * i + k] >= 0) a[(size_t)i * n + xi[b.hc[3 * i + k]]] = 1;
    for (k = 0; k < n; k++) {
        if (a[(size_t)k * n + k] == 0) {
            for (i = k + 1; i < n && a[(size_t)i * n + k] == 0; i++);
            if (i == n) { free(a); free(xi); bx_free(&b); return 0; }
            for (j = 0; j < n; j++) {
                i64 t = a[(size_t)k * n + j]; a[(size_t)k * n + j] = a[(size_t)i * n + j];
                a[(size_t)i * n + j] = t;
            }
            sign = -sign;
        }
        for (i = k + 1; i < n; i++) for (j = k + 1; j < n; j++) {
            __int128 t = (__int128)a[(size_t)i * n + j] * a[(size_t)k * n + k]
                       - (__int128)a[(size_t)i * n + k] * a[(size_t)k * n + j];
            a[(size_t)i * n + j] = (i64)(t / prev);
        }
        prev = a[(size_t)k * n + k];
    }
    det = n ? a[(size_t)(n - 1) * n + n - 1] : 1;
    (void)sign;
    free(a); free(xi); bx_free(&b);
    return det < 0 ? -det : det;
}

/* ------------------------------------------------------------------ */
/* Pairs                                                                */
/* ------------------------------------------------------------------ */

typedef struct {
    WS *inner; i64 budget, pairs, pairs_good, work; i64 *byc; int n, censored;
    int *fr; unsigned char *seen;
    i64 nodes, cands, tests;
} PairCtx;

static int pair_inner_cb(WS *w, void *ctx)
{
    PairCtx *p = ctx;
    const int *r = w->avoid, *s = w->s;
    int n = p->n, i, c = 0;
    for (i = 0; i < n; i++) { p->fr[r[i]] = i; p->seen[i] = 0; }
    for (i = 0; i < n; i++) if (!p->seen[i]) {
        int j = i;
        c++;
        while (!p->seen[j]) { p->seen[j] = 1; j = p->fr[s[j]]; }
    }
    p->pairs++;
    p->byc[c]++;
    if (w->bad == 0) p->pairs_good++;
    return 0;
}

static int pair_outer_cb(WS *w, void *ctx)
{
    PairCtx *p = ctx;
    int st;
    p->inner->avoid = w->s;
    st = enumerate(p->inner, 0, p->budget, &p->nodes, &p->cands, &p->tests,
                   pair_inner_cb, p);
    if (st == 2) { p->censored = 1; return 1; }
    return 0;
}

/* All pairs (r, s).  out = [status, pairs, pairs with s good, m, number of
   2-factors, number of 2-factors with m cycles, largest number of cycles,
   nodes of the inner searches]; byc[c] (length n+1) is the number of pairs
   whose 2-factor has c cycles.  status 2: the budget on inner nodes ran out. */
BX_API int bx_pairs(const int *F, int nf, int nv, int t0, i64 budget, i64 *out, i64 *byc)
{
    BX b; WS w1, w2; PairCtx p; i64 nodes = 0, cands = 0, tests = 0;
    int rc = bx_setup(&b, F, nf, nv, t0), st, c, m = -1, maxc = 0;
    i64 n2f = 0, n2fm = 0;
    if (rc) return rc;
    ws_init(&w1, &b); ws_init(&w2, &b);
    memset(&p, 0, sizeof p);
    p.inner = &w2; p.budget = budget; p.byc = byc; p.n = b.n;
    p.fr = malloc(sizeof(int) * (nv + 1)); p.seen = malloc(b.n + 1);
    memset(byc, 0, sizeof(i64) * (b.n + 1));
    st = enumerate(&w1, 0, budget, &nodes, &cands, &tests, pair_outer_cb, &p);
    if (p.censored) st = 2;
    for (c = 0; c <= b.n; c++) if (byc[c]) {
        if (m < 0) { m = c; n2fm = byc[c] >> c; }
        n2f += byc[c] >> c; maxc = c;
    }
    out[0] = st; out[1] = p.pairs; out[2] = p.pairs_good; out[3] = m; out[4] = n2f;
    out[5] = n2fm; out[6] = maxc; out[7] = p.nodes;
    free(p.fr); free(p.seen);
    ws_free(&w1); ws_free(&w2); bx_free(&b);
    return 0;
}

/* ------------------------------------------------------------------ */
/* A first pair by a flow (Proposition 4.6)                             */
/* ------------------------------------------------------------------ */

/* A 2-factor of H by augmenting paths, split into two states as in the
   reference first_pair().  Returns 1 and fills r, s, or 0 if there is none. */
static int first_pair(const BX *b, int *r, int *s)
{
    int n = b->n, nv = b->nv, i, k, x, ok = 1;
    unsigned char *in = calloc(3 * n + 3, 1);
    int *degf = calloc(n + 1, sizeof(int)), *degx = calloc(nv + 1, sizeof(int));
    int *pf = malloc(sizeof(int) * (n + 1));      /* face -> edge slot it was reached by */
    int *px = malloc(sizeof(int) * (nv + 1));     /* vertex -> edge (3*f+k) it was reached by */
    int *sf = calloc(n + 1, sizeof(int)), *sx = calloc(nv + 1, sizeof(int));
    int *queue = malloc(sizeof(int) * (nv + 1)), st = 0;
    for (x = 0; x < nv && ok; x++) {
        if (!b->present[x] || b->isroot[x]) continue;
        while (degx[x] < 2) {
            int qh = 0, qt = 0, found = -1, p;
            st++;
            sx[x] = st; px[x] = -1; queue[qt++] = x;
            while (qh < qt && found < 0) {
                int y = queue[qh++];
                for (p = b->vfs[y]; p < b->vfs[y + 1] && found < 0; p++) {
                    int f = b->vf[p], e = 3 * f + b->vslot[p];
                    if (in[e] || sf[f] == st) continue;
                    sf[f] = st; pf[f] = e;
                    if (degf[f] < 2) { found = f; break; }
                    for (k = 0; k < 3; k++) {
                        int z = b->hc[3 * f + k];
                        if (z < 0 || !in[3 * f + k] || sx[z] == st) continue;
                        sx[z] = st; px[z] = 3 * f + k; queue[qt++] = z;
                    }
                }
            }
            if (found < 0) { ok = 0; break; }
            degf[found]++; degx[x]++;
            {
                int f = found;
                for (;;) {
                    int e = pf[f], y = b->hc[e];
                    in[e] = 1;
                    if (px[y] < 0) break;
                    in[px[y]] = 0;
                    f = px[y] / 3;
                }
            }
        }
    }
    if (ok) {
        for (i = 0; i < n; i++) { r[i] = -1; s[i] = -1; }
        for (i = 0; i < n; i++) {
            int t = i;
            x = -1;
            for (k = 0; k < 3; k++) if (in[3 * t + k]) { x = b->hc[3 * t + k]; break; }
            while (s[t] < 0) {
                int p, y = -1, t2 = -1;
                s[t] = x;
                for (k = 0; k < 3; k++) if (in[3 * t + k] && b->hc[3 * t + k] != x) y = b->hc[3 * t + k];
                r[t] = x = y;
                for (p = b->vfs[x]; p < b->vfs[x + 1]; p++) {
                    int f = b->vf[p];
                    if (f != t && in[3 * f + b->vslot[p]]) { t2 = f; break; }
                }
                t = t2;
            }
        }
    }
    free(in); free(degf); free(degx); free(pf); free(px); free(sf); free(sx); free(queue);
    return ok;
}

BX_API int bx_first_pair(const int *F, int nf, int nv, int t0, int *r, int *s)
{
    BX b; int rc = bx_setup(&b, F, nf, nv, t0), ok;
    if (rc) return rc;
    ok = first_pair(&b, r, s);
    bx_free(&b);
    return ok;
}

/* ------------------------------------------------------------------ */
/* The exchange walk (Algorithm W)                                      */
/* ------------------------------------------------------------------ */

/* The local weights omega(t, v) for the arcs gamma_y that follow the paths
   of a breadth-first tree of G from t0, as in the reference corner_weights().
   kappa[3*i+k] belongs to the corner in slot k of the face A[i].          */
static void corner_weights(const BX *b, int *kappa)
{
    int nf = b->nf, f, k, qh = 0, qt = 0, i;
    int *parent = malloc(sizeof(int) * nf), *pside = malloc(sizeof(int) * nf);
    int *queue = malloc(sizeof(int) * nf), *wc = calloc(nf, sizeof(int));
    for (f = 0; f < nf; f++) parent[f] = -2;
    parent[b->t0] = -1; pside[b->t0] = -1; queue[qt++] = b->t0;
    while (qh < qt) {
        f = queue[qh++];
        for (k = 0; k < 3; k++) {
            int y = b->nb[3 * f + k];
            if (parent[y] == -2) { parent[y] = f; pside[y] = k; queue[qt++] = y; }
        }
    }
    for (i = nf - 1; i >= 0; i--) {
        f = queue[i];
        if (!b->black[f]) wc[f]++;
        if (parent[f] >= 0) wc[parent[f]] += wc[f];
    }
    memset(kappa, 0, sizeof(int) * 3 * b->n);
    for (i = 1; i < nf; i++) {
        int c = queue[i], t = parent[c], ks, ke, v, a, bb, e1, e2, x1, x2, j, kv;
        if (t == b->t0 || !b->black[t]) continue;
        ks = pside[c];                       /* side of t shared with the child  */
        e1 = b->F[3 * t + ks]; e2 = b->F[3 * t + (ks + 1) % 3];
        /* side of t shared with its parent: the side of parent[t] is stored  */
        {
            int pt = parent[t], kp = pside[t];
            x1 = b->F[3 * pt + kp]; x2 = b->F[3 * pt + (kp + 1) % 3];
        }
        ke = 0; (void)ke;
        if (e1 == x1 || e1 == x2) { v = e1; a = e2; } else { v = e2; a = e1; }
        bb = (x1 == v) ? x2 : x1;
        kv = 0;
        for (j = 0; j < 3; j++) if (b->F[3 * t + j] == v) kv = j;
        if (b->F[3 * t + (kv + 1) % 3] == a && b->F[3 * t + (kv + 2) % 3] == bb)
            kappa[3 * b->aidx[t] + kv] += wc[c];
        else
            kappa[3 * b->aidx[t] + kv] -= wc[c];
    }
    free(parent); free(pside); free(queue); free(wc);
}

typedef struct {
    const BX *b; int n;
    int *alpha;         /* 3*n: alpha(t, corner in slot k)                 */
    int *r, *s;         /* the pair, as slots 0..2 of each face            */
    int *fr;            /* vertex -> the face t with r(t) = vertex         */
    int *cyc;           /* face -> least face of its cycle of D(r, s)      */
    int *pre_s, *pre_r, *tot_s, *tot_r, *cnt;
    int *tokf, *tokj; int h;
    int *col, *kf;
} Walk;

static void walk_cycles(Walk *w)
{
    const BX *b = w->b; int n = w->n, i;
    for (i = 0; i < n; i++) { w->fr[b->hc[3 * i + w->r[i]]] = i; w->cyc[i] = -1; }
    for (i = 0; i < n; i++) if (w->cyc[i] < 0) {
        int j = i;
        while (w->cyc[j] < 0) { w->cyc[j] = i; j = w->fr[b->hc[3 * j + w->s[j]]]; }
    }
}

/* prefix sums of the pools, by cycle, faces in increasing index */
static void walk_pools(Walk *w)
{
    int n = w->n, i;
    for (i = 0; i < n; i++) { w->tot_s[i] = 0; w->tot_r[i] = 0; }
    for (i = 0; i < n; i++) {
        int c = w->cyc[i];
        w->pre_s[i] = w->tot_s[c]; w->pre_r[i] = w->tot_r[c];
        w->tot_s[c] += w->alpha[3 * i + w->s[i]];
        w->tot_r[c] += w->alpha[3 * i + w->r[i]];
    }
}

static void walk_reverse_D(Walk *w, int c)
{
    int n = w->n, i;
    for (i = 0; i < n; i++) if (w->cyc[i] == c) { int t = w->r[i]; w->r[i] = w->s[i]; w->s[i] = t; }
}

/* The first cycle of Q_s directed by r; reverses it and returns 1, or
   returns 0 if Q_s has no cycle.                                          */
static int walk_beta(Walk *w)
{
    const BX *b = w->b; int n = w->n, i, best = -1, nk = 0, stamp = 0;
    for (i = 0; i < n; i++) { w->fr[b->hc[3 * i + w->r[i]]] = i; w->col[i] = 0; }
    /* col[i]: 0 unvisited, >0 the number of the walk that visited it */
    for (i = 0; i < n; i++) if (!w->col[i]) {
        int j = i;
        stamp++;
        while (j >= 0 && !w->col[j]) {
            int u = b->F[3 * b->A[j] + 3 - w->r[j] - w->s[j]];   /* third corner */
            w->col[j] = stamp;
            j = b->isroot[u] ? -1 : w->fr[u];
        }
        if (j >= 0 && w->col[j] == stamp) {          /* a new cycle through j */
            int k = j, mn = j, len = 0;
            do {
                int u = b->F[3 * b->A[k] + 3 - w->r[k] - w->s[k]];
                if (k < mn) mn = k;
                len++;
                k = w->fr[u];
            } while (k != j);
            if (best < 0 || mn < best) {
                best = mn; nk = 0; k = j;
                do {
                    int u = b->F[3 * b->A[k] + 3 - w->r[k] - w->s[k]];
                    w->kf[nk++] = k;
                    k = w->fr[u];
                } while (k != j);
            }
            (void)len;
        }
    }
    if (best < 0) return 0;
    for (i = 0; i < nk; i++) { int k = w->kf[i]; w->r[k] = 3 - w->r[k] - w->s[k]; }
    return 1;
}

/* The move alpha.  Returns 1 if a cycle was reversed, 0 at a fixed point. */
static int walk_alpha(Walk *w)
{
    int n = w->n, i, c;
    walk_cycles(w);
    for (i = 0; i < n; i++) w->cnt[i] = 0;
    for (i = 0; i < w->h; i++) w->cnt[w->cyc[w->tokf[i]]]++;
    for (c = 0; c < n; c++) if (w->cyc[c] == c && w->cnt[c] == 0) { walk_reverse_D(w, c); return 1; }
    walk_pools(w);
    for (c = 0; c < n; c++) if (w->cyc[c] == c) {
        int ok = 1;
        for (i = 0; i < w->h && ok; i++) if (w->cyc[w->tokf[i]] == c)
            if (w->pre_s[w->tokf[i]] + w->tokj[i] - 1 >= w->tot_r[c]) ok = 0;
        if (!ok) continue;
        for (i = 0; i < w->h; i++) if (w->cyc[w->tokf[i]] == c) {
            int rank = w->pre_s[w->tokf[i]] + w->tokj[i] - 1, t;
            for (t = 0; t < n; t++)
                if (w->cyc[t] == c && w->pre_r[t] <= rank
                    && rank < w->pre_r[t] + w->alpha[3 * t + w->r[t]]) break;
            w->tokf[i] = t; w->tokj[i] = rank - w->pre_r[t] + 1;
        }
        walk_reverse_D(w, c);
        return 1;
    }
    return 0;
}

/* Runs Algorithm W from the pair (r, s), given as vertex labels and
   overwritten with the final pair.  out = [status, moves, rounds, number of
   cycles of D at the start, number at the end]; status 0: the second state
   is good, 1: stopped after max_moves moves.                              */
static void exchange_walk(const BX *b, int *r, int *s, i64 max_moves, i64 *out)
{
    Walk w; int n = b->n, i, k, *kappa = malloc(sizeof(int) * 3 * (n + 1));
    i64 moves = 0, rounds = 0; int status = -1, c0 = -1, c;
    w.b = b; w.n = n;
    w.alpha = malloc(sizeof(int) * 3 * (n + 1));
    w.r = malloc(sizeof(int) * (n + 1)); w.s = malloc(sizeof(int) * (n + 1));
    w.fr = malloc(sizeof(int) * (b->nv + 1)); w.cyc = malloc(sizeof(int) * (n + 1));
    w.pre_s = malloc(sizeof(int) * (n + 1)); w.pre_r = malloc(sizeof(int) * (n + 1));
    w.tot_s = malloc(sizeof(int) * (n + 1)); w.tot_r = malloc(sizeof(int) * (n + 1));
    w.cnt = malloc(sizeof(int) * (n + 1));
    w.tokf = malloc(sizeof(int) * (n + 1)); w.tokj = malloc(sizeof(int) * (n + 1));
    w.col = malloc(sizeof(int) * (n + 1)); w.kf = malloc(sizeof(int) * (n + 1));
    corner_weights(b, kappa);
    for (i = 0; i < n; i++) {
        int lo = kappa[3 * i];
        if (kappa[3 * i + 1] < lo) lo = kappa[3 * i + 1];
        if (kappa[3 * i + 2] < lo) lo = kappa[3 * i + 2];
        for (k = 0; k < 3; k++) {
            w.alpha[3 * i + k] = kappa[3 * i + k] - lo;
            if (b->hc[3 * i + k] == r[i]) w.r[i] = k;
            if (b->hc[3 * i + k] == s[i]) w.s[i] = k;
        }
    }
    while (status < 0) {
        rounds++;
        walk_cycles(&w); walk_pools(&w);
        for (c = 0; c < n; c++) if (w.cyc[c] == c && w.tot_s[c] < w.tot_r[c]) walk_reverse_D(&w, c);
        walk_cycles(&w); walk_pools(&w);
        w.h = 0;
        for (c = 0; c < n; c++) if (w.cyc[c] == c) {
            int rank = w.tot_r[c], t;
            for (t = 0; t < n; t++)
                if (w.cyc[t] == c && w.pre_s[t] <= rank
                    && rank < w.pre_s[t] + w.alpha[3 * t + w.s[t]]) break;
            w.tokf[w.h] = t; w.tokj[w.h] = rank - w.pre_s[t] + 1; w.h++;
        }
        if (c0 < 0) c0 = w.h;
        for (;;) {
            /* is there a cycle of Q_s?  test before counting the move */
            if (max_moves >= 0 && moves >= max_moves) {
                /* the reference tests for a cycle first, then the budget */
                Walk probe = w; int *rsave = malloc(sizeof(int) * (n + 1)), had;
                memcpy(rsave, w.r, sizeof(int) * n);
                had = walk_beta(&probe);
                memcpy(w.r, rsave, sizeof(int) * n); free(rsave);
                status = had ? 1 : 0;
                break;
            }
            if (!walk_beta(&w)) { status = 0; break; }
            moves++;
            if (!walk_alpha(&w)) break;
            moves++;
        }
    }
    for (i = 0; i < n; i++) { r[i] = b->hc[3 * i + w.r[i]]; s[i] = b->hc[3 * i + w.s[i]]; }
    walk_cycles(&w);
    for (c = 0, k = 0; c < n; c++) if (w.cyc[c] == c) k++;
    out[0] = status; out[1] = moves; out[2] = rounds; out[3] = c0; out[4] = k;
    free(kappa); free(w.alpha); free(w.r); free(w.s); free(w.fr); free(w.cyc);
    free(w.pre_s); free(w.pre_r); free(w.tot_s); free(w.tot_r); free(w.cnt);
    free(w.tokf); free(w.tokj); free(w.col); free(w.kf);
}

BX_API int bx_walk(const int *F, int nf, int nv, int t0, int *r, int *s, i64 max_moves, i64 *out)
{
    BX b; int rc = bx_setup(&b, F, nf, nv, t0);
    if (rc) return rc;
    exchange_walk(&b, r, s, max_moves, out);
    bx_free(&b);
    return 0;
}

BX_API int bx_corner_weights(const int *F, int nf, int nv, int t0, int *kappa)
{
    BX b; int rc = bx_setup(&b, F, nf, nv, t0);
    if (rc) return rc;
    corner_weights(&b, kappa);
    bx_free(&b);
    return 0;
}

/* ------------------------------------------------------------------ */
/* From a good state to the cycle (Lemma 3.4, Proposition 3.5)          */
/* ------------------------------------------------------------------ */

/* The set P = M^* of the good state s with e0 = {ea, eb}: writes its n+1
   edges as vertex pairs to P (2*(n+1) ints).  Returns 0, or -1 if s is not
   good.                                                                   */
static int selection(const BX *b, const int *s, int ea, int eb, int *P)
{
    int n = b->n, nv = b->nv, i, k, np = 0, ne = 0, qh = 0, qt = 0, cnt = 0, nvp = 0;
    int *eu = malloc(sizeof(int) * (n + 3)), *ev = malloc(sizeof(int) * (n + 3));
    int *deg = calloc(nv + 2, sizeof(int)), *adj = malloc(sizeof(int) * 2 * (n + 3));
    int *queue = malloc(sizeof(int) * (nv + 1));
    signed char *col = malloc(nv + 1);
    memset(col, -1, nv + 1);
    for (i = 0; i < n; i++) {
        int f = b->A[i];
        for (k = 0; k < 3; k++) if (b->F[3 * f + k] == s[i]) break;
        if (k == 3) goto bad;
        eu[ne] = b->F[3 * f + (k + 1) % 3]; ev[ne] = b->F[3 * f + (k + 2) % 3]; ne++;
    }
    for (k = 0; k < 3; k++) {
        int v = b->root[k], w = b->root[(k + 1) % 3];
        if ((v == ea && w == eb) || (v == eb && w == ea)) continue;
        eu[ne] = v; ev[ne] = w; ne++;
    }
    if (ne != n + 2) goto bad;
    for (i = 0; i < ne; i++) { deg[eu[i] + 1]++; deg[ev[i] + 1]++; }
    for (i = 0; i < nv; i++) deg[i + 1] += deg[i];
    {
        int *pos = malloc(sizeof(int) * (nv + 1));
        memcpy(pos, deg, sizeof(int) * (nv + 1));
        for (i = 0; i < ne; i++) { adj[pos[eu[i]]++] = ev[i]; adj[pos[ev[i]]++] = eu[i]; }
        free(pos);
    }
    col[b->root[0]] = 0; queue[qt++] = b->root[0];
    while (qh < qt) {
        int v = queue[qh++];
        cnt++;
        for (i = deg[v]; i < deg[v + 1]; i++)
            if (col[adj[i]] < 0) { col[adj[i]] = 1 - col[v]; queue[qt++] = adj[i]; }
    }
    for (i = 0; i < nv; i++) nvp += b->present[i];
    if (cnt != nvp) goto bad;                  /* not a spanning tree */
    for (i = 0; i < 3 * b->nf; i++) {
        int v = b->dv[i], w = b->dw[i];
        if (v < w && col[v] == col[w]) {
            if (np == n + 1) goto bad;
            P[2 * np] = v; P[2 * np + 1] = w; np++;
        }
    }
    if (np != n + 1) goto bad;
    free(eu); free(ev); free(deg); free(adj); free(queue); free(col);
    return 0;
bad:
    free(eu); free(ev); free(deg); free(adj); free(queue); free(col);
    return -1;
}

/* The cycle that crosses exactly the edges not in P, as in the reference
   cycle_of_selection(); P is given as np vertex pairs.  Returns 0 or -1.  */
static int cycle_of_selection(const BX *b, const int *P, int np, int *cycle)
{
    int nf = b->nf, i, k, len = 0, prev = -1, t = b->t0, rc = -1;
    unsigned char *inP = calloc(3 * nf, 1);
    for (i = 0; i < np; i++) {
        int d1 = dart_find(b, P[2 * i], P[2 * i + 1]), d2 = dart_find(b, P[2 * i + 1], P[2 * i]);
        if (d1 < 0 || d2 < 0) goto done;
        inP[3 * b->df[d1] + b->dk[d1]] = 1; inP[3 * b->df[d2] + b->dk[d2]] = 1;
    }
    cycle[len++] = t;
    for (;;) {
        int step[3], ns = 0, nxt;
        for (k = 0; k < 3; k++) if (!inP[3 * t + k]) step[ns++] = b->nb[3 * t + k];
        if (ns != 2) goto done;
        nxt = (step[0] == prev) ? step[1] : step[0];
        if (nxt == b->t0) break;
        if (len >= nf) goto done;
        cycle[len++] = nxt;
        prev = t; t = nxt;
    }
    if (len == nf) rc = 0;
done:
    free(inP);
    return rc;
}

/* Independent check that cycle lists every face once, consecutive faces
   sharing a side, without crossing the side k0 of the face f0.            */
BX_API int bx_check_cycle(const int *F, int nf, int nv, const int *cycle, int f0, int k0)
{
    BX b; int i, k, ok = 1, other;
    unsigned char *seen;
    if (bx_setup(&b, F, nf, nv, f0)) return 0;
    other = b.nb[3 * f0 + k0];
    seen = calloc(nf, 1);
    for (i = 0; i < nf && ok; i++) {
        int f = cycle[i], g = cycle[(i + 1) % nf];
        if (f < 0 || f >= nf || seen[f]) { ok = 0; break; }
        seen[f] = 1;
        for (k = 0; k < 3; k++) if (b.nb[3 * f + k] == g) break;
        if (k == 3) ok = 0;
        if ((f == f0 && g == other) || (f == other && g == f0)) ok = 0;
    }
    free(seen); bx_free(&b);
    return ok;
}

/* ------------------------------------------------------------------ */
/* The whole algorithm, with the cut along separating triangles         */
/* ------------------------------------------------------------------ */

/* The first separating triangle in the order of the reference
   separating_triangle(): edges vw with v < w in lexicographic order, then
   the common neighbours x in increasing order.                            */
static int separating_triangle(const BX *b, int *tri)
{
    int v, p, q, r;
    for (v = 0; v < b->nv; v++) for (p = b->vstart[v]; p < b->vstart[v + 1]; p++) {
        int w = b->dw[p], f1, f2, x1, x2;
        if (w < v) continue;
        f1 = b->df[p]; x1 = b->F[3 * f1 + (b->dk[p] + 2) % 3];
        q = dart_find(b, w, v);
        f2 = b->df[q]; x2 = b->F[3 * f2 + (b->dk[q] + 2) % 3];
        q = b->vstart[v]; r = b->vstart[w];
        while (q < b->vstart[v + 1] && r < b->vstart[w + 1]) {
            if (b->dw[q] < b->dw[r]) q++;
            else if (b->dw[q] > b->dw[r]) r++;
            else {
                int x = b->dw[q];
                if (x != x1 && x != x2) { tri[0] = v; tri[1] = w; tri[2] = x; return 1; }
                q++; r++;
            }
        }
    }
    return 0;
}

typedef struct {
    int method;             /* 0 search, 1 walk                              */
    i64 node_budget, move_budget;
    i64 nodes, cands, tests, moves, rounds;
    int npieces, cuts, censored, error, maxn;
    int *piece_n; i64 *piece_cost; int piece_cap;
} Solve;

typedef struct Piece {
    BX b; int has_pair; int *state; int tri[3];
    struct Piece *first, *second;
} Piece;

static void piece_free(Piece *p)
{
    if (!p) return;
    piece_free(p->first); piece_free(p->second);
    free(p->state); bx_free(&p->b); free(p);
}

static Piece *decompose(const int *F, int nf, int nv, int t0, Solve *S)
{
    Piece *p = calloc(1, sizeof *p);
    int n, *r, *s;
    if (bx_setup(&p->b, F, nf, nv, t0)) { S->error = 1; free(p); return NULL; }
    n = p->b.n;
    r = malloc(sizeof(int) * (n + 1)); s = malloc(sizeof(int) * (n + 1));
    p->has_pair = first_pair(&p->b, r, s);
    if (p->has_pair) {
        i64 cost = 0;
        p->state = malloc(sizeof(int) * (n + 1));
        if (S->method == 0) {
            WS w; CountCtx c = {0, 0, p->state, 1};
            i64 nodes = 0, cands = 0, tests = 0; int st;
            ws_init(&w, &p->b);
            st = enumerate(&w, 1, S->node_budget, &nodes, &cands, &tests, count_cb, &c);
            ws_free(&w);
            S->nodes += nodes; S->cands += cands; S->tests += tests; cost = nodes;
            if (st == 2) S->censored = 1;
            else if (st != 1) S->error = 2;        /* a pair but no good state */
        } else {
            i64 out[5];
            exchange_walk(&p->b, r, s, S->move_budget, out);
            S->moves += out[1]; S->rounds += out[2]; cost = out[1];
            if (out[0] == 1) S->censored = 1;
            memcpy(p->state, s, sizeof(int) * n);
        }
        if (S->npieces < S->piece_cap) { S->piece_n[S->npieces] = n; S->piece_cost[S->npieces] = cost; }
        S->npieces++;
        if (n > S->maxn) S->maxn = n;
    } else {
        const BX *b = &p->b;
        int *side = calloc(nf, sizeof(int)), *queue = malloc(sizeof(int) * nf), qh = 0, qt = 0;
        int *F1, *F2, n1 = 0, n2 = 0, f, k, t01 = -1, x, y, z, d;
        if (!separating_triangle(b, p->tri)) { S->error = 3; free(side); free(queue); free(r); free(s); return p; }
        S->cuts++;
        x = p->tri[0]; y = p->tri[1]; z = p->tri[2];
        side[t0] = 1; queue[qt++] = t0;
        while (qh < qt) {
            f = queue[qh++];
            for (k = 0; k < 3; k++) {
                int v = b->F[3 * f + k], w = b->F[3 * f + (k + 1) % 3], g = b->nb[3 * f + k];
                int cut = (v == x || v == y || v == z) && (w == x || w == y || w == z);
                if (!cut && !side[g]) { side[g] = 1; queue[qt++] = g; }
            }
        }
        F1 = malloc(sizeof(int) * 3 * (qt + 1)); F2 = malloc(sizeof(int) * 3 * (nf - qt + 1));
        for (f = 0; f < nf; f++) {
            if (side[f]) { if (f == t0) t01 = n1; memcpy(F1 + 3 * n1++, b->F + 3 * f, 3 * sizeof(int)); }
            else memcpy(F2 + 3 * n2++, b->F + 3 * f, 3 * sizeof(int));
        }
        d = dart_find(b, x, y);
        if (!side[b->df[d]]) { F1[3 * n1] = x; F1[3 * n1 + 1] = y; F1[3 * n1 + 2] = z; }
        else { F1[3 * n1] = x; F1[3 * n1 + 1] = z; F1[3 * n1 + 2] = y; }
        F2[3 * n2] = F1[3 * n1 + 2]; F2[3 * n2 + 1] = F1[3 * n1 + 1]; F2[3 * n2 + 2] = F1[3 * n1];
        n1++; n2++;
        p->first = decompose(F1, n1, nv, t01, S);
        p->second = decompose(F2, n2, nv, n2 - 1, S);
        free(F1); free(F2); free(side); free(queue);
    }
    free(r); free(s);
    return p;
}

/* P for the piece p with e0 = {ea, eb}, appended to P (vertex pairs). */
static int assemble(const Piece *p, int ea, int eb, int *P, int *np)
{
    if (!p) return -1;
    if (p->has_pair) {
        int rc = selection(&p->b, p->state, ea, eb, P + 2 * *np);
        if (rc) return rc;
        *np += p->b.n + 1;
        return 0;
    } else {
        int start = *np, i, a = -1, c = -1, x = p->tri[0], y = p->tri[1], z = p->tri[2];
        if (!p->first || !p->second) return -1;
        if (assemble(p->first, ea, eb, P, np)) return -1;
        for (i = start; i < *np; i++) {
            int v = P[2 * i], w = P[2 * i + 1];
            if ((v == x || v == y || v == z) && (w == x || w == y || w == z)) { a = v; c = w; }
        }
        if (a < 0) return -1;
        return assemble(p->second, a, c, P, np);
    }
}

/* The algorithm of hamiltonian_cycle(): a pair by a flow; if there is one, a
   good state by the search (method 0) or by the exchange walk (method 1);
   otherwise cut along the first separating triangle and recurse.  For each of
   the three sides k of t0 the cycle avoiding the dual of that side is written
   to cycles[k*nf ..]; ok[k] says whether it was obtained.
   stats = [status, pieces, cuts, largest n of a piece, nodes, cands, tests,
            moves, rounds]; status 0 done, 1 a budget ran out, <0 an error
   (-2: a triangulation with a pair but without good state, -3: no pair and
   no separating triangle, -4: a state returned is not good, -1: bad input). */
BX_API int bx_solve(const int *F, int nf, int nv, int t0, int method, i64 node_budget,
                    i64 move_budget, int *cycles, int *ok, i64 *stats,
                    int *piece_n, i64 *piece_cost, int piece_cap)
{
    Solve S; Piece *root; int k, status = 0;
    memset(&S, 0, sizeof S);
    S.method = method; S.node_budget = node_budget; S.move_budget = move_budget;
    S.piece_n = piece_n; S.piece_cost = piece_cost; S.piece_cap = piece_cap;
    root = decompose(F, nf, nv, t0, &S);
    ok[0] = ok[1] = ok[2] = 0;
    if (S.error == 1 || !root) status = -1;
    else if (S.error == 2) status = -2;
    else if (S.error == 3) status = -3;
    else if (S.censored) status = 1;
    if (status == 0) {
        int *P = malloc(sizeof(int) * 2 * (2 * nf + 8));
        for (k = 0; k < 3; k++) {
            int np = 0, ea = F[3 * t0 + k], eb = F[3 * t0 + (k + 1) % 3];
            if (assemble(root, ea, eb, P, &np) == 0 && np == nf / 2 + S.cuts
                && cycle_of_selection(&root->b, P, np, cycles + (size_t)k * nf) == 0) ok[k] = 1;
            else status = -4;
        }
        free(P);
    }
    stats[0] = status; stats[1] = S.npieces; stats[2] = S.cuts; stats[3] = S.maxn;
    stats[4] = S.nodes; stats[5] = S.cands; stats[6] = S.tests; stats[7] = S.moves;
    stats[8] = S.rounds;
    piece_free(root);
    return 0;
}

/* The cycle of a given good state, for the side k of t0. */
BX_API int bx_cycle_of_state(const int *F, int nf, int nv, int t0, int k, const int *s, int *cycle)
{
    BX b; int rc = bx_setup(&b, F, nf, nv, t0), *P;
    if (rc) return rc;
    P = malloc(sizeof(int) * 2 * (b.n + 2));
    rc = selection(&b, s, F[3 * t0 + k], F[3 * t0 + (k + 1) % 3], P);
    if (!rc) rc = cycle_of_selection(&b, P, b.n + 1, cycle);
    free(P); bx_free(&b);
    return rc;
}

/* All separating triangles: their number, and for each the number of faces
   on the side that does not contain the face 0 (written to sizes, up to cap).
   A triangle is separating when it is not the boundary of a face.         */
BX_API int bx_separating_triangles(const int *F, int nf, int nv, int *sizes, int cap)
{
    BX b; int v, p, q, r, count = 0;
    int *side, *queue;
    if (bx_setup(&b, F, nf, nv, 0)) return -1;
    side = malloc(sizeof(int) * nf); queue = malloc(sizeof(int) * nf);
    for (v = 0; v < b.nv; v++) for (p = b.vstart[v]; p < b.vstart[v + 1]; p++) {
        int w = b.dw[p], f1, f2, x1, x2;
        if (w < v) continue;
        f1 = b.df[p]; x1 = b.F[3 * f1 + (b.dk[p] + 2) % 3];
        q = dart_find(&b, w, v);
        f2 = b.df[q]; x2 = b.F[3 * f2 + (b.dk[q] + 2) % 3];
        q = b.vstart[v]; r = b.vstart[w];
        while (q < b.vstart[v + 1] && r < b.vstart[w + 1]) {
            if (b.dw[q] < b.dw[r]) q++;
            else if (b.dw[q] > b.dw[r]) r++;
            else {
                int x = b.dw[q];
                if (x > w && x != x1 && x != x2) {
                    if (count < cap) {
                        int qh = 0, qt = 0, f, k;
                        memset(side, 0, sizeof(int) * nf);
                        side[0] = 1; queue[qt++] = 0;
                        while (qh < qt) {
                            f = queue[qh++];
                            for (k = 0; k < 3; k++) {
                                int a = b.F[3 * f + k], c = b.F[3 * f + (k + 1) % 3], g = b.nb[3 * f + k];
                                int cut = (a == v || a == w || a == x) && (c == v || c == w || c == x);
                                if (!cut && !side[g]) { side[g] = 1; queue[qt++] = g; }
                            }
                        }
                        sizes[count] = nf - qt;
                    }
                    count++;
                }
                q++; r++;
            }
        }
    }
    free(side); free(queue); bx_free(&b);
    return count;
}

/* ------------------------------------------------------------------ */
/* Hamiltonian cycles of G                                              */
/* ------------------------------------------------------------------ */

/* Counts the perfect matchings M of G for which M^* is acyclic, that is, the
   Hamiltonian cycles G - M (Lemma 2.3).  avoid[3*f+k] is the number of
   Hamiltonian cycles that avoid the dual of the side k of the face f.
   out = [status, number of Hamiltonian cycles, nodes]; status 2: budget.   */
BX_API int bx_hamiltonian_cycles(const int *F, int nf, int nv, i64 budget, i64 *out, i64 *avoid)
{
    BX b; int i, lvl = 0, nb, *bf, *ci, *par, *sz, *ustack, usp = 0, *choice, status = 0;
    unsigned char *matched;
    i64 total = 0, nodes = 0;
    if (bx_setup(&b, F, nf, nv, 0)) return -1;
    nb = nf / 2;
    bf = malloc(sizeof(int) * nb); ci = malloc(sizeof(int) * (nb + 1));
    choice = malloc(sizeof(int) * nb);
    par = malloc(sizeof(int) * nv); sz = malloc(sizeof(int) * nv); ustack = malloc(sizeof(int) * nb);
    matched = calloc(nf, 1);
    for (i = 0, lvl = 0; i < nf; i++) if (b.black[i]) bf[lvl++] = i;
    for (i = 0; i < nv; i++) { par[i] = i; sz[i] = 1; }
    memset(avoid, 0, sizeof(i64) * 3 * nf);
    lvl = 0; ci[0] = 0;
    for (;;) {
        int f, k, g, ra, rb;
        if (lvl == nb) {
            total++;
            for (i = 0; i < nb; i++) {
                int ff = bf[i], kk = choice[i], gg = b.nb[3 * ff + kk], j;
                avoid[3 * ff + kk]++;
                for (j = 0; j < 3; j++) if (b.nb[3 * gg + j] == ff) avoid[3 * gg + j]++;
            }
            goto up;
        }
        if (ci[lvl] >= 3) {
        up:
            if (lvl == 0) break;
            lvl--;
            f = bf[lvl]; k = choice[lvl];
            matched[b.nb[3 * f + k]] = 0;
            { int r = ustack[--usp]; sz[par[r]] -= sz[r]; par[r] = r; }
            continue;
        }
        k = ci[lvl]++;
        f = bf[lvl]; g = b.nb[3 * f + k];
        if (matched[g]) continue;
        ra = uf_find(par, b.F[3 * f + k]); rb = uf_find(par, b.F[3 * f + (k + 1) % 3]);
        if (ra == rb) continue;
        if (++nodes > budget) { status = 2; break; }
        if (sz[ra] > sz[rb]) { int t = ra; ra = rb; rb = t; }
        par[ra] = rb; sz[rb] += sz[ra]; ustack[usp++] = ra;
        matched[g] = 1; choice[lvl] = k;
        lvl++; ci[lvl] = 0;
    }
    out[0] = status; out[1] = total; out[2] = nodes;
    free(bf); free(ci); free(choice); free(par); free(sz); free(ustack); free(matched);
    bx_free(&b);
    return 0;
}

/* ------------------------------------------------------------------ */
/* Canonical form and automorphisms of the plane triangulation          */
/* ------------------------------------------------------------------ */

/* code      canonical code of T up to isomorphism of plane graphs, mirror
             images included (length 3*nf/... = nv + 3*nf ints)
   info      [order of the full group, order of the orientation-preserving
             subgroup, number of automorphisms described below]
   autos     for the first cap automorphisms: nv ints, the image of each
             vertex
   aut_info  for each of them: [1 if orientation-preserving else 0, its
             order, 1 if it fixes a vertex, an edge or a face]
   forbit    face -> least face of its orbit under the full group
   dorbit    (face, side) -> least 3*face+side of its orbit                 */
BX_API int bx_canon(const int *F, int nf, int nv, int *code, i64 *info, int *autos,
                    int *aut_info, int cap, int *forbit, int *dorbit)
{
    BX b; int nd = 3 * nf, i, d, dir, len, mindeg, nbest = 0, nop = 0, first_dir = -1, nstore = 0;
    int *twin, *num, *fd, *cur, *best, *deg, *lab0, *inv0, *fo, *dorb, *img;
    if (bx_setup(&b, F, nf, nv, 0)) return -1;
    for (i = 0; i < nv; i++) if (!b.present[i]) { bx_free(&b); return -2; }
    len = nv + nd;
    twin = malloc(sizeof(int) * nd); num = malloc(sizeof(int) * nv); fd = malloc(sizeof(int) * nv);
    cur = malloc(sizeof(int) * len); best = malloc(sizeof(int) * len); deg = malloc(sizeof(int) * nv);
    lab0 = malloc(sizeof(int) * nv); inv0 = malloc(sizeof(int) * nv);
    fo = malloc(sizeof(int) * nf); dorb = malloc(sizeof(int) * nd); img = malloc(sizeof(int) * nv);
    for (d = 0; d < nd; d++) {
        int f = d / 3, k = d % 3, q = dart_find(&b, F[3 * f + (k + 1) % 3], F[3 * f + k]);
        twin[d] = 3 * b.df[q] + b.dk[q];
    }
    mindeg = nd;
    for (i = 0; i < nv; i++) { deg[i] = b.vstart[i + 1] - b.vstart[i]; if (deg[i] < mindeg) mindeg = deg[i]; }
    for (i = 0; i < nf; i++) fo[i] = i;
    for (i = 0; i < nd; i++) dorb[i] = i;
    for (dir = 0; dir < 2; dir++) for (d = 0; d < nd; d++) {
        int cnt = 1, pos = 0, cmp = 0, v0 = F[d], j;
        if (deg[v0] != mindeg) continue;
        for (i = 0; i < nv; i++) num[i] = -1;
        num[v0] = 0; fd[0] = d;
        for (i = 0; i < nv && cmp <= 0; i++) {
            int e = fd[i], e0 = e;
            do {
                int w = F[3 * (e / 3) + (e % 3 + 1) % 3];
                if (num[w] < 0) { num[w] = cnt; fd[cnt] = twin[e]; cnt++; }
                cur[pos] = num[w] + 1;
                if (nbest && cmp == 0) { if (cur[pos] < best[pos]) cmp = -1; else if (cur[pos] > best[pos]) { cmp = 1; break; } }
                pos++;
                /* next dart around the tail: counterclockwise or clockwise */
                if (dir == 0) e = twin[3 * (e / 3) + (e % 3 + 2) % 3];
                else { int t = twin[e]; e = 3 * (t / 3) + (t % 3 + 1) % 3; }
            } while (e != e0);
            if (cmp > 0) break;
            cur[pos] = 0;
            if (nbest && cmp == 0) { if (cur[pos] < best[pos]) cmp = -1; else if (cur[pos] > best[pos]) { cmp = 1; break; } }
            pos++;
        }
        if (cmp > 0) continue;
        if (!nbest || cmp < 0) {
            memcpy(best, cur, sizeof(int) * len);
            nbest = 0; nop = 0; nstore = 0; first_dir = dir;
            memcpy(lab0, num, sizeof(int) * nv);
            for (j = 0; j < nv; j++) inv0[num[j]] = j;
            for (j = 0; j < nf; j++) fo[j] = j;
            for (j = 0; j < nd; j++) dorb[j] = j;
        }
        nbest++;
        if (dir == first_dir) nop++;
        {   /* the automorphism v -> inv0[num[v]] */
            int op = (dir == first_dir), order = 1, fixed = 0, f, k;
            for (j = 0; j < nv; j++) img[j] = inv0[num[j]];
            for (j = 0; j < nv; j++) num[j] = 0;        /* reuse as visited */
            for (j = 0; j < nv; j++) if (!num[j]) {
                int l = 0, x = j, g, a2, b2;
                while (!num[x]) { num[x] = 1; x = img[x]; l++; }
                if (l == 1) fixed = 1;
                a2 = order; b2 = l;
                while (b2) { g = a2 % b2; a2 = b2; b2 = g; }
                order = order / a2 * l;
            }
            for (f = 0; f < nf; f++) for (k = 0; k < 3; k++) {
                int v = img[F[3 * f + k]], w = img[F[3 * f + (k + 1) % 3]];
                int q = op ? dart_find(&b, v, w) : dart_find(&b, w, v);
                int f2 = b.df[q], k2 = b.dk[q], x, y;
                if (f2 == f) fixed = 1;
                if ((v == F[3 * f + (k + 1) % 3] && w == F[3 * f + k])) fixed = 1;
                /* union the dart orbits and the face orbits */
                x = 3 * f + k; y = 3 * f2 + k2;
                while (dorb[x] != x) x = dorb[x];
                while (dorb[y] != y) y = dorb[y];
                if (x < y) dorb[y] = x; else dorb[x] = y;
                x = f; y = f2;
                while (fo[x] != x) x = fo[x];
                while (fo[y] != y) y = fo[y];
                if (x < y) fo[y] = x; else fo[x] = y;
            }
            if (nstore < cap) {
                memcpy(autos + (size_t)nstore * nv, img, sizeof(int) * nv);
                aut_info[3 * nstore] = op; aut_info[3 * nstore + 1] = order; aut_info[3 * nstore + 2] = fixed;
                nstore++;
            }
        }
    }
    for (i = 0; i < nf; i++) { int x = i; while (fo[x] != x) x = fo[x]; forbit[i] = x; }
    for (i = 0; i < nd; i++) { int x = i; while (dorb[x] != x) x = dorb[x]; dorbit[i] = x; }
    memcpy(code, best, sizeof(int) * len);
    info[0] = nbest; info[1] = nop; info[2] = nstore;
    free(twin); free(num); free(fd); free(cur); free(best); free(deg); free(lab0); free(inv0);
    free(fo); free(dorb); free(img);
    bx_free(&b);
    return 0;
}

/* ------------------------------------------------------------------ */
/* Random states: exact sampling and sequential importance sampling     */
/* ------------------------------------------------------------------ */

static u64 rng_s[4];
static u64 rotl(u64 x, int k) { return (x << k) | (x >> (64 - k)); }
static u64 rng_next(void)
{
    u64 r = rotl(rng_s[1] * 5, 7) * 9, t = rng_s[1] << 17;
    rng_s[2] ^= rng_s[0]; rng_s[3] ^= rng_s[1]; rng_s[1] ^= rng_s[2]; rng_s[0] ^= rng_s[3];
    rng_s[2] ^= t; rng_s[3] = rotl(rng_s[3], 45);
    return r;
}
static void rng_seed(u64 seed)
{
    int i;
    for (i = 0; i < 4; i++) {
        u64 z = (seed += 0x9e3779b97f4a7c15ULL);
        z = (z ^ (z >> 30)) * 0xbf58476d1ce4e5b9ULL;
        z = (z ^ (z >> 27)) * 0x94d049bb133111ebULL;
        rng_s[i] = z ^ (z >> 31);
    }
}
static double rng_unif(void) { return (rng_next() >> 11) * (1.0 / 9007199254740992.0); }

/* Draws states of T and estimates the proportion of good states.

   The states all have the same sign in det K, so in a uniformly random state
   the probability that the face t has the corner x is |K^{-1}[x, t]|.  Fixing
   corners face by face and updating the inverse gives exact uniform samples.

   Uniform draws (n_uniform of them): counts the good states among them and
   adds up the number of cycles of Q_s.
   Importance sampling (n_sis draws): at each face only the corners that pass
   test (2) are allowed, one of them is drawn in proportion to its conditional
   probability, and the weight of the draw is the product over the faces of
   the total conditional probability of the allowed corners (zero if none is
   allowed).  The mean weight is an unbiased estimate of g / M.

   out = [log |det K|, uniform draws that were good, sum of the numbers of
          cycles of Q_s over the uniform draws, mean weight, sum of squared
          weights / n_sis, number of nonzero weights, largest deviation from 1
          of a total conditional probability, largest weight]
   Returns 0, -5 if K is singular (no state), other negatives on bad input. */
BX_API int bx_sample(const int *F, int nf, int nv, int t0, int n_uniform, int n_sis,
                     u64 seed, double *out)
{
    BX b; int n, i, j, k, it, *xi, nx = 0, *perm, rc;
    double *K, *B, *W, logdet = 0, maxdev = 0, sumw = 0, sumw2 = 0, maxw = 0;
    i64 good = 0, cyc = 0, nonzero = 0;
    int *par, *fr, *s, *col;
    unsigned char *usedx;
    rc = bx_setup(&b, F, nf, nv, t0);
    if (rc) return rc;
    n = b.n;
    rng_seed(seed);
    xi = malloc(sizeof(int) * nv);
    for (i = 0; i < nv; i++) xi[i] = (b.present[i] && !b.isroot[i]) ? nx++ : -1;
    K = calloc((size_t)n * 2 * n, sizeof(double));
    /* Gauss-Jordan on [K | I]; K[i][x]: face i, vertex index x */
    for (i = 0; i < n; i++) {
        for (k = 0; k < 3; k++) if (b.hc[3 * i + k] >= 0) K[(size_t)i * 2 * n + xi[b.hc[3 * i + k]]] = 1;
        K[(size_t)i * 2 * n + n + i] = 1;
    }
    perm = malloc(sizeof(int) * n);
    for (j = 0; j < n; j++) {
        int p = j; double best = fabs(K[(size_t)j * 2 * n + j]), piv;
        for (i = j + 1; i < n; i++) if (fabs(K[(size_t)i * 2 * n + j]) > best) { best = fabs(K[(size_t)i * 2 * n + j]); p = i; }
        if (best < 1e-9) { free(K); free(xi); free(perm); bx_free(&b); return -5; }
        if (p != j) for (k = 0; k < 2 * n; k++) {
            double t = K[(size_t)j * 2 * n + k]; K[(size_t)j * 2 * n + k] = K[(size_t)p * 2 * n + k]; K[(size_t)p * 2 * n + k] = t;
        }
        piv = K[(size_t)j * 2 * n + j];
        logdet += log(fabs(piv));
        for (k = 0; k < 2 * n; k++) K[(size_t)j * 2 * n + k] /= piv;
        for (i = 0; i < n; i++) if (i != j) {
            double f = K[(size_t)i * 2 * n + j];
            if (f != 0) for (k = j; k < 2 * n; k++) K[(size_t)i * 2 * n + k] -= f * K[(size_t)j * 2 * n + k];
        }
    }
    /* B[x][i] = (K^{-1})[x][i], row x = vertex index, column i = face */
    B = malloc(sizeof(double) * (size_t)n * n); W = malloc(sizeof(double) * (size_t)n * n);
    for (i = 0; i < n; i++) for (j = 0; j < n; j++) B[(size_t)i * n + j] = K[(size_t)i * 2 * n + n + j];
    free(K); free(perm);
    par = malloc(sizeof(int) * nv); fr = malloc(sizeof(int) * nv); s = malloc(sizeof(int) * (n + 1));
    col = malloc(sizeof(int) * (n + 1)); usedx = malloc(n + 1);
    for (it = 0; it < n_uniform + n_sis; it++) {
        int sis = it >= n_uniform, dead = 0;
        double weight = 1;
        memcpy(W, B, sizeof(double) * (size_t)n * n);
        memset(usedx, 0, n);
        for (i = 0; i < nv; i++) par[i] = i;
        par[b.root[1]] = b.root[0]; par[b.root[2]] = b.root[0];
        for (i = 0; i < n && !dead; i++) {
            double p[3], tot = 0, allowed = 0, u, piv; int x[3], okc[3], ch = -1, f = b.A[i], xc;
            for (k = 0; k < 3; k++) {
                int v = b.hc[3 * i + k];
                p[k] = 0; okc[k] = 0; x[k] = -1;
                if (v < 0 || usedx[xi[v]]) continue;
                x[k] = xi[v];
                p[k] = fabs(W[(size_t)x[k] * n + i]);
                if (p[k] < 1e-12) { p[k] = 0; continue; }
                tot += p[k];
                okc[k] = 1;
                if (sis) {
                    int ra = uf_find(par, b.F[3 * f + (k + 1) % 3]), rb = uf_find(par, b.F[3 * f + (k + 2) % 3]);
                    if (ra == rb) okc[k] = 0;
                }
                if (okc[k]) allowed += p[k];
            }
            if (fabs(tot - 1) > maxdev) maxdev = fabs(tot - 1);
            if (allowed <= 0) { dead = 1; weight = 0; break; }
            weight *= allowed / tot;
            u = rng_unif() * allowed;
            for (k = 0; k < 3; k++) if (okc[k]) { ch = k; if (u < p[k]) break; u -= p[k]; }
            s[i] = b.hc[3 * i + ch]; xc = x[ch]; usedx[xc] = 1;
            if (sis) {
                int ra = uf_find(par, b.F[3 * f + (ch + 1) % 3]), rb = uf_find(par, b.F[3 * f + (ch + 2) % 3]);
                par[ra] = rb;
            }
            piv = W[(size_t)xc * n + i];
            for (j = 0; j < n; j++) if (!usedx[j]) {
                double fct = W[(size_t)j * n + i] / piv;
                if (fct != 0) {
                    double *rowj = W + (size_t)j * n, *rowx = W + (size_t)xc * n;
                    for (k = i + 1; k < n; k++) rowj[k] -= fct * rowx[k];
                }
            }
        }
        if (sis) {
            sumw += weight; sumw2 += weight * weight;
            if (weight > 0) nonzero++;
            if (weight > maxw) maxw = weight;
        } else {
            /* the number of cycles of Q_s: n edges on n+3 vertices, roots identified */
            int q = 0;
            for (i = 0; i < nv; i++) par[i] = i;
            par[b.root[1]] = b.root[0]; par[b.root[2]] = b.root[0];
            for (i = 0; i < n; i++) {
                int f = b.A[i], ra, rb;
                for (k = 0; k < 3; k++) if (b.F[3 * f + k] == s[i]) break;
                ra = uf_find(par, b.F[3 * f + (k + 1) % 3]); rb = uf_find(par, b.F[3 * f + (k + 2) % 3]);
                if (ra == rb) q++; else par[ra] = rb;
            }
            if (q == 0) good++;
            cyc += q;
        }
    }
    out[0] = logdet; out[1] = (double)good; out[2] = (double)cyc;
    out[3] = n_sis ? sumw / n_sis : 0; out[4] = n_sis ? sumw2 / n_sis : 0;
    out[5] = (double)nonzero; out[6] = maxdev; out[7] = maxw;
    free(B); free(W); free(par); free(fr); free(s); free(col); free(usedx); free(xi);
    bx_free(&b);
    return 0;
}

/* ------------------------------------------------------------------ */
/* Random Eulerian triangulations by a Markov chain                     */
/* ------------------------------------------------------------------ */

/* Half-edge structure: the half-edges 2e and 2e+1 are the two directions of
   the edge e; to[h] is the head, nx[h] the next half-edge with the same tail
   in clockwise order, pv[h] the previous one.  The face on the left of h is
   h, nx[h^1], nx[nx[h^1]^1].                                              */
typedef struct {
    int capv, cape, nv, ne;
    int *to, *nx, *pv, *deg, *vh;
    int *vlist, *vpos, *elist, *epos, *vfree, *efree; int nvfree, nefree;
    int *mark; int stamp;
} MC;

static int mc_newv(MC *m)
{
    int v = m->vfree[--m->nvfree];
    m->vpos[v] = m->nv; m->vlist[m->nv++] = v;
    return v;
}
static void mc_delv(MC *m, int v)
{
    int p = m->vpos[v], last = m->vlist[--m->nv];
    m->vlist[p] = last; m->vpos[last] = p; m->vpos[v] = -1;
    m->vfree[m->nvfree++] = v;
}
static int mc_newe(MC *m, int a, int b)       /* returns the half-edge a -> b */
{
    int e = m->efree[--m->nefree];
    m->epos[e] = m->ne; m->elist[m->ne++] = e;
    m->to[2 * e] = b; m->to[2 * e + 1] = a;
    return 2 * e;
}
static void mc_dele(MC *m, int h)
{
    int e = h >> 1, p = m->epos[e], last = m->elist[--m->ne];
    m->elist[p] = last; m->epos[last] = p; m->epos[e] = -1;
    m->efree[m->nefree++] = e;
}
static void mc_link(MC *m, int h1, int h2) { m->nx[h1] = h2; m->pv[h2] = h1; }
static int mc_rand(int k) { return (int)(((rng_next() >> 32) * (u64)k) >> 32); }

/* The split of the vertex a at the half-edges h1 and h2 (same tail a, an odd
   number of half-edges strictly between them on either side).             */
static void mc_split(MC *m, int h1, int h2)
{
    int a = m->to[h1 ^ 1], b = m->to[h1], d = m->to[h2];
    int g1 = m->nx[h2], gq = m->pv[h1], c = mc_newv(m), v = mc_newv(m), g, q = 0;
    int cb, cd, va, vb, vc, vd, ba = h1 ^ 1, da = h2 ^ 1, bnext = m->nx[ba], dprev = m->pv[da];
    for (g = g1; g != h1; g = m->nx[g]) { m->to[g ^ 1] = c; q++; }
    cb = mc_newe(m, c, b); cd = mc_newe(m, c, d);
    va = mc_newe(m, v, a); vb = mc_newe(m, v, b); vc = mc_newe(m, v, c); vd = mc_newe(m, v, d);
    mc_link(m, h2, va ^ 1); mc_link(m, va ^ 1, h1);
    mc_link(m, cd, g1); mc_link(m, gq, cb); mc_link(m, cb, vc ^ 1); mc_link(m, vc ^ 1, cd);
    mc_link(m, ba, vb ^ 1); mc_link(m, vb ^ 1, cb ^ 1); mc_link(m, cb ^ 1, bnext);
    mc_link(m, dprev, cd ^ 1); mc_link(m, cd ^ 1, vd ^ 1); mc_link(m, vd ^ 1, da);
    mc_link(m, vb, va); mc_link(m, va, vd); mc_link(m, vd, vc); mc_link(m, vc, vb);
    m->deg[c] = q + 3; m->deg[a] -= q - 1; m->deg[b] += 2; m->deg[d] += 2; m->deg[v] = 4;
    m->vh[c] = cb; m->vh[v] = va; m->vh[a] = h1;
}

/* The inverse: v has degree four and its neighbours in clockwise order from
   e = v -> b are b, a, d, c; a and c are identified.  If nosep is set, the
   move is refused when it creates a separating triangle.  Returns 1 if the
   move was made; with dry set it only reports whether it is allowed and
   stores the degree of the merged vertex in *dnew.                        */
static int mc_merge(MC *m, int e, int nosep, int dry, int *dnew)
{
    int va = m->nx[e], vd = m->nx[va], vc = m->nx[vd];
    int v = m->to[e ^ 1], a = m->to[va], b = m->to[e], c = m->to[vc], d = m->to[vd];
    int h, h0, common = 0, h1, h2, cv, cd, cb, g1, gq, g, ba, bc, da, dc;
    if (m->deg[v] != 4 || m->nv < 8) return 0;
    m->stamp++;
    h0 = h = m->vh[a];
    do { m->mark[m->to[h]] = m->stamp; h = m->nx[h]; } while (h != h0);
    if (m->mark[c] == m->stamp) return 0;
    h0 = h = m->vh[c];
    do { if (m->mark[m->to[h]] == m->stamp) common++; h = m->nx[h]; } while (h != h0);
    if (common != 3) return 0;
    if (nosep) {
        /* no edge between a neighbour of a and a neighbour of c, other than b, d, v */
        h0 = h = m->vh[c];
        do {
            int y = m->to[h], k, k0;
            if (y != b && y != d && y != v) {
                k0 = k = m->vh[y];
                do {
                    int z = m->to[k];
                    if (z != b && z != d && z != v && z != c && m->mark[z] == m->stamp) return 0;
                    k = m->nx[k];
                } while (k != k0);
            }
            h = m->nx[h];
        } while (h != h0);
    }
    *dnew = m->deg[a] + m->deg[c] - 4;
    if (dry) return 1;
    h1 = m->nx[va ^ 1]; h2 = m->pv[va ^ 1];
    cv = vc ^ 1; cd = m->nx[cv]; cb = m->pv[cv]; g1 = m->nx[cd]; gq = m->pv[cb];
    ba = h1 ^ 1; bc = cb ^ 1; da = h2 ^ 1; dc = cd ^ 1;
    for (g = g1; g != cb; g = m->nx[g]) m->to[g ^ 1] = a;
    mc_link(m, h2, g1); mc_link(m, gq, h1);
    mc_link(m, ba, m->nx[bc]);
    mc_link(m, m->pv[dc], da);
    m->deg[a] = *dnew; m->deg[b] -= 2; m->deg[d] -= 2;
    m->vh[a] = h1; m->vh[b] = ba; m->vh[d] = da;
    mc_dele(m, cb); mc_dele(m, cd); mc_dele(m, va); mc_dele(m, e); mc_dele(m, vc); mc_dele(m, vd);
    mc_delv(m, c); mc_delv(m, v);
    return 1;
}

/* An octahedron in the face on the left of h. */
static void mc_octa(MC *m, int h)
{
    int hy = m->nx[h ^ 1], hz = m->nx[hy ^ 1];
    int x = m->to[hz], y = m->to[h], z = m->to[hy];
    int p = mc_newv(m), q = mc_newv(m), r = mc_newv(m);
    int rx = mc_newe(m, r, x), ry = mc_newe(m, r, y), py = mc_newe(m, p, y), pz = mc_newe(m, p, z);
    int qz = mc_newe(m, q, z), qx = mc_newe(m, q, x), pq = mc_newe(m, p, q), qr = mc_newe(m, q, r);
    int rp = mc_newe(m, r, p);
    mc_link(m, hz ^ 1, qx ^ 1); mc_link(m, qx ^ 1, rx ^ 1); mc_link(m, rx ^ 1, h);
    mc_link(m, h ^ 1, ry ^ 1); mc_link(m, ry ^ 1, py ^ 1); mc_link(m, py ^ 1, hy);
    mc_link(m, hy ^ 1, pz ^ 1); mc_link(m, pz ^ 1, qz ^ 1); mc_link(m, qz ^ 1, hz);
    mc_link(m, ry, rx); mc_link(m, rx, qr ^ 1); mc_link(m, qr ^ 1, rp); mc_link(m, rp, ry);
    mc_link(m, pz, py); mc_link(m, py, rp ^ 1); mc_link(m, rp ^ 1, pq); mc_link(m, pq, pz);
    mc_link(m, qx, qz); mc_link(m, qz, pq ^ 1); mc_link(m, pq ^ 1, qr); mc_link(m, qr, qx);
    m->deg[x] += 2; m->deg[y] += 2; m->deg[z] += 2;
    m->deg[p] = m->deg[q] = m->deg[r] = 4;
    m->vh[p] = pq; m->vh[q] = qr; m->vh[r] = rp;
}

/* The inverse: the face on the left of h = p -> q has three corners of
   degree four.  Returns 1 if the move was made (or is allowed, with dry).  */
static int mc_unocta(MC *m, int h, int dry)
{
    int h2 = m->nx[h ^ 1], h3 = m->nx[h2 ^ 1];
    int p = m->to[h3], q = m->to[h], r = m->to[h2], i;
    int e[9], vs[3], k;
    if (m->deg[p] != 4 || m->deg[q] != 4 || m->deg[r] != 4 || m->nv < 9) return 0;
    if (dry) return 1;
    vs[0] = p; vs[1] = q; vs[2] = r;
    /* the two outer half-edges at each inner vertex, and the three inner edges */
    k = 0;
    {
        int hh[3]; hh[0] = h; hh[1] = h2; hh[2] = h3;      /* p->q, q->r, r->p */
        for (i = 0; i < 3; i++) {
            int o1 = m->nx[hh[i]], o2 = m->nx[o1];         /* two outer half-edges */
            int w1 = m->to[o1], w2 = m->to[o2];
            /* remove o1^1 from the rotation at w1 and o2^1 at w2 */
            mc_link(m, m->pv[o1 ^ 1], m->nx[o1 ^ 1]); m->vh[w1] = m->nx[o1 ^ 1];
            mc_link(m, m->pv[o2 ^ 1], m->nx[o2 ^ 1]); m->vh[w2] = m->nx[o2 ^ 1];
            m->deg[w1]--; m->deg[w2]--;
            e[k++] = o1; e[k++] = o2; e[k++] = hh[i];
        }
    }
    for (i = 0; i < 9; i++) mc_dele(m, e[i]);
    for (i = 0; i < 3; i++) mc_delv(m, vs[i]);
    return 1;
}

/* Metropolis-Hastings chain on simple Eulerian triangulations with at most
   target + headroom vertices; a triangulation with V > target vertices has
   the additional weight gamma^(target - V).  A step proposes, with equal probabilities, a vertex
   split, its inverse, an octahedron in a face, or its inverse (kind 0); with
   kind 1 only the first two, and the inverse is refused if it creates a
   separating triangle.  The acceptance probabilities make the chain
   reversible with respect to the measure that gives every triangulation the
   weight 1/|Aut|, that is, the uniform measure on rooted triangulations of
   each size.  Every `thin` steps, if the triangulation has `target` vertices,
   its faces are written to out (3*(2*target-4) ints per sample).
   stats = [steps, split accepted, merge accepted, octahedron accepted,
            inverse accepted, steps at the target size].                   */
BX_API int bx_mcmc(const int *F, int nf, int nv, int target, int kind, int headroom,
                   double gamma, i64 steps, i64 thin, int nsamples, u64 seed, int *out,
                   int *got, i64 *stats)
{
    MC m; BX b; int i, f, k, rc, *dart2h, maxf = 2 * target - 4;
    i64 step, acc[4] = {0, 0, 0, 0}, attarget = 0;
    rc = bx_setup(&b, F, nf, nv, 0);
    if (rc) return rc;
    if (nv > target + headroom || target < 6) { bx_free(&b); return -4; }
    rng_seed(seed);
    m.capv = target + headroom + 4; m.cape = 3 * m.capv;
    m.to = malloc(sizeof(int) * 2 * m.cape); m.nx = malloc(sizeof(int) * 2 * m.cape);
    m.pv = malloc(sizeof(int) * 2 * m.cape);
    m.deg = calloc(m.capv, sizeof(int)); m.vh = malloc(sizeof(int) * m.capv);
    m.vlist = malloc(sizeof(int) * m.capv); m.vpos = malloc(sizeof(int) * m.capv);
    m.elist = malloc(sizeof(int) * m.cape); m.epos = malloc(sizeof(int) * m.cape);
    m.vfree = malloc(sizeof(int) * m.capv); m.efree = malloc(sizeof(int) * m.cape);
    m.mark = calloc(m.capv, sizeof(int)); m.stamp = 0;
    m.nv = 0; m.ne = 0; m.nvfree = 0; m.nefree = 0;
    for (i = m.capv - 1; i >= 0; i--) m.vfree[m.nvfree++] = i;
    for (i = m.cape - 1; i >= 0; i--) m.efree[m.nefree++] = i;
    for (i = 0; i < nv; i++) mc_newv(&m);
    dart2h = malloc(sizeof(int) * 3 * nf);
    for (i = 0; i < 3 * nf; i++) dart2h[i] = -1;
    for (i = 0; i < 3 * nf; i++) {             /* darts sorted by (tail, head) */
        int v = b.dv[i], w = b.dw[i];
        if (v < w) { int h = mc_newe(&m, v, w); dart2h[i] = h; dart2h[dart_find(&b, w, v)] = h ^ 1; }
    }
    for (f = 0; f < nf; f++) for (k = 0; k < 3; k++) {
        int v = F[3 * f + k], a = F[3 * f + (k + 1) % 3], c = F[3 * f + (k + 2) % 3];
        int hva = dart2h[dart_find(&b, v, a)], hvc = dart2h[dart_find(&b, v, c)];
        mc_link(&m, hvc, hva);
        m.vh[v] = hva; m.deg[v]++;
    }
    free(dart2h);
    *got = 0;
#define MC_W(V) ((V) > target ? pow(gamma, -(double)((V) - target)) : 1.0)
    for (step = 1; step <= steps && *got < nsamples; step++) {
        int type = mc_rand(kind == 1 ? 2 : 4), V = m.nv, E = m.ne;
        if (type == 0) {                       /* split */
            int h1 = 2 * m.elist[mc_rand(E)] + mc_rand(2), a = m.to[h1 ^ 1], d = m.deg[a];
            int j = 1 + mc_rand(d - 1);
            if ((j & 1) == 0 && V + 2 <= target + headroom) {
                double ratio = (2.0 * E * (d - 1)) / (4.0 * (V + 2)) * MC_W(V + 2) / MC_W(V);
                if (ratio >= 1 || rng_unif() < ratio) {
                    int h2 = h1;
                    for (i = 0; i < j; i++) h2 = m.nx[h2];
                    mc_split(&m, h1, h2); acc[0]++;
                }
            }
        } else if (type == 1) {                /* merge */
            int v = m.vlist[mc_rand(V)], e = m.vh[v], dnew;
            if (mc_rand(2)) e = m.nx[e];
            if (mc_merge(&m, e, kind == 1, 1, &dnew)) {
                double ratio = (4.0 * V) / (2.0 * (E - 6) * (dnew - 1)) * MC_W(V - 2) / MC_W(V);
                if (ratio >= 1 || rng_unif() < ratio) { mc_merge(&m, e, kind == 1, 0, &dnew); acc[1]++; }
            }
        } else if (type == 2) {                /* octahedron */
            int h = 2 * m.elist[mc_rand(E)] + mc_rand(2);
            if (V + 3 <= target + headroom) {
                double ratio = (2.0 * V - 4) / (2.0 * V + 2) * MC_W(V + 3) / MC_W(V);
                if (rng_unif() < ratio) { mc_octa(&m, h); acc[2]++; }
            }
        } else {
            int h = 2 * m.elist[mc_rand(E)] + mc_rand(2);
            if (mc_unocta(&m, h, 1)) {
                double ratio = (2.0 * V - 4) / (2.0 * V - 10) * MC_W(V - 3) / MC_W(V);
                if (ratio >= 1 || rng_unif() < ratio) { mc_unocta(&m, h, 0); acc[3]++; }
            }
        }
        if (m.nv == target) attarget++;
        if (step % thin == 0 && m.nv == target) {
            int *o = out + (size_t)(*got) * 3 * maxf, *lab = m.mark, nfo = 0, e;
            unsigned char *seen = calloc(2 * m.cape, 1);
            for (i = 0; i < m.nv; i++) lab[m.vlist[i]] = i;
            for (i = 0; i < m.ne; i++) for (e = 2 * m.elist[i]; e < 2 * m.elist[i] + 2; e++) {
                if (!seen[e]) {
                    int e2 = m.nx[e ^ 1], e3 = m.nx[e2 ^ 1];
                    seen[e] = seen[e2] = seen[e3] = 1;
                    o[3 * nfo] = lab[m.to[e3]]; o[3 * nfo + 1] = lab[m.to[e]]; o[3 * nfo + 2] = lab[m.to[e2]];
                    nfo++;
                }
            }
            free(seen);
            for (i = 0; i < m.capv; i++) m.mark[i] = 0;
            m.stamp = 0;
            (*got)++;
        }
    }
    stats[0] = step - 1; stats[1] = acc[0]; stats[2] = acc[1]; stats[3] = acc[2]; stats[4] = acc[3];
    stats[5] = attarget;
    free(m.to); free(m.nx); free(m.pv); free(m.deg); free(m.vh); free(m.vlist); free(m.vpos);
    free(m.elist); free(m.epos); free(m.vfree); free(m.efree); free(m.mark);
    bx_free(&b);
    return 0;
}

/* ------------------------------------------------------------------ */
/* The structure of the separating triangles                            */
/* ------------------------------------------------------------------ */

/* Cutting T along all its separating triangles leaves pieces, which form a
   tree with one edge for every separating triangle.
   out = [number of separating triangles, diameter of the tree (the largest
          number of separating triangles between two faces), largest n of a
          piece, smallest n of a piece].  A piece with k faces of T and c
   separating triangles on its boundary is a triangulation with k + c faces,
   so its n is (k + c)/2 - 1.                                              */
BX_API int bx_sep_structure(const int *F, int nf, int nv, int *out)
{
    BX b; int v, p, q, r, ns = 0, cap = 64, f, k, i;
    unsigned char *far; int *queue, *tri, *d0, *cnt;
    u64 *sig, *hash;
    if (bx_setup(&b, F, nf, nv, 0)) return -1;
    far = malloc((size_t)cap * nf); tri = malloc(sizeof(int) * 3 * cap);
    queue = malloc(sizeof(int) * nf);
    for (v = 0; v < b.nv; v++) for (p = b.vstart[v]; p < b.vstart[v + 1]; p++) {
        int w = b.dw[p], x1, x2;
        if (w < v) continue;
        x1 = b.F[3 * b.df[p] + (b.dk[p] + 2) % 3];
        q = dart_find(&b, w, v);
        x2 = b.F[3 * b.df[q] + (b.dk[q] + 2) % 3];
        q = b.vstart[v]; r = b.vstart[w];
        while (q < b.vstart[v + 1] && r < b.vstart[w + 1]) {
            if (b.dw[q] < b.dw[r]) q++;
            else if (b.dw[q] > b.dw[r]) r++;
            else {
                int x = b.dw[q];
                if (x > w && x != x1 && x != x2) {
                    int qh = 0, qt = 0;
                    unsigned char *row;
                    if (ns == cap) {
                        cap *= 2;
                        far = realloc(far, (size_t)cap * nf); tri = realloc(tri, sizeof(int) * 3 * cap);
                    }
                    row = far + (size_t)ns * nf;
                    memset(row, 1, nf);
                    row[0] = 0; queue[qt++] = 0;
                    while (qh < qt) {
                        f = queue[qh++];
                        for (k = 0; k < 3; k++) {
                            int a = b.F[3 * f + k], c = b.F[3 * f + (k + 1) % 3], g = b.nb[3 * f + k];
                            int cut = (a == v || a == w || a == x) && (c == v || c == w || c == x);
                            if (!cut && row[g]) { row[g] = 0; queue[qt++] = g; }
                        }
                    }
                    tri[3 * ns] = v; tri[3 * ns + 1] = w; tri[3 * ns + 2] = x;
                    ns++;
                }
                q++; r++;
            }
        }
    }
    sig = calloc(nf, sizeof(u64)); hash = malloc(sizeof(u64) * (ns + 1));
    d0 = calloc(nf, sizeof(int));
    rng_seed(12345);
    for (i = 0; i < ns; i++) hash[i] = rng_next();
    for (i = 0; i < ns; i++) for (f = 0; f < nf; f++)
        if (far[(size_t)i * nf + f]) { sig[f] ^= hash[i]; d0[f]++; }
    {
        int f1 = 0, diam = 0, maxn = 0, minn = nf;
        for (f = 0; f < nf; f++) if (d0[f] > d0[f1]) f1 = f;
        for (f = 0; f < nf; f++) {
            int d = 0;
            for (i = 0; i < ns; i++) d += far[(size_t)i * nf + f] != far[(size_t)i * nf + f1];
            if (d > diam) diam = d;
        }
        /* pieces: a piece is known by the set of triangles that separate it
           from the face 0; a triangle bounds the piece just beyond it and
           the piece just before it */
        {
            int np = 0, j, *size = calloc(ns + 1, sizeof(int));
            u64 *key = malloc(sizeof(u64) * (nf + 2 * ns + 1));
            u64 *sfar = malloc(sizeof(u64) * (ns + 1));
            cnt = calloc(nf + 2 * ns + 1, sizeof(int));
            for (i = 0; i < ns; i++) for (f = 0; f < nf; f++) size[i] += far[(size_t)i * nf + f];
            for (i = 0; i < ns; i++) {
                int d1 = dart_find(&b, tri[3 * i], tri[3 * i + 1]), d2 = dart_find(&b, tri[3 * i + 1], tri[3 * i]);
                int fi = far[(size_t)i * nf + b.df[d1]] ? b.df[d1] : b.df[d2];
                sfar[i] = 0;
                for (j = 0; j < ns; j++)
                    if (far[(size_t)j * nf + fi] && size[j] >= size[i]) sfar[i] ^= hash[j];
            }
            for (f = 0; f < nf + 2 * ns; f++) {
                u64 kf = f < nf ? sig[f] : (f - nf) % 2 ? sfar[(f - nf) / 2] : sfar[(f - nf) / 2] ^ hash[(f - nf) / 2];
                for (j = 0; j < np && key[j] != kf; j++);
                if (j == np) key[np++] = kf;
                cnt[j]++;
            }
            for (j = 0; j < np; j++) {
                int n = cnt[j] / 2 - 1;
                if (n > maxn) maxn = n;
                if (n < minn) minn = n;
            }
            free(size); free(key); free(sfar); free(cnt);
        }
        out[0] = ns; out[1] = diam; out[2] = maxn; out[3] = minn;
    }
    free(far); free(tri); free(queue); free(sig); free(hash); free(d0);
    bx_free(&b);
    return 0;
}
