import pandas as pd
import numpy as np
from pulp import LpMinimize, LpProblem, LpVariable, lpSum, LpStatus

def optimize_production(df_machines, df_orders):
    # Create the optimization model
    model = LpProblem("Production Optimization with Multiple Orders", LpMinimize)

    # Decision variables: assignment of each order to each machine
    production = {}
    for _, machine in df_machines.iterrows():
        for _, order in df_orders.iterrows():
            if not pd.isna(machine[f'change_product_{order["product"]}']):
                production[(machine["machine"], order["order_id"])] = LpVariable(
                    f"production_{machine['machine']}_order_{order['order_id']}", 0, order["quantity"], cat="Integer"
                )

    # Objective function: minimize the total production time weighted by priority and balance workload
    objective = []
    for (machine, order_id), variable in production.items():
        order = df_orders.loc[df_orders["order_id"] == order_id].iloc[0]
        product = order["product"]
        production_time = df_machines.loc[df_machines["machine"] == machine, f'change_product_{product}'].values[0]
        priority = order["priority"]
        priority_weight = 1 / priority  # Higher priority reduces time in the objective function
        objective.append(production_time * priority_weight * variable)

    model += lpSum(objective), "Total Time Weighted by Priority"

    # Constraints
    # 1. Meet the demand for each order
    for _, order in df_orders.iterrows():
        order_id = order["order_id"]
        model += lpSum(production.get((machine, order_id), 0) for machine in df_machines["machine"]) == order["quantity"], f"demand_order_{order_id}"

    # 2. Limit maximum production capacity per hour for each machine
    for _, machine in df_machines.iterrows():
        max_capacity = machine["capacity_per_hour"]
        total_time = lpSum(production.get((machine["machine"], order_id), 0) for order_id in df_orders["order_id"])
        model += total_time <= max_capacity, f"capacity_{machine['machine']}"

    # 3. Limit total operating time of each machine to 8 hours (480 minutes) and balance workload
    max_machine_time = 480  # in minutes
    for _, machine in df_machines.iterrows():
        total_machine_time = lpSum(production.get((machine["machine"], order_id), 0) *
                                df_machines.loc[df_machines["machine"] == machine["machine"], 
                                f'change_product_{df_orders.loc[df_orders["order_id"] == order_id]["product"].values[0]}'].values[0]
                                for order_id in df_orders["order_id"] 
                                if (machine["machine"], order_id) in production)
        
        model += total_machine_time <= max_machine_time, f"total_time_machine_{machine['machine']}"

    # Solve the model
    model.solve()
    
    # Lists to collect results
    machine_list = []
    order_id_list = []
    produced_units = []
    production_time = []
    weighted_production_time = []

    # Loop through decision variables and calculate production time and weighted production time
    for (machine, order_id), variable in production.items():
        if variable.varValue > 0:
            # Find product type and priority for the order
            order_info = df_orders.loc[df_orders["order_id"] == order_id].iloc[0]
            product = order_info["product"]
            priority = order_info["priority"]
            
            # Get the time per unit for this machine and product type
            time_per_unit = df_machines.loc[df_machines["machine"] == machine, f'change_product_{product}'].values[0]
            
            # Calculate total production time
            total_time = variable.varValue * time_per_unit  # Produced units * time per unit
            weighted_time = total_time / priority  # Apply priority weighting as per objective

            # Append data to lists
            machine_list.append(machine)
            order_id_list.append(order_id)
            produced_units.append(variable.varValue)
            production_time.append(total_time)
            weighted_production_time.append(weighted_time)

    # Create DataFrame with results including weighted production time
    results_df = pd.DataFrame({
        "Machine": machine_list,
        "Order_ID": order_id_list,
        "Produced_Units": produced_units,
        "Production_Time_Min": production_time,
        "Weighted_Production_Time": weighted_production_time
    })
    
    
    return results_df