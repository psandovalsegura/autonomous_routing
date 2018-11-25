for i in {1..5}; do
    echo Rep, $i
    python controller.py "random"
    python controller.py "dijkstra"
    python controller.py "lessCarAhead"
    python controller.py "dynamicRandom"
    python controller.py "decmcts"
    #python controller.py "decmcts1Block"
    #python controller.py "decmcts2Block"
    #python controller.py "decmcts5Block"
done
