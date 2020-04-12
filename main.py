import cityflow
eng = cityflow.Engine("examples/config.json", thread_num=1)




for i in range (1000):
    eng.next_step()

    dist = eng.get_vehicle_distance()
    vehicles = eng.get_vehicles()

    # print("Dist: ", dist)
    # for car in vehicles:
    #     print(dist[car])
    locs = eng.get_vehicle_location()
    all_locs = []
    for car, location in locs.items():
        all_locs.append(location[0])
        all_locs.append(location[1])

    if(len(all_locs) != len(set(all_locs))):
        print
        print("collision at step", i)
        #exit()
    
        
    #print("step finished")
    # for car in vehicles:
    #     if(dist[car] != 1.0):
    #         print(dist[car])

# eng.set_tl_phase("intersection_1_1", 0)

# for i in range(1, 1000):
    
#     eng.next_step()
