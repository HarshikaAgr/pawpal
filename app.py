import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

# ===== MEMORY VAULT (Session State) =====
# Initialize memory to store Owner and pets
if "owner" not in st.session_state:
    st.session_state.owner = None

if "current_pet" not in st.session_state:
    st.session_state.current_pet = None

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
available_time = st.number_input("Available time (minutes):", value=60, min_value=1)

# ===== BUTTON: CREATE OWNER =====
if st.button("Create Owner"):
    # Call Owner class constructor
    st.session_state.owner = Owner(owner_name, available_time)
    st.success(f"✓ Owner '{owner_name}' created with {available_time} minutes!")

# Show current owner
if st.session_state.owner:
    st.info(f"Current owner: **{st.session_state.owner.name}** ({st.session_state.owner.available_minutes} min)")

st.divider()

# ===== ADD PET SECTION =====
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])
pet_age = st.number_input("Pet age (years):", value=1, min_value=0)

# ===== BUTTON: ADD PET =====
if st.button("Add Pet"):
    if st.session_state.owner:
        # Call Pet class constructor
        new_pet = Pet(pet_name, species, pet_age)
        # Call Owner.add_pet() method
        st.session_state.owner.add_pet(new_pet)
        st.session_state.current_pet = new_pet
        st.success(f"✓ Pet '{pet_name}' added!")
    else:
        st.error("Create an owner first!")

# Show pets
if st.session_state.owner and st.session_state.owner.pets:
    st.write("**Your Pets:**")
    for pet in st.session_state.owner.pets:
        st.write(f"  🐾 {pet.get_pet_info()}")

st.markdown("### Tasks")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

# ===== BUTTON: ADD TASK =====
if st.button("Add task"):
    if st.session_state.owner and st.session_state.owner.pets:
        selected_pet = st.session_state.owner.pets[-1]  # Use last added pet
        # Call Task class constructor
        new_task = Task(task_title, duration, priority, "care")
        # Call Pet.add_task() method
        selected_pet.add_task(new_task)
        st.success(f"✓ Task '{task_title}' added to {selected_pet.name}!")
    else:
        st.error("Create an owner and pet first!")

# Show tasks for each pet
if st.session_state.owner and st.session_state.owner.pets:
    st.write("**Tasks by Pet:**")
    for pet in st.session_state.owner.pets:
        if pet.tasks:
            st.write(f"**{pet.name}:**")
            for task in pet.tasks:
                st.write(f"  ✓ {task.get_task_details()}")
        else:
            st.write(f"**{pet.name}:** No tasks yet")

st.divider()

st.subheader("Build Schedule")
st.caption("This button should call your scheduling logic once you implement it.")

# ===== BUTTON: GENERATE SCHEDULE =====
if st.button("Generate schedule"):
    if st.session_state.owner and st.session_state.owner.pets:
        # Call Scheduler class
        scheduler = Scheduler(st.session_state.owner)
        planned_tasks = scheduler.generate_plan()

        # Show the schedule explanation
        st.write(scheduler.explain_plan())

        if planned_tasks:
            st.success(f"✓ {len(planned_tasks)} tasks fit in your schedule!")
        else:
            st.warning("⚠️ No tasks fit in your available time. Try adding more time.")
    else:
        st.error("Create an owner and add pets/tasks first!")
