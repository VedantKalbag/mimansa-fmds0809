import json
from enum import Enum, auto

class CommodityClass(Enum):
    C1 = "C1"
    C2 = "C2"
    C3 = "C3"
    C4 = "C4"
    CartonedPlastics = "CartonedPlastics"
    UncartonedPlastics = "UncartonedPlastics"

class FMDS0809_FIGURES():
    Fig2j = 'fig2j.jpg'
    Fig2k = 'fig2k.jpg'
    Fig5 = 'fig5.jpg'
    Fig6a = 'fig6a.jpg'
    Fig8 = 'fig8.jpg'
    Fig9 = 'fig9.jpg'
    Fig9a = 'fig9a.jpg'
    Fig10 = 'fig10.jpg'
    Fig11 = 'fig11.jpg'
    Fig11a = 'fig11a.jpg'
    Fig12 = 'fig12.jpg'
    Fig12a = 'fig12a.jpg'
    Fig13 = 'fig13.jpg'
    Fig14 = 'fig14.jpg'

def mm_to_m(mm):
    return mm*1e-3

def mm2_to_m2(mm2):
    return mm2*1e-6

class Rack():
    def __init__(self, rack_dict):
        self.F_SRR_RACK_DEPTH_THRESHOLD_MM = 900
        self.F_DRR_RACK_DEPTH_THRESHOLD_MM = 2700
        self.F_MRR_RACK_DEPTH_THRESHOLD_MM = None # TODO: Implement MRR


        # rack_dict = json.load(open(path_to_json))

        self.s_rack_type = rack_dict['s_rack_type'] # SRR, DRR, MRR
        self.s_commodity_class = CommodityClass(rack_dict['s_commodity_class']) # C1, C2, C3, C4, Plastics
        self.b_open_top_containers = rack_dict['b_open_top_containers'] # True or False
        # self.f_rack_height_mm = rack_dict['f_rack_height_mm']
        self.f_rack_depth_mm = rack_dict['f_rack_depth_mm']
        self.f_beam_length_mm = rack_dict['f_beam_length_mm']
        self.f_vertical_clearance_mm = rack_dict['f_vertical_clearance_mm'] # Distance from top of storage to IRAS
        self.b_horizontal_barriers = rack_dict['b_horizontal_barriers'] # True or False
        self.f_transverse_flue_length_mm = rack_dict['f_transverse_flue_length_mm'] # MINIMUM 150MM
        self.f_longitudinal_flue_length_mm = rack_dict['f_longitudinal_flue_length_mm']
        self.b_solid_shelves = rack_dict['b_solid_shelves'] # True or False
        if self.b_solid_shelves:
            if self.s_rack_type == 'SRR':
                self.f_solid_shelf_area_m2 = mm2_to_m2(self.f_beam_length_mm * self.f_rack_depth_mm)
            elif self.s_rack_type == 'DRR':
                self.f_solid_shelf_area_m2 = mm2_to_m2(self.f_beam_length_mm * self.f_rack_depth_mm / 2)
            elif self.s_rack_type == 'MRR':
                raise NotImplementedError  # TODO: Implement MRR
        else:
            self.f_solid_shelf_area_m2 = 0
        self.f_max_storage_height_m = rack_dict['f_max_storage_height_m']
        # self.b_uncartoned_plastics = rack_dict['b_uncartoned_plastics'] # True or False
    
    def __repr__(self):
        return "{}({!r})".format(self.__class__.__name__, self.__dict__)
    
class Building():
    def __init__(self,path_to_json):
        data = json.load(open(path_to_json))
        self.f_max_ceiling_height_m = data['f_max_ceiling_height_m']
        self.f_building_slope_deg = data['f_building_slope_deg']
        self.rack = Rack(data['rack'])
        self.F_BUILDING_HEIGHT_THRESH_M = 12

    def __repr__(self):
        return "{}({!r})".format(self.__class__.__name__, self.__dict__)
    
    def check_building_height(self):
        if self.f_max_ceiling_height_m < self.F_BUILDING_HEIGHT_THRESH_M:
            print("Building height is less than 12m. Roof-only available. Continue with in-racks?")
            # Take user input for continue with in-racks or not
    
    def main(self):
        if self.rack.s_rack_type == 'SRR':
            figures = self.srr()
        elif self.rack.s_rack_type == 'DRR':
            figures = self.drr()
        elif self.rack.s_rack_type == 'MRR':
            figures = self.mrr()
        else:
            raise ValueError("Invalid rack type")
        if len(figures) > 0 :
            # print([f for f in figures])
            return figures
        
    def srr(self):
        if self.rack.f_rack_depth_mm <= self.rack.F_SRR_RACK_DEPTH_THRESHOLD_MM:
            return self.srr_under_threshold()
        else:
            return self.srr_over_threshold()
    
    def srr_under_threshold(self):
        if self.rack.b_open_top_containers:
            print("See Section 2.2.4")
            # TODO: Display Section 2.2.4
            return []
        else:
            if self.rack.f_vertical_clearance_mm < 150:
                return [FMDS0809_FIGURES.Fig11]
            else:
                if self.rack.b_horizontal_barriers:
                    return [FMDS0809_FIGURES.Fig8, FMDS0809_FIGURES.Fig11]
                else:
                    if self.rack.b_solid_shelves:
                        if self.rack.f_solid_shelf_area_m2 > 6:
                            return [FMDS0809_FIGURES.Fig8, FMDS0809_FIGURES.Fig11]
                        elif (2 <= self.rack.f_solid_shelf_area_m2 <= 6):
                            if self.rack.f_max_storage_height_m >= 7.5:
                                return [FMDS0809_FIGURES.Fig11]
                            else:
                                return [FMDS0809_FIGURES.Fig8, FMDS0809_FIGURES.Fig11]
                        else:
                            pass
                    if self.rack.f_max_storage_height_m <= 7.5:
                        if self.rack.s_commodity_class in [CommodityClass.C4, CommodityClass.CartonedPlastics, CommodityClass.UncartonedPlastics]:
                            if self.rack.s_commodity_class == CommodityClass.UncartonedPlastics:
                                if self.f_max_ceiling_height_m >= 7.5:
                                    return [FMDS0809_FIGURES.Fig11]
                                else:
                                    return [FMDS0809_FIGURES.Fig8, FMDS0809_FIGURES.Fig11]
                            else:
                                if self.f_max_ceiling_height_m <= 9:
                                    return[FMDS0809_FIGURES.Fig8, FMDS0809_FIGURES.Fig11]
                                else:
                                    return [FMDS0809_FIGURES.Fig11]
                        else:
                            return [FMDS0809_FIGURES.Fig8, FMDS0809_FIGURES.Fig11]
                    else:
                        return [FMDS0809_FIGURES.Fig11]
                        
    def srr_over_threshold(self):
        if self.rack.b_open_top_containers:
            print("See Section 2.2.4")
            return []
        else:
            if self.rack.f_vertical_clearance_mm < 150: # Strictly less than
                return [FMDS0809_FIGURES.Fig11a]
            else:
                if self.rack.b_horizontal_barriers:
                    if self.rack.f_max_storage_height_m > 7.5: # Strictly greater than
                        if self.rack.s_commodity_class == CommodityClass.UncartonedPlastics:
                            return [FMDS0809_FIGURES.Fig2j, FMDS0809_FIGURES.Fig11a]
                        else:
                            return [FMDS0809_FIGURES.Fig8, FMDS0809_FIGURES.Fig11, FMDS0809_FIGURES.Fig2j, FMDS0809_FIGURES.Fig11a]
                    else:
                        return [FMDS0809_FIGURES.Fig8, FMDS0809_FIGURES.Fig11, FMDS0809_FIGURES.Fig2j, FMDS0809_FIGURES.Fig11a]
                else:
                    if self.rack.b_solid_shelves:
                        if self.rack.f_solid_shelf_area_m2 > 6:
                            if self.rack.f_max_storage_height_m > 7.5: # Strictly greater than
                                if self.rack.s_commodity_class == CommodityClass.UncartonedPlastics:
                                    return [FMDS0809_FIGURES.Fig2j, FMDS0809_FIGURES.Fig11a]
                                else:
                                    return [FMDS0809_FIGURES.Fig8, FMDS0809_FIGURES.Fig11, FMDS0809_FIGURES.Fig2j, FMDS0809_FIGURES.Fig11a]
                            else:
                                return [FMDS0809_FIGURES.Fig8, FMDS0809_FIGURES.Fig11, FMDS0809_FIGURES.Fig2j, FMDS0809_FIGURES.Fig11a]
                        elif (2 < self.rack.f_solid_shelf_area_m2 <= 6):
                            if self.rack.f_max_storage_height_m > 7.5: # Strictly greater than
                                if self.rack.s_commodity_class == CommodityClass.UncartonedPlastics:
                                    return [FMDS0809_FIGURES.Fig11a]
                                else:
                                    return [FMDS0809_FIGURES.Fig8, FMDS0809_FIGURES.Fig11, FMDS0809_FIGURES.Fig2j, FMDS0809_FIGURES.Fig11a]
                            else:
                                return [FMDS0809_FIGURES.Fig8, FMDS0809_FIGURES.Fig11, FMDS0809_FIGURES.Fig2j, FMDS0809_FIGURES.Fig11a]
                        else:
                            pass
                    if self.rack.f_max_storage_height_m <= 7.5:
                        if self.rack.s_commodity_class in [CommodityClass.C4, CommodityClass.CartonedPlastics, CommodityClass.UncartonedPlastics]:
                            if self.rack.s_commodity_class == CommodityClass.UncartonedPlastics:
                                if self.f_max_ceiling_height_m > 7.5: # Strictly greater than
                                    return [FMDS0809_FIGURES.Fig8, FMDS0809_FIGURES.Fig11, FMDS0809_FIGURES.Fig2j, FMDS0809_FIGURES.Fig11a]
                                else:
                                    return [FMDS0809_FIGURES.Fig11, FMDS0809_FIGURES.Fig11a]
                            else:
                                if self.f_max_ceiling_height_m > 9: # Strictly greater than
                                    return [FMDS0809_FIGURES.Fig11, FMDS0809_FIGURES.Fig11a]
                                else:
                                    [FMDS0809_FIGURES.Fig8, FMDS0809_FIGURES.Fig11, FMDS0809_FIGURES.Fig2j, FMDS0809_FIGURES.Fig11a]
                        else:
                            [FMDS0809_FIGURES.Fig8, FMDS0809_FIGURES.Fig11, FMDS0809_FIGURES.Fig2j, FMDS0809_FIGURES.Fig11a]
                    else:
                        if self.rack.s_commodity_class == CommodityClass.UncartonedPlastics:
                            return [FMDS0809_FIGURES.Fig11a]
                        else:
                            return [FMDS0809_FIGURES.Fig11, FMDS0809_FIGURES.Fig11a]    
                    
    def drr(self):
        if self.rack.f_rack_depth_mm <= self.rack.F_DRR_RACK_DEPTH_THRESHOLD_MM:
            return self.drr_under_threshold()
        else:
            return self.drr_over_threshold()
    
    def drr_under_threshold(self):
        if self.rack.b_open_top_containers:
            print("See Section 2.2.4")
            return []
        else:
            if self.rack.f_vertical_clearance_mm < 150: # Strictly less than
                return [FMDS0809_FIGURES.Fig13]
            else:
                if self.rack.b_horizontal_barriers:
                    if self.rack.f_max_storage_height_m > 7.5: # Strictly greater than
                        if self.rack.s_commodity_class == CommodityClass.UncartonedPlastics:
                            return [FMDS0809_FIGURES.Fig2k, FMDS0809_FIGURES.Fig13]
                        else:
                            return [FMDS0809_FIGURES.Fig9, FMDS0809_FIGURES.Fig9a, FMDS0809_FIGURES.Fig12, FMDS0809_FIGURES.Fig12a, FMDS0809_FIGURES.Fig2k, FMDS0809_FIGURES.Fig13]
                    else:
                        return [FMDS0809_FIGURES.Fig9, FMDS0809_FIGURES.Fig9a, FMDS0809_FIGURES.Fig12, FMDS0809_FIGURES.Fig12a, FMDS0809_FIGURES.Fig2k, FMDS0809_FIGURES.Fig13]
                else:
                    if self.rack.b_solid_shelves:
                        if self.rack.f_solid_shelf_area_m2 > 6: # Strictly greater than
                            if self.rack.f_max_storage_height_m > 7.5: # Strictly greater than
                                if self.rack.s_commodity_class == CommodityClass.UncartonedPlastics:
                                    return [FMDS0809_FIGURES.Fig2k, FMDS0809_FIGURES.Fig13]
                                else:
                                    return [FMDS0809_FIGURES.Fig9, FMDS0809_FIGURES.Fig9a, FMDS0809_FIGURES.Fig12, FMDS0809_FIGURES.Fig12a, FMDS0809_FIGURES.Fig2k, FMDS0809_FIGURES.Fig13]
                            else:
                                return [FMDS0809_FIGURES.Fig9, FMDS0809_FIGURES.Fig9a, FMDS0809_FIGURES.Fig12, FMDS0809_FIGURES.Fig12a, FMDS0809_FIGURES.Fig2k, FMDS0809_FIGURES.Fig13]
                        elif (2 < self.rack.f_solid_shelf_area_m2 <= 6):
                            if self.rack.f_max_storage_height_m > 7.5: # Strictly greater than
                                return [FMDS0809_FIGURES.Fig13]
                            else:
                                return [FMDS0809_FIGURES.Fig9, FMDS0809_FIGURES.Fig9a, FMDS0809_FIGURES.Fig12, FMDS0809_FIGURES.Fig12a, FMDS0809_FIGURES.Fig2k, FMDS0809_FIGURES.Fig13]
                        else:
                            pass
                    if self.rack.f_max_storage_height_m > 7.5: # Strictly greater than
                        if self.rack.s_commodity_class in [CommodityClass.C4, CommodityClass.CartonedPlastics, CommodityClass.UncartonedPlastics]:
                            if self.rack.s_commodity_class == CommodityClass.UncartonedPlastics:
                                if self.f_max_ceiling_height_m > 7.5: # Strictly greater than
                                    return [FMDS0809_FIGURES.Fig12, FMDS0809_FIGURES.Fig13]
                                else:
                                    return [FMDS0809_FIGURES.Fig9, FMDS0809_FIGURES.Fig9a, FMDS0809_FIGURES.Fig12, FMDS0809_FIGURES.Fig12a, FMDS0809_FIGURES.Fig2k, FMDS0809_FIGURES.Fig13]
                            else:
                                if self.f_max_ceiling_height_m <= 9:
                                    return [FMDS0809_FIGURES.Fig9, FMDS0809_FIGURES.Fig9a, FMDS0809_FIGURES.Fig12, FMDS0809_FIGURES.Fig12a, FMDS0809_FIGURES.Fig2k, FMDS0809_FIGURES.Fig13]
                                else:
                                    return [FMDS0809_FIGURES.Fig12, FMDS0809_FIGURES.Fig13]
                        else:
                            return [FMDS0809_FIGURES.Fig9, FMDS0809_FIGURES.Fig9a, FMDS0809_FIGURES.Fig12, FMDS0809_FIGURES.Fig12a, FMDS0809_FIGURES.Fig2k, FMDS0809_FIGURES.Fig13]
                    else:
                        return [FMDS0809_FIGURES.Fig13]
                                
    def drr_over_threshold(self):
        if self.rack.b_open_top_containers:
            print("See Section 2.2.4")
            return []
        else:
            if self.rack.f_vertical_clearance_mm < 150: # Strictly less than
                return [FMDS0809_FIGURES.Fig13]
            else:
                if self.rack.b_horizontal_barriers:
                    if self.rack.f_max_storage_height_m > 7.5: # Strictly greater than
                        if self.rack.s_commodity_class == CommodityClass.UncartonedPlastics:
                            return [FMDS0809_FIGURES.Fig2k, FMDS0809_FIGURES.Fig13]
                        else:
                            return [FMDS0809_FIGURES.Fig9a, FMDS0809_FIGURES.Fig12a, FMDS0809_FIGURES.Fig2k, FMDS0809_FIGURES.Fig13]
                    else:
                        return [FMDS0809_FIGURES.Fig9a, FMDS0809_FIGURES.Fig12a, FMDS0809_FIGURES.Fig2k, FMDS0809_FIGURES.Fig13]
                else:
                    if self.rack.b_solid_shelves:
                        if self.rack.f_solid_shelf_area_m2 > 6:
                            if self.rack.f_max_storage_height_m > 7.5:
                                if self.rack.s_commodity_class == CommodityClass.UncartonedPlastics:
                                    return [FMDS0809_FIGURES.Fig2k, FMDS0809_FIGURES.Fig13]
                                else:
                                    return [FMDS0809_FIGURES.Fig9a, FMDS0809_FIGURES.Fig12a, FMDS0809_FIGURES.Fig2k, FMDS0809_FIGURES.Fig13]
                            else:
                                return [FMDS0809_FIGURES.Fig9a, FMDS0809_FIGURES.Fig12a, FMDS0809_FIGURES.Fig2k, FMDS0809_FIGURES.Fig13]
                        elif (2 < self.rack.f_solid_shelf_area_m2 <= 6):
                            if self.rack.f_max_storage_height_m > 7.5:
                                return [FMDS0809_FIGURES.Fig13]
                            else:
                                return [FMDS0809_FIGURES.Fig9a, FMDS0809_FIGURES.Fig12a, FMDS0809_FIGURES.Fig2k, FMDS0809_FIGURES.Fig13]
                        else:
                            pass
                    if self.rack.f_max_storage_height_m > 7.5: # Strictly greater than
                        if self.rack.s_commodity_class in [CommodityClass.C4, CommodityClass.CartonedPlastics, CommodityClass.UncartonedPlastics]:
                            if self.rack.s_commodity_class == CommodityClass.UncartonedPlastics:
                                if self.f_max_ceiling_height_m > 7.5:
                                    return [FMDS0809_FIGURES.Fig12a, FMDS0809_FIGURES.Fig13]
                                else:
                                    return [FMDS0809_FIGURES.Fig9a, FMDS0809_FIGURES.Fig12a, FMDS0809_FIGURES.Fig2k, FMDS0809_FIGURES.Fig13]
                            else:
                                if self.f_max_ceiling_height_m <= 9:
                                    return [FMDS0809_FIGURES.Fig9a, FMDS0809_FIGURES.Fig12a, FMDS0809_FIGURES.Fig2k, FMDS0809_FIGURES.Fig13]
                                else:
                                    return [FMDS0809_FIGURES.Fig12a, FMDS0809_FIGURES.Fig13]
                        else:
                            return [FMDS0809_FIGURES.Fig9a, FMDS0809_FIGURES.Fig12a, FMDS0809_FIGURES.Fig2k, FMDS0809_FIGURES.Fig13]
                    else:
                        return [FMDS0809_FIGURES.Fig13]
                    
    def mrr(self):
        if self.rack.b_open_top_containers:
            print("See Section 2.2.4")
        else:
            if self.rack.b_horizontal_barriers:
                return [FMDS0809_FIGURES.Fig10, FMDS0809_FIGURES.Fig14]
            else:
                if self.rack.b_solid_shelves:
                    if self.rack.f_solid_shelf_area_m2 > 6:
                        return [FMDS0809_FIGURES.Fig10, FMDS0809_FIGURES.Fig14]
                    elif (2 < self.rack.f_solid_shelf_area_m2 <= 6):
                        if self.rack.f_max_storage_height_m > 7.5:
                            return [FMDS0809_FIGURES.Fig14]
                        else:
                            return [FMDS0809_FIGURES.Fig10, FMDS0809_FIGURES.Fig14]
                    else:
                        pass
                if self.rack.f_max_storage_height_m <= 7.5:
                    if self.rack.s_commodity_class in [CommodityClass.C4, CommodityClass.CartonedPlastics, CommodityClass.UncartonedPlastics]:
                        if self.rack.s_commodity_class == CommodityClass.UncartonedPlastics:
                            if self.f_max_ceiling_height_m > 7.5:
                                return [FMDS0809_FIGURES.Fig14]
                            else:
                                return [FMDS0809_FIGURES.Fig10, FMDS0809_FIGURES.Fig14]
                        else:
                            if self.f_max_ceiling_height_m <= 9:
                                return [FMDS0809_FIGURES.Fig10, FMDS0809_FIGURES.Fig14]
                            else:
                                return [FMDS0809_FIGURES.Fig14]
                    else:
                        return [FMDS0809_FIGURES.Fig10, FMDS0809_FIGURES.Fig14]
                else:
                    return [FMDS0809_FIGURES.Fig14]
                
if __name__ == '__main__':
    building = Building('src/test_data.json')
    print(building.main())