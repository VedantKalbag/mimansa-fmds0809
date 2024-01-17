import streamlit as st
import fmds0809
import json



col1, col2 = st.columns(2)
with col1:
    st.markdown("# FM Global DS 8-9 Tool \n #### Mimansa Risk Consulting")


def input_form():
    col1, col2, col3 = st.columns([1, 1, 1])
    f_max_ceiling_height = col1.number_input('What is the maximum ceiling height (in m)?', min_value=0.0, max_value=100.0, value=12.0, step=0.01)
    f_building_slope_deg = col1.number_input('What is the building slope (in degrees)?', min_value=0.0, max_value=90.0, value=0.0, step=0.01)
    s_rack_type = col1.selectbox('What is the rack type?', ('SRR', 'DRR','MRR'))

    commodity_class = col1.selectbox('What is the commodity class?', ('Class I', 'Class II', 'Class III', 'Class IV', 'Uncartoned Plastics', 'Cartoned Plastics'))
    if commodity_class == 'Class I':
        s_commodity_class = 'C1'
    elif commodity_class == 'Class II':
        s_commodity_class = 'C2'
    elif commodity_class == 'Class III':
        s_commodity_class = 'C3'
    elif commodity_class == 'Class IV':
        s_commodity_class = 'C4'
    else:
        s_commodity_class = commodity_class
    open_top = col2.selectbox('Are there open top containers?', ('Yes', 'No'), index=1)
    if open_top == 'Yes':
        b_open_top_containers = True
    else:
        b_open_top_containers = False
    f_rack_depth_mm = col2.number_input('What is the rack depth (in mm)?', min_value=0.0, max_value=10000.0, value=1200.0, step=0.01)
    f_beam_length_mm = col2.number_input('What is the beam length (in mm)?', min_value=0.0, max_value=10000.0, value=2700.0, step=0.01)
    f_vertical_clearance_mm = col2.number_input('What is the vertical clearance (in mm)?', min_value=0.0, max_value=10000.0, value=100.0, step=0.01)
    horizontal_barriers = col3.selectbox('Are there horizontal barriers?', ('Yes', 'No'))
    if horizontal_barriers == 'Yes':
        b_horizontal_barriers = True
    else:
        b_horizontal_barriers = False
    f_transverse_flue_length_mm = col3.number_input('What is the transverse flue length (in mm)?', min_value=0.0, max_value=10000.0, value=0.0, step=0.01)
    f_longitudinal_flue_length_mm = col3.number_input('What is the longitudinal flue length (in mm)?', min_value=0.0, max_value=10000.0, value=0.0, step=0.01)

    solid_shelves = col3.selectbox('Are there solid shelves?', ('No','Yes'))
    if solid_shelves == 'Yes':
        b_solid_shelves = True
    else:
        b_solid_shelves = False
    f_max_storage_height = col3.number_input('What is the maximum storage height (in m)?', min_value=0.0, max_value=100.0, value=12.0, step=0.01)

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
        st.write("Please verify that the below information is correct:")
        st.json(json.dumps(d))
        return d

def write_json(d):
    json.dump(d, open("data.json", "w"))

def run_model():
    building = fmds0809.Building('data.json')
    return building.main()

def set_state(i):
    st.session_state.stage = i



if __name__=='__main__':
    paths=[]
    if 'stage' not in st.session_state:
        st.session_state.stage = 0

    if st.session_state.stage == 0:
        d = input_form()
        if d != None:
            st.button('Yes, the information is correct', on_click=set_state, args=[1])
            write_json(d)
            # set_state(1)
    if st.session_state.stage == 1:
        # st.write("Please wait while we generate the designs...")
        paths = run_model()
        print(paths)
        # st.write(paths)
        with st.container():
            for path in paths:
                st.image('./resources/'+path)


        st.button('Reset', on_click=set_state, args=[0])