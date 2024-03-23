#include <iostream>
#include <assert.h>
#include <stdlib.h>
#include <list>

class Point{
    public:
        int x; 
        int y;

        Point(): Point(0, 0) {}
        Point(int x, int y): x(x), y(y) {}
};

class Shape {
    public:
        Point center_;
        virtual void draw()=0;
};

class Circle: public Shape {
    virtual void draw() {
        std::cerr <<"in drawCircle\n";
    };

    private:
        double radius_;
};

class Square: public Shape {
    virtual void draw() {
        std::cerr <<"in drawSquare\n";
    };

    private:
        double side_;
};

class Rhomb: public Shape {
    virtual void draw() {
        std::cerr <<"in drawRhomb\n";
    };

    private:
        double side_;
};

void drawShapes (const std::list<Shape*>& fig) {
    std::list<Shape*>::const_iterator it;
    for (it = fig.begin(); it != fig.end(); ++ it ){
        (*it)->draw();
    } 
}

void moveShapes (const std::list<Shape*>& fig, int dx, int dy) {
    std::list<Shape*>::const_iterator it;
    for (it = fig.begin(); it != fig.end(); ++ it ){
        (*it)->center_.x += dx;
        (*it)->center_.y += dy;
    } 
}

int main(void) {
    std::list<Shape*> shapes = { (Shape *) new Circle, (Shape *) new Square, (Shape *) new Rhomb, (Shape *) new Circle };
    drawShapes(shapes);
}