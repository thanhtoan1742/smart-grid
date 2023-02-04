#include <iostream>
#include <vector>
using namespace std;

enum NodeType{
    GEN, CON
};

class ABSPlace{
    public: 
        static int cnt;

        int id;
        ABSPlace(){
            id = cnt;
            cnt++;
        }
};

class ABSTransition{
    public: 
        static int cnt;

        int id;
        ABSTransition(){
            id = cnt;
            cnt++;
        }

        // virtual bool isEnable() = 0;
        // virtual vector<ABSPlace*> Firing() = 0;
};

class State;
class Node{
    public:
        static int cnt;

        int id;
        NodeType type;
        int c;

        Node(){}

        Node(NodeType _type, int _c){
            id = cnt;
            cnt++;
            type = _type;
            c = _c;
        }

        Node(Node &node){
            id = node.id;
            type = node.type;
            c = node.c;
        }

        friend ostream& operator <<(ostream& os, const Node& node){
            os << "id = " << node.id << ", type = " << node.type << ", c = " << node.c;
        }

};

class NodePower{
    public:
        Node* data;
        int power;
        
        NodePower(Node* _data, int _power = 0){
            data = new Node(*data);
            power = _power;
        }

        NodePower(NodeType _type, int _c, int _power = 0){
            data = new Node(_type, _c);
            power = _power;
        }

        NodePower(NodePower &node){
            data = new Node(*node.data);
            power = node.power;
        }

        friend ostream& operator <<(ostream& os, const NodePower& node){
            os << "{" << (*node.data) << "}, p = " << node.power;
        }
};

class GenConPlace: public ABSPlace{
    public:
        vector<NodePower*> token;
        GenConPlace(){}
        GenConPlace(vector<NodePower*> _token){
            token = _token;
        }

        GenConPlace(GenConPlace &place){
            for (int i = 0; i < place.token.size(); i++){
                NodePower* node = new NodePower(*place.token[i]);
                this->push(node);
            }
        }

        void push(NodePower* new_token){
            token.push_back(new_token);
        }

        friend ostream& operator <<(ostream& os, const GenConPlace& place){
            os << '\n';
            for(int i = 0; i < place.token.size(); i++){
                os << '\t' << *place.token[i] << '\n';
            }
            return os;
        }
};

class GeneratedPlace: public ABSPlace{
    public:
        int power;
        GeneratedPlace(): ABSPlace(){
            power = 0;
        }
        GeneratedPlace(int _power): ABSPlace(){
            power = _power;
        }

        GeneratedPlace(GeneratedPlace &place){
            power = place.power;
        }

        friend ostream& operator <<(ostream& os, const GeneratedPlace& generated){
            os << generated.power;
            return os;
        }
};

class GenTransition: public ABSTransition{
    public:
        GenTransition() : ABSTransition(){

        }

        bool isEnable(GenConPlace* generater){
            return generater->token.size() > 0;
        }

        vector<State*> Firing(State* state);
};

class ConsTransition: public ABSTransition{
    public:
        ConsTransition() : ABSTransition(){
            
        }

        bool isEnable(State* state){
            return true;
        }

        vector<State*> Firing(State* state);
};

class State{
    public:
        static int cnt;
        int id;
        GenConPlace* generater, *consumner;
        GeneratedPlace* generated;
        GenTransition* gen;
        ConsTransition* con;
        vector<State*> next_state;

        State(){
            generater = new GenConPlace();
            generated = new GeneratedPlace();
            consumner = new GenConPlace();
            Init();
        }

        State(State &state){
            generater = new GenConPlace(*state.generater);
            generated = new GeneratedPlace(*state.generated);
            consumner = new GenConPlace(*state.consumner);
            Init();
        }

        void Init(){
            id = cnt++;
            gen = new GenTransition();
            con = new ConsTransition();
        }

        void GenNextState(){
            vector<State*> new_state = gen->Firing(this);
            for(int i = 0; i < new_state.size(); i++) next_state.push_back(new_state[i]);
        
            new_state = con->Firing(this);
            for(int i = 0; i < new_state.size(); i++) next_state.push_back(new_state[i]);
            // cout << *new_state;
            // cout << *this << '\n';
        }

        friend ostream& operator <<(ostream& os, const State& state){
            os << "=========================================\n" ;
            os << "State: " << state.id << '\n';
            os << "Generater: " << *state.generater << '\n';
            os << "Generated: " << *state.generated << '\n';
            os << "Consumer: " << *state.consumner << '\n';
            os << "=========================================\n";
            return os;
        }
};

class StateSpace{
    public:
        vector<State*> states;
        StateSpace(){}

        StateSpace(State* state){
            states.push_back(state);
        }

        StateSpace(vector<int> gen_cap, vector<int> con_req){
            State* initState = new State();
            for(int i = 0; i < gen_cap.size(); i++){
                NodePower * newNodePower = new NodePower(GEN, gen_cap[i], gen_cap[i]);
                initState->generater->push(newNodePower);
            }
            for(int i = 0; i < con_req.size(); i++){
                NodePower * newNodePower = new NodePower(CON, con_req[i]);
                initState->consumner->push(newNodePower);
            }
            states.push_back(initState);
        }

        void GenFullStateSpace(){
            int k = 0;
            while (k < states.size()){
                cout << *states[k];
                states[k]->GenNextState();
                for(int i = 0; i < states[k]->next_state.size(); i++){
                    states.push_back(states[k]->next_state[i]);
                }
                k++;
            }

            cout << states.size();
        }
};

int Node::cnt = 0;
int ABSPlace::cnt = 0;
int ABSTransition::cnt = 0;
int State::cnt = 0;

vector<State*> GenTransition::Firing(State* state){
    vector<State*> gen_state;
    for (int i = 0; i < state->generater->token.size(); i++){
        State* new_state = new State(*state);
        new_state->generated->power += new_state->generater->token.back()->power;
        new_state->generater->token.pop_back();
        gen_state.push_back(new_state);
    }
    return gen_state;
}

vector<State*> ConsTransition::Firing(State* state){
    vector<State*> gen_state;
    int generated_power = state->generated->power;
    int idx = -1;
    int cons_req = 0;
    for(int i = 0; i < state->consumner->token.size(); i++){
        cons_req = state->consumner->token[i]->data->c;
        if (generated_power >= cons_req){
            State* new_state = new State(*state);
            new_state->generated->power -= cons_req;
            new_state->consumner->token[i]->power += cons_req;
            gen_state.push_back(new_state);
        }
    }
    
    return gen_state;
}
int main(){
    vector<int> gen{2, 1};
    vector<int> con{1, 1};
    StateSpace* graph = new StateSpace(gen, con);
    graph->GenFullStateSpace();
}