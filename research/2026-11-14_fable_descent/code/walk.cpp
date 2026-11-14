// walk.cpp -- sampling version of descent.cpp for instances too large to enumerate.
//
// For each input triangulation (same formats as descent.cpp) and up to R roots with a pair:
//   start from a max-flow 2-factor with random cycle directions, run a random walk on the
//   exchange graph (biased towards many Q-cycles), and at sampled pairs with k > 0 measure
//     sink   : no single D-swap lowers k
//     rho    : least number of exchange moves to a pair with smaller k (BFS, capped)
//     C3     : is k = 0 reachable by moves that never increase k (BFS, capped)
//     len    : number of moves used by "nearest improvement" descent (repeat: go to the
//              nearest pair with smaller k) until k = 0
// Usage: walk.exe [-R roots] [-steps n] [-gap g] [-bias b] [-seed s] [-dcap depth] [-ncap nodes]
#define main descent_main
#include "descent.cpp"
#undef main

static mt19937_64 rng(1);
struct LNode { int k; vector<string> nb; vector<char> ty; };
static unordered_map<string, LNode> cache;

static const LNode& expand(const string& key) {
    auto it = cache.find(key);
    if (it != cache.end()) return it->second;
    LNode nd; vector<Cyc> dc, qc; dcycles(key, dc); qcycles(key, qc);
    nd.k = qc.size();
    for (auto &c : dc) { string k2 = key; for (int i : c.fs) { int ri = k2[i] / 3, si = k2[i] % 3; k2[i] = si * 3 + ri; } nd.nb.push_back(k2); nd.ty.push_back(0); }
    for (auto &c : qc) { string k2 = key; for (int i : c.fs) { int ri = k2[i] / 3, si = k2[i] % 3, ui = 3 - ri - si; k2[i] = ui * 3 + si; } nd.nb.push_back(k2); nd.ty.push_back(1); }
    return cache.emplace(key, std::move(nd)).first->second;
}
static int kOf(const string& key) { vector<Cyc> qc; qcycles(key, qc); return qc.size(); }

// max-flow 2-factor (Kuhn with capacities)
static vector<int> asg; static vector<vector<int>> load; static vector<char> vis;
static bool tryFace(int i) {
    for (int j = 0; j < 3; j++) {
        int x = I.fc[i][j]; if (I.isRoot[x] || vis[x]) continue; vis[x] = 1;
        if ((int)load[x].size() < need[x]) { load[x].push_back(i); asg[i] = j; return true; }
        for (size_t q = 0; q < load[x].size(); q++) { int f2 = load[x][q]; if (tryFace(f2)) { load[x][q] = i; asg[i] = j; return true; } }
    }
    return false;
}
static bool flowFactor(string& key) {
    int n = I.n; need.assign(V, 0); vector<int> cnt(V, 0);
    for (int i = 0; i < n; i++) { int nr = 0; for (int j = 0; j < 3; j++) { cnt[I.fc[i][j]]++; nr += I.isRoot[I.fc[i][j]]; } if (nr >= 2) return false; }
    for (int x = 0; x < V; x++) if (!I.isRoot[x]) { need[x] = cnt[x] - 2; if (need[x] < 0) return false; }
    asg.assign(n, -1); load.assign(V, {});
    for (int i = 0; i < n; i++) {
        int rootc = -1; for (int j = 0; j < 3; j++) if (I.isRoot[I.fc[i][j]]) rootc = j;
        if (rootc >= 0) { asg[i] = rootc; continue; }
        vis.assign(V, 0); if (!tryFace(i)) return false;
    }
    // random direction per D-cycle
    vector<array<int,2>> vf(V, {-1,-1});
    for (int i = 0; i < n; i++) for (int j = 0; j < 3; j++) if (j != asg[i]) { int x = I.fc[i][j]; if (vf[x][0] < 0) vf[x][0] = i; else vf[x][1] = i; }
    key.assign(n, 0); vector<char> fseen(n, 0);
    for (int i0 = 0; i0 < n; i0++) if (!fseen[i0]) {
        bool flip = rng() & 1; int i = i0, tail = -1;
        for (int j = 0; j < 3; j++) if (j != asg[i]) { tail = j; break; }
        while (!fseen[i]) {
            fseen[i] = 1; int head = 3 - asg[i] - tail; int y = I.fc[i][head];
            key[i] = flip ? head * 3 + tail : tail * 3 + head;
            int nx = vf[y][0] == i ? vf[y][1] : vf[y][0]; int nt = -1;
            for (int j = 0; j < 3; j++) if (I.fc[nx][j] == y) nt = j;
            i = nx; tail = nt;
        }
    }
    return true;
}

static int dcap = 8; static ll ncap = 200000;
// nearest pair with smaller k: returns distance (or -1 if capped), sets target
static int nearestLower(const string& start, string& target) {
    int k0 = expand(start).k;
    unordered_map<string,int> d; deque<string> q; d[start] = 0; q.push_back(start);
    while (!q.empty()) {
        string a = q.front(); q.pop_front(); int da = d[a];
        if (da >= dcap) return -1;
        LNode nd = expand(a);
        for (auto &b : nd.nb) if (!d.count(b)) {
            d[b] = da + 1;
            if (kOf(b) < k0) { target = b; return da + 1; }
            q.push_back(b);
            if ((ll)d.size() > ncap) return -1;
        }
    }
    return -2;   // component exhausted without improvement (cannot happen by the component theorem)
}
// C3: non-increasing path to k = 0. returns monotone distance, -1 capped, -2 trapped (closed set exhausted)
static int monotone(const string& start, ll& visited) {
    unordered_map<string,int> d; deque<string> q; d[start] = 0; q.push_back(start);
    while (!q.empty()) {
        string a = q.front(); q.pop_front(); int da = d[a]; LNode nd = expand(a);
        for (auto &b : nd.nb) if (!d.count(b)) {
            int kb = kOf(b); if (kb > nd.k) continue;
            d[b] = da + 1; if (kb == 0) { visited = d.size(); return da + 1; }
            q.push_back(b);
            if ((ll)d.size() > ncap) { visited = d.size(); return -1; }
        }
    }
    visited = d.size(); return -2;
}

int main(int argc, char** argv) {
    int R = 2; ll steps = 2000; int gap = 5; double bias = 0.5; ll seed = 1; bool doC3 = true;
    for (int i = 1; i < argc; i++) {
        string a = argv[i];
        if (a == "-R") R = atoi(argv[++i]); else if (a == "-steps") steps = atoll(argv[++i]);
        else if (a == "-gap") gap = atoi(argv[++i]); else if (a == "-bias") bias = atof(argv[++i]);
        else if (a == "-seed") seed = atoll(argv[++i]); else if (a == "-dcap") dcap = atoi(argv[++i]);
        else if (a == "-ncap") ncap = atoll(argv[++i]); else if (a == "-noc3") doC3 = false;
    }
    rng.seed(seed);
    ll inst = 0, samples = 0, sinks = 0, c3fail = 0, c3cap = 0, rhocap = 0; ll rhoHist[12] = {0}; int maxRho = 0, maxMono = 0, maxLen = 0, maxK = 0, maxLenK = 0; ll maxVisited = 0;
    ll lenSum = 0, lenCnt = 0; int wit = 0;
    string line; curGraph = -1;
    while (getline(cin, line)) {
        if (line.empty()) continue;
        array<int,3> roots; bool hasRoots;
        if (!parseLine(line, roots, hasRoots)) continue;
        curGraph++; curLine = line; buildFaces();
        vector<int> cand(F); iota(cand.begin(), cand.end(), 0); shuffle(cand.begin(), cand.end(), rng);
        int used = 0;
        for (int t0 : cand) {
            if (used >= R) break;
            if (hasRoots) { set<int> a(faces[t0].begin(), faces[t0].end()), b(roots.begin(), roots.end()); if (a != b) continue; }
            if (!I.init(t0)) { fprintf(stderr, "not Eulerian\n"); exit(1); }
            string cur; if (!flowFactor(cur)) continue;
            used++; inst++; cache.clear();
            for (ll st = 0; st < steps; st++) {
                const LNode& nd = expand(cur);
                if (nd.nb.empty()) break;
                string nxt = nd.nb[rng() % nd.nb.size()];
                if ((rng() % 1000) < bias * 1000) { // biased step: among 3 random neighbours take the one with most Q-cycles
                    int bk = kOf(nxt);
                    for (int z = 0; z < 2; z++) { const string& c2 = nd.nb[rng() % nd.nb.size()]; int kk = kOf(c2); if (kk > bk) { bk = kk; nxt = c2; } }
                }
                cur = nxt;
                if (cache.size() > 400000) cache.clear();
                if (st % gap) continue;
                LNode here = expand(cur); int k0 = here.k; if (k0 == 0) continue;
                samples++; maxK = max(maxK, k0);
                bool strict = false; for (size_t j = 0; j < here.nb.size(); j++) if (here.ty[j] == 0 && kOf(here.nb[j]) < k0) { strict = true; break; }
                int rho = 1; string tgt;
                if (!strict) { sinks++; rho = nearestLower(cur, tgt); }
                if (rho < 0) { rhocap++; if (wit < 20) { wit++; printf("W RHOCAP V=%d graph=%d t0=%d,%d,%d k=%d code=%d | %s | pair", V, curGraph, faces[I.t0][0], faces[I.t0][1], faces[I.t0][2], k0, rho, curLine.c_str()); for (int i = 0; i < I.n; i++) printf(" %d>%d", I.fc[i][cur[i]/3], I.fc[i][cur[i]%3]); printf("\n"); } }
                else { rhoHist[min(rho, 11)]++; if (rho > maxRho || (rho >= 3 && wit < 20)) { wit++; printf("W RHO V=%d graph=%d t0=%d,%d,%d k=%d rho=%d | %s | pair", V, curGraph, faces[I.t0][0], faces[I.t0][1], faces[I.t0][2], k0, rho, curLine.c_str()); for (int i = 0; i < I.n; i++) printf(" %d>%d", I.fc[i][cur[i]/3], I.fc[i][cur[i]%3]); printf("\n"); } maxRho = max(maxRho, rho); }
                if (doC3 && !strict) {
                    ll vis2 = 0; int m = monotone(cur, vis2); maxVisited = max(maxVisited, vis2);
                    if (m == -2) { c3fail++; printf("W C3FAIL V=%d graph=%d t0=%d,%d,%d k=%d closed_set=%lld | %s | pair", V, curGraph, faces[I.t0][0], faces[I.t0][1], faces[I.t0][2], k0, vis2, curLine.c_str()); for (int i = 0; i < I.n; i++) printf(" %d>%d", I.fc[i][cur[i]/3], I.fc[i][cur[i]%3]); printf("\n"); }
                    else if (m == -1) c3cap++; else maxMono = max(maxMono, m);
                }
                // nearest-improvement descent length
                { string a = cur; int len = 0; bool ok = true;
                  while (true) { int ka = expand(a).k; if (ka == 0) break; string t2; int r2 = nearestLower(a, t2); if (r2 < 0) { ok = false; break; } len += r2; a = t2; }
                  if (ok) { lenSum += len; lenCnt++; if (len > maxLen) { maxLen = len; maxLenK = k0; } } }
            }
        }
    }
    printf("WALK V=%d instances=%lld samples_k>0=%lld maxk=%d sinks=%lld rho_capped=%lld maxrho=%d c3fail=%lld c3capped=%lld maxmono=%d max_closed_visited=%lld descent_maxlen=%d(at k=%d) descent_meanlen=%.3f rhohist",
           V, inst, samples, maxK, sinks, rhocap, maxRho, c3fail, c3cap, maxMono, maxVisited, maxLen, maxLenK, lenCnt ? (double)lenSum / lenCnt : 0.0);
    for (int j = 1; j < 12; j++) if (rhoHist[j]) printf(" %d:%lld", j, rhoHist[j]);
    printf("\n");
    return 0;
}
