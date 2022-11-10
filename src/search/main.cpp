#include <vector>
#include <queue>
#include <utility>
using namespace std;
const float MAX_VALUE = LLONG_MAX;

typedef int Power;
typedef pair<float, int> ii;

enum NodeType{
    GEN, CON
};

enum EdgeType{
    TRANS, GEN
};

class Node{
    public:
        int id;
        NodeType type;
        int cap;

        Node(){
            id = 0;
            type = NodeType::GEN;
            cap = 0;
        }
        Node(int _id, NodeType _type, int _cap){
            id = _id;
            type = _type;
            cap = _cap;
        }
        
};

class Node_Power{
    public:
        Node* node;
        Power power;
    
        Node_Power(){
            node = nullptr;
            power = 0;
        }

        Node_Power(Node* _node, Power _power){
            node = _node;
            power = _power;
        }
};

class State{
    public:
        int id;
        Power store;
        vector<Node_Power*> generator;
        vector<Node_Power*> consumer;
        
        State(){
            id = 0;
            store = 0;
        }

        State(int _id, Power _power, vector<Node_Power*> _generator, vector<Node_Power*> _consumer){
            id = _id;
            store = _power;
            _generator = generator;
            _consumer = consumer;
        }

};

class Edge{
    public:
        int from;
        int to;
        float cost;
        EdgeType type;

        Edge(){
            from = -1;
            to = -1;
            type = EdgeType::GEN;
            cost = 0;
        }
        
        Edge(int from, int to, EdgeType type){
            this->from = from;
            this->to = to;
            this->type = type;
            cost = 1;
        }
};

class StateSpace{
    public: 
        vector<State*> stateInfo;
        vector<vector<Edge*>> edges;

        StateSpace(){}

        int length(){
            return stateInfo.size(); 
        }

        void addState(State* state){
            stateInfo.push_back(state);
        }

        void addEdge(Edge* e){
            if (edges.size() == 0){
                edges = vector<vector<Edge*>>(this->length());
            }
            edges[e->from].push_back(e);
        }

        State* get_state(int id){
            return stateInfo[id];
        }

        vector<Edge*> get_adj_edge(int state_id){
            return edges[state_id];
        }
};

class Search{
    public:
        StateSpace * stateSpace;
        int start;
        vector<float> f;
        vector<int> came_from;
        State* req_state;

        void addRequestState(State* req_state){
            this->req_state = req_state;
        }

        void Init(StateSpace* stateSpace){
            this->stateSpace = stateSpace;
            start = 1;
            f = vector<float>(stateSpace->length(), MAX_VALUE);
            came_from = vector<int>(stateSpace->length(), -1);
        }

        float heuristic(int id){
            return 0;
        }

        bool isFinale(int id){
            State* state = stateSpace->get_state(id);
            for(int i = 0; i < req_state->consumer.size(); i++){
                int req_power = req_state->consumer[i]->power;
                int state_power = state->consumer[i]->power;
                if (state_power < req_power) return false;
            }
            return true;
        }

        void AStart(){
            priority_queue<ii, vector<ii>, greater<ii> > Q;
            f[start] = 0;
            Q.push(ii(heuristic(start), start));
            while(!Q.empty()){
                ii u = Q.top();
                Q.pop();
                if (u.first - heuristic(u.second) != f[u.second]) continue;
                if (isFinale(u.second)){
                    PrintResult();
                    return;
                }
                State* u_state = stateSpace->get_state(u.second);
                for(Edge* e: stateSpace->get_adj_edge(u_state->id)){
                    float new_cost = f[u_state->id] + e->cost;
                    if (new_cost < f[u_state->id]){
                        f[u_state->id] = new_cost;
                        float priority = heuristic(e->to) + new_cost;
                        Q.push(ii(priority, e->to));
                        came_from[e->to] = u_state->id;
                    }
                }
            }
        }

        void PrintResult(){

        }
};

int main(){
    
}