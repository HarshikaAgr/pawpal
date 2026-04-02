import streamlit as st
from datetime import datetime
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")


def is_valid_time(time_text):
    """Check HH:MM time format."""
    try:
        datetime.strptime(time_text, "%H:%M")
        return True
    except ValueError:
        return False


def get_pet_by_name(owner, pet_name):
    """Find one pet by name."""
    for pet in owner.pets:
        if pet.name == pet_name:
            return pet
    return None


def build_task_label(task, index):
    """Create a readable unique label for selectboxes."""
    pet_name = task.pet.name if task.pet else "No pet"
    return f"{index}. {task.title} | {pet_name} | {task.start_time} | {task.priority}"


def task_to_row(task):
    """Convert task object to table row."""
    return {
        "Pet": task.pet.name if task.pet else "No pet",
        "Task": task.title,
        "Time": task.start_time,
        "Duration": task.duration_minutes,
        "Priority": task.priority,
        "Category": task.category,
        "Recurring": task.recurring,
        "Status": "Done" if task.completed else "To Do",
    }


if "owner" not in st.session_state:
    st.session_state.owner = None

st.title("🐾 PawPal+")
st.caption("Smart pet care scheduling with sorting, recurrence, and conflict warnings.")

st.markdown(
    """
PawPal+ helps a pet owner:
- create pets and care tasks,
- organize tasks by priority, duration, or time,
- generate a daily plan based on available time,
- detect simple conflicts,
- and auto-create the next daily/weekly task when one is completed.
"""
)

st.divider()

# ---------------- OWNER ----------------
st.subheader("1. Owner")
owner_name = st.text_input("Owner name", value="Jordan")
available_time = st.number_input("Available time today (minutes)", min_value=1, value=60)

if st.button("Create / Update Owner"):
    if st.session_state.owner is None:
        st.session_state.owner = Owner(owner_name, available_time)
        st.success(f"Owner '{owner_name}' created.")
    else:
        st.session_state.owner.name = owner_name
        st.session_state.owner.set_available_time(available_time)
        st.success("Owner updated.")

if st.session_state.owner:
    st.info(
        f"Current owner: **{st.session_state.owner.name}** | "
        f"Available time: **{st.session_state.owner.available_minutes} min**"
    )

st.divider()

# ---------------- PETS ----------------
st.subheader("2. Add Pet")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])
pet_age = st.number_input("Pet age (years)", min_value=0, value=1)

if st.button("Add Pet"):
    if st.session_state.owner is None:
        st.error("Create the owner first.")
    else:
        existing_pet = get_pet_by_name(st.session_state.owner, pet_name)
        if existing_pet:
            st.warning("A pet with this name already exists.")
        else:
            new_pet = Pet(pet_name, species, pet_age)
            st.session_state.owner.add_pet(new_pet)
            st.success(f"Pet '{pet_name}' added.")

if st.session_state.owner and st.session_state.owner.pets:
    st.write("**Current pets:**")
    for pet in st.session_state.owner.pets:
        st.write(f"🐾 {pet.get_pet_info()}")

st.divider()

# ---------------- ADD TASK ----------------
st.subheader("3. Add Task")

if st.session_state.owner and st.session_state.owner.pets:
    pet_names = [pet.name for pet in st.session_state.owner.pets]
    selected_pet_name = st.selectbox("Choose pet", pet_names, key="add_task_pet")

    task_title = st.text_input("Task title", value="Morning walk")
    col1, col2, col3 = st.columns(3)
    with col1:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col2:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
    with col3:
        category = st.selectbox("Category", ["feeding", "exercise", "grooming", "medicine", "play"])

    col4, col5 = st.columns(2)
    with col4:
        recurring = st.selectbox("Recurring", ["none", "daily", "weekly"])
    with col5:
        start_time = st.text_input("Start time (HH:MM)", value="08:00")

    is_required = st.checkbox("Required task?", value=False)

    if st.button("Add Task"):
        if not is_valid_time(start_time):
            st.error("Please enter time in HH:MM format, for example 08:00.")
        else:
            selected_pet = get_pet_by_name(st.session_state.owner, selected_pet_name)
            new_task = Task(
                task_title,
                duration,
                priority,
                category,
                recurring=recurring,
                start_time=start_time,
            )
            new_task.is_required = is_required
            selected_pet.add_task(new_task)
            st.success(f"Task '{task_title}' added to {selected_pet.name}.")
else:
    st.caption("Create the owner and at least one pet before adding tasks.")

st.divider()

# ---------------- VIEW TASKS ----------------
st.subheader("4. Current Tasks")

if st.session_state.owner and st.session_state.owner.pets:
    any_tasks = False
    for pet in st.session_state.owner.pets:
        with st.expander(f"{pet.name}'s tasks", expanded=False):
            if pet.tasks:
                any_tasks = True
                rows = [task_to_row(task) for task in pet.tasks]
                st.table(rows)
            else:
                st.write("No tasks yet.")
    if not any_tasks:
        st.write("No tasks yet.")
else:
    st.write("No pets yet.")

st.divider()

# ---------------- EDIT TASK ----------------
st.subheader("5. Edit Task")

if st.session_state.owner and st.session_state.owner.get_all_tasks():
    edit_pet_name = st.selectbox(
        "Choose pet whose task you want to edit",
        [pet.name for pet in st.session_state.owner.pets],
        key="edit_pet_name",
    )
    edit_pet = get_pet_by_name(st.session_state.owner, edit_pet_name)

    edit_task_options = {
        build_task_label(task, i + 1): task for i, task in enumerate(edit_pet.tasks)
    }

    if edit_task_options:
        selected_edit_label = st.selectbox(
            "Choose task to edit",
            list(edit_task_options.keys()),
            key="edit_task_label",
        )
        task_to_edit = edit_task_options[selected_edit_label]
        widget_suffix = selected_edit_label.replace(" ", "_").replace("|", "_")

        new_title = st.text_input(
            "Edit title",
            value=task_to_edit.title,
            key=f"edit_title_{widget_suffix}",
        )
        col1, col2, col3 = st.columns(3)
        with col1:
            new_duration = st.number_input(
                "Edit duration",
                min_value=1,
                max_value=240,
                value=task_to_edit.duration_minutes,
                key=f"edit_duration_{widget_suffix}",
            )
        with col2:
            new_priority = st.selectbox(
                "Edit priority",
                ["low", "medium", "high"],
                index=["low", "medium", "high"].index(task_to_edit.priority),
                key=f"edit_priority_{widget_suffix}",
            )
        with col3:
            new_category = st.selectbox(
                "Edit category",
                ["feeding", "exercise", "grooming", "medicine", "play"],
                index=["feeding", "exercise", "grooming", "medicine", "play"].index(task_to_edit.category),
                key=f"edit_category_{widget_suffix}",
            )

        col4, col5 = st.columns(2)
        with col4:
            new_recurring = st.selectbox(
                "Edit recurring",
                ["none", "daily", "weekly"],
                index=["none", "daily", "weekly"].index(task_to_edit.recurring),
                key=f"edit_recurring_{widget_suffix}",
            )
        with col5:
            new_start_time = st.text_input(
                "Edit start time",
                value=task_to_edit.start_time,
                key=f"edit_start_time_{widget_suffix}",
            )

        new_required = st.checkbox(
            "Required task",
            value=task_to_edit.is_required,
            key=f"edit_required_{widget_suffix}",
        )

        if st.button("Update Task"):
            if not is_valid_time(new_start_time):
                st.error("Please enter time in HH:MM format, for example 08:00.")
            else:
                task_to_edit.update_task(
                    new_title,
                    new_duration,
                    new_priority,
                    new_category,
                    is_required=new_required,
                    recurring=new_recurring,
                    start_time=new_start_time,
                )
                st.success("Task updated.")
    else:
        st.write("That pet has no tasks yet.")
else:
    st.write("No tasks available to edit yet.")

st.divider()

# ---------------- COMPLETE TASK ----------------
st.subheader("6. Mark Task Complete")

if st.session_state.owner and st.session_state.owner.get_incomplete_tasks():
    incomplete_tasks = st.session_state.owner.get_incomplete_tasks()
    complete_options = {
        build_task_label(task, i + 1): task for i, task in enumerate(incomplete_tasks)
    }

    selected_complete_label = st.selectbox(
        "Choose task to complete",
        list(complete_options.keys()),
        key="complete_task_label",
    )
    task_to_complete = complete_options[selected_complete_label]

    if st.button("Mark Complete"):
        pet_for_task = task_to_complete.pet
        next_task = pet_for_task.complete_task(task_to_complete)
        st.success(f"Task '{task_to_complete.title}' marked complete.")

        if next_task:
            st.info(
                f"Recurring task created for next time: "
                f"'{next_task.title}' on {next_task.due_date}"
            )
else:
    st.write("No incomplete tasks to complete.")

st.divider()

# ---------------- SCHEDULE ----------------
st.subheader("7. Build Schedule")
st.caption("The final plan always uses priority first, then checks what fits in the available time.")

sort_option = st.selectbox(
    "View incomplete tasks sorted by:",
    ["Priority (High→Low)", "Duration (Short→Long)", "Time (Early→Late)"]
)

if st.button("Generate Schedule"):
    if st.session_state.owner is None or not st.session_state.owner.pets:
        st.error("Create the owner, pets, and tasks first.")
    else:
        scheduler = Scheduler(st.session_state.owner)

        if sort_option == "Priority (High→Low)":
            sorted_tasks = scheduler.sort_tasks_by_priority()
        elif sort_option == "Duration (Short→Long)":
            sorted_tasks = scheduler.sort_tasks_by_duration()
        else:
            sorted_tasks = scheduler.sort_by_time()

        st.write("**Available incomplete tasks:**")
        if sorted_tasks:
            st.table([task_to_row(task) for task in sorted_tasks])
        else:
            st.warning("No incomplete tasks available.")

        planned_tasks = scheduler.generate_plan()
        conflicts = scheduler.detect_all_conflicts()

        if conflicts:
            for conflict in conflicts:
                st.warning(conflict)

        stats = scheduler.get_schedule_stats()
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Tasks", stats["total_tasks"])
        with col2:
            st.metric("Completed", stats["completed_tasks"])
        with col3:
            st.metric("Time Remaining", f"{stats['time_remaining']} min")

        st.write("**Planned schedule:**")
        if planned_tasks:
            st.table([task_to_row(task) for task in planned_tasks])
            st.success(f"{len(planned_tasks)} task(s) fit in the schedule.")
        else:
            st.warning("No tasks fit in the available time.")

        st.text(scheduler.explain_plan())