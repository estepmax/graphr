### GraphR: Graph Based Recommendation
This is a quick and dirty graph based recommendation system for experimentation with sequence data.

### Example
I will be using Instacart shopping cart data  to construct the recommendation graph. We can think
of the Instacart shopping cart data as a chain linking one purchased item to another, which is 
perfectly represented as a graph. Another cool experiment would be to use readily available music playlist (LastFM) data to generate playlists. 

Instacart data: https://www.kaggle.com/c/instacart-market-basket-analysis

## Gatherting data + initializing recommendation graph + calculating weights 
```python
## Gathering Data 

import pandas as pd 
path = "E:/Downloads/order_products__train.csv"

data = pd.read_csv(path)
order_id = list(set(data["order_id"]))
number_of_orders = order_id[0:1000] ## will only look at 1000 carts

orders = list()
for order in number_of_orders:
    product_list = list(data[data.order_id == order].product_id)
    if len(product_list):
        orders.append(product_list)
    
## Initializing Recommendation Graph

graph = GraphR()

for chain in orders:
    graph.insert_chained_edges(chain)

## Calculating weights

graph.node_weights() ## parent weights
graph.child_node_weights() ## child weights
```
A great artifact of generating the recommendation graph and calculating the weights is that you can query the most frequented products right away. 

```python
print(graph.frequented(1))
## [(<__main__.Node object at 0x000001B5C2264940>, 24852, 0.01431556948798328)]
## [(node object,product id,weight)]
```
After running the frequented method, it turns out a banana (24852 => product id, a full list can be downloaded from the kaggle link) is the most popular item customers add to their cart. Yes, a singluar banana....

We can generate a grocery list of a specific size using the max_depth method. But first, we need an
item in our cart to generate recommendations, so, we will place a banana into our cart to see what is recommended. 

```python 
print(graph.max_depth(frequented[0][0],10)) ## pass the banana node object 
## [24852, 10305, 29941, 25340, 22169, 22142, 43789, 39858, 13176, 11526]
## [banana, black plum, red plums,large yellow flesh nectarine,pineapple slices,
##  100% pure pumpkin,organic basil,hydrogen peroxide,bag of organic bananas,
#   napa cabbage]
```
Why is hydrogen peroxide recommended?

Oh, apparently it is used to wash produce according to this article: https://www.dallasnews.com/food/cooking/2019/01/19/how-to-properly-clean-your-fruits-and-vegetables-the-organic-way/

I had no idea......

### A visualization for 20 Shopping Carts as a recommendation graph

![20_cart_graph](https://github.com/estepmax/graphr/blob/master/screenshots/20_Cart_Graph.png)