// descent.cpp -- exhaustive analysis of descent variants on the exchange graph.
//
// Input (stdin), one triangulation per line, either
//   plantri ascii:  "V abc,def,..."          (rotation order as printed by plantri -a)
//   text format:    "V d n1..nd d n1..nd ... [r0 r1 r2]"   (bar.c -t / gen.py format)
// For every rooted instance (every face as t0, or the given roots) the program
//   1. enumerates all 2-factors u of the incidence graph and all 2^c ordered pairs (r,s),
//   2. builds the exchange graph (D-swaps, Q-reversals),
//   3. checks that Psi (changed by Q-reversals) and omega (changed by D-swaps) are
//      well-defined potentials (path independent),
//   4. for each potential in the menu reports: trapped pairs under non-increasing moves
//      (with single moves and with macro moves of length <= 2), strict local minima,
//      lookahead radius, longest shortest monotone path, longest strict descent path.
// Output: one summary line per potential ("S ..."), and witness lines ("W ...") for the
// first few failures of each kind.
//
// Conventions: a pair is stored per face of A as corner indices (ri, si) in 0..2.
// "inside" of a cycle = the side not containing the outer face t0.
// sense of a directed cycle = +1 if the traced face of its first dart is inside.
#include <bits/stdc++.h>
using namespace std;
typedef long long ll;

static int V;
static vector<vector<int>> rot;
static vector<array<int,3>> faces;
static map<pair<int,int>,int> faceOf;   // dart -> face
static int F;

static void buildFaces() {
    faces.clear(); faceOf.clear();
    vector<map<int,int>> pos(V);
    for (int v = 0; v < V; v++) for (int i = 0; i < (int)rot[v].size(); i++) pos[v][rot[v][i]] = i;
    for (int v = 0; v < V; v++) for (int w : rot[v]) {
        if (faceOf.count({v,w})) continue;
        vector<int> f; int a = v, b = w;
        while (!faceOf.count({a,b})) {
            faceOf[{a,b}] = faces.size(); f.push_back(a);
            int d = rot[b].size();
            int c = rot[b][(pos[b][a] - 1 + d) % d];
            a = b; b = c;
        }
        if (f.size() != 3) { fprintf(stderr, "non-triangular face\n"); exit(1); }
        faces.push_back({f[0], f[1], f[2]});
    }
    F = faces.size();
}

struct Inst {
    int t0; vector<int> col;            // 0 = black (colour of t0)
    vector<int> A; int n;               // black faces other than t0
    vector<array<int,3>> fc;            // corners of A faces
    vector<char> isRoot;
    vector<vector<int>> fadj;           // dual adjacency: fadj[f][j] = face across edge j
    bool init(int root) {
        t0 = root; col.assign(F, -1); col[t0] = 0;
        vector<int> st = {t0};
        fadj.assign(F, {});
        for (int f = 0; f < F; f++) { auto &q = faces[f]; for (int j = 0; j < 3; j++) fadj[f].push_back(faceOf[{q[(j+1)%3], q[j]}]); }
        while (!st.empty()) { int f = st.back(); st.pop_back(); for (int g : fadj[f]) { if (col[g] < 0) { col[g] = 1 - col[f]; st.push_back(g); } else if (col[g] == col[f]) return false; } }
        A.clear(); fc.clear();
        for (int f = 0; f < F; f++) if (col[f] == 0 && f != t0) { A.push_back(f); fc.push_back(faces[f]); }
        n = A.size();
        isRoot.assign(V, 0); for (int v : faces[t0]) isRoot[v] = 1;
        return true;
    }
    // inside of a closed walk given by its vertex sequence; returns white count, sets sense
    int enclosed(const vector<int>& cyc, int &sense) const {
        set<pair<int,int>> blocked;
        int h = cyc.size();
        for (int i = 0; i < h; i++) { int a = cyc[i], b = cyc[(i+1)%h]; blocked.insert({min(a,b), max(a,b)}); }
        vector<char> out(F, 0); out[t0] = 1; vector<int> st = {t0};
        while (!st.empty()) {
            int f = st.back(); st.pop_back(); auto &q = faces[f];
            for (int j = 0; j < 3; j++) {
                int a = q[j], b = q[(j+1)%3];
                if (blocked.count({min(a,b), max(a,b)})) continue;
                int g = fadj[f][j]; if (!out[g]) { out[g] = 1; st.push_back(g); }
            }
        }
        int W = 0; for (int f = 0; f < F; f++) if (!out[f] && col[f] == 1) W++;
        int lf = faceOf.at({cyc[0], cyc[1]});
        sense = out[lf] ? -1 : +1;
        return W;
    }
};

struct Move { int to; int type; int W; int sense; int len; };   // type 0 = D-swap, 1 = Q-reversal
struct Node {
    string key; int k, c, vq, wq, wd; ll psi, om; bool have;
    vector<Move> mv;
};

static Inst I;
static vector<Node> nodes;
static unordered_map<string,int> idx;

struct Cyc { vector<int> fs; vector<int> vs; };
static void dcycles(const string& key, vector<Cyc>& out) {
    int n = I.n; out.clear();
    vector<int> sv(V, -1), sf(V, -1);
    for (int i = 0; i < n; i++) { int ri = key[i] / 3, si = key[i] % 3; sv[I.fc[i][ri]] = I.fc[i][si]; sf[I.fc[i][ri]] = i; }
    vector<char> seen(V, 0);
    for (int x = 0; x < V; x++) if (sf[x] >= 0 && !seen[x]) {
        Cyc c; int y = x;
        while (!seen[y]) { seen[y] = 1; c.fs.push_back(sf[y]); c.vs.push_back(y); y = sv[y]; }
        out.push_back(c);
    }
}
static void qcycles(const string& key, vector<Cyc>& out) {
    int n = I.n; out.clear();
    vector<int> sv(V, -1), sf(V, -1);
    for (int i = 0; i < n; i++) { int ri = key[i] / 3, si = key[i] % 3, ui = 3 - ri - si; sv[I.fc[i][ri]] = I.fc[i][ui]; sf[I.fc[i][ri]] = i; }
    vector<int> colr(V, -1);
    for (int x0 = 0; x0 < V; x0++) if (sf[x0] >= 0 && colr[x0] < 0) {
        int x = x0;
        while (sf[x] >= 0 && colr[x] < 0) { colr[x] = x0; x = sv[x]; }
        if (sf[x] >= 0 && colr[x] == x0) {
            Cyc c; int y = x;
            do { c.fs.push_back(sf[y]); c.vs.push_back(y); y = sv[y]; } while (y != x);
            out.push_back(c);
        }
    }
}

// enumerate 2-factors
static vector<int> need, remc, ucur;
static vector<string> allpairs;
static ll nfactors;
static void emitFactor() {
    nfactors++;
    int n = I.n;
    // kept corners per face; cycles of D
    vector<array<int,2>> vf(V, {-1,-1});
    for (int i = 0; i < n; i++) for (int j = 0; j < 3; j++) if (j != ucur[i]) { int x = I.fc[i][j]; if (vf[x][0] < 0) vf[x][0] = i; else vf[x][1] = i; }
    vector<vector<pair<int,int>>> cycs;   // list of (face, tailcorner index) in one orientation
    vector<char> fseen(n, 0);
    for (int i0 = 0; i0 < n; i0++) if (!fseen[i0]) {
        vector<pair<int,int>> cy; int i = i0; int tail = -1;
        for (int j = 0; j < 3; j++) if (j != ucur[i]) { tail = j; break; }
        while (!fseen[i]) {
            fseen[i] = 1; cy.push_back({i, tail});
            int head = 3 - ucur[i] - tail; int y = I.fc[i][head];
            int nx = vf[y][0] == i ? vf[y][1] : vf[y][0];
            int nt = -1; for (int j = 0; j < 3; j++) if (I.fc[nx][j] == y) nt = j;
            i = nx; tail = nt;
        }
        cycs.push_back(cy);
    }
    int c = cycs.size();
    for (int mask = 0; mask < (1 << c); mask++) {
        string key(n, 0);
        for (int j = 0; j < c; j++) for (auto &pr : cycs[j]) {
            int i = pr.first, tail = pr.second, head = 3 - ucur[i] - tail;
            int ri = (mask >> j & 1) ? head : tail, si = (mask >> j & 1) ? tail : head;
            key[i] = ri * 3 + si;
        }
        allpairs.push_back(key);
    }
}
static void recFactor(int i) {
    int n = I.n;
    if (i == n) { emitFactor(); return; }
    // feasibility: for each corner of remaining faces, remc >= need (checked incrementally)
    auto &q = I.fc[i];
    int rootc = -1, nroots = 0;
    for (int j = 0; j < 3; j++) if (I.isRoot[q[j]]) { rootc = j; nroots++; }
    for (int j = 0; j < 3; j++) remc[q[j]]--;
    for (int j = 0; j < 3; j++) {
        int x = q[j];
        if (nroots) { if (j != rootc) continue; }
        else if (need[x] == 0) continue;
        if (!I.isRoot[x]) need[x]--;
        bool ok = true;
        for (int jj = 0; jj < 3; jj++) { int y = q[jj]; if (!I.isRoot[y] && need[y] > remc[y]) ok = false; }
        if (ok) { ucur[i] = j; recFactor(i + 1); }
        if (!I.isRoot[x]) need[x]++;
    }
    for (int j = 0; j < 3; j++) remc[q[j]]++;
}

static bool enumeratePairs() {
    int n = I.n; allpairs.clear(); nfactors = 0;
    need.assign(V, 0); remc.assign(V, 0); ucur.assign(n, 0);
    for (int i = 0; i < n; i++) { int nr = 0; for (int j = 0; j < 3; j++) { remc[I.fc[i][j]]++; nr += I.isRoot[I.fc[i][j]]; } if (nr >= 2) return false; }
    for (int x = 0; x < V; x++) if (!I.isRoot[x]) { need[x] = remc[x] - 2; if (need[x] < 0) return false; }
    recFactor(0);
    return !allpairs.empty();
}

static void computeNode(int id) {
    Node &nd = nodes[id];
    int n = I.n;
    vector<Cyc> dc, qc; dcycles(nd.key, dc); qcycles(nd.key, qc);
    nd.c = dc.size(); nd.k = qc.size(); nd.vq = 0; nd.wq = 0; nd.wd = 0;
    for (auto &c : dc) {
        int sense; int W = I.enclosed(c.vs, sense); nd.wd += W;
        string k2 = nd.key;
        for (int i : c.fs) { int ri = k2[i] / 3, si = k2[i] % 3; k2[i] = si * 3 + ri; }
        auto it = idx.find(k2); if (it == idx.end()) { fprintf(stderr, "closure failure D\n"); exit(1); }
        nd.mv.push_back({it->second, 0, W, sense, (int)c.fs.size()});
    }
    for (auto &c : qc) {
        int sense; int W = I.enclosed(c.vs, sense); nd.wq += W; nd.vq += c.vs.size();
        string k2 = nd.key;
        for (int i : c.fs) { int ri = k2[i] / 3, si = k2[i] % 3, ui = 3 - ri - si; k2[i] = ui * 3 + si; }
        auto it = idx.find(k2); if (it == idx.end()) { fprintf(stderr, "closure failure Q\n"); exit(1); }
        nd.mv.push_back({it->second, 1, W, sense, (int)c.fs.size()});
    }
    (void)n;
}

// ---- potentials ----
typedef array<ll,4> Phi;
static const int NPOT = 28;
static const char* potName[NPOT] = {
    "k", "k+c", "vq", "wq", "(k,c)", "(c,k)", "(c,wq)", "(k,wq)", "(k,vq)", "(c,vq)",
    "(k,+psi,+om)", "(k,+psi,-om)", "(k,-psi,+om)", "(k,-psi,-om)",
    "(k,+om,+psi)", "(k,+om,-psi)", "(k,-om,+psi)", "(k,-om,-psi)",
    "(k,+psi)", "(k,-psi)", "(k,+om)", "(k,-om)",
    "(k,c,wq)", "(k,wq+wd)", "wq+wd", "(c,k,wq)", "(k,c,+psi)", "(k,c,-psi)" };
static Phi pot(int p, const Node& x) {
    ll k = x.k, c = x.c, P = x.psi, O = x.om;
    switch (p) {
        case 0: return {k,0,0,0}; case 1: return {k+c,0,0,0}; case 2: return {x.vq,0,0,0}; case 3: return {x.wq,0,0,0};
        case 4: return {k,c,0,0}; case 5: return {c,k,0,0}; case 6: return {c,x.wq,0,0}; case 7: return {k,x.wq,0,0};
        case 8: return {k,x.vq,0,0}; case 9: return {c,x.vq,0,0};
        case 10: return {k,P,O,0}; case 11: return {k,P,-O,0}; case 12: return {k,-P,O,0}; case 13: return {k,-P,-O,0};
        case 14: return {k,O,P,0}; case 15: return {k,O,-P,0}; case 16: return {k,-O,P,0}; case 17: return {k,-O,-P,0};
        case 18: return {k,P,0,0}; case 19: return {k,-P,0,0}; case 20: return {k,O,0,0}; case 21: return {k,-O,0,0};
        case 22: return {k,c,x.wq,0}; case 23: return {k,x.wq+x.wd,0,0}; case 24: return {x.wq+x.wd,0,0,0};
        case 25: return {c,k,x.wq,0}; case 26: return {k,c,P,0}; case 27: return {k,c,-P,0};
    }
    return {0,0,0,0};
}

struct Stat {
    ll nontarget = 0, trapped1 = 0, trapped2 = 0, sinks = 0, instTrap1 = 0, instTrap2 = 0, instSink = 0;
    int maxRho = 0, maxMono = 0, maxStrictLong = 0; ll rhoHist[8] = {0};
    int wit1 = 0, wit2 = 0, witS = 0, witR = 0;
};
static Stat stats[NPOT];
static ll totInst = 0, totPairs = 0, totTree = 0, totFactors = 0, totComp = 0, maxFree = 0, totNontarget = 0;
static ll kHist[16] = {0};
static int maxWit = 2;
static string curLine; static int curGraph;

static string pairStr(const Node& x) {
    string s; for (int i = 0; i < I.n; i++) { if (i) s += ' '; s += to_string(I.fc[i][x.key[i]/3]) + ">" + to_string(I.fc[i][x.key[i]%3]); } return s;
}
static void witness(const char* kind, int p, int id, int extra) {
    printf("W %s pot=%s V=%d graph=%d t0=%d,%d,%d k=%d c=%d extra=%d | %s | faces", kind, potName[p], V, curGraph,
           faces[I.t0][0], faces[I.t0][1], faces[I.t0][2], nodes[id].k, nodes[id].c, extra, curLine.c_str());
    for (int i = 0; i < I.n; i++) printf(" %d,%d,%d", I.fc[i][0], I.fc[i][1], I.fc[i][2]);
    printf(" | pair %s\n", pairStr(nodes[id]).c_str());
}

static bool quiet = false; static int potMask = -1;
static void analyse() {
    int N = nodes.size();
    // potentials psi, omega by traversal; consistency check
    vector<int> comp(N, -1); int ncomp = 0;
    for (int s = 0; s < N; s++) if (comp[s] < 0) {
        comp[s] = ncomp; nodes[s].psi = 0; nodes[s].om = 0; vector<int> st = {s};
        while (!st.empty()) {
            int a = st.back(); st.pop_back();
            for (auto &m : nodes[a].mv) {
                ll np = nodes[a].psi, no = nodes[a].om;
                if (m.type == 0) no -= (ll)m.W * m.sense; else np -= (ll)m.W * m.sense;
                if (comp[m.to] < 0) { comp[m.to] = ncomp; nodes[m.to].psi = np; nodes[m.to].om = no; st.push_back(m.to); }
                else if (nodes[m.to].psi != np || nodes[m.to].om != no) { fprintf(stderr, "POTENTIAL INCONSISTENT graph %d\n", curGraph); exit(2); }
            }
        }
        ncomp++;
    }
    totComp += ncomp;
    vector<char> hasTree(ncomp, 0);
    for (int a = 0; a < N; a++) { if (nodes[a].k == 0) { hasTree[comp[a]] = 1; totTree++; } kHist[min(nodes[a].k, 15)]++; }
    for (int cidx = 0; cidx < ncomp; cidx++) if (!hasTree[cidx]) { fprintf(stderr, "COMPONENT WITHOUT TREE PAIR graph %d\n", curGraph); exit(3); }
    // free distance to target
    {
        vector<int> d(N, -1); deque<int> q;
        for (int a = 0; a < N; a++) if (nodes[a].k == 0) { d[a] = 0; q.push_back(a); }
        while (!q.empty()) { int a = q.front(); q.pop_front(); for (auto &m : nodes[a].mv) if (d[m.to] < 0) { d[m.to] = d[a] + 1; q.push_back(m.to); } }
        for (int a = 0; a < N; a++) maxFree = max(maxFree, (ll)d[a]);
    }
    // 2-neighbourhoods
    vector<vector<int>> n2(N);
    for (int a = 0; a < N; a++) {
        set<int> s2;
        for (auto &m : nodes[a].mv) { s2.insert(m.to); for (auto &m2 : nodes[m.to].mv) s2.insert(m2.to); }
        s2.erase(a); n2[a].assign(s2.begin(), s2.end());
    }
    vector<Phi> ph(N);
    for (int p = 0; p < NPOT; p++) {
        if (!(potMask >> p & 1)) continue;
        Stat &S = stats[p];
        for (int a = 0; a < N; a++) ph[a] = pot(p, nodes[a]);
        // reverse BFS, single moves
        vector<int> d1(N, -1), d2(N, -1); deque<int> q;
        for (int a = 0; a < N; a++) if (nodes[a].k == 0) { d1[a] = 0; q.push_back(a); }
        while (!q.empty()) { int b = q.front(); q.pop_front(); for (auto &m : nodes[b].mv) { int a = m.to; if (d1[a] < 0 && ph[b] <= ph[a]) { d1[a] = d1[b] + 1; q.push_back(a); } } }
        for (int a = 0; a < N; a++) if (nodes[a].k == 0) { d2[a] = 0; q.push_back(a); }
        while (!q.empty()) { int b = q.front(); q.pop_front(); for (int a : n2[b]) if (d2[a] < 0 && ph[b] <= ph[a]) { d2[a] = d2[b] + 1; q.push_back(a); } }
        bool it1 = false, it2 = false, its = false;
        // longest strict descent path (adversarial), by DP in increasing phi order
        vector<int> order(N); iota(order.begin(), order.end(), 0);
        sort(order.begin(), order.end(), [&](int a, int b) { return ph[a] < ph[b]; });
        vector<int> L(N, 0);
        for (int a : order) { int best = 0; for (auto &m : nodes[a].mv) if (ph[m.to] < ph[a]) best = max(best, L[m.to] + 1); L[a] = best; }
        for (int a = 0; a < N; a++) {
            if (nodes[a].k == 0) continue;
            S.nontarget++;
            S.maxStrictLong = max(S.maxStrictLong, L[a]);
            if (d1[a] < 0) { S.trapped1++; if (!it1 && S.wit1 < maxWit) { S.wit1++; witness("TRAP1", p, a, 0); } it1 = true; }
            else S.maxMono = max(S.maxMono, d1[a]);
            if (d2[a] < 0) { S.trapped2++; if (!it2 && S.wit2 < maxWit) { S.wit2++; witness("TRAP2", p, a, 0); } it2 = true; }
            bool strict = false; for (auto &m : nodes[a].mv) if (ph[m.to] < ph[a]) { strict = true; break; }
            int rho = 1;
            if (!strict) {
                S.sinks++; if (!its && S.witS < maxWit) { S.witS++; witness("SINK", p, a, 0); } its = true;
                // lookahead radius: BFS to strictly smaller phi
                vector<int> dd(N, -1); deque<int> qq; dd[a] = 0; qq.push_back(a); rho = -1;
                while (!qq.empty() && rho < 0) { int b = qq.front(); qq.pop_front(); for (auto &m : nodes[b].mv) if (dd[m.to] < 0) { dd[m.to] = dd[b] + 1; if (ph[m.to] < ph[a]) { rho = dd[m.to]; break; } qq.push_back(m.to); } }
                if (rho < 0) rho = 99;   // no strictly smaller value in the component
            }
            if (rho > S.maxRho && rho >= 3 && S.witR < 6) { S.witR++; witness("RHO", p, a, rho); }
            S.maxRho = max(S.maxRho, rho); S.rhoHist[min(rho, 7)]++;
        }
        S.instTrap1 += it1; S.instTrap2 += it2; S.instSink += its;
    }
}

static bool parseLine(const string& line, array<int,3>& roots, bool& hasRoots) {
    hasRoots = false; rot.clear();
    if (line.find(',') != string::npos || (line.size() > 2 && isalpha(line[line.find(' ') + 1]))) {
        istringstream is(line); string adj; is >> V >> adj;
        rot.assign(V, {}); int v = 0;
        for (char ch : adj) { if (ch == ',') v++; else rot[v].push_back(ch - 'a'); }
        return true;
    }
    istringstream is(line); vector<int> a; int x; while (is >> x) a.push_back(x);
    if (a.empty()) return false;
    V = a[0]; rot.assign(V, {}); size_t p = 1;
    for (int v = 0; v < V; v++) { int d = a[p++]; for (int j = 0; j < d; j++) rot[v].push_back(a[p++]); }
    if (a.size() >= p + 3) { hasRoots = true; roots = {a[p], a[p+1], a[p+2]}; }
    return true;
}

int main(int argc, char** argv) {
    ll capPairs = 2000000; int onlyGraph = -1; bool allRoots = false;
    for (int i = 1; i < argc; i++) {
        string a = argv[i];
        if (a == "-w") maxWit = atoi(argv[++i]);
        else if (a == "-cap") capPairs = atoll(argv[++i]);
        else if (a == "-g") onlyGraph = atoi(argv[++i]);
        else if (a == "-pots") potMask = strtol(argv[++i], 0, 0);
        else if (a == "-allroots") allRoots = true;
    }
    string line; curGraph = -1; ll skipped = 0;
    while (getline(cin, line)) {
        if (line.empty()) continue;
        array<int,3> roots; bool hasRoots;
        if (!parseLine(line, roots, hasRoots)) continue;
        curGraph++; if (onlyGraph >= 0 && curGraph != onlyGraph) continue;
        curLine = line; buildFaces();
        for (int t0 = 0; t0 < F; t0++) {
            if (hasRoots && !allRoots) { set<int> a(faces[t0].begin(), faces[t0].end()), b(roots.begin(), roots.end()); if (a != b) continue; }
            if (!I.init(t0)) { fprintf(stderr, "not Eulerian\n"); exit(1); }
            if (!enumeratePairs()) continue;
            if ((ll)allpairs.size() > capPairs) { skipped++; continue; }
            totInst++; totPairs += allpairs.size(); totFactors += nfactors;
            nodes.clear(); idx.clear(); nodes.resize(allpairs.size());
            for (size_t j = 0; j < allpairs.size(); j++) { nodes[j].key = allpairs[j]; idx[allpairs[j]] = j; }
            for (size_t j = 0; j < allpairs.size(); j++) computeNode(j);
            analyse();
        }
    }
    printf("T V=%d rooted_with_pair=%lld factors=%lld pairs=%lld tree_pairs=%lld components=%lld max_free_dist=%lld skipped=%lld\n",
           V, totInst, totFactors, totPairs, totTree, totComp, maxFree, skipped);
    printf("K V=%d khist", V); for (int j = 0; j < 16; j++) if (kHist[j]) printf(" %d:%lld", j, kHist[j]); printf("\n");
    for (int p = 0; p < NPOT; p++) {
        if (!(potMask >> p & 1)) continue;
        Stat &S = stats[p];
        printf("S V=%d pot=%s nontarget=%lld trap1=%lld(inst %lld) trap2=%lld(inst %lld) sinks=%lld(inst %lld) maxrho=%d maxmono=%d maxstrictlen=%d rhohist",
               V, potName[p], S.nontarget, S.trapped1, S.instTrap1, S.trapped2, S.instTrap2, S.sinks, S.instSink, S.maxRho, S.maxMono, S.maxStrictLong);
        for (int j = 1; j < 8; j++) printf(" %d:%lld", j, S.rhoHist[j]);
        printf("\n");
    }
    return 0;
}
