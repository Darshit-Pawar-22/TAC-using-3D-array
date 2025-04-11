import streamlit as st

def generate_compact_tac(lhs, rhs1, rhs2,
                         lhs_indices, rhs1_indices, rhs2_indices,
                         lhs_dims, rhs1_dims, rhs2_dims,
                         bpw=4, operator='+'):
    tac = []
    
    def compute_offset(name, indices, dims, temp_base):
        d2, d3 = dims[1], dims[2]
        t = temp_base
        code = [
            f"t{t} = {indices[0]} * {d2}",
            f"t{t} = t{t} + {indices[1]}",
            f"t{t} = t{t} * {d3}",
            f"t{t} = t{t} + {indices[2]}",
            f"t{t+1} = t{t} * {bpw}",
            f"t{t+2} = address({name}) + t{t+1}"
        ]
        return code, f"t{t+2}", t + 3

    code_lhs, lhs_addr, next_temp = compute_offset(lhs, lhs_indices, lhs_dims, 1)
    tac.extend(code_lhs)

    code_rhs1, rhs1_addr, next_temp = compute_offset(rhs1, rhs1_indices, rhs1_dims, next_temp)
    tac.extend(code_rhs1)
    tac.append(f"t{next_temp} = *{rhs1_addr}")
    rhs1_val = f"t{next_temp}"
    next_temp += 1

    code_rhs2, rhs2_addr, next_temp = compute_offset(rhs2, rhs2_indices, rhs2_dims, next_temp)
    tac.extend(code_rhs2)
    tac.append(f"t{next_temp} = *{rhs2_addr}")
    rhs2_val = f"t{next_temp}"
    next_temp += 1

    tac.append(f"t{next_temp} = {rhs1_val} {operator} {rhs2_val}")
    tac.append(f"*{lhs_addr} = t{next_temp}")

    return tac

st.title(" Three Address Code Generator for 3D Arrays")

with st.form("tac_form"):
    st.subheader("LHS Array")
    lhs = st.text_input("LHS Array Name", value="a")
    lhs_indices = [st.text_input(f"LHS Index {i}", value=i) for i in ['i', 'j', 'k']]
    lhs_dims = [st.number_input(f"LHS Dimension {d}", min_value=1, value=3) for d in ['d1', 'd2', 'd3']]

    st.subheader("RHS Array 1")
    rhs1 = st.text_input("RHS1 Array Name", value="b")
    rhs1_indices = [st.text_input(f"RHS1 Index {i}", value=i) for i in ['i', 'j', 'k']]
    rhs1_dims = [st.number_input(f"RHS1 Dimension {d}", min_value=1, value=3) for d in ['d1', 'd2', 'd3']]

    st.subheader("RHS Array 2")
    rhs2 = st.text_input("RHS2 Array Name", value="c")
    rhs2_indices = [st.text_input(f"RHS2 Index {i}", value=i) for i in ['i', 'j', 'k']]
    rhs2_dims = [st.number_input(f"RHS2 Dimension {d}", min_value=1, value=3) for d in ['d1', 'd2', 'd3']]

    operator = st.selectbox("Operation", ['+', '-', '*', '/'])
    bpw = st.number_input("Bytes per Word (bpw)", min_value=1, value=4)

    submitted = st.form_submit_button("Generate TAC")

if submitted:
    try:
        tac_code = generate_compact_tac(lhs, rhs1, rhs2,
                                        lhs_indices, rhs1_indices, rhs2_indices,
                                        lhs_dims, rhs1_dims, rhs2_dims,
                                        bpw, operator)
        st.success("Three Address Code Generated:")
        st.code("\n".join(tac_code), language="plaintext")
    except Exception as e:
        st.error(f"Error generating TAC: {e}")