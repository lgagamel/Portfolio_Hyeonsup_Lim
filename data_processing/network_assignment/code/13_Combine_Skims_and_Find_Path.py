import pandas as pd
import numpy as np
import itertools
import pickle
import networkx as nx
import time

output_folder = "output/13/"



# # =============================================================================
# # get GC
# # =============================================================================
# b1 = 5
# b2 = 1
# b3 = 100
# b4 = 10
# b5 = 1
# b6 = 2

# =============================================================================
# get df_parm - a set of parameters to be tested
# =============================================================================
N = 50
print(N)


b1_list = [1.3]
b2_list = [0.3]
b3_list = [1.7]
b4_list = [50]
b5_list = [10]
b6_list = [30]
b7_list = [0.02]
b8_list = [80]
b9_list = [0.6]
b10_list = [3.1]

# b1_list = [5]
# b2_list = [1]
# b3_list = [100]
# b4_list = [100]
# b5_list = [1]
# b6_list = [2]


# Generate all combinations
combinations = list(itertools.product(b1_list, 
                                      b2_list, 
                                      b3_list,
                                      b4_list,
                                      b5_list,
                                      b6_list,
                                      b7_list,
                                      b8_list,
                                      b9_list,
                                      b10_list
                                      ))

# Convert to a DataFrame
df_parm = pd.DataFrame(combinations, columns=['b1', 'b2', 'b3', 'b4', 'b5', 'b6','b7','b8','b9','b10'])

# # add where only b2=1
# df_parm.loc[len(df_parm)] = {'b1': 0, 
#                     'b2': 0, 
#                     'b3': 1,
#                     'b4': 0,
#                     'b5': 0,
#                     'b6': 1,
#                     'b7': 1,
#                     'b8': 0,
#                     'b9': 0,
#                     'b10': 1,
# }

df_parm.to_csv(output_folder + "parm_set.csv",index=False)

for parm_i, parm in df_parm.iterrows():    
    # update parm    
    b1 = parm["b1"]
    b2 = parm["b2"]
    b3 = parm["b3"]
    b4 = parm["b4"]
    b5 = parm["b5"]
    b6 = parm["b6"]
    b7 = parm["b7"]
    b8 = parm["b8"]
    b9 = parm["b9"]
    b10 = parm["b10"]
    
    
    
    
    
    # =============================================================================
    # read data
    # =============================================================================
    df_domestic_od = pd.read_csv("output/10/10_1/county_od.csv")
    df_truck_to_port = pd.read_csv("output/08/truck_port_to_centroid_skim_only_feasible.csv")    
    df_port = pd.read_csv("output/06/ports.csv")

    df_foreign_link_volume = pd.read_csv("output/12/foreign_flow_link_volume.csv")


    # =============================================================================
    # check null values
    # =============================================================================
    ind = df_truck_to_port["distance"].isnull()
    # print("df_truck_to_port",sum(ind))
    

    ind = df_domestic_od["FIPS_O"]==df_domestic_od["FIPS_D"]
    # print("df_domestic_od intra-county",sum(ind))


    # =============================================================================
    # filter
    # =============================================================================
    ind = df_truck_to_port["distance"].isnull()
    df_truck_to_port = df_truck_to_port.loc[~ind]

    # # check
    # ind = df_domestic_od["final"].isnull()
    # df_domestic_od.loc[ind].to_csv(output_folder + "check1.csv",index=False)


    # =============================================================================
    # prepare for merging
    # =============================================================================
    df_domestic_od = df_domestic_od.dropna()
    df_domestic_od = df_domestic_od[['ST_O', 'ST_D', 'FIPS_O', 'FIPS_D','node_id_O', 'node_id_D', 'final']].copy()
    df_domestic_od = df_domestic_od.rename(columns={"final":"tons"})



    df_truck_to_port_O = df_truck_to_port[['node_id_t','node_id_p', 'hour', 'distance', 'path']].copy()
    df_truck_to_port_O = df_truck_to_port_O.rename(columns={'node_id_t':'node_id_O',
                                                            'node_id_p':'node_id_p_o',
                                                            'hour':'hour_1',
                                                            'distance':'distance_1',
                                                            'path':'path_1',
                                                            })
    
    df_truck_to_port_D = df_truck_to_port[['node_id_p', 'node_id_t', 'hour', 'distance', 'path']].copy()
    df_truck_to_port_D = df_truck_to_port_D.rename(columns={'node_id_p':'node_id_p_d',
                                                            'node_id_t':'node_id_D',
                                                            'hour':'hour_3',
                                                            'distance':'distance_3',
                                                            'path':'path_3',
                                                            })

    df_port_O = df_port[['node_id_p', 'TOTAL']].copy()
    df_port_O = df_port_O.rename(columns={'node_id_p':'node_id_p_o',
                                          'TOTAL':'capacity_o'
                                          })


    df_port_D = df_port[['node_id_p', 'TOTAL']].copy()
    df_port_D = df_port_D.rename(columns={'node_id_p':'node_id_p_d',
                                          'TOTAL':'capacity_d'
                                          })


    # =============================================================================
    # merge
    # =============================================================================
    # df_truck_to_port_1 = df_truck_to_port.loc[ind,['node_id_t', 'node_id_p', 'hour', 'distance', 'path']].copy()


    output_columns = ['ST_O','ST_D','FIPS_O','FIPS_D','tons','node_id_O',
                      'hour_1','distance_1','path_1','node_id_p_o','capacity_o','tons_o',
                      'hour_2','distance_2','c_2','path_2','node_id_p_d','capacity_d','tons_d',
                      'hour_3','distance_3','path_3','node_id_D',                  
                      ]
    
    # =============================================================================
    # port volume
    # =============================================================================
    port_volume = {}
    port_list = list(df_port['node_id_p'])
    for port in port_list:
        port_volume[port]=0
    
    # =============================================================================
    # assign foreign volume
    # =============================================================================
    for i,row in df_foreign_link_volume.iterrows():
        port = row["link_id"].replace("PW","P")
        tons = row["tons"]
        try:
            port_volume[port] = port_volume[port] + tons
        except:
            pass
    
    
    # =============================================================================
    # main loop
    # =============================================================================    
    FIPS_O_list = list(df_domestic_od["FIPS_O"].unique())
    
    truck_link_volume = {}
    water_link_volume = {}
    
    with open("output/11/G_water.pickle", 'rb') as file:
        G_water = pickle.load(file)
    
    # update volume
    for u, v in G_water.edges():    
        G_water[u][v]['volume'] = 0
            

    # =============================================================================
    # assign foreign volume to water links
    # =============================================================================
    for i,row in df_foreign_link_volume.iterrows():
        link = row["link_id"]
        tons = row["tons"]
        if link[0]=="W":
            try:
                water_link_volume[link] = water_link_volume[link] + tons
            except:
                water_link_volume[link] = tons
    
    
    for itr in range(N):
        print(parm_i, itr)
        
        # =============================================================================
        # water port-to-port routing
        # =============================================================================
        # update volume
        if len(water_link_volume)>0:
            for u, v in G_water.edges():
                try:
                    link_id = G_water[u][v]['link_id']
                    tons = water_link_volume[link_id]
                except:
                    tons = 0
                G_water[u][v]['volume'] = tons
                # print(link_id,G_water[u][v]['volume'])
                
        # update C
        for u, v in G_water.edges():
            if G_water[u][v]['capacity']<10:
                G_water[u][v]['C'] = G_water[u][v]['hour']*(2+b2*(G_water[u][v]['volume']/10)**b3)+\
                    b4*(G_water[u][v]['link_type']=="CHG")+\
                    b5*G_water[u][v]['hour']*G_water[u][v]['link_p']
                    # G_water[u][v]['hour']*(1+b5*(1**b6))+\
            elif G_water[u][v]['capacity']>=10:
                G_water[u][v]['C'] = G_water[u][v]['hour']*(1+b5*(G_water[u][v]['volume']/G_water[u][v]['capacity'])**b6)+\
                    b3*(G_water[u][v]['link_type']=="CHG")+\
                    b5*G_water[u][v]['hour']*G_water[u][v]['link_p']
            else:
                raise("negative capacity")
                                
            if (np.isnan(G_water[u][v]['C']))|(np.isinf(G_water[u][v]['C'])):
                raise()
        
        # centroid & port        
        port_df = pd.read_csv('output/06/ports.csv')
        node_id_w_list = list(port_df["node_id_w"])
        node_id_p_list = list(port_df["node_id_p"])

        # output hour and distance        
        # print(len(G_water.edges))
        f_out = open(output_folder+"water_port_to_port_skim.csv", 'w')
        # f_out.write("o,d,path,dist\n")
        f_out.write("node_id_p_o,node_id_w_o,node_id_p_d,node_id_w_d,hour,distance,c,path\n")
        for i,o in enumerate(node_id_w_list):
            node_id_w_o = o
            node_id_p_o = node_id_p_list[i]    
            C_by_o,path_by_o = nx.single_source_dijkstra(G=G_water, source=o, weight='C')
            # path_by_o = nx.single_source_dijkstra_path(G=G, source=o, weight='hour')
            for j,d in enumerate(node_id_w_list):
                if o!=d:
                    node_id_w_d = d
                    node_id_p_d = node_id_p_list[j]
                    # print("O",i,o,node_id_p_o)
                    # print("D",j,d,node_id_p_d)            
                    try:
                        c = C_by_o[d]         
                        distance = 0
                        hour = 0 
                        path_od = path_by_o[d]
                        path_join = []
                        if len(path_od)>=2:
                            for i in range(len(path_od)-1):
                                e = (path_od[i],path_od[i+1])
                                distance = distance + G_water.edges[e]["distance"]
                                hour = hour + G_water.edges[e]["hour"]
                                # G_water.edges[e]["volume"] = G_water.edges[e]["volume"] + tons
                                path_join.append(G_water.edges[e]["link_id"])
                        c = str(round(c,4))
                        hour = str(round(hour,4))
                        distance = str(round(distance,4))
                        path_join = "-".join(path_join)
                    except:
                        c = ""
                        hour = ""
                        distance = ""
                        path_join = ""
                    tmp_line = ",".join([node_id_p_o,node_id_w_o,node_id_p_d,node_id_w_d,hour,distance,c,path_join]) + "\n"
                    f_out.write(tmp_line)
        f_out.close()
        
        time.sleep(5)
        df_port_to_port = pd.read_csv(output_folder+ "water_port_to_port_skim.csv")
        ind = df_port_to_port["distance"].isnull()
        df_port_to_port.loc[ind]
        # print("df_port_to_port",sum(ind))
        
        ind = df_port_to_port["distance"].isnull()
        df_port_to_port = df_port_to_port.loc[~ind]

        ind = df_port_to_port["node_id_p_o"] == df_port_to_port["node_id_p_d"]
        df_port_to_port = df_port_to_port.loc[~ind]
        
        df_port_to_port = df_port_to_port[['node_id_p_o', 'node_id_p_d','hour', 'distance','c','path']].copy()
        df_port_to_port = df_port_to_port.rename(columns={'hour':'hour_2',
                                                          'distance':'distance_2',
                                                          'c':'c_2',
                                                          'path':'path_2',
                                                          })
        
        df_port_volume_O = pd.DataFrame(list(port_volume.items()), columns=['node_id_p_o', 'tons_o'])
        df_port_volume_D = pd.DataFrame(list(port_volume.items()), columns=['node_id_p_d', 'tons_d'])
        df_out = pd.DataFrame()
        for i,FIPS_O in enumerate(FIPS_O_list):        
            ind = df_domestic_od["FIPS_O"]==FIPS_O
            df = df_domestic_od.loc[ind].copy()
            total_tons = sum(df["tons"])/N
            df = df.merge(df_truck_to_port_O,on=['node_id_O'],how="left")    
            df = df.merge(df_truck_to_port_D,on=['node_id_D'],how="left")    
            df = df.merge(df_port_to_port,on=['node_id_p_o', 'node_id_p_d'],how="left")    
            df = df.merge(df_port_O,on=['node_id_p_o'],how="left")
            df = df.merge(df_port_D,on=['node_id_p_d'],how="left")
            df = df.merge(df_port_volume_O,on=['node_id_p_o'],how="left")
            df = df.merge(df_port_volume_D,on=['node_id_p_d'],how="left")
            
            # df["check"] = (df.isnull().sum(axis=1)==0)*1
            # df_grp = df.groupby(["FIPS_O","FIPS_D"],as_index=False).agg(check_sum=("check","sum"))
            # df_grp.to_csv(output_folder+"check2.csv",index=False)
            
            # df = df.merge(df_grp,on=["FIPS_O","FIPS_D"],how="left")
            # df.to_csv(output_folder+"check3.csv",index=False)
            # raise()
            
            ind = df[["hour_1","distance_1","hour_2","distance_2","c_2","hour_3","distance_3"]].isnull().sum(axis=1)==0
            df = df.loc[ind]
            # df = df.dropna()
            df = df[output_columns]
            
            # df["GC_wo_port_delay"] = b1*(df['hour_1']+df['hour_2']+df['hour_3'])+\
            #                 b2*(0.5*(df['distance_1']+df['distance_3']) + 0.015*df['distance_2'])
                            
            # df["GC"] = b1*(df['hour_1']+df['hour_2']+df['hour_3'])+\
            #                 b2*(0.5*(df['distance_1']+df['distance_3']) + 0.015*df['distance_2'])+\
            #                 b4*(1+b5*(df['tons_o']/df['capacity_o'])**b6)+\
            #                 b4*(1+b5*(df['tons_d']/df['capacity_d'])**b6)
            
            df["GC"] = b1*(df['hour_1']+df['c_2']+df['hour_3'])+\
                b6*(df['distance_1']+df['distance_3'])+\
                b7*df['distance_2']+\
                b8*(1+b9*(df['tons_o']/df['capacity_o'])**b10)+\
                b8*(1+b9*(df['tons_d']/df['capacity_d'])**b10)
                    
            df_grp = df.groupby(['FIPS_O','FIPS_D','node_id_O','node_id_D'],as_index=False).agg(GC_min=('GC','min'))
            df = df.merge(df_grp,on=['FIPS_O','FIPS_D','node_id_O','node_id_D'],how="left")
            # df.to_csv(output_folder + f"{FIPS_O}.csv",index=False)
            # raise()
            
            ind = df["GC"]==df["GC_min"]
            df = df.loc[ind]
            df["cnt"] = 1
            df_grp = df.groupby(['FIPS_O','FIPS_D','node_id_O','node_id_D'],as_index=False).agg(cnt_sum=('cnt','sum'))
            df = df.merge(df_grp,on=['FIPS_O','FIPS_D','node_id_O','node_id_D'],how="left")
            df["assigned_tons"] = df["tons"]/df["cnt_sum"]/N
            adj_f = total_tons/sum(df["assigned_tons"])
            df["assigned_tons"] = df["assigned_tons"] * adj_f
            # print(itr,i,FIPS_O,round(adj_f,3))
            # df.to_csv(output_folder + f"{FIPS_O}_selected.csv",index=False)
            # raise()
            
            df_out = pd.concat([df_out,df], ignore_index=True)
            # update port volume
            for i,row in df.iterrows():
                tons = row["assigned_tons"]        
                port = row["node_id_p_o"]
                port_volume[port] = port_volume[port] + tons
                port = row["node_id_p_d"]
                port_volume[port] = port_volume[port] + tons
        
        # needed only if we want to save routing info.
        df_out.to_csv(output_folder + f"routing_{b1}_{b2}_{b3}_{b4}_{b5}_{b6}_{b7}_{b8}_{b9}_{b10}_itr_{itr}.csv",index=False)
        
        
        # print("updating link volume")
        for i,row in df_out.iterrows():
            tons = row["assigned_tons"]
            
            for col in ["path_1","path_3"]:
                try:
                    path = row[col].split("-")        
                except:
                    path = []
                for link in path:
                    if len(link)>0:
                        try:
                            truck_link_volume[link] = truck_link_volume[link] + tons
                        except:
                            truck_link_volume[link] = tons
                    
            for col in ["path_2"]:
                try:
                    path = row[col].split("-")        
                except:
                    path = []
                for link in path:
                    if len(link)>0:
                        try:
                            water_link_volume[link] = water_link_volume[link] + tons
                        except:
                            water_link_volume[link] = tons
                    
    
    df_truck_link_volume = pd.DataFrame(list(truck_link_volume.items()), columns=['link_id', 'tons'])
    df_water_link_volume = pd.DataFrame(list(water_link_volume.items()), columns=['link_id', 'tons'])
    df_port_volume = pd.DataFrame(list(port_volume.items()), columns=['node_id_p', 'tons'])
    df_truck_link_volume = df_truck_link_volume.loc[df_truck_link_volume["tons"]>0]
    df_water_link_volume = df_water_link_volume.loc[df_water_link_volume["tons"]>0]
    df_port_volume = df_port_volume.loc[df_port_volume["tons"]>0]
    df_truck_link_volume.to_csv(output_folder + f"truck_link_volume_{b1}_{b2}_{b3}_{b4}_{b5}_{b6}_{b7}_{b8}_{b9}_{b10}.csv",index=False)
    df_water_link_volume.to_csv(output_folder + f"water_link_volume_{b1}_{b2}_{b3}_{b4}_{b5}_{b6}_{b7}_{b8}_{b9}_{b10}.csv",index=False)
    df_port_volume.to_csv(output_folder + f"port_volume_{b1}_{b2}_{b3}_{b4}_{b5}_{b6}_{b7}_{b8}_{b9}_{b10}.csv",index=False)