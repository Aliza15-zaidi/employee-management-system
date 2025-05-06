import streamlit as st
import pandas as pd
from datetime import datetime

# Set layout
st.set_page_config(layout="wide")

# Employee class
def parse_date(date_str):
    if isinstance(date_str, str):
        try:
            return str(pd.to_datetime(date_str).date())
        except:
            return ""
    elif isinstance(date_str, datetime):
        return str(date_str.date())
    else:
        return ""

class Employee:
    def __init__(self, emp_id: int, name: str, designation: str, salary: float, nic: str,
                 address: str, joining_date: str, nic_issue_date: str, nic_expiry_date: str,
                 marital_status: str, dob: str):
        self.emp_id = emp_id
        self.name = name
        self.designation = designation
        self.salary = salary
        self.nic = nic
        self.address = address
        self.joining_date = joining_date
        self.nic_issue_date = nic_issue_date
        self.nic_expiry_date = nic_expiry_date
        self.marital_status = marital_status
        self.dob = dob
        self.exit_date = None

    def get_employee_info(self):
        return {
            "emp_id": self.emp_id,
            "name": self.name,
            "designation": self.designation,
            "salary": self.salary,
            "nic": self.nic,
            "address": self.address,
            "joining_date": self.joining_date,
            "nic_issue_date": self.nic_issue_date,
            "nic_expiry_date": self.nic_expiry_date,
            "marital_status": self.marital_status,
            "dob": self.dob,
            "exit_date": self.exit_date
        }

    def apply_promotion(self, increase_percentage: float):
        self.salary += self.salary * (increase_percentage / 100)
        return self.salary

    def exit_employee(self, exit_date):
        self.exit_date = exit_date

class EmployeeManagementSystem:
    def __init__(self):
        if 'employees' not in st.session_state:
            st.session_state.employees = []
        if 'exited_employees' not in st.session_state:
            st.session_state.exited_employees = []

    def add_employee(self, employee):
        st.session_state.employees.append(employee)

    def list_employees(self):
        return [emp.get_employee_info() for emp in st.session_state.employees]

    def list_exited_employees(self):
        return [emp.get_employee_info() for emp in st.session_state.exited_employees]

    def promote_employee(self, emp_id, increase_percentage):
        for emp in st.session_state.employees:
            if emp.emp_id == emp_id:
                return emp.apply_promotion(increase_percentage)
        return None

    def search_employee_by_id(self, emp_id):
        for emp in st.session_state.employees:
            if emp.emp_id == emp_id:
                return emp.get_employee_info()
        return None

    def delete_employee(self, emp_id):
        st.session_state.employees = [emp for emp in st.session_state.employees if emp.emp_id != emp_id]

    def update_employee(self, emp_id, new_salary=None, new_designation=None):
        for emp in st.session_state.employees:
            if emp.emp_id == emp_id:
                if new_salary:
                    emp.salary = new_salary
                if new_designation:
                    emp.designation = new_designation
                return emp.get_employee_info()
        return None

    def filter_by_designation(self, designation):
        return [emp.get_employee_info() for emp in st.session_state.employees if emp.designation == designation]

    def sort_by_salary(self, reverse=False):
        return sorted(self.list_employees(), key=lambda x: x["salary"], reverse=reverse)

    def exit_employee(self, emp_id, exit_date):
        for emp in st.session_state.employees:
            if emp.emp_id == emp_id:
                emp.exit_employee(exit_date)
                st.session_state.exited_employees.append(emp)
                st.session_state.employees = [e for e in st.session_state.employees if e.emp_id != emp_id]
                return emp.get_employee_info()
        return None

system = EmployeeManagementSystem()

st.title("Employee Management System")
menu = ["Add from Excel", "Add Employee", "List Employees", "Exit Employee", "Exit Employees List", "Promote Employee", "Search Employee", "Delete Employee", "Update Employee", "Filter by Designation", "Sort by Salary"]
choice = st.sidebar.selectbox("Select an Option", menu)

# Upload Excel and Add
if choice == "Add from Excel":
    st.subheader("Upload Employee Excel Sheet")
    file = st.file_uploader("Upload Excel/CSV", type=["xlsx", "csv"])

    if file:
        df = pd.read_excel(file) if file.name.endswith("xlsx") else pd.read_csv(file)
        st.dataframe(df)

        selected_index = st.number_input("Select Row to Fill Details", min_value=0, max_value=len(df) - 1)
        selected_row = df.iloc[selected_index]

        emp_id = int(selected_row.get("emp_id", 0))
        name = selected_row.get("name", "")
        designation = selected_row.get("designation", "")
        salary = float(selected_row.get("salary", 0.0))
        nic = selected_row.get("nic", "")

        address = st.text_area("Address")
        joining_date = st.date_input("Joining Date", min_value=datetime(2000, 1, 1))
        nic_issue_date = st.date_input("NIC Issue Date")
        nic_expiry_date = st.date_input("NIC Expiry Date")
        marital_status = st.selectbox("Marital Status", ["Single", "Married", "Divorced"])
        dob = st.date_input("Date of Birth")

        if st.button("Add Employee"):
            emp = Employee(emp_id, name, designation, salary, nic, address, str(joining_date), str(nic_issue_date),
                           str(nic_expiry_date), marital_status, str(dob))
            system.add_employee(emp)
            st.success(f"Employee {name} added successfully!")

# List Employees
elif choice == "List Employees":
    st.subheader("Employee List")
    employees = system.list_employees()
    if employees:
        df = pd.DataFrame(employees)
        with st.container():
            st.dataframe(df, use_container_width=True)
    else:
        st.write("No employees found.")

# Exit Employee
elif choice == "Exit Employee":
    st.subheader("Exit Employee")
    exit_id = st.number_input("Enter Employee ID to exit", min_value=1)
    exit_date = st.date_input("Exit Date", min_value=datetime.today())
    if st.button("Exit Employee"):
        exited_employee = system.exit_employee(exit_id, str(exit_date))
        if exited_employee:
            st.success(f"Employee with ID {exit_id} has exited.")
        else:
            st.error(f"Employee with ID {exit_id} not found.")

# Exit Employees List
elif choice == "Exit Employees List":
    st.subheader("Exited Employees")
    exited_employees = system.list_exited_employees()
    if exited_employees:
        df = pd.DataFrame(exited_employees)
        with st.container():
            st.dataframe(df, use_container_width=True)
    else:
        st.write("No exited employees found.")

# Promote Employee
elif choice == "Promote Employee":
    st.subheader("Promote Employee")
    emp_id = st.number_input("Employee ID to promote", min_value=1)
    increase_percentage = st.number_input("Salary Increase Percentage", min_value=0.0, max_value=100.0)
    if st.button("Promote Employee"):
        new_salary = system.promote_employee(emp_id, increase_percentage)
        if new_salary:
            st.success(f"Employee promoted! New salary: {new_salary}")
        else:
            st.error(f"Employee with ID {emp_id} not found.")

# Search Employee
elif choice == "Search Employee":
    st.subheader("Search Employee by ID")
    search_id = st.number_input("Enter Employee ID to search", min_value=1)
    if st.button("Search Employee"):
        employee = system.search_employee_by_id(search_id)
        if employee:
            st.json(employee)
        else:
            st.write(f"Employee with ID {search_id} not found.")

# Delete Employee
elif choice == "Delete Employee":
    st.subheader("Delete Employee by ID")
    delete_id = st.number_input("Enter Employee ID to delete", min_value=1)
    if st.button("Delete Employee"):
        system.delete_employee(delete_id)
        st.success(f"Employee with ID {delete_id} has been deleted.")

# Update Employee
elif choice == "Update Employee":
    st.subheader("Update Employee Information")
    update_id = st.number_input("Enter Employee ID to update", min_value=1)
    new_salary = st.number_input("Enter new Salary", min_value=0.0)
    new_designation = st.text_input("Enter new Designation")
    if st.button("Update Employee"):
        updated_employee = system.update_employee(update_id, new_salary, new_designation)
        if updated_employee:
            st.success(f"Employee with ID {update_id} has been updated!")
            st.json(updated_employee)
        else:
            st.error(f"Employee with ID {update_id} not found.")

# Filter by Designation
elif choice == "Filter by Designation":
    st.subheader("Filter Employees by Designation")
    designations = ["Manager", "Team Lead", "Developer", "HR"]
    selected_designation = st.selectbox("Select Designation", designations)
    filtered_employees = system.filter_by_designation(selected_designation)
    if filtered_employees:
        df = pd.DataFrame(filtered_employees)
        with st.container():
            st.dataframe(df, use_container_width=True)
    else:
        st.write(f"No employees found with the designation {selected_designation}.")

# Sort by Salary
elif choice == "Sort by Salary":
    st.subheader("Sort Employees by Salary")
    sort_order = st.selectbox("Select Sort Order", ["Ascending", "Descending"])
    reverse = sort_order == "Descending"
    sorted_employees = system.sort_by_salary(reverse)
    if sorted_employees:
        df = pd.DataFrame(sorted_employees)
        with st.container():
            st.dataframe(df, use_container_width=True)
    else:
        st.write("No employees found.")
