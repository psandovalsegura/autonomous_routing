for i in {1..20}; do
    echo Rep, $i
    #./controller.py "random"
    #./controller.py "dijkstra"
    #./controller.py "lessCarAhead"
    ./controller.py "dynamicRandom"
done

