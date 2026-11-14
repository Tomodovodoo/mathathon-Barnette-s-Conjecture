// Independent all-root factor/forest counter. No author source included.
#include <algorithm>
#include <array>
#include <chrono>
#include <iostream>
#include <numeric>
#include <sstream>
#include <string>
#include <vector>
using namespace std;
using ll=long long;
int V,n;vector<vector<int>> rot;vector<array<int,3>> faces,A;
vector<int> cap,u;vector<bool> root;
ll graphs=0,roots=0,feasible=0,factors=0,pairs=0,trees=0,equality=0,violations=0;
ll localF,localP,localT;int cmin;

void complete(){
    vector<vector<pair<int,int>>> adj(V);
    for(int k=0;k<n;k++){
        vector<int> e;for(int v:A[k])if(v!=u[k])e.push_back(v);
        adj[e[0]].push_back({e[1],k});adj[e[1]].push_back({e[0],k});
    }
    vector<bool> seen(V,false);vector<vector<array<int,3>>> cycles;
    for(int a=0;a<V;a++)if(!root[a]&&!seen[a]){
        vector<array<int,3>> c;int v=a,last=-1;
        do{
            seen[v]=true;auto e=adj[v][adj[v][0].second==last?1:0];
            c.push_back({v,e.first,e.second});v=e.first;last=e.second;
        }while(v!=a);
        cycles.push_back(c);
    }
    int c=cycles.size();cmin=min(cmin,c);localF++;
    for(int mask=0;mask<(1<<c);mask++){
        localP++;vector<int> par(V);iota(par.begin(),par.end(),0);bool good=true;
        auto find=[&](int a){while(a!=par[a])a=par[a];return a;};
        // Q_s has edges {u(t),r(t)}. Its edges are distinct by black incidence.
        for(int j=0;j<c&&good;j++)for(auto e:cycles[j]){
            int r=(mask>>j&1)?e[1]:e[0];int a=find(u[e[2]]),b=find(r);
            if(a==b){good=false;break;}par[a]=b;
        }
        localT+=good;
    }
}

void visit(vector<int> todo){
    if(todo.empty()){complete();return;}
    int best=-1,bestcount=4;vector<int> available(V,0);
    for(int k:todo){
        int count=0;for(int v:A[k])if(cap[v]>0){count++;available[v]++;}
        if(!count)return;
        if(count<bestcount){best=k;bestcount=count;}
    }
    for(int v=0;v<V;v++)if(cap[v]>available[v])return;
    // Unit propagation of vertex saturation.
    for(int v=0;v<V;v++)if(cap[v]>0&&cap[v]==available[v]){
        vector<int> keep;int taken=0;
        for(int k:todo){
            if(find(A[k].begin(),A[k].end(),v)!=A[k].end()){u[k]=v;taken++;}
            else keep.push_back(k);
        }
        cap[v]-=taken;visit(keep);cap[v]+=taken;return;
    }
    todo.erase(find(todo.begin(),todo.end(),best));
    for(int v:A[best])if(cap[v]>0){u[best]=v;cap[v]--;visit(todo);cap[v]++;}
}

void graph(){
    vector<vector<int>> left(V,vector<int>(V,-1));faces.clear();
    for(int a=0;a<V;a++)for(int b:rot[a])if(left[a][b]<0){
        array<int,3> f;int x=a,y=b;
        for(int j=0;j<3;j++){
            f[j]=x;left[x][y]=faces.size();
            int p=find(rot[y].begin(),rot[y].end(),x)-rot[y].begin();
            int z=rot[y][(p+rot[y].size()-1)%rot[y].size()];x=y;y=z;
        }
        if(x!=a||y!=b)throw runtime_error("nontriangular");faces.push_back(f);
    }
    for(int f0=0;f0<(int)faces.size();f0++){
        roots++;root.assign(V,false);for(int v:faces[f0])root[v]=true;
        vector<int> color(faces.size(),-1),q{f0};color[f0]=0;
        for(size_t k=0;k<q.size();k++){
            int f=q[k];for(int j=0;j<3;j++){
                int g=left[faces[f][(j+1)%3]][faces[f][j]];
                if(color[g]<0){color[g]=1-color[f];q.push_back(g);}
                else if(color[g]==color[f])throw runtime_error("not Eulerian");
            }
        }
        A.clear();for(int j=0;j<(int)faces.size();j++)if(j!=f0&&color[j]==0)A.push_back(faces[j]);
        n=A.size();u.assign(n,-1);cap.assign(V,0);vector<int> todo;
        for(int v=0;v<V;v++)cap[v]=root[v]?0:(int)rot[v].size()/2-2;
        for(int k=0;k<n;k++){
            for(int v:A[k])if(root[v])u[k]=v;
            if(u[k]<0)todo.push_back(k);
        }
        localF=localP=localT=0;cmin=100;visit(todo);
        factors+=localF;pairs+=localP;trees+=localT;
        if(localF){feasible++;equality+=localT==(1LL<<cmin);violations+=localT<(1LL<<cmin);
            if((localT==(1LL<<cmin))!=(localF==1))throw runtime_error("equality converse failure");}
    }
}

int main(){
    auto start=chrono::steady_clock::now();string line;
    while(getline(cin,line)){
        if(line.empty())continue;istringstream in(line);string s;in>>V>>s;rot.clear();
        istringstream ns(s);string part;
        while(getline(ns,part,',')){vector<int> r;for(char c:part)r.push_back(c-'a');rot.push_back(r);}
        if((int)rot.size()!=V)throw runtime_error("bad input");graphs++;graph();
    }
    cout<<"{\"V\":"<<V<<",\"graphs\":"<<graphs<<",\"roots\":"<<roots<<",\"feasible\":"<<feasible
        <<",\"factors\":"<<factors<<",\"pairs\":"<<pairs<<",\"TM\":"<<trees<<",\"equality\":"<<equality
        <<",\"violations\":"<<violations<<",\"seconds\":"<<chrono::duration<double>(chrono::steady_clock::now()-start).count()<<"}\n";
}
