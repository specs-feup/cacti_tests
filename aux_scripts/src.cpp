
struct Vector {
    double x, y;

    Vector operator+(const Vector& other) const {
        return {x + other.x, y + other.y};
    }
};

int main(){
    Vector v{1.0,2.0};
    Vector v1{1.0, 2.0};
    Vector r = v + v1;
    return 0;
}