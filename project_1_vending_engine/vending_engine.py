import copy
class VendingMetricEngine:
    def __init__(self):
        self.payload = {}
    

    @property
    def inventory_snapshot(self):
        return copy.deepcopy(self.payload)
    
    def add_incoming_data(self, machine_id: str, item_name: str, price: float, quantity: int):
        
        if not isinstance(machine_id, str):
           raise ValueError("machine_id must be a string.")
        if not isinstance(item_name, str):
            raise ValueError("item_name must be a string.")
        if not isinstance(price, (int, float)) or price <= 0:
            raise ValueError("price must be a positive number.")
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("quantity must be a positive integer.")

        
        if not item_name.strip():
            raise ValueError("item_name cannot be blank or whitespace.")
        if not machine_id.strip():
            raise ValueError("machine_id cannot be blank or whitespace.")
            
        if machine_id not in self.payload:
            self.payload[machine_id] = {
                "total_revenue" : 0,
                "items_sold"     : {}
            }        

        machine = self.payload[machine_id]
        machine["total_revenue"] += price * quantity
        machine["items_sold"][item_name] = machine["items_sold"].get(item_name, 0) + quantity        

    def __repr__(self) -> str:
        active_machine = list(self.payload.keys())
        total_rev = sum(m["total_revenue"] for m in self.payload.values())
        return f"{self.__class__.__name__} (active_machine:- {active_machine}, total_rev :- {total_rev}"

engine = VendingMetricEngine()
engine.add_incoming_data(machine_id="machine_101", item_name="soda", price=2.50, quantity=2)
engine.add_incoming_data(machine_id="machine_102", item_name="canday", price=1, quantity=12)
engine.add_incoming_data(machine_id="machine_101", item_name="chips", price=1.75, quantity=1)

print(engine.inventory_snapshot)
print(engine)