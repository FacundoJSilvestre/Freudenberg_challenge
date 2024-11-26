import pymongo

def create_data_base():
    # Connect to MongoDB
    client = pymongo.MongoClient("mongodb://admin:freudenberg@localhost:27017/")
    
    # Create DB if not exists
    db = client['injections']
    
    # Seleccionar o crear la colección
    collection = db['injections']
    
    # Main data of the plastic injections
    data_plastic_injections = [
        {
            "machine_id": 1,
            "optimization_case": "Cycle Time Optimization",
            "machine": "Injector 1000A",
            "material": ["Polypropylene", "Polyethylene"],
            "parameters": {
                "initial_cycle_time_sec": 30,
                "optimized_cycle_time_sec": 25,
                "temperature_fusion_c": 230,
                "injection_pressure_bar": 90,
                "cooling_time_sec": 10
            },
            "result": {
                "capacity_per_hour": 144,
                "type":"dual",
                "change_product_A": 2.4,
                "change_product_B": 1.75,
                "defect_rate": "2%",
                "improvement_percentage": "16.67%"
            }
        },
        {
            "machine_id": 2,
            "optimization_case": "Cycle Time Optimization",
            "machine": "Injector 1000A",
            "material": ["Polypropylene", "Polyethylene"],
            "parameters": {
                "initial_cycle_time_sec": 30,
                "optimized_cycle_time_sec": 25,
                "temperature_fusion_c": 230,
                "injection_pressure_bar": 90,
                "cooling_time_sec": 10
            },
            "result": {
                "capacity_per_hour": 144,
                "type":"dual",
                "change_product_A": 2.4,
                "change_product_B": 1.75,
                "defect_rate": "2%",
                "improvement_percentage": "16.67%"
            }
        },
        {
            "machine_id": 3,
            "optimization_case": "Shrinkage Reduction",
            "machine": "Injector 2000C",
            "material": "Polyethylene",
            "parameters": {
                "initial_shrinkage_mm": 0.5,
                "optimized_shrinkage_mm": 0.2,
                "temperature_fusion_c": 220,
                "cooling_time_sec": 12,
                "injection_pressure_bar": 95,
                "mold_temperature_c": 40
            },
            "result": {
                "shrinkage_reduction": "60%",
                "type":"simple",
                "change_product_B": 2.1,
                "cycle_time_sec": 35,
                "capacity_per_hour": 105
            }
        },
        {
            "machine_id": 4,
            "optimization_case": "Shrinkage Reduction",
            "machine": "Injector 2000C",
            "material": "Polyethylene",
            "parameters": {
                "initial_shrinkage_mm": 0.5,
                "optimized_shrinkage_mm": 0.2,
                "temperature_fusion_c": 220,
                "cooling_time_sec": 12,
                "injection_pressure_bar": 95,
                "mold_temperature_c": 40
            },
            "result": {
                "shrinkage_reduction": "60%",
                "cycle_time_sec": 35,
                "type":"simple",
                "change_product_B": 2.1,
                "capacity_per_hour": 105
            }
        },
        {
            "machine_id": 5,
            "optimization_case": "Material Viscosity Adjustment",
            "machine": "Injector 1200D",
            "material": "Nylon",
            "parameters": {
                "viscosity_grade": "High",
                "temperature_fusion_c": 260,
                "injection_speed_mm_sec": 100,
                "injection_pressure_bar": 115,
                "mold_temperature_c": 70
            },
            "result": {
                "pieces_produced": 800,
                "defect_rate": "1.5%",
                "flow_consistency": "Stable"
            }
        }
    ]
    try:
        collection.insert_many(data_plastic_injections)
        print("Data is been populated")
    except Exception as e:
        print(f"Error at insert many {e}") 
    
if __name__ == "__main__":
    create_data_base()
