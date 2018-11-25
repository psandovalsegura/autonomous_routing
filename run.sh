for i in {1..10}; do
    echo Rep, $i
    #./controller.py "random"
    #./controller.py "dijkstra"
    #./controller.py "lessCarAhead"
    #./controller.py "dynamicRandom"
    ./controller.py "decmcts"
    #python controller.py "decmcts1Block"
    #python controller.py "decmcts2Block"
    #python controller.py "decmcts5Block"
done
