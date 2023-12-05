#ifndef BAG_H
#define BAG_H

#include "Pennant.h"
#include <stdio.h>
#include <stdlib.h>
#include <math.h>

extern "C++"{
 
class Bag{

 public:
  Bag();
  Bag(const Bag* & bag);
  ~Bag();

  void insert(int item);
  bool empty() const;
  void merge(Bag* bag);
  Bag* split();
  void clear();
  int size() const;
  bool can_split() const;
  void print() const;
  void recursive_print(Node* node) const; // prints in-order
  void recursive_print_sum(Node* node, int & sum) const;
  void remove_all();
  int* write_array();
  void recursive_write_array(int* & array, Node* node, int &count);

  friend class Bag_reducer;

  int forest_size;

  Pennant** forest;
};

 
class Bag_reducer{
  
 public:

  Bag_reducer()  {}
  int get_forest_size()
  {
    return imp_.forest_size;
  }
  Pennant* get_forest(int i)
  {
    return imp_.forest[i];
  }
  void set_forest(int i, Pennant* tree)
  {
    imp_.forest[i] = tree;
  }
  void insert(int item)
  {
  imp_.insert(item);
  }
  void merge(Bag_reducer* br)
  {
  this->imp_.merge(&br->imp_);
  }
  Bag* split()
  {
    return imp_.split();
  }
  bool empty() const
  {
  return imp_.empty();
  }
  void clear()
  {
  return imp_.clear();
  }
  Bag &get_reference()
  {
  return imp_;
  }
  int size()
  {
    return imp_.size();
  }
  int* write_array()
  {
    return imp_.write_array();
  }
  

 private:
  Bag imp_;

};
}

#endif


