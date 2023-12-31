#include <iostream>
#include <fstream>
#include <vector>
#include <deque>
#include <algorithm>
#include <cmath>
#include <bitset>
#include <map>
#include <numeric>
#include <chrono>
//#include <string>
using namespace std;
using namespace std::chrono;


void permu(vector<int>& List, const vector<int>& cycle_chain, int index) {
    int mod = cycle_chain.size();
    if (index < 0) {
        index += mod;
    }
    vector<int> copied_list = List;
    for (int i = 0; i < mod; i++) {
        int new_index = (i + index) % mod;
        List[cycle_chain[new_index]] = copied_list[cycle_chain[i]];
    }
}

// Helper function to calculate factorial
unsigned factorial(unsigned n)
{
    return n <= 1 ? 1 : n * factorial(n - 1);
}

class PermutationIndexer {
private:
    int N;
    int K;
    vector<int> ones_count_lookup;
    vector<int> factorials;

public:
    PermutationIndexer(int N, int K = -1) {
        if (K == -1) {
            K = N;
        }
        this->N = N;
        this->K = K;

        // Precomputed table containing the number of ones in the binary representation of each number.
        ones_count_lookup.resize(static_cast<vector<int, allocator<int>>::size_type>(1) << N);
        for (int i = 0; i < (1 << N); ++i) {
            ones_count_lookup[i] = bitset<32>(i).count();  // Using bitset to count bits
        }

        // Precomputed table of factorials in reverse order.
        factorials.resize(K);
        for (int i = 0; i < K; ++i) {
            factorials[i] = factorial(N - 1 - i) / factorial(N - K);
        }
    }

    int rank(const vector<int>& perm) {
        vector<int> lehmer(K, 0);
        int seen = 0;

        // The first digit of the Lehmer code is always the first digit of the permutation.
        lehmer[0] = perm[0];
        // Mark the digit as seen.
        seen |= 1 << (N - 1 - perm[0]);

        for (int i = 1; i < K; ++i) {
            seen |= 1 << (N - 1 - perm[i]);
            // Calculate the number of "seen" digits to the left of this digit.
            int num_ones = ones_count_lookup[seen >> (N - perm[i])];
            lehmer[i] = perm[i] - num_ones;
        }

        // Convert the Lehmer code to base-10.
        int index = 0;
        for (int i = 0; i < K; ++i) {
            index += lehmer[i] * factorials[i];
        }
        return index;
    }
};

class Korf_Cube {
public:
    vector<int> corner;
    vector<int> corner_o;
    vector<int> edge;
    vector<int> edge_o;

    Korf_Cube() : corner(8, -1), corner_o(8, -1), edge(12, -1), edge_o(12, -1) {}

    void string_handle(const string& state) {
        vector<char> colors;
        for (int i = 0; i < 6; ++i) {
            colors.push_back(state[4 + 9 * i]);
        }

        map<char, int> color_value;
        color_value[colors[0]] = 16;
        color_value[colors[5]] = -16;
        for (int i = 1; i < 5; ++i) {
            color_value[colors[i]] = static_cast<int>(pow(2, i - 1));
        }

        map<int, int> value_corner = {
            {25, 0}, {28, 1}, {22, 2}, {19, 3}, {-7, 4}, {-4, 5}, {-10, 6}, {-13, 7}
        };
        map<int, int> value_edge = {
            {24, 0}, {20, 1}, {18, 2}, {17, 3}, {9, 4}, {12, 5}, {6, 6}, {3, 7},
            {-8, 8}, {-12, 9}, {-14, 10}, {-15, 11}
        };

        vector<vector<int>> set_of_corner_indices = {
            {0, 9, 38}, {2, 29, 36}, {8, 20, 27}, {6, 11, 18},
            {51, 15, 44}, {53, 35, 42}, {47, 26, 33}, {45, 17, 24}
        };
        vector<vector<int>> set_of_edge_indices = {
            {1, 37}, {5, 28}, {7, 19}, {3, 10}, {12, 41}, {32, 39},
            {30, 23}, {14, 21}, {52, 43}, {50, 34}, {46, 25}, {48, 16}
        };

        for (int i = 0; i < 8; i++) {
            vector<int> corner_indices = set_of_corner_indices[i];
            vector<int> corner_value;
            for (int j = 0; j < 3; j++) {
                corner_value.push_back(color_value[state[corner_indices[j]]]);
            }
            int value = accumulate(corner_value.begin(), corner_value.end(), 0);
            corner[i] = value_corner[value];

            int pivot = corner_value[0];
            if (value > 0) {
                if (pivot == 16) {
                    corner_o[i] = 0;
                }
                else if ((value - 16 - pivot) != 9) {
                    if (pivot > (value - 16 - pivot)) {
                        corner_o[i] = 1;
                    }
                    else {
                        corner_o[i] = 2;
                    }
                }
                else {
                    if (pivot > (value - 16 - pivot)) {
                        corner_o[i] = 2;
                    }
                    else {
                        corner_o[i] = 1;
                    }
                }
            }
            else if (value < 0) {
                if (pivot == -16) {
                    corner_o[i] = 0;
                }
                else if ((value + 16 - pivot) != 9) {
                    if (pivot > (value + 16 - pivot)) {
                        corner_o[i] = 2;
                    }
                    else {
                        corner_o[i] = 1;
                    }
                }
                else {
                    if (pivot > (value + 16 - pivot)) {
                        corner_o[i] = 1;
                    }
                    else {
                        corner_o[i] = 2;
                    }
                }
            }
        }

        for (int i = 0; i < 12; i++) {
            vector<int> edge_indices = set_of_edge_indices[i];
            vector<int> edge_value;
            for (int j = 0; j < 2; j++) {
                edge_value.push_back(color_value[state[edge_indices[j]]]);
            }
            int value = accumulate(edge_value.begin(), edge_value.end(), 0);
            edge[i] = value_edge[value];

            int pivot = edge_value[0];
            if (find(edge_value.begin(), edge_value.end(), 16) != edge_value.end()) {
                if (pivot == 16) {
                    edge_o[i] = 0;
                }
                else {
                    edge_o[i] = 1;
                }
            }
            else if (find(edge_value.begin(), edge_value.end(), -16) != edge_value.end()) {
                if (pivot == -16) {
                    edge_o[i] = 0;
                }
                else {
                    edge_o[i] = 1;
                }
            }
            else {
                if (pivot == 1 || pivot == 4) {
                    edge_o[i] = 0;
                }
                else {
                    edge_o[i] = 1;
                }
            }
        }
    }

    void show() {
        for (int i = 0; i < 8; i++) {
            cout << corner[i] << " ";
        }
        cout << endl;
        for (int i = 0; i < 8; i++) {
            cout << corner_o[i] << " ";
        }
        cout << endl;
        for (int i = 0; i < 12; i++) {
            cout << edge[i] << " ";
        }
        cout << endl;
        for (int i = 0; i < 12; i++) {
            cout << edge_o[i] << " ";
        }
        cout << endl;
    }

    void U() {
        permu(corner, { 0, 1, 2, 3 }, 1);
        permu(edge, { 0, 1, 2, 3 }, 1);
        permu(corner_o, { 0, 1, 2, 3 }, 1);
        permu(edge_o, { 0, 1, 2, 3 }, 1);
    }

    void U2() {
        permu(corner, { 0, 1, 2, 3 }, 2);
        permu(edge, { 0, 1, 2, 3 }, 2);
        permu(corner_o, { 0, 1, 2, 3 }, 2);
        permu(edge_o, { 0, 1, 2, 3 }, 2);
    }

    void Ui() {
        permu(corner, { 0, 1, 2, 3 }, -1);
        permu(edge, { 0, 1, 2, 3 }, -1);
        permu(corner_o, { 0, 1, 2, 3 }, -1);
        permu(edge_o, { 0, 1, 2, 3 }, -1);
    }

    void D() {
        permu(corner, { 4, 5, 6, 7 }, -1);
        permu(edge, { 8, 9, 10, 11 }, -1);
        permu(corner_o, { 4, 5, 6, 7 }, -1);
        permu(edge_o, { 8, 9, 10, 11 }, -1);
    }

    void D2() {
        permu(corner, { 4, 5, 6, 7 }, -2);
        permu(edge, { 8, 9, 10, 11 }, -2);
        permu(corner_o, { 4, 5, 6, 7 }, -2);
        permu(edge_o, { 8, 9, 10, 11 }, -2);
    }

    void Di() {
        permu(corner, { 4, 5, 6, 7 }, 1);
        permu(edge, { 8, 9, 10, 11 }, 1);
        permu(corner_o, { 4, 5, 6, 7 }, 1);
        permu(edge_o, { 8, 9, 10, 11 }, 1);
    }

    void F() {
        permu(corner, { 3, 2, 6, 7 }, 1);
        permu(edge, { 2, 6, 10, 7 }, 1);
        permu(edge_o, { 2, 6, 10, 7 }, 1);
        vector<int> corner_o_copy = corner_o;
        corner_o[6] = (corner_o_copy[2] + 1) % 3;
        corner_o[7] = (corner_o_copy[6] + 2) % 3;
        corner_o[3] = (corner_o_copy[7] + 1) % 3;
        corner_o[2] = (corner_o_copy[3] + 2) % 3;
    }

    void F2() {
        permu(corner, { 3, 2, 6, 7 }, 2);
        permu(edge, { 2, 6, 10, 7 }, 2);
        permu(edge_o, { 2, 6, 10, 7 }, 2);
        vector<int> corner_o_copy = corner_o;
        corner_o[6] = corner_o_copy[3];
        corner_o[3] = corner_o_copy[6];
        corner_o[7] = corner_o_copy[2];
        corner_o[2] = corner_o_copy[7];
    }

    void Fi() {
        permu(corner, { 3, 2, 6, 7 }, -1);
        permu(edge, { 2, 6, 10, 7 }, -1);
        permu(edge_o, { 2, 6, 10, 7 }, -1);
        vector<int> corner_o_copy = corner_o;
        corner_o[2] = (corner_o_copy[6] + 2) % 3;
        corner_o[7] = (corner_o_copy[3] + 2) % 3;
        corner_o[3] = (corner_o_copy[2] + 1) % 3;
        corner_o[6] = (corner_o_copy[7] + 1) % 3;
    }

    void B() {
        permu(corner, { 1, 0, 4, 5 }, 1);
        permu(edge, { 0, 4, 8, 5 }, 1);
        permu(edge_o, { 0, 4, 8, 5 }, 1);
        vector<int> corner_o_copy = corner_o;
        corner_o[4] = (corner_o_copy[0] + 1) % 3;
        corner_o[5] = (corner_o_copy[4] + 2) % 3;
        corner_o[1] = (corner_o_copy[5] + 1) % 3;
        corner_o[0] = (corner_o_copy[1] + 2) % 3;
    }

    void B2() {
        permu(corner, { 1, 0, 4, 5 }, 2);
        permu(edge, { 0, 4, 8, 5 }, 2);
        permu(edge_o, { 0, 4, 8, 5 }, 2);
        vector<int> corner_o_copy = corner_o;
        corner_o[1] = corner_o_copy[4];
        corner_o[4] = corner_o_copy[1];
        corner_o[0] = corner_o_copy[5];
        corner_o[5] = corner_o_copy[0];
    }

    void Bi() {
        permu(corner, { 1, 0, 4, 5 }, -1);
        permu(edge, { 0, 4, 8, 5 }, -1);
        permu(edge_o, { 0, 4, 8, 5 }, -1);
        vector<int> corner_o_copy = corner_o;
        corner_o[0] = (corner_o_copy[4] + 2) % 3;
        corner_o[4] = (corner_o_copy[5] + 1) % 3;
        corner_o[5] = (corner_o_copy[1] + 2) % 3;
        corner_o[1] = (corner_o_copy[0] + 1) % 3;
    }

    void L() {
        permu(corner, { 0, 3, 7, 4 }, 1);
        permu(edge, { 3, 7, 11, 4 }, 1);
        vector<int> corner_o_copy = corner_o;
        corner_o[3] = (corner_o_copy[0] + 2) % 3;
        corner_o[7] = (corner_o_copy[3] + 1) % 3;
        corner_o[4] = (corner_o_copy[7] + 2) % 3;
        corner_o[0] = (corner_o_copy[4] + 1) % 3;
        vector<int> edge_o_copy = edge_o;
        edge_o[7] = (edge_o_copy[3] + 1) % 2;
        edge_o[11] = (edge_o_copy[7] + 1) % 2;
        edge_o[4] = (edge_o_copy[11] + 1) % 2;
        edge_o[3] = (edge_o_copy[4] + 1) % 2;
    }

    void L2() {
        permu(corner, { 0, 3, 7, 4 }, 2);
        permu(edge, { 3, 7, 11, 4 }, 2);
        vector<int> corner_o_copy = corner_o;
        corner_o[0] = corner_o_copy[7];
        corner_o[7] = corner_o_copy[0];
        corner_o[4] = corner_o_copy[3];
        corner_o[3] = corner_o_copy[4];
        vector<int> edge_o_copy = edge_o;
        edge_o[3] = edge_o_copy[11];
        edge_o[11] = edge_o_copy[3];
        edge_o[7] = edge_o_copy[4];
        edge_o[4] = edge_o_copy[7];
    }

    void Li() {
        permu(corner, { 0, 3, 7, 4 }, -1);
        permu(edge, { 3, 7, 11, 4 }, -1);
        vector<int> corner_o_copy = corner_o;
        corner_o[0] = (corner_o_copy[3] + 1) % 3;
        corner_o[4] = (corner_o_copy[0] + 2) % 3;
        corner_o[7] = (corner_o_copy[4] + 1) % 3;
        corner_o[3] = (corner_o_copy[7] + 2) % 3;
        vector<int> edge_o_copy = edge_o;
        edge_o[3] = (edge_o_copy[7] + 1) % 2;
        edge_o[4] = (edge_o_copy[3] + 1) % 2;
        edge_o[11] = (edge_o_copy[4] + 1) % 2;
        edge_o[7] = (edge_o_copy[11] + 1) % 2;
    }
    void R() {
        permu(corner, { 2, 1, 5, 6 }, 1);
        permu(edge, { 1, 5, 9, 6 }, 1);
        vector<int> corner_o_copy = corner_o;
        corner_o[1] = (corner_o_copy[2] + 2) % 3;
        corner_o[5] = (corner_o_copy[1] + 1) % 3;
        corner_o[6] = (corner_o_copy[5] + 2) % 3;
        corner_o[2] = (corner_o_copy[6] + 1) % 3;

        vector<int> edge_o_copy = edge_o;
        edge_o[1] = (edge_o_copy[6] + 1) % 2;
        edge_o[5] = (edge_o_copy[1] + 1) % 2;
        edge_o[9] = (edge_o_copy[5] + 1) % 2;
        edge_o[6] = (edge_o_copy[9] + 1) % 2;
    }

    void R2() {
        permu(corner, { 2, 1, 5, 6 }, 2);
        permu(edge, { 1, 5, 9, 6 }, 2);
        vector<int> corner_o_copy = corner_o;
        corner_o[1] = corner_o_copy[6];
        corner_o[6] = corner_o_copy[1];
        corner_o[2] = corner_o_copy[5];
        corner_o[5] = corner_o_copy[2];

        vector<int> edge_o_copy = edge_o;
        edge_o[1] = edge_o_copy[9];
        edge_o[9] = edge_o_copy[1];
        edge_o[5] = edge_o_copy[6];
        edge_o[6] = edge_o_copy[5];
    }

    void Ri() {
        permu(corner, { 2, 1, 5, 6 }, -1);
        permu(edge, { 1, 5, 9, 6 }, -1);
        vector<int> corner_o_copy = corner_o;
        corner_o[2] = (corner_o_copy[1] + 1) % 3;
        corner_o[6] = (corner_o_copy[2] + 2) % 3;
        corner_o[5] = (corner_o_copy[6] + 1) % 3;
        corner_o[1] = (corner_o_copy[5] + 2) % 3;

        vector<int> edge_o_copy = edge_o;
        edge_o[6] = (edge_o_copy[1] + 1) % 2;
        edge_o[9] = (edge_o_copy[6] + 1) % 2;
        edge_o[5] = (edge_o_copy[9] + 1) % 2;
        edge_o[1] = (edge_o_copy[5] + 1) % 2;
    }
};

class Node {
public:
    Korf_Cube state;
    Node* parent;
    void (Korf_Cube::* action)();
    int depth;
    vector<Node*> children;

    Node(Korf_Cube state, Node* parent = nullptr, void (Korf_Cube::* action)() = nullptr, int depth = 0) {
        this->state = state;
        this->parent = parent;
        this->action = action;
        this->depth = depth;
        if (parent) {
            this->depth = parent->depth + 1;
        }
    }

    vector<Node*> expand() {
        vector<void (Korf_Cube::*)()> MoveList = { &Korf_Cube::F, &Korf_Cube::F2, &Korf_Cube::Fi, &Korf_Cube::B, &Korf_Cube::B2, &Korf_Cube::Bi, &Korf_Cube::L, &Korf_Cube::L2, &Korf_Cube::Li, &Korf_Cube::R, &Korf_Cube::R2, &Korf_Cube::Ri, &Korf_Cube::U, &Korf_Cube::U2, &Korf_Cube::Ui, &Korf_Cube::D, &Korf_Cube::D2, &Korf_Cube::Di };
        vector<void (Korf_Cube::*)()> FeasibleMoveList = MoveList;
        for (int i = 0; i < 18; i++) {
            if (this->action == MoveList[i]) {
                int group_index = i / 3;

                // Erase the group of moves
                int erase_start_index = 3 * group_index;
                FeasibleMoveList.erase(FeasibleMoveList.begin() + erase_start_index,
                    FeasibleMoveList.begin() + erase_start_index + 3);

                // If the action belongs to B, R, D group, erase the group of moves before
                if (group_index % 2 == 1) {
                    erase_start_index = 3 * (group_index - 1);
                    FeasibleMoveList.erase(FeasibleMoveList.begin() + erase_start_index,
                        FeasibleMoveList.begin() + erase_start_index + 3);
                }

                break;
            }
        }

        for (auto move : FeasibleMoveList) {
            Korf_Cube child_state = this->state;
            (child_state.*move)();
            Node* child_node = new Node(child_state, this, move, this->depth + 1);
            this->children.push_back(child_node);
        }
        return this->children;
    }
};

class GenerateDB {
public:
    unsigned length;
    unsigned indexed;
    vector<int> lookup_table;
    Korf_Cube initial_state;
    Node* initial; // Declare initial as a member variable

    GenerateDB() { 
        this->length = 0;
        this->indexed = 0;
        string solved_state = "yyyyyyyyyrrrrrrrrrgggggggggooooooooobbbbbbbbbwwwwwwwww";
        initial_state.string_handle(solved_state);
        initial = new Node(initial_state);
        // initial is already initialized as a member variable
    }

    bool goal_test() {
        if (this->length > 0) {
            return this->indexed == this->length;
        }
        else {
            return false;
        }
    }
};

class CornerDB : public GenerateDB {
public:
    CornerDB() {
        this->length = 88179840;
        this->lookup_table = vector<int>(88179840, -1);
    }
};

void breadth_first_corner_search(CornerDB& problem) {
    deque<Node*> frontier;
    frontier.push_back(problem.initial);
    PermutationIndexer corner_permu_ranking(8);
    while (!frontier.empty()) {
        Node* node = frontier.front();
        frontier.pop_front();
        vector<int> corner_perm = node->state.corner;
        unsigned corner_perm_rank = corner_permu_ranking.rank(corner_perm);
        unsigned corner_index = static_cast<int>(pow(3, 7)) * corner_perm_rank;
        for (int i = 0; i < 7; i++) {
            corner_index += node->state.corner_o[i] * static_cast<int>(pow(3, i));
        }
        if (problem.lookup_table[corner_index] == -1) {
            problem.lookup_table[corner_index] = node->depth;
            cout << corner_index << ": " << node->depth << endl;
            if (problem.goal_test()) {
                return;
            }
            else {
                vector<Node*> children = node->expand();
                for (auto child : children) {
                    vector<int> child_corner_perm = child->state.corner;
                    unsigned child_corner_perm_rank = corner_permu_ranking.rank(child_corner_perm);
                    unsigned child_corner_index = static_cast<int>(pow(3, 7)) * child_corner_perm_rank;
                    for (int i = 0; i < 7; i++) {
                        child_corner_index += child->state.corner_o[i] * static_cast<int>(pow(3, i));
                    }
                    if (problem.lookup_table[child_corner_index] == -1) {
						frontier.push_back(child);
					}
                }
            }
        }
    }
}

//string getActionName(void(Korf_Cube::* action)()) {
//    if (action == &Korf_Cube::F) return "F";
//    else if (action == &Korf_Cube::F2) return "F2";
//    else if (action == &Korf_Cube::Fi) return "Fi";
//    else if (action == &Korf_Cube::B) return "B";
//    else if (action == &Korf_Cube::B2) return "B2";
//    else if (action == &Korf_Cube::Bi) return "Bi";
//    else if (action == &Korf_Cube::L) return "L";
//    else if (action == &Korf_Cube::L2) return "L2";
//    else if (action == &Korf_Cube::Li) return "Li";
//    else if (action == &Korf_Cube::R) return "R";
//    else if (action == &Korf_Cube::R2) return "R2";
//    else if (action == &Korf_Cube::Ri) return "Ri";
//    else if (action == &Korf_Cube::U) return "U";
//    else if (action == &Korf_Cube::U2) return "U2";
//    else if (action == &Korf_Cube::Ui) return "Ui";
//    else if (action == &Korf_Cube::D) return "D";
//    else if (action == &Korf_Cube::D2) return "D2";
//    else if (action == &Korf_Cube::Di) return "Di";
//    else return "Unknown Action";
//}

void writeVectorToBinaryFile(const vector<int>& vec, const string& filename) {
    ofstream outFile(filename, ios::binary | ios::out);

    if (!outFile) {
        cerr << "Error opening file for writing." << endl;
        return;
    }

    bitset<8> byteBuffer;
    int bitCount = 0;

    for (int value : vec) {
        if (value < 0 || value > 15) {
            cerr << "Value out of range: " << value << endl;
            return;
        }

        bitset<4> bits(value);
        for (int i = 0; i < 4; ++i) {
            byteBuffer[bitCount++] = bits[i];

            if (bitCount == 8) {
                unsigned long byte = byteBuffer.to_ulong();
                outFile.write(reinterpret_cast<const char*>(&byte), 1);
                bitCount = 0;
                byteBuffer.reset();
            }
        }
    }

    // Write any remaining bits (padded with zeros if necessary)
    if (bitCount > 0) {
        unsigned long byte = byteBuffer.to_ulong();
        outFile.write(reinterpret_cast<const char*>(&byte), 1);
    }

    outFile.close();
}


int main() {
    auto start = high_resolution_clock::now();
    CornerDB problem;
    breadth_first_corner_search(problem);
    string filename = "cornerDB.bin";  

    writeVectorToBinaryFile(problem.lookup_table, filename);
    auto stop = high_resolution_clock::now();
    auto duration = duration_cast<minutes>(stop - start);

    // Print the elapsed time in minutes
    cout << "Time taken by program: " << duration.count() << " minutes" << endl;
    return 0;
}