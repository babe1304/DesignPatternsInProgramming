#include <iostream>
#include <assert.h>
#include <stdlib.h>

struct Point{
int x; int y;
};
struct Shape {
    enum EType {circle, square, rhomb};
    EType type_;
};
struct Circle {
    Shape::EType type_;
    double radius_;
    Point center_;
};
struct Square {
    Shape::EType type_;
    double side_;
    Point center_;
};
struct Rhomb {
    Shape::EType type_;
    double side_;
    Point center_;
};

void drawSquare(struct Square*) {
    std::cerr <<"in drawSquare\n";
}
void drawCircle(struct Circle*) {
    std::cerr <<"in drawCircle\n";
}
void drawRhomb(struct Rhomb*) {
    std::cerr <<"in drawRhomb\n";
}
void drawShapes(Shape** shapes, int n){
    for (int i=0; i<n; ++i){
        struct Shape* s = shapes[i];
        switch (s->type_) {
            case Shape::square:
                drawSquare((struct Square*)s);
                break;
            case Shape::circle:
                drawCircle((struct Circle*)s);
                break;
            case Shape::rhomb:
                drawRhomb((struct Rhomb*)s);
                break;
            default:
                assert(0); 
                exit(0);
        }
    }
}

void moveShapes(Shape** shapes, int n, int dx, int dy) {
    for (int i=0; i<n; i++) {
        Shape *s = shapes[i];
        switch(s->type_) {
            case Shape::circle: {
                Circle *circle = (Circle *) s;
                circle->center_.x += dx;
                circle->center_.y += dy;
                break;
            }
            case Shape::square: {
                Square *sq = (Square *) s;
                sq->center_.x += dx;
                sq->center_.y += dy;
                break;
            }
            // Program bi trebao puknuti bez ovog zakomentiranog dijela
            // case Shape::rhomb: {
            //     Rhomb *sq = (Rhomb *) s;
            //     sq->center_.x += dx;
            //     sq->center_.y += dy;
            //     break;
            // }
            default:
                assert(0);
                exit(0);
        }
    }
}

int main(){
    Shape* shapes[4];
    shapes[0]=(Shape*)new Circle;
    shapes[0]->type_=Shape::circle;
    shapes[1]=(Shape*)new Square;
    shapes[1]->type_=Shape::square;
    shapes[2]=(Shape*)new Square;
    shapes[2]->type_=Shape::square;
    shapes[3]=(Shape*)new Rhomb;
    shapes[3]->type_=Shape::rhomb;

    drawShapes(shapes, 4);
}