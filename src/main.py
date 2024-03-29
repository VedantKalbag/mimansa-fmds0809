import streamlit as st
import fmds0809
import json
import os


RACK_TYPE=['Single Row Rack', 'Double Row Rack','Multi Row Rack']
COMMODITY_CLASS = ['Class I', 'Class II', 'Class III', 'Class IV', 'Uncartoned Plastics', 'Cartoned Plastics']
YES_NO = [1, 0]
NO_YES = [0, 1]


def process_rack_type(rack_type):
    if rack_type == 'SRR':
        return 'Single Row Rack'
    elif rack_type == 'DRR':
        return 'Double Row Rack'
    else:
        return 'Multi Row Rack'

def process_commodity_class(commodity_class):
    if commodity_class == 'Class I':
        return 'C1'
    elif commodity_class == 'Class II':
        return 'C2'
    elif commodity_class == 'Class III':
        return 'C3'
    elif commodity_class == 'Class IV':
        return 'C4'
    else:
        return commodity_class.replace(" ","")
    
def process_commodity_class_reverse(commodity_class):
    if commodity_class == 'C1':
        return 'Class I'
    elif commodity_class == 'C2':
        return 'Class II'
    elif commodity_class == 'C3':
        return 'Class III'
    elif commodity_class == 'C4':
        return 'Class IV'
    else:
        return commodity_class

def input_form(path_to_json):
    if path_to_json != None:
        with open(path_to_json) as f:
            data = json.load(f)
        f_max_ceiling_height_default = data['f_max_ceiling_height_m']
        f_building_slope_deg_default = data['f_building_slope_deg']
        s_rack_type_default = RACK_TYPE.index(process_rack_type(data['rack']['s_rack_type']))
        s_commodity_class_default = COMMODITY_CLASS.index(process_commodity_class_reverse(data['rack']['s_commodity_class']))
        b_open_top_containers_default = YES_NO.index(data['rack']['b_open_top_containers'])
        f_rack_depth_mm_default = data['rack']['f_rack_depth_mm']
        f_beam_length_mm_default = data['rack']['f_beam_length_mm']
        f_vertical_clearance_mm_default = data['rack']['f_vertical_clearance_mm']
        b_horizontal_barriers_default = YES_NO.index(data['rack']['b_horizontal_barriers'])
        f_transverse_flue_length_mm_default = data['rack']['f_transverse_flue_length_mm']
        f_longitudinal_flue_length_mm_default = data['rack']['f_longitudinal_flue_length_mm']
        b_solid_shelves_default = NO_YES.index(data['rack']['b_solid_shelves'])
        f_max_storage_height_default = data['rack']['f_max_storage_height_m']
        os.remove(path_to_json)
    else:
        f_max_ceiling_height_default = 12.0
        f_building_slope_deg_default = 0.0
        s_rack_type_default = 0
        s_commodity_class_default = 0
        b_open_top_containers_default = 1
        f_rack_depth_mm_default = 1200
        f_beam_length_mm_default = 2700
        f_vertical_clearance_mm_default = 100
        b_horizontal_barriers_default = 1
        f_transverse_flue_length_mm_default = 0
        f_longitudinal_flue_length_mm_default = 0
        b_solid_shelves_default = 0
        f_max_storage_height_default = 12.0
    
        
    col1, col2, col3 = st.columns([1, 1, 1])
    f_max_ceiling_height = col1.number_input('Maximum Ceiling Height (in m)?', min_value=0.0, max_value=100.0, value=f_max_ceiling_height_default, step=0.1, format="%.1f")
    f_building_slope_deg = col1.number_input('Building Slope (in degrees)?', min_value=0.0, max_value=90.0, value=f_building_slope_deg_default, step=0.1, format="%.1f")
    s_rack_type = col1.selectbox('Type of Rack', ('Single Row Rack', 'Double Row Rack','Multi Row Rack'), index = s_rack_type_default)
    if s_rack_type == 'Single Row Rack':
        s_rack_type = 'SRR'
    elif s_rack_type == 'Double Row Rack':
        s_rack_type = 'DRR'
    else:
        s_rack_type = 'MRR'

    commodity_class = col1.selectbox('Class of Commodity Stored', ('Class I', 'Class II', 'Class III', 'Class IV', 'Uncartoned Plastics', 'Cartoned Plastics'), index = s_commodity_class_default)
    if commodity_class == 'Class I':
        s_commodity_class = 'C1'
    elif commodity_class == 'Class II':
        s_commodity_class = 'C2'
    elif commodity_class == 'Class III':
        s_commodity_class = 'C3'
    elif commodity_class == 'Class IV':
        s_commodity_class = 'C4'
    else:
        s_commodity_class = commodity_class.replace(" ", "")
    open_top = col2.selectbox('Open Top Containers?', ('Yes', 'No'), index=b_open_top_containers_default)
    if open_top == 'Yes':
        b_open_top_containers = True
    else:
        b_open_top_containers = False
    f_rack_depth_mm = col2.number_input('Rack Depth (in mm)?', min_value=0, max_value=10000, value=f_rack_depth_mm_default, step=1)
    f_beam_length_mm = col2.number_input('Beam Length (in mm)?', min_value=0, max_value=10000, value=f_beam_length_mm_default, step=1)
    f_vertical_clearance_mm = col2.number_input('Distance between in-rack deflector and top of storage (in mm)?', min_value=0, max_value=10000, value=f_vertical_clearance_mm_default, step=1)
    horizontal_barriers = col3.selectbox('Horizontal Barriers?', ('Yes', 'No'), index=b_horizontal_barriers_default)
    if horizontal_barriers == 'Yes':
        b_horizontal_barriers = True
    else:
        b_horizontal_barriers = False
    f_transverse_flue_length_mm = col3.number_input('Transverse Flue Length (in mm)?', min_value=0, max_value=10000, value=f_transverse_flue_length_mm_default, step=1)
    f_longitudinal_flue_length_mm = col3.number_input('Longitudinal Flue Length (in mm)?', min_value=0, max_value=10000, value=f_longitudinal_flue_length_mm_default, step=1)

    solid_shelves = col3.selectbox('Solid Shelves?', ('No','Yes'), index=b_solid_shelves_default)
    if solid_shelves == 'Yes':
        b_solid_shelves = True
    else:
        b_solid_shelves = False
    f_max_storage_height = col3.number_input('Maximum Storage Height (in m)?', min_value=0.0, max_value=100.0, value=f_max_storage_height_default, step=0.1, format="%.1f")

    submitted = st.button("Submit")
    if submitted:
        d = {
                "f_max_ceiling_height_m": f_max_ceiling_height,
                "f_building_slope_deg": f_building_slope_deg,
                "rack":{
                    "s_rack_type": s_rack_type,
                    "s_commodity_class": s_commodity_class,
                    "b_open_top_containers": b_open_top_containers,
                    "f_rack_depth_mm": f_rack_depth_mm,
                    "f_beam_length_mm": f_beam_length_mm,
                    "f_vertical_clearance_mm": f_vertical_clearance_mm,
                    "b_horizontal_barriers": b_horizontal_barriers,
                    "f_transverse_flue_length_mm": f_transverse_flue_length_mm,
                    "f_longitudinal_flue_length_mm": f_longitudinal_flue_length_mm,
                    "b_solid_shelves": b_solid_shelves,
                    "f_max_storage_height_m": f_max_storage_height
                }
            }
        write_json(d)
        set_state(1)
        # st.write("Please verify that the below information is correct:")
        # st.json(json.dumps(d))
        return d

def write_json(d):
    json.dump(d, open("data.json", "w"))

def run_model():
    building = fmds0809.Building('data.json')
    return building.main()

def set_state(i):
    st.session_state.stage = i



if __name__=='__main__':

    st.image('./resources/mimansa-logo.png', width=350)
    st.markdown("### FM Global DS 8-9 Tool For In-Rack Options")
    if 'stage' not in st.session_state:
        st.session_state.stage = 0

    if st.session_state.stage == 0:
        if os.path.exists('data.json'):
            d = input_form('data.json')
        else:
            d = input_form(None)
        # if d != None:
            # st.button('Yes, the information is correct', on_click=set_state, args=[1])
            # write_json(d)
            # set_state(1)
    if st.session_state.stage == 1:
        # st.write("Please wait while we generate the designs...")
        try:
            paths = run_model()
            if len(paths) == 0:
                st.write("Please refer to Section 2.2.4 of FM 8-9")
            with st.container():
                st.write("Here are the acceptable designs, as per FM 8-9:")
                for path in paths:
                    st.image('./resources/'+path)
        except NotImplementedError as e:
            st.write("Please refer to Section 2.2.4 of FM 8-9")
        # print(paths)
        # st.write(paths)
        # st.button('Reset', on_click=set_state, args=[0])
        set_state(0)

    # if st.session_state.stage == 2:
    #     # os.remove('data.json')
    #     set_state(0)

