import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.set_page_config(page_title="OrganizeIt", layout="wide")


if "token" not in st.session_state:
    st.session_state.token = None
if "user_id" not in st.session_state:
    st.session_state.user_id = None

def auth_headers():
    return {"Authorization": f"Bearer {st.session_state.token}"}


def show_response(response):
    try:
        data = response.json()
    except ValueError:
        data = response.text.strip() or "No content"

    if response.status_code in (200, 201, 204):
        st.success(f"✅ {response.status_code} — {data}")
    else:
        st.error(f"❌ {response.status_code} — {data}")


st.sidebar.title("OrganizeIt")

if st.session_state.token:
    st.sidebar.success("Logged in")
    if st.sidebar.button("Logout"):
        response = requests.post(
            f"{API_URL}/auth/logout",
            headers=auth_headers()
        )
        show_response(response)
        if response.status_code == 200:
            st.session_state.token = None
            st.session_state.user_id = None
            st.rerun()
else:
    st.sidebar.subheader("Login")
    login_email = st.sidebar.text_input("Email", key="login_email")
    login_password = st.sidebar.text_input("Password", type="password", key="login_password")
    if st.sidebar.button("Login"):
        response = requests.post(
            f"{API_URL}/auth/login",
            json={"email": login_email, "password": login_password}
        )
        if response.status_code == 200:
            st.session_state.token = response.json()["access_token"]
            st.sidebar.success("Logged in!")
            st.rerun()
        else:
            st.sidebar.error(f"❌ {response.json()}")

tab_users, tab_tasks, tab_metrics = st.tabs(["Users", "Tasks", "Metrics"])


with tab_users:
    st.header("Users")

    with st.expander("➕ Register User"):
        full_name = st.text_input("Full Name", key="reg_name")
        email = st.text_input("Email", key="reg_email")
        password = st.text_input("Password", type="password", key="reg_pass")
        birth_date = st.date_input("Birth Date", key="reg_birth")
        role = st.selectbox("Role", ["guest", "user", "admin"], key="reg_role")
        if st.button("Register", key="btn_register"):
            response = requests.post(
                f"{API_URL}/users/",
                params={"role": role},
                json={
                    "full_name": full_name,
                    "email": email,
                    "password": password,
                    "birth_date": str(birth_date)
                }
            )
            show_response(response)

    with st.expander("🔍 Get User by ID"):
        get_user_id = st.number_input("User ID", min_value=1, step=1, key="get_user_id")
        if st.button("Get User", key="btn_get_user"):
            response = requests.get(
                f"{API_URL}/users/{int(get_user_id)}",
                headers=auth_headers()
            )
            show_response(response)

    with st.expander("✏️ Update User"):
        upd_user_id = st.number_input("User ID", min_value=1, step=1, key="upd_user_id")
        upd_full_name = st.text_input("New Full Name (optional)", key="upd_name")
        upd_email = st.text_input("New Email (optional)", key="upd_email")
        upd_password = st.text_input("New Password (optional)", type="password", key="upd_pass")
        upd_birth = st.date_input("New Birth Date (optional)", key="upd_birth")
        if st.button("Update User", key="btn_update_user"):
            body = {}
            if upd_full_name: body["full_name"] = upd_full_name
            if upd_email: body["email"] = upd_email
            if upd_password: body["password"] = upd_password
            if upd_birth: body["birth_date"] = str(upd_birth)
            response = requests.put(
                f"{API_URL}/users/{int(upd_user_id)}",
                json=body,
                headers=auth_headers()
            )
            show_response(response)

    with st.expander("🗑️ Delete User (soft delete)"):
        del_user_id = st.number_input("User ID", min_value=1, step=1, key="del_user_id")
        if st.button("Delete User", key="btn_delete_user"):
            response = requests.delete(
                f"{API_URL}/users/{int(del_user_id)}",
                headers=auth_headers()
            )
            show_response(response)

with tab_tasks:
    st.header("Tasks")

    with st.expander("➕ Create Task"):
        task_name = st.text_input("Name", key="task_name")
        task_desc = st.text_area("Description", key="task_desc")
        task_priority = st.selectbox("Priority", ["", "low", "medium", "high"], key="task_priority")
        task_due = st.date_input("Due Date (optional)", key="task_due")
        if st.button("Create Task", key="btn_create_task"):
            body = {"name": task_name, "description": task_desc}
            if task_priority: body["priority"] = task_priority
            if task_due: body["due_date"] = str(task_due)
            response = requests.post(
                f"{API_URL}/tasks/",
                json=body,
                headers=auth_headers()
            )
            show_response(response)

    with st.expander("🔍 Get Task by ID"):
        get_task_id = st.number_input("Task ID", min_value=1, step=1, key="get_task_id")
        if st.button("Get Task", key="btn_get_task"):
            response = requests.get(
                f"{API_URL}/tasks/{int(get_task_id)}",
                headers=auth_headers()
            )
            show_response(response)

    with st.expander("📋 Get Assigned Tasks"):
        assigned_user_id = st.number_input("User ID", min_value=1, step=1, key="assigned_uid")
        if st.button("Get Tasks", key="btn_assigned"):
            response = requests.get(
                f"{API_URL}/tasks/",
                params={"assignedTo": int(assigned_user_id)},
                headers=auth_headers()
            )
            show_response(response)

    with st.expander("✏️ Update Task"):
        upd_task_id = st.number_input("Task ID", min_value=1, step=1, key="upd_task_id")
        upd_task_name = st.text_input("New Name (optional)", key="upd_task_name")
        upd_task_desc = st.text_area("New Description (optional)", key="upd_task_desc")
        upd_task_status = st.selectbox("New Status (optional)", ["", "pending", "in_progress", "complete"], key="upd_task_status")
        if st.button("Update Task", key="btn_update_task"):
            body = {}
            if upd_task_name: body["name"] = upd_task_name
            if upd_task_desc: body["description"] = upd_task_desc
            if upd_task_status: body["status"] = upd_task_status
            response = requests.put(
                f"{API_URL}/tasks/{int(upd_task_id)}",
                json=body,
                headers=auth_headers()
            )
            show_response(response)

    with st.expander("🗑️ Delete Task"):
        del_task_id = st.number_input("Task ID", min_value=1, step=1, key="del_task_id")
        if st.button("Delete Task", key="btn_delete_task"):
            response = requests.delete(
                f"{API_URL}/tasks/{int(del_task_id)}",
                headers=auth_headers()
            )
            show_response(response)

    with st.expander("👤 Assign Task to User"):
        assign_task_id = st.number_input("Task ID", min_value=1, step=1, key="assign_task_id")
        assign_user_id = st.number_input("User ID", min_value=1, step=1, key="assign_user_id")
        if st.button("Assign Task", key="btn_assign"):
            response = requests.post(
                f"{API_URL}/tasks/{int(assign_task_id)}/assignments",
                params={"user_id": int(assign_user_id)},
                headers=auth_headers()
            )
            show_response(response)

with tab_metrics:
    st.header("Metrics")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Tasks by Status")
        if st.button("Load", key="btn_status"):
            response = requests.get(
                f"{API_URL}/metrics/tasks-by-status",
                headers=auth_headers()
            )
            if response.status_code == 200:
                data = response.json()
                st.bar_chart(data)
            else:
                st.error(f"❌ {response.json()}")

    with col2:
        st.subheader("Tasks by User")

        filter_uid = st.number_input("User ID", min_value=1, step=1, key="metric_uid")

        if st.button("Load", key="btn_user_metric"):
            response = requests.get(
                f"{API_URL}/metrics/tasks-by-user/{int(filter_uid)}",
                headers=auth_headers()
            )

            if response.status_code == 200:
                data = response.json()
                st.table(data)
            else:
                st.error(f"❌ {response.json()}")