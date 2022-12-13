from pydantic import BaseModel, constr

class VehicleBase(BaseModel):
    vin: constr(min_length=17, max_length=17)
    
    @staticmethod 
    def convert_array_to_dictionary(array_json):
        vin_object_array = list(map(VehicleBase.__map_variable_and_value, array_json))
        vin_object_dictionary = {vin_object_array[i][0]: vin_object_array[i][1] for i in range(0, len(vin_object_array))}
        return vin_object_dictionary
        
    @staticmethod
    def __map_variable_and_value(vin_object):
        return [vin_object['Variable'], vin_object['Value']]

class VehicleAdd(VehicleBase):
    make: str 
    model: str 
    model_year: str 
    body_class: str 
    
class VehicleDelete(VehicleBase):
    cached_delete_success: bool