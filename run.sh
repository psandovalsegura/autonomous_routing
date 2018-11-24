for i in {1..5}; do
    echo Rep, $i
    ./controller.py "random"
    ./controller.py "dijkstra"
    ./controller.py "lessCarAhead"
    ./controller.py "dynamicRandom"
    ./controller.py "decmcts"
done
